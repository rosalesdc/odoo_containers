# -*- coding: utf-8 -*-
from odoo import models,fields

class Autos(models.Model):
	_name='personas.autos'

	name=fields.Char(
			string="Matricula",
		)
	color=fields.Char(
			string="Color",
		)
	anio=fields.Char(
			string="Año",
		)
