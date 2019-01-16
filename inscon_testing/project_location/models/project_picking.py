# -*- coding: utf-8 -*-

from odoo import fields, models, api

class projectPicking(models.Model):
	_inherit = 'project.project'

	picking_ids = fields.One2many('stock.picking.type','project_id',string='Ubicaciones')

	@api.multi
	def get_main_picking(self, name, code, seq):
		self.ensure_one()
		return self.picking_ids.filtered(
			lambda l: l.name == name and l.code == code and l.seq == seq)

	def _create_main_project_picking(self):
		parent = self.env['stock.picking.type'].search(['|',('name', '=', self.name),('name', '=', self.name+' entrega')])
		project_loc = self.env['stock.location'].search([('name', '=', self.name)])
		ubicacion = self.env.ref('stock.stock_location_stock').id
		if not parent:
			for record in project_loc:
				print('locationd id',str(record.id))
				print('name location',str(record.name))
				if record.usage == 'customer':
					location = (
					self.get_main_picking(record.name,'outgoing',32) or
					self._create_main_picking(record.name+' entrega','outgoing',32,record.id,record.id))
				if record.usage == 'internal':
					location = (
					self.get_main_picking(record.name,'internal',34) or
					self._create_main_picking(record.name,'internal',34,ubicacion,record.id))

	@api.multi
	def _create_main_picking(self, name, code, seq, parent, location):
		self.ensure_one()

		#parent = (self.get_main_picking(name,code))

		return self.env['stock.picking.type'].create({
			'name': self.name,
			'code': code,
			'sequence_id':seq,
			'default_location_src_id': parent,
			'default_location_dest_id':location
		})

	@api.model
	def create(self, vals):
		partner = super(projectPicking, self).create(vals)

		if vals.get('name', False):
			partner._create_main_project_picking()

		return partner

	@api.multi
	def write(self, vals):
		if vals.get('name'):
			for partner in self:
				locations = partner.picking_ids.filtered(
					lambda l: l.name == partner.name)
				locations.write({'name': vals.get('name')})

		res = super(projectPicking, self).write(vals)
		return res

class pickingProject(models.Model):
	_inherit = 'stock.picking.type'

	project_id = fields.Many2one('project.project',string='Proyecto')