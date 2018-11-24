# - * - coding: utf-8 - * -

from odoo import api
from odoo import fields
from odoo import models

class IncrementaLote(models.Model):
    _inherit = 'stock.move.line'
    
    @api.model
    def _crear_numero_lote(self):
        folio=1
        for record in self:
            print ('HIIIIIIIIIIIIIII')
        
        product_string=str(self.product_id)
        print ('creando lote 1: ',product_string)
        
        move_string=str(self.picking_id)
        print ('creando lote 1: ',move_string)
        
        lote=product_string+'/'+move_string+str(folio)
        folio+=1
        return lote
        
    lot_name = fields.Char(default=_crear_numero_lote)
