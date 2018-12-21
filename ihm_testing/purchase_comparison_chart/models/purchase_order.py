from odoo import models, fields,api,_
from urllib.parse import urljoin
from odoo.addons.website.models.website import slugify
from odoo.exceptions import UserError
import xlwt
import base64
from datetime import datetime

from werkzeug.urls import url_encode
import werkzeug

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.model
    def create(self,vals):
        if vals.get('requisition_id'):
            purchase_ids = self.env['purchase.order'].search([('requisition_id','=',vals.get('requisition_id'))])
            for po_id in purchase_ids:
                if vals.get('partner_id') == po_id.partner_id.id:
                    raise UserError(_('RFQ is available for this purchase agreement for the same vendor'))
        return super(PurchaseOrder, self).create(vals)

    @api.multi
    def write(self, vals):
        if vals.get('partner_id') or vals.get('requisition_id'):
            purchase_ids = self.env['purchase.order'].search([('requisition_id', '=', vals.get('requisition_id'))])
            for po_id in purchase_ids:
                if vals.get('partner_id') == po_id.partner_id.id:
                    raise UserError(_('RFQ is available for this purchase agreement for the same vendor'))
        return super(PurchaseOrder, self).write(vals)


