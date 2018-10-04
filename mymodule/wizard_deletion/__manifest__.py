# -*- coding: utf-8 -*-
{
    'name': "Wizard para borrar compras",

    'summary': """Ejercicios
    """,

    'description': """
        Modulos funcionales para capacitación
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
	'views/wizard_deletion_view.xml',
        'views/new_wizard_view.xml',
    ],
	'demo':[

	],
    'installable':True,
}
