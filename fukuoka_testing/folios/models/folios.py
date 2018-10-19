# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Folios(models.Model):
    _name = 'folio.datos'

    prefijo = fields.Char(
        string="Prefijo",
        size=20,
        required=True,
    )

    secuencial = fields.Integer(
        string="Número actual",
        default=0,
    )

    _sql_constraints = [
        ('prefijo_unique',
         'UNIQUE(prefijo)',
         ("El prefijo ya existe, asegurese de que este sea único \
          o eliminar el anterior para reiniciar la cuenta")),
    ]

    @api.model
    def get_folio(self, usoprefijo):
        # Buscar si existe el folio en la tabla de folios
        datos_folio = self.search([('prefijo', '=', usoprefijo)])

        # Verificar ya esta registrado el folio
        if datos_folio:
            numeralfinal = datos_folio.secuencial
            numeral_consecutivo = numeralfinal + 1
            datos_folio.write({
                'secuencial': numeral_consecutivo,
            })
            longfolio = 10000 + numeral_consecutivo
            strfolio = str(longfolio)
            folio_final = strfolio[1:5]
            return folio_final
        else:
            numerostr = "001"
            numero = 1
            self.create({
                'prefijo': usoprefijo,
                'secuencial': numero,
            })
            return numerostr
