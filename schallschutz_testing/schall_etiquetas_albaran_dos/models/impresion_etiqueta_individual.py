# - * - coding: utf-8 - * -
from odoo import _
from odoo import api
from odoo import exceptions
from odoo import fields
from odoo import models

class IncrementaLote(models.Model):
    _inherit = 'stock.move.line'
    
    @api.multi
    def print_individual(self):
        active_context = self._context
        if not 'default_move_id' in active_context:
            print ('Salida: '+str(active_context))
            #print(' '+active_context['active_ids[]'])
            print('No imprimiendo...')
        else:
            rec = self.env['stock.move'].browse((active_context['default_move_id']))
            print('Si imprimiendo...' + str(rec.origin + '/' + rec.product_id.name + '/'))
        print('Terminando funcion')
        return True
        
#ASI SE MANDA A LLAMAR EN STOCK PICKING        
#        pickings = self.mapped('picking_ids')
#        if not pickings:
#            raise UserError(_('Nothing to print.'))    
#        return self.env.ref('stock.action_report_picking').with_context(active_ids=pickings.ids, active_model='stock.picking').report_action([])
    
        #return self.env.ref('stock.action_report_picking').report_action(self) //abre la configuración de documentos
        
    #return self.env.ref('etiquetas_albaran_dos').report_action(self, data=data, config=False)

    x_print_individual = fields.Char('atributo')
    
    #etiquetas_albaran_qweb
    #,impresion_individual_icono
    #,schall_etiquetas_albaran_dos.etiquetas_albaran_view
    #,schall_etiquetas_albaran_dos
    #,report_etiquetas_albaran
    #,etiquetas_albaran_dos
    #,stock.view_picking_form
    #,stock.report_picking
    #https://poncesoft.blogspot.com/2016/12/retornar-un-reporte-mediante-una.html
    #https://www.odoo.com/es_ES/forum/ayuda-1/question/report-in-odoo-11-125808
  
#METODO MAL
#        @api.multi
#    def print_individual(self):
#        active_context = self._context
#        if not 'default_move_id' in active_context:
#            print ('Salida: '+str(active_context))
#            print('No imprimiendo...')
#        else:
#            rec = self.env['stock.move'].browse((active_context['default_move_id']))
#            print('Si imprimiendo...' + str(rec.origin + '/' + rec.product_id.name + '/'))
#        print('Terminando funcion')
#        return True