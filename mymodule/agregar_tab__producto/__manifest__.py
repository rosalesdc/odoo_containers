# -*- coding: utf-8 -*-
{
    'name': "Agrega un TAB",

    'summary': """
    """,

    'description': """
        Agrega un TAB a la vista de productos
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
        'product',
        # es el nombre de la aplicacion de la que extendemos
    ],

    # always loaded
    'data': [
    'views/add_tab_product.xml'
    ],
    'installable':True,
}
