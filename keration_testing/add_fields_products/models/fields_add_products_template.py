# -*- coding: utf-8 -*-

from odoo import fields
from odoo import models

class fields_add_products_template(models.Model): 
    _inherit = 'product.template'#modelo de la aplicación, se puede obtener desde la URL de la aplicación
    
    quilate = fields.Float(string='Quilate', digits=(4, 2), default=0.0)
    balance_quilate = fields.Float(string='Balance quilate', digits=(4, 2), default=0.0)
    medida = fields.Char(string='Medida')
    lote = fields.Boolean()
#    nombre_proveedor=fields.Char(string='Nombre del Proveedor', default='Ingresa Texto')
#    referencia_proveedor=fields.Char(string='No. de referencia de proveedor', default='Ingresa Texto')
#    procedencia=fields.Char(string='Lugar de procedencia', default='Ingresa Texto')
    
    piedra_formas_id = fields.Many2one(
                                       'fields_add_products_template.piedra_formas', #modelo relacionado
                                       string="Forma",
                                       required=True,
                                       )
    piedra_colores_id = fields.Many2one(
                                        'fields_add_products_template.piedra_colores', #modelo relacionado
                                        string="Color",
                                        required=True,
                                        )
    piedra_laboratorios_id = fields.Many2one(
                                       'fields_add_products_template.piedra_laboratorios',#modelo relacionado
                                       string="Laboratorio",
                                       required=True,
                                       )
    piedra_cortes_id = fields.Many2one(
                                       'fields_add_products_template.piedra_cortes',#modelo relacionado
                                       string="Corte",
                                       required=True,
                                       )
    piedra_claridades_id = fields.Many2one(
                                       'fields_add_products_template.piedra_claridades',#modelo relacionado
                                       string="Claridad",
                                       required=True,
                                       )
    piedra_pulidos_id = fields.Many2one(
                                       'fields_add_products_template.piedra_pulidos',#modelo relacionado
                                       string="Pulido",
                                       required=True,
                                       )
    piedra_fluorescencias_id = fields.Many2one(
                                       'fields_add_products_template.piedra_fluorescencias',#modelo relacionado
                                       string="Fluorescencia",
                                       required=True,
                                       )
    piedra_simetrias_id = fields.Many2one(
                                       'fields_add_products_template.piedra_simetrias',#modelo relacionado
                                       string="Simetría",
                                       required=True,
                                       )