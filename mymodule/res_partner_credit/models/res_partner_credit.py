# -*- coding: utf-8 -*-

from odoo import fields, models, api

class resPartnerCredit(models.Model):
    _inherit = 'res.partner'
    nss = fields.Char(string='Num seguridad social')
    barcode = fields.Char(compute='_set_id_partner')
    #codigo=fields.Char(related='barcode',store=True)
    
    @api.multi
    def _set_id_partner(self):
        for record in self:
            identificador = str(record.id)
            record.barcode = identificador