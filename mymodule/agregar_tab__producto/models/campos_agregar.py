# -*- coding: utf-8 -*-

from odoo import fields
from odoo import models

class campos_agregar(models.Model): 
    _inherit = 'product.template'#modelo de la aplicación, se puede obtener desde la URL de la aplicación
    quilate = fields.Float(string='Quilate', digits=(4, 2), default=0.0)
    balance_quilate = fields.Float(string='Balance quilate', digits=(4, 2), default=0.0)
    medida = fields.Char(string='Medida', default='Ingresa Texto')
    lote = fields.Boolean()
    dato01 = fields.Char(string='dato01', default='Ingresa Texto')
    dato02 = fields.Char(string='dato02', default='Ingresa Texto')
    dato03 = fields.Char(string='dato03', default='Ingresa Texto')
    dato04 = fields.Char(string='dato04', default='Ingresa Texto')
    dato05 = fields.Char(string='dato05', default='Ingresa Texto')
    dato06 = fields.Char(string='dato06', default='Ingresa Texto')
    dato07 = fields.Char(string='dato07', default='Ingresa Texto')
    dato08 = fields.Char(string='dato08', default='Ingresa Texto')