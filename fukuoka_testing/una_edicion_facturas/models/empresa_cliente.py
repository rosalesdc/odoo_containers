# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Empresa_cliente(models.Model):
    _inherit = 'account.invoice'

    empresa_relacionada = fields.Many2one(
        'res.partner',
        string="Empresa del cliente",
        related='partner_id',
        store=True,
    )

    grupo_cliente = fields.Many2one(
        'ops4g_fukuoka.grupos',
        string="Grupo del cliente",
        related='partner_id.x_fukuoka_grupo',
        store=True
    )

    color_grupo = fields.Char(
        string="Color del grupo",
        related='partner_id.x_fukuoka_grupo.color',
        store=True
    )

    codigo_consecutivo_porgrupo = fields.Char(
        string="Consecutivo por grupo",
    )

    ultimo_pago = fields.Char(
        string="Fecha de pago",
        compute='get_ultimo_pago',
    )

    @api.multi
    def get_ultimo_pago(self):
        for record in self:
            pagos = record.payment_ids
            if len(pagos) > 0:
                ultimo_pago = pagos[0].payment_date
                record.ultimo_pago = str(ultimo_pago)

    @api.multi
    def obtener_consecutivo_grupo(self, vals):
        # Asignacion del prefijo del prefijo se devuelve como un entero
        partner_id = vals['partner_id']

        # Extraer el objeto de la empresa cliente
        objeto_cliente_id = self.env['res.partner'].sudo().search(
            [
                ('id', '=', partner_id)
            ]
        )

        codigo_grupo_facturas_cliente = objeto_cliente_id.x_fukuoka_grupo.codigo_facturas

        # obtencion de la matricula
        if codigo_grupo_facturas_cliente != ' ' or codigo_grupo_facturas_cliente != False:
            matricula_numeral = self.env['folio.datos'].get_folio(codigo_grupo_facturas_cliente)
        else:
            codigo_grupo_facturas_cliente = "Demo"
            matricula_numeral = self.env['folio.datos'].get_folio("Demo")

        # Matricula en string
        consecutivostr = codigo_grupo_facturas_cliente + str(matricula_numeral)

        # Regreso de la matricula
        return consecutivostr



    @api.model
    def create(self, values):
        # Asignacion de la matricula con el parametro values, valores del registro
        values['codigo_consecutivo_porgrupo'] = self.obtener_consecutivo_grupo(values)

        # Llamado al constructor de la clase a la cual se le reescribio el metodo create
        factura_consecutiva = super(Empresa_cliente, self).create(values)
        return factura_consecutiva