# -*- coding: utf-8 -*-
from odoo import _
from odoo import api
from odoo import fields
from odoo import models
from odoo import tools
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError
from odoo.http import request
from odoo.tools import float_is_zero

class asientosContables(models.Model):
    _inherit = 'account.invoice'
        
    #cada factura se relaciona con un asiento
    asiento_ids = fields.Many2many('account.move', string='Asientos')
        
    def _prepare_asientos(self,monto_impuesto,fecha_pago):
        """
        Prepara el diccionario de datos para crear el nuevo asiento
	"""
        return {
            'ref':self.number
            ,'journal_id':'6' #Diario: Effectively Paid (MXN) en la base en producción es 5
            ,'amount':monto_impuesto
            ,'date':fecha_pago
            #,'partner_id':self.partner_id
		}
    
    @api.multi
    def action_crear_asientos(self,monto_iva,empresa,fecha_vencimiento,fecha_pago):
        asiento_obj = self.env['account.move']
        #asientos = {}
        #references = {}
#        for facturas in self: 
#            for line in facturas.tax_line_ids:
#                asiento_data=facturas._prepare_asientos(monto_iva)
#                print('haciendo algo')
#                asiento_contable = asiento_obj.create(asiento_data)
        for facturas in self: 
            asiento_data=facturas._prepare_asientos(monto_iva,fecha_pago)
            #print('haciendo algo')
            asiento_contable = asiento_obj.create(asiento_data) #regresa un objeto account_move
            #print(type(asiento_contable))
            linea_obj=asiento_contable.env['account.move.line']
            #print(type(linea_obj))
            linea_asiento=linea_obj.asiento_lines_create(asiento_contable.id,empresa,monto_iva,fecha_vencimiento)
            #print(asiento_contable.partner_id.name)
            #linea_asiento=linea_obj.asiento_lines_create(asiento_contable.id,asiento_contable.partner_id,monto_iva)
            
            
class asientosLines(models.Model):
    _inherit = 'account.move.line'    
    
    @api.multi
    def asiento_lines_create(self, asiento_id, empresa, debe_haber,fecha_vencimiento):
	"""
        Crea las líneas para los asientos contables
	"""
        vals_debe={
        'move_id':asiento_id
        ,'account_id':12
        ,'partner_id':empresa
        ,'name':'118.01 IVA acreditable pagado'
        ,'debit':debe_haber
        ,'date_maturity':fecha_vencimiento
        }
        vals_haber={
        'move_id':asiento_id
        ,'account_id':13
        ,'partner_id':empresa
        ,'name':'119.01 IVA pendiente de pago'
        ,'credit':debe_haber
        ,'date_maturity':fecha_vencimiento
        }
        self.create(vals_debe)
	self.create(vals_haber)
        #self.env['account.invoice.line'].create(vals_debe)
        #self.env['account.invoice.line'].create(vals_haber)

    
#NOTAS
#CODIGO         NOMBRE                  ID  ETIQUETA
#118.01.01	IVA acreditable pagado	12  118.01 IVA acreditable pagado
#119.01.01	IVA pendiente de pago	13  119.01 IVA pendiente de pago


