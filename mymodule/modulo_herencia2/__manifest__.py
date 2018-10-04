# -*- coding: utf-8 -*-
{
    'name': "Modelo Herencia 2",

    'summary': """
    """,

    'description': """
        Modulo creado como practica
    """,

    'author': "Soluciones4G",
    'website': "http://www.soluciones4g.com",

    # Categories can be used to filter modules in modules listing
    # for the full list
    'category': 'Uncategorized',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': [
        'base','stock',
    ],

    # always loaded
    'data': [
    'views/report_move.xml',
    'views/report_move_qweb.xml',
    'views/herencia_stock.xml',
    ],
    'installable':True,
}
