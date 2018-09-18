# -*- coding: utf-8 -*-
from odoo import models,fields

class Refaccion(models.Model): #paquete.clase
	_name='refaccion.informacion_detalle' #por convencion nombre significativo.loque se va a guardar, name siempre se ha de poner
	name=fields.Char(
		string="Nombre de la Refaccion", #es una etiqueta
		required=True,
		index=True,
		)

	proveedor = fields.Selection(
		selection=[
			('1', 'AutoZone'),
			('2', 'Refacciones California'),
			('3', 'Refaccionaria del Pacifico')
		],
		string="Proveedor",
		required=True,
		default="AutoZone"
	)

	unidades_inicial=fields.Integer(
		string="Número de unidades inicial",
		default=7,
		required=True,
		)
	descontinuado=fields.Boolean(
		string="Producto descontinuado",
		)
	fecha_registro=fields.Date(
		string="fecha_registro",
		)