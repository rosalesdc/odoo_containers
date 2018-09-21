# - * - coding: utf-8 - * -

from odoo import api
from odoo import fields
from odoo import models


class indice_partida(models.Model):
    _inherit = 'sale.order.line'

#    def _verificar(self, self2=1):
#        if self.x_num_partida == 0:
#            return 3
#        else:
#            return 6
#            
#    @api.multi
#    def _write(self,self2=1):
#        indice = 0
#        for record in self:
#            indice = indice + 1
#            record.x_num_partida = indice

    @api.multi
    def _write_values(self, self2=1):
        indice = 0
        for record in self:
            if record.x_num_partida == 0:
                indice = indice + 1
                record.x_num_partida_computed = indice
            else:
                record.x_num_partida_computed = record.x_num_partida
    
    
    x_num_partida = fields.Integer(string="Índice editable", default='0')
    x_num_partida_computed = fields.Integer(string="Índice", compute='_write_values')