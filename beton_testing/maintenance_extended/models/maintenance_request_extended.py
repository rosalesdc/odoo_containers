# -*- coding: utf-8 -*-
"""
* Created by gonzalezoscar on 2/08/18
* beton_dev
"""
from datetime import datetime

from odoo import api, fields, models
from odoo.exceptions import ValidationError

class MaintenanceRequestExtended(models.Model):
    _inherit = 'maintenance.request'

    x_orden_trabajo = fields.Many2one(
        'ops4g.orden_trabajo',
        string="Orden de trabajo",
    )

    x_proveedor_materiales_id = fields.Many2one(
        'res.partner',
        string="Proveedor para la orden de compra",
        domain="[('supplier', '=', True)]"
    )

    orden_compra_creada = fields.Boolean(
        string="Orden de compra creada",
        help="Si esta casilla se encuentra marcada significa que ya fue "
             "creada una orden de compra para esta petición de mantenimiento.\n"
             "Si desea volver a crear la orden de compra desmarque esta opción",
        default=False,
        track_visibility='onchange',
    )

    x_costo_ot = fields.Float(
        string="Costo de la orden de trabajo",
        related='x_orden_trabajo.costo_total',
    )

    # Recibe un objeto
    @api.multi
    def actualizar_stock_producto(self, product_id, stock_usado):
        if product_id.type == "product":
            stock_producto_obj = self.env['stock.quant'].sudo().search(
                [
                    ('product_id.id', '=', product_id.id)
                ]
            )
            stock_actual = stock_producto_obj.qty
            nuevo_stock = stock_actual - stock_usado
            stock_producto_obj.qty = nuevo_stock
        else:
            print ("\n ********************Este producto no es almacenable")
            print (product_id)

    @api.multi
    def crear_orden_compra(self):
        if self.x_orden_trabajo:
            if self.x_proveedor_materiales_id:
                proveedor = self.x_proveedor_materiales_id.id
            else:
                proveedor = self.env['res.partner'].sudo().search(
                    [
                        ('supplier', '=', True)
                    ]
                )
                proveedor = proveedor[0].id

            orden_compra = self.env['purchase.order'].sudo().create(
                {
                    'partner_id': proveedor,
                }
            )

            orden_compra.sudo().write(
                {
                    'x_s4g_orden_trabajo': self.x_orden_trabajo.id,
                }
            )

            orden_trabajo = self.x_orden_trabajo
            for tarea in orden_trabajo.tareas_ids:
                tarea_odoo = tarea.tarea_id
                # Ciclo para obtener los materiales y crear una linea de orden de compra
                for material in tarea_odoo.listado_materiales_ids:
                    unidad_medida = material.product_id.uom_id
                    precio_unitario = material.product_id.standard_price
                    fecha_planeada = datetime.now()
                    nombre_producto = material.product_id.name + \
                                      " del mantenimiento " + \
                                      orden_trabajo.name + \
                                      " de " + self.name

                    # Actualizar primero el stock del producto usado
                    self.actualizar_stock_producto(material.product_id, material.cantidad)

                    # Crear linea de la orden de compra por cada producto
                    self.env['purchase.order.line'].sudo().create(
                        {
                            'name': nombre_producto ,
                            'order_id': orden_compra.id,
                            'product_id': material.product_id.id,
                            'product_uom': unidad_medida.id,
                            'price_unit': precio_unitario,
                            'date_planned': fecha_planeada,
                            'product_qty': material.cantidad,
                        }
                    )
            self.orden_compra_creada = True
        else:
            raise ValidationError("Por favor asigne una orden de trabajo")
