# -*- coding: utf-8 -*-
{
    'name': "Incrementar Lotes",

    'summary': """
    """,

    'description': """
        Autoincrementa el número de lote automaticamente para operaciones de stock
    """,

    'author': "Soluciones4G",
    'website': "http://www.soluciones4g.com",

    # Categories can be used to filter modules in modules listing
    # for the full list
    'category': 'Uncategorized',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': [
        'base','stock'
    ],
    # always loaded
	'data': [
        'sequences/paca_sequence.xml',
	'views/increment_lote_view.xml',
    ],
	'demo':[

	],
    'installable':True,
}
