# - * - coding: utf-8 - * -

from odoo import api
from odoo import fields
from odoo import models


class porcentaje_rapaport(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('x_rapaport_cost')
    def _compute_costo_quilate_usd(self):
        for record in self:
            self.porcentaje_rap = (self.price_unit/self.x_rapaport_cost * 100) - (100)
            
    
    porcentaje_rap = fields.Float(string='Rap_p', digits=(4, 2), default=0.0)