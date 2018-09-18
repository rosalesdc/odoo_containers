
import random
from odoo import models, fields, api

class ComputedModel(models.Model):
    _name = 'test.computed'
    name = fields.Char(compute='_compute_name')

    @api.multi
    def _compute_name(self):
        for record in self:
            record.name = str(random.randint(1, 1e6))