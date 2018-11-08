# -*- coding: utf-8 -*-
# Copyright YEAR(S), AUTHOR(S)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import _
from odoo import api
from odoo import fields
from odoo import models
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError
import time

class ClassName(models.TransientModel):
    _name = 'wizard.pos.invoice'

    #regresa el número de elementos seleccionados
    @api.model
    def _count(self):
        return len(self._context.get('active_ids', []))

    @api.model
    def _get_advance_payment_method(self):
        if self._count() == 1:
            sale_obj = self.env['pos.order']
            order = sale_obj.browse(self._context.get('active_ids'))[0]
            if all([line.product_id.invoice_policy == 'order' for line in order.lines]):
                return 'all'
        return 'delivered'

    advance_payment_method = fields.Selection([
                                              ('delivered', 'Lineas de factura'),
                                              ('all', 'Lineas de factura (deducir pagos por adelantado)'),
                                              ('percentage', 'Deposito (porcentaje)'),
                                              ('fixed', 'Deposito (cantidad fija)')
                                              ], string='¿Que quiere facturar?', default=_get_advance_payment_method, required=True)
    count = fields.Integer(default=_count, string='# de Ordenes')

    @api.onchange('advance_payment_method')
    def onchange_advance_payment_method(self):
        if self.advance_payment_method == 'percentage':
            return {'value': {'amount': 0}}
        return {}

    @api.multi
    def create_invoices(self):
        sale_orders = self.env['pos.order'].browse(self._context.get('active_ids', []))

        if self.advance_payment_method == 'delivered':
            sale_orders.action_invoices_create()
        elif self.advance_payment_method == 'all':
            sale_orders.action_invoices_create()
        return {'type': 'ir.actions.act_window_close'}
    