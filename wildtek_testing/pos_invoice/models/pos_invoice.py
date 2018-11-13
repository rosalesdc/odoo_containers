# -*- coding: utf-8 -*-
# Copyright YEAR(S), AUTHOR(S)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _
from odoo import api
from odoo import fields
from odoo import models
from odoo import tools
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError
from odoo.http import request
from odoo.tools import float_is_zero

class posInvoice(models.Model):
    _inherit = 'pos.order'

    invoice_ids = fields.Many2many('account.invoice', string='Facturas')

    def _prepare_invoices(self, partner):
        """
		Prepare the dict of values to create the new invoice for a pos order.
		"""
        return {
            'name': self.name,
            'origin': self.name,
            'account_id': partner.property_account_receivable_id.id,
            'journal_id': self.session_id.config_id.invoice_journal_id.id,
            'type': 'out_invoice',
            'reference': self.name,
            'partner_id': partner.id,
            'comment': self.note or '',
            # considering partner's sale pricelist's currency
            'currency_id': self.pricelist_id.currency_id.id,
            'user_id': self.env.uid,
        }

        
    
        
    @api.multi
    def action_invoices_create(self, grouped=False, final=False):
        """
		Create the invoice associated to the SO.
		:param grouped: if True, invoices are grouped by SO id. If False, invoices are grouped by
						(partner_invoice_id, currency)
		:param final: if True, refunds will be generated if necessary
		:returns: list of created invoices
		"""
        #YO
        ##VACIAR TODAS LAS LINEAS DE TODOS LOS PEDIDOS EN UNA LISTA
        nueva_orden=[]
        print("INICIAN LINEAS")
        for order in self:
            for line in order.lines:
                nueva_orden.append(line)
                #print(line.product_id.name,'|',line.qty,'|',line.price_unit,'|',line.discount,'|',line.tax_ids_after_fiscal_position,'|',line.price_subtotal,'|',line.price_subtotal_incl)
        print("FIN DE LINEAS")
        #####
        
        ##VACIAR LINEAS CON PRODUCTOS NO REPETIDOS
        nueva_orden2=[]
        ft=True;
        existe=False
        print("INICIAN LINEAS SIN REPETIR")
        for order in self:
            print('hola nuevo for1')
            for line in order.lines:
                ##Ahora se itera el nuevo objeto en busca de elemento repetido
                print('hola nuevo for2')
                if ft:
                    nueva_orden2.append(line)
                    ft=False
                    print('FT')
                for registros in nueva_orden2:
                    print('hola nuevo for3')
                    print(registros.product_id.name,'??',line.product_id.name);
                    if registros.product_id.name==line.product_id.name:
                        print('elemento SI repetido')
                        existe=True;
                    else:
                        print('elemento NO repetido')
                        existe=False;
                    if existe==True:
                        break
                if existe==False:
                        nueva_orden2.append(line)
        print("FIN DE LINEAS SIN REPETIR")
        
        print('INICIA CONTENIDO DE LA LISTA NUEVA::::::')
        for registros in nueva_orden2:
            print(registros.product_id.name,'\t|',registros.qty,'\t|',registros.price_unit,'\t|',registros.discount,'\t|',registros.tax_ids_after_fiscal_position,'\t|',registros.price_subtotal,'\t|',registros.price_subtotal_incl)
        print('FIN CONTENIDO DE LA LISTA NUEVA::::::')
        #####
        #

        inv_obj = self.env['account.invoice']
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        invoices = {} # diccionarios
        references = {} # diccionarios
        for order in self: #ids seleccionados de pos.order
            if order.partner_id or not order.partner_id:
                partner = self.env['res.partner'].search([('vat', '=', 'XAXX010101000')], limit=1)#partner tiene todos los datos del RFC genérico
            group_key = order.id if grouped else (partner.id, order.pricelist_id.currency_id.id)
            if order.amount_total > 0:
                for line in order.lines.sorted(key=lambda l: l.qty < 0): #varible line
                    if float_is_zero(line.qty, precision_digits=precision):
                        continue
                    if group_key not in invoices:
                        inv_data = order._prepare_invoices(partner)
                        invoice = inv_obj.create(inv_data)
                        references[invoice] = order
                        invoices[group_key] = invoice
                    elif group_key in invoices:
                        print('group in invoices')
                        vals = {}
                        if order.name not in invoices[group_key].origin.split(', '):
                            vals['origin'] = invoices[group_key].origin + ', ' + order.name
                        if order.pos_reference and order.pos_reference not in invoices[group_key].name.split(', ') and order.pos_reference != invoices[group_key].name:
                            vals['name'] = invoices[group_key].name + ', ' + order.pos_reference
                        invoices[group_key].write(vals)
                    if line.qty > 0:
                        print ('cantidad >>>> 0', line.qty)
                        print ('invoices group key ', invoices[group_key].id)
                        line.invoice_lines_create(invoices[group_key].id, line.qty)
                    elif line.qty < 0 and final:
                        print ('cantidad <<<< 0 and final', line.qty)
                        line.invoice_lines_create(invoices[group_key].id, line.qty)

                if references.get(invoices.get(group_key)):
                    print ('if references get invoices group key', references[invoice])
                    if order not in references[invoices[group_key]]:
                        print ('if order not in references invoices', references[invoice], order)
                        references[invoice] = references[invoice] | order
                order.write({'state':'invoiced'})
        #esto ya no entraria al if amount_total > 0		
        if not invoices:
            raise UserError(_('There is no invoicable line.error 1'))

        for invoice in invoices.values():
            print ('<<<<<<<<>>>>>>>>>>', invoice)
            if not invoice.invoice_line_ids:
                raise UserError(_('There is no invoicable line.error 2'))
            # If invoice is negative, do a refund invoice instead
            if invoice.amount_untaxed < 0:
                invoice.type = 'out_refund'
                for line in invoice.invoice_line_ids:
                    line.quantity = -line.quantity
            # Use additional field helper function (for account extensions)
            for line in invoice.invoice_line_ids:
                line._set_additional_fields(invoice)
            invoice.compute_taxes()
            invoice.message_post_with_view('mail.message_origin_link',
                                           values={'self': invoice, 'origin': references[invoice]},
                                           subtype_id=self.env.ref('mail.mt_note').id)
        return [inv.id for inv in invoices.values()]

class posOrderLineInvoices(models.Model):
    _inherit = 'pos.order.line'

    @api.multi
    def invoice_lines_create(self, invoice_id, qty):
        """
		Create an invoice line. The quantity to invoice can be positive (invoice) or negative
		(refund).

		:param invoice_id: integer
		:param qty: float quantity to invoice
		"""
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        for line in self:
            if not float_is_zero(qty, precision_digits=precision):
                vals = line._prepare_invoice_lines(qty=qty)
                vals.update({'invoice_id': invoice_id, 'pos_line_ids': [(6, 0, [line.id])]})
                print ('vals line create ', vals)
                self.env['account.invoice.line'].create(vals)

    @api.multi
    def _prepare_invoice_lines(self, qty):
        """
		Prepare the dict of values to create the new invoice line for a sales order line.

		:param qty: float quantity to invoice
		"""
        self.ensure_one()
        res = {}
        account = self.product_id.property_account_income_id or self.product_id.categ_id.property_account_income_categ_id
        if not account:
            raise UserError(_('Please define income account for this product: "%s" (id:%d) - or for its category: "%s".') %
                            (self.product_id.name, self.product_id.id, self.product_id.categ_id.name))

        partner = self.env['res.partner'].search([('vat', '=', 'XAXX010101000')], limit=1)
        fpos = self.order_id.fiscal_position_id or partner.property_account_position_id
        if fpos:
            account = fpos.map_account(account)
        res = {
            'name': self.product_id.name,
            'account_id': account.id,
            'price_unit': self.price_unit,
            'quantity': qty,
            'discount': self.discount,
            'product_id': self.product_id.id or False,
            'uom_id': self.product_id.uom_id.id,
        }
        return res

class accountInvoicePos(models.Model):
    _inherit = 'account.invoice.line'
    pos_line_ids = fields.Many2many('pos.order.line', string='Lines de pedido TPV')
    