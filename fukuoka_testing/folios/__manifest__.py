# -*- coding: utf-8 -*-
{
    'name': "Folios",

    'summary': """
        Creación de folios
        """,

    'description':
        """
            Generación de folios de acuerdo a un prefijo y un número 
        """,

    'author': "Soluciones4G OGM",
    'website': "http://soluciones4g.com",

    'category': 'Extra Tools',
    'version': '1.0',

    'depends': [
        'base',
    ],

    'demo': [],

    'data': [
        'views/folios_view.xml',
        'security/ir.model.access.csv',
    ],

    'installable': True,
    'auto_install': False,
}