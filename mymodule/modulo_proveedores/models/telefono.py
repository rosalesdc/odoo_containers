from odoo import models,fields

class Telefono(models.Model):
    _name='proveedor.telefono'
    
    numero_telefonico=fields.Char(
        string="Número telefónico",
        required=True,
    )

    proveedor_id=fields.Many2one(
		'proveedor.informacion_data',
		string="Persona"
		)