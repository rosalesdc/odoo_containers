
# -*- coding: utf-8 -*-
from odoo import fields
from odoo import models

class Proveedor(models.Model):
    _name = 'proveedor.informacion_data'
        
    name = fields.Char(
                       string="Nombre",
                       required=True,
                       index=True,
                       )

    direccion = fields.Char(
                            string="Dirección",
                            required=True,
                            )