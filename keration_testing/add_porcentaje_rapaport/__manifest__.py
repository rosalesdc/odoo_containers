# -*- coding: utf-8 -*-
{
    'name': "Incrementar indice de productos",

    'summary': """
    """,

    'description': """
        Autoincrementar indices de productos por Web
    """,

    'author': "Soluciones4G",
    'website': "http://www.soluciones4g.com",

    # Categories can be used to filter modules in modules listing
    # for the full list
    'category': 'Uncategorized',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': [
        'base','sale',
    ],

    # always loaded
	'data': [
	'views/porcentaje_rapaport_view.xml',
    ],
	'demo':[

	],
    'installable':True,
}
