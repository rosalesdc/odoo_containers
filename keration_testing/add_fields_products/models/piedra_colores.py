# -*- coding: utf-8 -*-

from odoo import fields
from odoo import models

class piedra_colores(models.Model):
    _name = 'fields_add_products_template.piedra_colores'

    name = fields.Char(
                       string="Color",
                       required=True,
                       )