# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, fields,api,_

from odoo.exceptions import UserError, ValidationError

class QuantityBudget(models.Model):
    _name = 'qty.budget'
    _description = 'Quantity Budget'
    
    name = fields.Many2one("product.category",string="Product Category",required=True)
    qty = fields.Float("Quantity",required=True)
    uom_id = fields.Many2one("uom.uom",string="UOM",required=True)
    project_id = fields.Many2one("project.project",string="Project")
    cantidad_total=fields.Float(string="Presupuesto",default=0.0)


    @api.model
    def create(self, vals):

        rec=super(QuantityBudget, self).create(vals)
        print(rec.project_id)
        total=self.search_count([('name', '=', rec.name.id), ('project_id', '=', rec.project_id.id)])
        print(total)
        if total>1:
            raise ValidationError(_('Product Category should not be repeat!'))
        print(rec)
        return rec
    
