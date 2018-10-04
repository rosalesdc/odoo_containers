# - * - coding: utf-8 - * -

from odoo import api
from odoo import fields
from odoo import models

class add_rapaport_cost(models.Model):
    _inherit = 'sale.order.line'

    x_rapaport_cost = fields.Float(string='Costo R', digits=(4, 2),default=1)
    