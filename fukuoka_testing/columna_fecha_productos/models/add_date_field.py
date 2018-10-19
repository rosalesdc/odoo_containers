# -*- coding: utf-8 -*-
from odoo import api
from odoo import fields
from odoo import models

class add_date_field(models.Model):
    _inherit = 'account.invoice.line'
    #_inherit = 'account.payment'
    
    x_fecha_registro = fields.Date(string="Fecha de registro", default=fields.Date.context_today,store=True)
    x_invoice_date = fields.Date(
		string="XFecha de factura",
		related="invoice_id.date_invoice",
		store=True
	)