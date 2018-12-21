# -*- coding: utf-8 -*-
from odoo import _ #importa la función /clase/módulo _ en el namespace actual
from odoo import api
from odoo import exceptions
from odoo import fields
from odoo import models
from odoo.exceptions import UserError
from datetime import datetime, date, timedelta

class Wizard_Asientos_Invoice(models.TransientModel):
    
    _name = 'wizard_asientos_invoice'	#cuando se utiliza este modelo se manejan los registros provistos por TransientModel

    def default_invoices(self):
        return self.env['account.invoice'].browse(self._context.get('active_id'))

    def procesar_asientos(self):
        facturas_sin_impuesto=False
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
        monto_impuesto=0
        lineas_impuesto=0
        for facturas in facturas_todas:
            fecha_pago='1970-01-01'
            print('desde facturas todas: '+str(facturas.number))
            #print(type(facturas))
            ##Verificacion todas las facturas seleccionadas no tienen la columna de impuestos
            empresa=facturas.partner_id.id
            fecha_vencimiento=facturas.date_due
            for invoices_lin in facturas.invoice_line_ids:
                lineas_impuesto=invoices_lin.invoice_line_tax_ids.amount
                if lineas_impuesto != 0:
                    raise UserError(_('Factura seleccionada con impuestos en columnas: '+facturas.number))
            ##Verificacion todas las facturas seleccionadas no tienen la columna de impuestos
            for lines in facturas.tax_line_ids:
                #print('Impuesto: '+str(lines.name))
                #print('Importe: '+str(lines.amount))
                #print('Cuenta: '+str(lines.account_id.name)+'ID cuenta: '+str(lines.account_id.id))
                if lines.account_id.id==13:
                    monto_impuesto=lines.amount
             
            #Verificar que las lineas de abajo sí tengan el impuesto registrado(de otra forma saldrían asientos con 0)
            #print('monto de la cuenta 13: '+str(monto_impuesto))
            if monto_impuesto == 0:
                raise UserError(_('Factura con lineas inferiores sin registro de IVA o en cero: '+facturas.number))
            #Verificar que las lineas de abajo sí tengan el impuesto registrado(de otra forma saldrían asientos con 0)
            
            #Obtener fecha de último pago para la fecha del asiento
            for pagos in facturas.payment_ids:
                fecha_linea=pagos.payment_date
                fecha_pago=self.obtener_fecha_posterior(fecha_pago,fecha_linea)
            if fecha_pago=='' or fecha_pago=='1970-01-01':
                raise UserError(_('Error en fecha de pagos, sin pago?: '+facturas.number))
            #Obtener fecha de último pago para la fecha del asiento
            
            facturas.action_crear_asientos(monto_impuesto,empresa,fecha_vencimiento,fecha_pago)
    
    def obtener_fecha_posterior(self,fecha_1,fecha_2):
        if fecha_1>=fecha_2:
            return fecha_1
        else:
            return fecha_2
        
    
    invoices_ids = fields.Many2many('account.invoice', string='Facturas', default=default_invoices)
