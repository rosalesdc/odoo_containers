# -*- coding: utf-8 -*-

from odoo import api
from odoo import fields
from odoo import models

class generaFactura(models.TransientModel): #genera registros temporales sólo al momento de llamar al wizard    
    
    _name='wizard.genera.factura'
    
    def _verificar_seleccion(self):
        print('Hello verificacion');
            
    #método default
    def _default_factura(self):
        return self.env['pos.order'].browse(self._context.get('active_ids'))
        
    pedidos_ids=fields.Many2many('pos.order',string='Pedidos',default=_default_factura)

            
    def genera_factura(self):
        print('Hello');
        _verificar_seleccion()
        #Revisar si los elementos tienen estado Publicado (paid,invoiced,done)
        for record in self.pedidos_ids:
            print('Elemento Seleccionado',str(record.id))
            if str(record.state)=='invoiced':
                print('Seleccion incorrecta: Elemento ya facturado')
            if str(record.state)=='paid':
                print('Seleccion incorrecta: Elemento sin cierre de sesion')
    
