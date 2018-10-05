# -*- coding: utf-8 -*-

from odoo import fields
from odoo import models

class add_fields_plan_contable_model(models.Model):
    _inherit = 'account.account'
    x_codigo_cuenta = fields.Char(string='Código de cuenta')
