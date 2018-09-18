# -*- coding: utf-8 -*-

from odoo import models,fields

class herenciaStock(models.Model):
    _inherit='stock.move'
    _name = 'herencia.stock'

