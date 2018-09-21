# -*- coding: utf-8 -*-

from odoo import models,fields,api,exceptions, _

class add_fields_rapaport_model(models.Model): 
	_inherit='product.template'

	numero_rapaport=fields.Integer('Costo Rapaport',store=True)
	descuento_rapaport=fields.Float('Porcentaje de descuento Rapaport',(9,2),store=True)
	costo_quilate_usd=fields.Float('Costo unitario del quilate en USD ',compute='_compute_costo_quilate_usd')
	costo_total=fields.Float('Costo total de la pieza',compute='_compute_costo_total')
#	name = fields.Char(compute='_compute_name')	
	@api.depends('costo_quilate_usd','numero_rapaport','descuento_rapaport')
	def _compute_costo_quilate_usd(self):
		for record in self:
			costo_quilate_usd=(100*self.numero_rapaport)*(1-(self.descuento_rapaport/100))
			record.description= "El costo por quilate recalculado es: $'{0}'".format(record.costo_quilate_usd)
			record.costo_quilate_usd=costo_quilate_usd
			return costo_quilate_usd


	@api.depends('costo_total','costo_quilate_usd')
	def _compute_costo_total(self): 
		for record in self:
			costo_total=record.costo_quilate_usd*record.quilate
			record.description= "El costo recalculado de la pieza es: $'{0}'".format(record.costo_total)
			record.costo_total=costo_total
			return costo_total


		

#	def _default_category(self):
#		print('RASTREANDO',str(self.env['product.product'].browse(self._context.get('categ_id'))))
#		return self.env['product.category'].browse(self._context.get('product.category'))

#	product_ids=fields.Many2many('product.product',string='Categorias', default=_default_category)

	
				
