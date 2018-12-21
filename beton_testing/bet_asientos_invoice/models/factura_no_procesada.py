# -*- coding: utf-8 -*-
from odoo import fields
from odoo import models

class facturasNoProcesadas(models.Model):
    _name = 'factura.noprocesada' #por convencion nombre significativo.loque se va a guardar, name siempre se ha de poner
    tipo_no_procesado = fields.Char(
                       string="Tipo", #motivo por el cual no se procesa esa factura
                       default="-1",
                       )

    factura = fields.Char(
                          string="Factura no procesada",
                          default="Sin nombre",
                          )

    def createRegistroFactura(self, dato1,dato2):
        data={'tipo_no_procesado':dato1,
            'factura':dato2
        }
        self.create(data)
        # print (data)
        return "registro creado"