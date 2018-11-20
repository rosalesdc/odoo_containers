# -*- coding: utf-8 -*-
from odoo import api, fields, models


class GruposClientes(models.Model):
    _name = 'ops4g_fukuoka.grupos'
    _order = 'name'

    name = fields.Char(
        string="Nombre del grupo",
        required=True,
        help="Nombre del grupo",
    )

    color = fields.Char(
        string="Color del grupo",
    )


    clientes_ids = fields.One2many(
        'res.partner',
        'x_fukuoka_grupo',
        string="Clientes"
    )

    codigo_facturas = fields.Char(
        string="Código para las facturas"
    )

    mostrar_en_facturas = fields.Boolean(
        string="¿Mostrar consecutivo en las facturas impresas?"
    )

    _sql_constraints = [
        (
            'name_uniq',
            'UNIQUE (name)',
            '¡¡Ya existe un grupo con este nombre!!'
        ),
        (
            'codigo_facturas_uniq',
            'UNIQUE (codigo_facturas)',
            '¡¡El código para las facturas debe ser único!!'
        )
    ]
