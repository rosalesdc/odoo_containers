# -*- coding: utf-8 -*-
from odoo import api
from odoo import fields
from odoo import models

class PurchaseOrderLinesIn(models.Model): 
    _inherit = 'purchase.order.line'

    def _prepareHistorico(self, consulta, self2=1):
        print("preparando valores")
        return{
        'product_id':consulta[0],
        'price_unit':consulta[1],
        'date_order':consulta[2],
        'partner_id':consulta[3],
        }
        
    @api.model
    def create(self, vals):
        print("CREATING VALUES:::::::::::::::::::::::::")
        ultimo_precio = -1 #un precio que no deba existir
        valores_historico = {}
        #se obtiene el ultimo precio registrado del producto que se está ingresando
        query = "select product_id,price_unit,order_id,partner_id,create_date from purchase_order_line WHERE product_id= %s ORDER BY create_date DESC LIMIT 1;"
        self.env.cr.execute(query, (vals['product_id'],))
        row = self.env.cr.fetchone()
        
        for columnas in row:
            print(columna)
        
        
        if row is not None: #si es la primera orden puede regresar None
            print('primera aparicion del producto')
            ultimo_precio = row[1]
            valores_historico = self._prepareHistorico(self, row)
            #ultimo_precio=self.env.cr.fetchone()[1]
        
        #se almacena el nuevo registro
        res = super(PurchaseOrderLinesIn, self).create(vals)
        #revisa si el ultimo precio es igual al precio que se está registrando
        if ultimo_precio == res['price_unit']:
            #res['x_precio_nuevo'] = False #variable usada en versión anterior
            print("es igual")
        else:
            #res['x_precio_nuevo'] = True #variable usada en versión anterior
            print("es diferente")
            
            #self.env['historico.variaciones'].create(vals)
            
        return res
    
    #x_precio_nuevo = fields.Boolean(default=True)

    #https://groups.google.com/forum/#!topic/openerp-spain-users/F6coQY-_AIQ
    #http://linkode.org/crzg1ABc81sHxXegbgSI26
    #https://www.odoo.com/es_ES/forum/ayuda-1/question/how-to-do-a-sql-query-in-odoo-10-119605
    #https://www.odoo.yenthevg.com/override-create-functions-odoo/
    
    
        