# -*- coding: utf-8 -*-
{
    'name': "Autoincrementar Registro Venta",

    'summary': """
    """,

    'description': """
        Modulo para autoenumerar los items de Ventas por Web
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
    ],

    # always loaded
	'data': [
	'views/partida_increment_view.xml',
    ],
	'demo':[

	],
    'installable':True,
}
