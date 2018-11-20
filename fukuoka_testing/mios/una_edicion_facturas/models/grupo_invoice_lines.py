# -*- coding: utf-8 -*-
from odoo import api
from odoo import fields
from odoo import models
from datetime import datetime

class GrupoInvoiceLines(models.Model):
    _inherit = 'account.invoice.line'
    
    x_solo_fecha = fields.Date(string="Fecha Registro", default=datetime.today(),store=True)
    
    invoice_date = fields.Date(
                               string="Fecha de factura",
                               related="invoice_id.date_invoice",
                               store=True
                               )

    x_fukuoka_grupo_id = fields.Many2one(
                                         'ops4g_fukuoka.grupos',
                                         string="Grupo",
                                         related="partner_id.x_fukuoka_grupo",
                                         store=True
                                         )

    #x_fecha_registro = fields.Char(string="Fecha Registro",default="factual")
    