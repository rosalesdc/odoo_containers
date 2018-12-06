# - * - coding: utf-8 - * -
from odoo import _
from odoo import api
from odoo import fields
from odoo import models
from odoo import exceptions
from openerp.http import request
from openerp import http

class IncrementaLote(models.Model):
    _inherit = 'stock.move.line'
    
    @api.model
    def _crear_numero_lote(self):
        active_id_=self._context
        if not 'default_move_id' in active_id_:
            #print ('default id: '+str(active_id_))
            matricula_tmp=''
        else:
            rec = self.env['stock.move'].browse((active_id_['default_move_id']))
            #prefijoMatricula=str(rec.origin+'/'+rec.product_id.name+'/') modificando, para checar si el escaner puede leer
            #GENERAR NUEVOS NOMBRES DE PACAS
            #print('Orden almacenada: '+rec.origin)
            norden=str(rec.origin)
            norden=norden[2:len(norden)]
            #print('Nueva Orden: '+norden)
            #print('Codigo Barras: '+str(rec.product_id.barcode))
            #print('nuevo codigo: '+norden+str(rec.product_id.barcode))
            #GENERAR NUEVOS NOMBRES DE PACAS
            prefijoMatricula=norden+str(rec.product_id.barcode)
            matricula_tmp = self.env['core_generador_folio'].getFolio(prefijoMatricula)
            if not matricula_tmp:
                formato_folio_id = self.env['core_formato_folio'].search([('formato', '=', "{prefijo}{contador}")]).id
                dic = {
                    'nombre_folio': "FOLIO" + prefijoMatricula,
                    'prefijo': prefijoMatricula,
                    'numero_zeros': 2,
                    'contador': 0,
                    'formato_fecha': "%y",
                    'tipo_folio_id': formato_folio_id,
                }
                matricula_tmp = self.env['core_generador_folio'].createGenericFolio(dic)
        print(matricula_tmp)
        return matricula_tmp

#    @api.model
#    def write(self):
#        #Reinicia Secuencia
#        secuencia = self.env['ir.sequence'].search([('code', '=','consecutivo.paca')])
#        secuencia.number_next=(1)

    lot_name = fields.Char(default=_crear_numero_lote)
    
class ModCodigo_Barras(models.Model):
    _inherit = 'product.product'
    barcode = fields.Char(required=True, size = 4)
 
    @api.constrains('barcode')
    def check_name(self):
        """ El campo debe contener 4 caracteres"""
        for rec in self:
            if len(rec.barcode)==4:
                print('todo bien')
                continue
            else:
                print('error')
                raise exceptions.ValidationError(_('Codigo de Barras debe ser exactamente de 4 caracteres'))

#class ReiniciaSequencePicking(models.Model):
#    _inherit = 'stock.picking'
#     
#    def view_init(self,self2=1):
#        print('vista SHOWME PICKINGGG')
#        secuencia = self.env['ir.sequence'].search([('code', '=','consecutivo.paca')])
#        secuencia.number_next=(1)
#

#Reinicia cuando se confirma el pedido
#class IniciaLineas(models.Model):
#    _inherit = 'stock.move'
#     
#    @api.model
#    def create(self,vals):
#        picking = self.env['stock.picking'].browse(vals.get('picking_id'))

#https://stackoverflow.com/questions/49384691/what-does-context-getactive-ids-mean-why-do-we-use-it