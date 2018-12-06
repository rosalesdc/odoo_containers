# -*- coding: utf-8 -*-

from odoo import api
from odoo import exceptions
from odoo import fields
from odoo import models

class Wizard_Asientos_Invoice(models.TransientModel):
    
    _name = 'wizard_asientos_invoice'	#cuando se utiliza este modelo se manejan los registros provistos por TransientModel

    def default_invoices(self):
        return self.env['account.invoice'].browse(self._context.get('active_id'))

    def procesar_asientos(self):
        monto_impuesto=0
        facturas_todas = self.env['account.invoice'].browse(self._context.get('active_ids', []))
#        for record in self.invoices_ids:
#            print('REFERENCIA:', str(record.number))
#            print('FECHA:', str(record.date))
#            print('EMPRESA:', str(record.partner_id.name))
#            print('LINEAS TAX:::')
#            for line in record.tax_line_ids:
#                print('IMPUESTO: '+str(line.name))
#                print('IMPORTE: '+str(line.amount))
#                print('CUENTA: '+str(line.account_id.name))
        
        for facturas in facturas_todas:
            print('desde facturas todas: '+str(facturas.number))
            print(type(facturas))
            empresa=facturas.partner_id.id
            for lines in facturas.tax_line_ids:
                print('Impuesto: '+str(lines.name))
                print('Importe: '+str(lines.amount))
                print('Cuenta: '+str(lines.account_id.name)+'ID cuenta: '+str(lines.account_id.id))
                if lines.account_id.id==13:
                    monto_impuesto=lines.amount
                    
            facturas.action_crear_asientos(monto_impuesto,empresa)

    invoices_ids = fields.Many2many('account.invoice', string='Facturas', default=default_invoices)
