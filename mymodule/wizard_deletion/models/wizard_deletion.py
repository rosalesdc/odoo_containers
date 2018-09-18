# -*- coding: utf-8 -*-

from odoo import api
from odoo import exceptions
from odoo import fields
from odoo import models

class Wizard_Deletion(models.TransientModel): #Crea registros que se utilizan cuando se ejecuta el Wizard
    _name = 'wizard_deletion'	#cuando se utiliza este modelo se manejan los registros provistos por TransientModel
	
    #El siguiente método predefinido busca los registros que se seleccionan de la vista Tree
    #sólo se puede mandar a llamar desde una relación
    def _default_rfq(self):
        return self.env['purchase.order'].browse(self._context.get('active_ids'))#browse es un método ORM para buscar los registros seleccionados dentro del modelo,(en nuestro caso purchase.order)
    #en este caso utilizamos browse (busca un dato del objeto o un arreglo del objeto), regresa el id del registro en el modelo (en nuestro caso purchase.order)
    #active_ids son variables predefinidas que contienen los registros seleccionados
    #existe también "search" hace una búsqueda de algún elemento dentro del objeto, parecido al SELECT
        
    #Se debe crear una relación muchos a muchos debido a los multiples (muchos registros que utilizaremos)
    #Es todo el conjunto de datos seleccionados en browse
    purchase_ids = fields.Many2many('purchase.order', string='Compras', default=_default_rfq)

    #Este nombre de función es arbitrario
    def delete_rfqs(self):
        #notar que se itera con el objeto purchase_ids definido anteriormente
        for record in self.purchase_ids:
            if record.state == 'draft':
                print('PURCHASE IDS', str(record.id))
                record.write({'state':'cancel'})
                record.unlink()
