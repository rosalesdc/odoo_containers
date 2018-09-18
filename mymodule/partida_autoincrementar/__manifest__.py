# -*- coding: utf-8 -*-
{
    'name': "Auto-incrementar Partida",

    'summary': """
    """,

    'description': """
        Auto-incrementar el campo Partida en la impresión del reporte
    """,

    'author': "Soluciones4G",
    'website': "http://www.soluciones4g.com",

    # Categories can be used to filter modules in modules listing
    # for the full list
    'category': 'Uncategorized',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'stock',
        'product',
        'sale',
        'sale_management'
    ],

    # always loaded
    'data': [
        'views/partida_increment_view.xml'
    ],
    'installable':True,
    'auto_install':False,
}