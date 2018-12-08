# coding: utf-8

import base64
import os

from lxml import etree, objectify

from odoo.tools import misc

from . import common


class TestL10nMxEdiInvoice(common.InvoiceTransactionCase):
    def setUp(self):
        super(TestL10nMxEdiInvoice, self).setUp()
        self.refund_model = self.env['account.invoice.refund']

        self.cert = misc.file_open(os.path.join(
            'l10n_mx_edi', 'demo', 'pac_credentials', 'certificate.cer'), 'rb').read()
        self.cert_key = misc.file_open(os.path.join(
            'l10n_mx_edi', 'demo', 'pac_credentials', 'certificate.key'), 'rb').read()
        self.cert_password = '12345678a'
        self.l10n_mx_edi_basic_configuration()
        self.company_partner = self.env.ref('base.main_partner')
        self.payment_term = self.ref('account.account_payment_term_net')
        self.config_parameter = self.env.ref(
            'l10n_mx_edi.l10n_mx_edi_version_cfdi')
        self.xml_expected_str = misc.file_open(os.path.join(
            'l10n_mx_edi', 'tests', 'expected_cfdi33.xml')).read().encode('UTF-8')
        self.xml_expected = objectify.fromstring(self.xml_expected_str)
        isr_tag = self.env['account.account.tag'].search(
            [('name', '=', 'ISR')])
        self.tax_negative.tag_ids |= isr_tag

    def l10n_mx_edi_basic_configuration(self):
        self.company.write({
            'currency_id': self.mxn.id,
            'name': 'YourCompany',
        })
        self.company.partner_id.write({
            'vat': 'ACO560518KW7',
            'country_id': self.env.ref('base.mx').id,
            'zip': '37200',
            'property_account_position_id': self.fiscal_position.id,
        })
        self.account_settings.create({
            'l10n_mx_edi_pac': 'finkok',
            'l10n_mx_edi_pac_test_env': True,
            'l10n_mx_edi_certificate_ids': [{
                'content': base64.encodestring(self.cert),
                'key': base64.encodestring(self.cert_key),
                'password': self.cert_password,
            }]
        }).execute()
        self.set_currency_rates(mxn_rate=21, usd_rate=1)

    def test_l10n_mx_edi_invoice_basic(self):
        # -----------------------
        # Testing sign process
        # -----------------------
        invoice = self.create_invoice()
        invoice.sudo().journal_id.l10n_mx_address_issued_id = self.company_partner.id
        invoice.move_name = 'INV/2017/999'
        invoice.action_invoice_open()
        self.assertEqual(invoice.state, "open")
        self.assertEqual(invoice.l10n_mx_edi_pac_status, "signed",
                         invoice.message_ids.mapped('body'))

        # ----------------
        # Testing discount
        # ----------------
        invoice_disc = invoice.copy()
        for line in invoice_disc.invoice_line_ids:
            line.discount = 10
            line.price_unit = 500
        invoice_disc.compute_taxes()
        invoice_disc.action_invoice_open()
        self.assertEqual(invoice_disc.state, "open")
        self.assertEqual(invoice_disc.l10n_mx_edi_pac_status, "signed",
                         invoice.message_ids.mapped('body'))
        xml = invoice_disc.l10n_mx_edi_get_xml_etree()
        xml_expected_disc = objectify.fromstring(self.xml_expected_str)
        version = xml.get('version', xml.get('Version', ''))
        if version == '3.3':
            xml_expected_disc.attrib['SubTotal'] = '500.00'
            xml_expected_disc.attrib['Descuento'] = '50.00'
            # 500 - 10% + taxes(16%, -10%)
            xml_expected_disc.attrib['Total'] = '477.00'
        self.xml_merge_dynamic_items(xml, xml_expected_disc)
        if version == '3.3':
            xml_expected_disc.attrib['Folio'] = xml.attrib['Folio']
            xml_expected_disc.attrib['Serie'] = xml.attrib['Serie']
            for concepto in xml_expected_disc.Conceptos:
                concepto.Concepto.attrib['ValorUnitario'] = '500.00'
                concepto.Concepto.attrib['Importe'] = '500.00'
                concepto.Concepto.attrib['Descuento'] = '50.00'
        self.assertEqualXML(xml, xml_expected_disc)

        # -----------------------
        # Testing re-sign process (recovery a previous signed xml)
        # -----------------------
        invoice.l10n_mx_edi_pac_status = "retry"
        self.assertEqual(invoice.l10n_mx_edi_pac_status, "retry")
        invoice.l10n_mx_edi_update_pac_status()
        self.assertEqual(invoice.l10n_mx_edi_pac_status, "signed",
                         invoice.message_ids.mapped('body'))
        xml_attachs = invoice.l10n_mx_edi_retrieve_attachments()
        self.assertEqual(len(xml_attachs), 2)
        xml_1 = objectify.fromstring(base64.decodestring(xml_attachs[0].datas))
        xml_2 = objectify.fromstring(base64.decodestring(xml_attachs[1].datas))
        if hasattr(xml_2, 'Addenda'):
            xml_2.remove(xml_2.Addenda)
        self.assertEqualXML(xml_1, xml_2)

        # -----------------------
        # Testing cancel PAC process
        # -----------------------
        invoice.sudo().journal_id.update_posted = True
        invoice.action_invoice_cancel()
        self.assertEqual(invoice.state, "cancel")
        self.assertEqual(invoice.l10n_mx_edi_pac_status, 'cancelled',
                         invoice.message_ids.mapped('body'))
        invoice.l10n_mx_edi_pac_status = "signed"

        # -----------------------
        # Testing cancel SAT process
        # -----------------------
        invoice.l10n_mx_edi_update_sat_status()
        self.assertNotEqual(invoice.l10n_mx_edi_sat_status, "cancelled")

        # Use a real UUID cancelled, only with CFDI version 3.2
        if version == '3.2':
            xml_tfd = invoice.l10n_mx_edi_get_tfd_etree(xml)
            xml_tfd.attrib['UUID'] = '0F481E0F-47A5-4647-B06B-8B471671F377'
            xml.Emisor.attrib['rfc'] = 'VAU111017CG9'
            xml.Receptor.attrib['rfc'] = 'IAL691030TK3'
            xml.attrib['total'] = '1.16'
            xml_attach = invoice.l10n_mx_edi_retrieve_last_attachment()
            xml_attach.datas = base64.encodestring(etree.tostring(xml))
            invoice.l10n_mx_edi_update_sat_status()
            self.assertEqual(invoice.l10n_mx_edi_sat_status, "cancelled",
                            invoice.message_ids.mapped('body'))

    def test_multi_currency(self):
        invoice = self.create_invoice()
        usd_rate = 20.0

        # -----------------------
        # Testing company.mxn.rate=1 and invoice.usd.rate=1/value
        # -----------------------
        self.set_currency_rates(mxn_rate=1, usd_rate=1/usd_rate)
        values = invoice._l10n_mx_edi_create_cfdi_values()
        self.assertEqual(float(values['rate']), usd_rate)

        # -----------------------
        # Testing company.mxn.rate=value and invoice.usd.rate=1
        # -----------------------
        self.set_currency_rates(mxn_rate=usd_rate, usd_rate=1)
        values = invoice._l10n_mx_edi_create_cfdi_values()
        self.assertEqual(float(values['rate']), usd_rate)

        # -----------------------
        # Testing using MXN currency for invoice and company
        # -----------------------
        invoice.currency_id = self.mxn.id
        values = invoice._l10n_mx_edi_create_cfdi_values()
        self.assertFalse(values['rate'])

    def test_addenda(self):
        invoice = self.create_invoice()
        addenda_autozone = self.ref('l10n_mx_edi.l10n_mx_edi_addenda_autozone')
        invoice.sudo().partner_id.l10n_mx_edi_addenda = addenda_autozone
        invoice.sudo().user_id.partner_id.ref = '8765'
        invoice.message_ids.unlink()
        invoice.action_invoice_open()
        self.assertEqual(invoice.state, "open")
        self.assertEqual(invoice.l10n_mx_edi_pac_status, "signed",
                         invoice.message_ids.mapped('body'))
        xml_str = base64.decodestring(invoice.message_ids[-2].attachment_ids.datas)
        xml = objectify.fromstring(xml_str)
        xml_expected = objectify.fromstring(
            '<ADDENDA10 xmlns:cfdi="http://www.sat.gob.mx/cfd/3" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            'xsi:noNamespaceSchemaLocation="https://azfes.autozone.com/xsd/Addenda_Merch_32.xsd" '
            'VERSION="1.0" BUYER="%s" VENDOR_ID="8765" '
            'EMAIL="%s"/>' % (invoice.partner_id.name,
                              invoice.company_id.partner_id.email))
        xml_addenda = xml.Addenda.xpath('//ADDENDA10')[0]
        self.assertEqualXML(xml_addenda, xml_expected)

    def test_l10n_mx_edi_invoice_basic_33(self):
        self.config_parameter.value = '3.3'
        self.xml_expected_str = misc.file_open(os.path.join(
            'l10n_mx_edi', 'tests', 'expected_cfdi33.xml')).read().encode('UTF-8')
        self.xml_expected = objectify.fromstring(self.xml_expected_str)
        self.test_l10n_mx_edi_invoice_basic()

        # -----------------------
        # Testing invoice refund to verify CFDI related section
        # -----------------------
        invoice = self.create_invoice()
        invoice.action_invoice_open()
        refund = self.refund_model.with_context(
            active_ids=invoice.ids).create({
                'filter_refund': 'refund',
                'description': 'Refund Test',
                'date': invoice.date_invoice,
            })
        result = refund.invoice_refund()
        refund_id = result.get('domain')[1][2]
        refund = self.invoice_model.browse(refund_id)
        refund.action_invoice_open()
        refund.refresh()
        xml = refund.l10n_mx_edi_get_xml_etree()
        self.assertEquals(xml.CfdiRelacionados.CfdiRelacionado.get('UUID'),
                          invoice.l10n_mx_edi_cfdi_uuid,
                          'Invoice UUID is different to CFDI related')

        # -----------------------
        # Testing invoice without product to verify no traceback
        # -----------------------
        invoice = self.create_invoice()
        invoice.invoice_line_ids[0].product_id = False
        invoice.compute_taxes()
        invoice.action_invoice_open()
        self.assertEqual(invoice.state, "open")

        # -----------------------
        # Testing send payment by email
        # -----------------------
        invoice = self.create_invoice()
        invoice.action_invoice_open()
        ctx = {'active_model': 'account.invoice', 'active_ids': [invoice.id]}
        bank_journal = self.env['account.journal'].search([
            ('type', '=', 'bank')], limit=1)
        register_payments = self.env['account.register.payments'].with_context(
            ctx).create({
                'payment_date': invoice.date,
                'l10n_mx_edi_payment_method_id': self.env.ref(
                    'l10n_mx_edi.payment_method_efectivo').id,
                'payment_method_id': self.env.ref(
                    "account.account_payment_method_manual_in").id,
                'journal_id': bank_journal.id,
                'communication': invoice.number,
                'amount': invoice.amount_total, })
        payment = register_payments.create_payments()
        payment = self.env['account.payment'].search(payment.get('domain', []))
        self.assertEqual(payment.l10n_mx_edi_pac_status, "signed",
                         payment.message_ids.mapped('body'))
        default_template = self.env.ref(
            'account.mail_template_data_payment_receipt')
        wizard_mail = self.env['mail.compose.message'].with_context({
            'default_template_id': default_template.id,
            'default_model': 'account.payment',
            'default_res_id': payment.id}).create({})
        res = wizard_mail.onchange_template_id(
            default_template.id, wizard_mail.composition_mode,
            'account_payment', payment.id)
        wizard_mail.write({'attachment_ids': res.get('value', {}).get(
            'attachment_ids', [])})
        wizard_mail.send_mail()
        attachment = payment.l10n_mx_edi_retrieve_attachments()
        self.assertEqual(len(attachment), 2,
                         'Documents not attached correctly')
