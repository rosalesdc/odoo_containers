# -*- coding: utf-8 -*-

from odoo import fields
from odoo import models

class piedra_pulidos(models.Model):
    _name = 'fields_add_products_template.piedra_pulidos'

    name = fields.Char(
                       string="Pulido",
                       required=True,
                       )
