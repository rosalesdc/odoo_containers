# - * - coding: utf-8 - * -

from odoo import api
from odoo import fields
from odoo import models

indicex = 10
class indice_partida(models.Model):
    _inherit = 'sale.order.line'
    edad = fields.Integer(default=0)

#    def create(cr, uid, vals, context=None):
#        # Your logic goes here or call your method
#        print("hi1")
#        res_id = super(indice_partida, self).create(cr, uid, vals, context=context)
#        # Your logic goes here or call your method
#        print("hi2")
#        return res_id

    @api.model
    @api.multi
    def write(self, vals):
        #res = super(sale.order.line, self).write(vals)
        print ("hello")
        return res
    
    #@api.constraint(x_num_partida,x_num_partida_compute)
    

#realiza en incremento utilizando dos columnas
    @api.multi
    def _write_values(self, self2=1):
        indice = 0
        for record in self:
            if record.x_num_partida == 0:
                indice = indice + 1
                record.x_num_partida_computed = indice
            else:
                record.x_num_partida_computed = record.x_num_partida

    @api.multi
    def create(self, vals):
        global indicex
        res_id = super(indice_partida, self).create(vals)
        for record in res_id:
            indicex = indicex + 1
            print (indicex)
            #print (record.x_num_partida_computed)
        indicex = 10
        return res_id

#    @api.multi            
#    def create(self, vals):
#        # Your logic goes here or call your method
#        print("hi1")
#        res_id = super(indice_partida, self).create(vals)
#        # Your logic goes here or call your method
#        print("hi2",str(res_id.name))
#        for record in res_id:
#            print ('hi3')
#            print (record.x_num_partida_computed)
#        return res_id
    
    x_num_partida = fields.Integer(string="Índice editable", default='0')
    x_num_partida_computed = fields.Integer(string="Índice", compute='_write_values', readonly=True)#campo computado, depende de lo almacenado en la otra columna

    #referencias:
    #https://stackoverflow.com/questions/41614321/how-can-i-override-a-save-action-in-odoo
    #https://www.odoo.yenthevg.com/override-create-functions-odoo/
    #https://www.odoo.com/es_ES/forum/ayuda-1/question/get-all-fields-data-from-write-function-on-save-130880