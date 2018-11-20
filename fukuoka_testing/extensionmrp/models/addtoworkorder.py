# -*- coding: utf-8 -*-
from odoo import api, fields, models

class AddToTorkOrder(models.Model):
    _inherit = 'mrp.workorder'

    cliente_id = fields.Many2one(
        'res.partner',
        string=u"Cliente",
        related='production_id.cliente'
    )
