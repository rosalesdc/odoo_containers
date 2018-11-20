# -*- coding: utf-8 -*-
from odoo import fields, models


class Agregar_campos_partners(models.Model):
    _inherit = 'res.partner'

    x_fukuoka_codigo_cliente = fields.Char("Código de cliente")
    x_fukuoka_grupo = fields.Many2one('ops4g_fukuoka.grupos', string="Grupo del cliente")
