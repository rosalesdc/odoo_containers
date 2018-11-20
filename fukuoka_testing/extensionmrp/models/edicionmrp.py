# -*- coding: utf-8 -*-
from odoo import api, models, fields


class Edicionmrp(models.Model):
    _inherit = 'mrp.production'

    order_venta_origen = fields.Many2one(
        'sale.order',
        string="Enlace a la orden de venta",
        help="Orden de venta con enlace",
        compute='get_customer',
        readonly=True
    )

    cliente = fields.Many2one(
        'res.partner',
        string=u"Cliente",
        compute='get_customer',
    )

    @api.one
    @api.depends('origin')
    def get_customer(self):
        for record in self:
            order_venta = record.env['sale.order'].search([('name', '=', record.origin)])
            record.order_venta_origen = order_venta
            cliente_id = order_venta.partner_id
            record.cliente = cliente_id
