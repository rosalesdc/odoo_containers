# -*- coding: utf-8 -*-

from odoo import fields
from odoo import models

class piedra_simetrias(models.Model):
    _name = 'fields_add_products_template.piedra_simetrias'

    name = fields.Char(
                       string="Simetría",
                       required=True,
                       )
