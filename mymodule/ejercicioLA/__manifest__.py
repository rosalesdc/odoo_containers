# -*- coding: utf-8 -*-
{
    'name': "Hide Purchase Module",

    'summary': """
    """,

    'description': """
        Módulo para eliminar la pestaña "PURCHASE" de los productos en módulo Inventario
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
    ],

    # always loaded
    'data': [
        'views/purchase_hide_view.xml'
    ],
    'installable':True,
    'auto_install':False,
}