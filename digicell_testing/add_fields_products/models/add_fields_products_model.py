# -*- coding: utf-8 -*-

from odoo import fields
from odoo import models

class add_fields_products_model(models.Model):
    _inherit = 'product.template'
    clave_alterna = fields.Char(string='Clave Alterna')
    clave_unidad = fields.Char(string='Clave Unidad')