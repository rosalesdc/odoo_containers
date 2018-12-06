# -*- coding: utf-8 -*-
# Copyright YEAR(S), AUTHOR(S)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import _ #importa la función /clase/módulo _ en el namespace actual
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
        ##PRUEBAS SOBRE REASIGNACION A LINEAS ORIGINALES-*-*-*-*-*-*-*-*-*-*-*-*-
        aux=[]
        lista_tuplas2=[]
        lista_tuplas=[]
        """
        print("Pintanto lineas originales...")
        for order in self:
            for line in order.lines:
                print(line.id,'\t',line.product_id.id,'\t',line.product_id.name,'\t|',line.qty,'\t|',line.price_unit,'\t|',line.discount,'\t|',line.tax_ids_after_fiscal_position,'\t|',line.price_subtotal,'\t|',line.price_subtotal_incl)
        """
        print("Poniendo registros en lista auxiliar y tuplas...")
        for order in self:
            for line in order.lines:
                tupla=(line.id,line.qty)
                lista_tuplas.append(tupla)
                aux.append(line)
        """                    
        print("Pintando nueva orden...")
        for registros in aux:
            registros.qty+=1
            print(registros.id,'\t',registros.product_id.id,'\t',registros.product_id.name,'\t|',registros.qty,'\t|',registros.price_unit,'\t|',registros.discount,'\t|',registros.tax_ids_after_fiscal_position,'\t|',registros.price_subtotal,'\t|',registros.price_subtotal_incl)
        """   
        """
        print('Regresando lineas originales...')
        for registros in self:
            for line in registros.lines:
                #print('id linea actual: ',line.id)
                for elementos in lista_tuplas:
                    #print('recorriendo tupla',line.id,'??',elementos[0])
                    if line.id==elementos[0]:
                        line.qty=elementos[1]
        """
        """
        print("Pintanto orden original")
        for order in self:
            for line in order.lines:
                print(line.id,'\t',line.product_id.id,'\t',line.product_id.name,'\t|',line.qty,'\t|',line.price_unit,'\t|',line.discount,'\t|',line.tax_ids_after_fiscal_position,'\t|',line.price_subtotal,'\t|',line.price_subtotal_incl)
        """
        
        """
        print('pintando tuplas')
        for elementos in lista_tuplas:
            print(elementos[0],'-',elementos[1])
        """
        ##PRUEBAS SOBRE REASIGNACION A LINEAS ORIGINALES-*-*-*-*-*-*-*-*-*-*-*-*-

        nueva_orden2=[]
        ft=True
        ft2=True
        existe=False
        
        print("INICIAN LINEAS SIN REPETIR")
        for order in self:
            print('hola nuevo for1')
            for line in order.lines:
                ##Se itera el nuevo objeto en busca de elemento repetido
                print('hola nuevo for2')
                if ft:
                    #Se carga siempre el primer elemento al iniciar para que el siguiente for pueda empezar a iterar
                    tupla2=(line.id,line.qty)
                    lista_tuplas2.append(tupla2)
                    nueva_orden2.append(line)
#                    if aux is line: print('son iguales =(') 
#                    else: print ('NO SON IGUALES')
                    ft=False
                    print('FT')
                for registros in nueva_orden2:
                    #print('hola nuevo for3')
                    #print(registros.product_id.name,'??',line.product_id.name)
                    if registros.product_id.id==line.product_id.id and registros.price_unit==line.price_unit:
                        if ft2:
                            ft2=False
                            existe=True
                            #print('UNA VEZ')
                        else:
                            #print('elemento SI repetido')
                            registros.qty+=line.qty
                            existe=True
                    else:
                        #print('elemento NO repetido')
                        existe=False
                    if existe==True:
                        break
                if existe==False:
                    #print('aqui no llega')
                    tupla2=(line.id,line.qty)
                    lista_tuplas2.append(tupla2)
                    nueva_orden2.append(line)
        print("FIN DE LINEAS SIN REPETIR")
        print('INICIA CONTENIDO DE LA LISTA NUEVA::::::')
        for registros in nueva_orden2:
            print(registros.product_id.id,'\t',registros.product_id.name,'\t|',registros.qty,'\t|',registros.price_unit,'\t|',registros.discount,'\t|',registros.tax_ids_after_fiscal_position,'\t|',registros.price_subtotal,'\t|',registros.price_subtotal_incl)
        print('FIN CONTENIDO DE LA LISTA NUEVA::::::')
        ####
 
        inv_obj = self.env['account.invoice']
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        invoices = {}
        references = {}
        ft=True
        for order in self:
            if order.partner_id or not order.partner_id:
                partner = self.env['res.partner'].search([('vat', '=', 'XAXX010101000')], limit=1)
            group_key = order.id if grouped else (partner.id, order.pricelist_id.currency_id.id)
            if ft==True:
                for line in nueva_orden2:
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
                    line.factura_acumulada=invoices[group_key].id #REGISTRA EN LA LINEA DE ORDEN, CUAL ES LA FACTURA DESTINO
                if references.get(invoices.get(group_key)):
                    print ('if references get invoices group key', references[invoice])
                    if order not in references[invoices[group_key]]:
                        print ('if order not in references invoices', references[invoice], order)
                        references[invoice] = references[invoice] | order
            order.write({'state':'invoiced'})
            ft=False
        if not invoices:
            raise UserError(_('There is no invoicable line.error 1'))

        for invoice in invoices.values():
            print ('<<<<<<<<>>>>>>>>>>', invoice)
            if not invoice.invoice_line_ids:
                raise UserError(_('There is no invoicable line.error 2'))

            if invoice.amount_untaxed < 0:
                invoice.type = 'out_refund'
                for line in invoice.invoice_line_ids:
                    line.quantity = -line.quantity

            for line in invoice.invoice_line_ids:
                line._set_additional_fields(invoice)
            invoice.compute_taxes()
            invoice.message_post_with_view('mail.message_origin_link',
                                           values={'self': invoice, 'origin': references[invoice]},
                                           subtype_id=self.env.ref('mail.mt_note').id)
#        print('pintando tuplas2')
#        for elementos in lista_tuplas2:
#            print(elementos[0],'-',elementos[1])
        print('Regresando lineas originales...')
        for registros in self:
            for line in registros.lines:
                #print('id linea actual: ',line.id)
                for elementos in lista_tuplas:
                    #print('recorriendo tupla',line.id,'??',elementos[0])
                    if line.id==elementos[0]:
                        line.qty=elementos[1]    
        print('finalizando....')
        
        return [inv.id for inv in invoices.values()]

class posOrderLineInvoices(models.Model):
    _inherit = 'pos.order.line'
    factura_acumulada = fields.Integer(#se había considerado un campo M2O con 'account.invoice', pero podría haber pedidos que no se facturen
                                       string="Factura acumulada donde se registró",
                                       )

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
