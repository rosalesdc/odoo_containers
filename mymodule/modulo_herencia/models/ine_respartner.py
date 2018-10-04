# -*- coding: utf-8 -*-

from odoo import models,fields

class ineResPartner(models.Model): 
    _inherit='res.partner'#modelo de la aplicación, se puede obtener desde la URL de la aplicación
    ine=fields.Char(string='INE')
