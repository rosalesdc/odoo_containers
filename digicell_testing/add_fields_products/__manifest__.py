# -*- coding: utf-8 -*-
{
    'name': "Digicell - Agrega campos en Productos",

    'summary': """ 
    """,

    'description': """
    Campos adicionales para productos
    -Clave Alterna
    -Clave Unidad
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
    ],

    # always loaded
	'data': [
	'views/add_fields_products_view.xml',
    ],
	'demo':[

	],
    'installable':True,
}
