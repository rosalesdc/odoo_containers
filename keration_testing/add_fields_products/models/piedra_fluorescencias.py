# -*- coding: utf-8 -*-

from odoo import fields
from odoo import models

class piedra_fluorescencias(models.Model):
    _name = 'fields_add_products_template.piedra_fluorescencias'

    name = fields.Char(
                       string="Fluorescencia",
                       required=True,
                       )

