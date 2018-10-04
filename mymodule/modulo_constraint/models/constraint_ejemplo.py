from odoo import models,fields,api

class constraitn_ejemplo(models.Model): 
    #_inherit='res.partner'#modelo de la aplicación, se puede obtener desde la URL de la aplicación
    ine=fields.Char(string='INE')
