# -*- coding: utf-8 -*-
from odoo import api, fields, models


class GrupoInvoiceLines(models.Model):
	_inherit = 'account.invoice.line'

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
