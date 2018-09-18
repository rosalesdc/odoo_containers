# - * - coding: utf-8 - * -
from odoo import api
from odoo import fields
from odoo import models


class numeroPartida(models.Model):
    _inherit = 'sale.order.line'
    x_num_partida = fields.Integer(string="xnum", default=7)
 #   x_num_partida = fields.Integer(string="xnum", default=_verificar)
    
    
#    @api.onchange('product_id')
#    def _onchange_price(self):
#        # set auto-changing field
#        self.x_num_partida = 5
#        # Can optionally return a warning and domains
#        return {
#            'warning': {
#                'title': "Something bad happened",
#                'message': "It was very bad indeed",
#            }
#            }
    
#    def _verificar(self, self2=1):
#        indice = 7
#        #self.x_num_partida = indice
#        return 7
        
#    @api.onchange('amount', 'unit_price')
#    def _onchange_price(self):
#        # set auto-changing field
#        self.price = self.amount * self.unit_price
#        # Can optionally return a warning and domains
#        return {
#        'warning': {
#            'title': "Something bad happened",
#            'message': "It was very bad indeed",
#        }
#    }

#    método usado si x_num_partida fuera computado
#    x_num_partida = fields.Integer(compute='_write')
#    @api.multi
#    def _write(self,self2=1):
#        indice = 0
#        for record in self:
#            indice = indice + 1
#            record.x_num_partida = indice
