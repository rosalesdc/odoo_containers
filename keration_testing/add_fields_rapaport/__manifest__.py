# -*- coding: utf-8 -*-
{
    'name': "Agrega campos de productos de joyería",

    'summary': """ Campos adicionales para productos Keration
    """,

    'description': """
    Rapaport (numérico); 
    Costo Rapaport (numérico con decimales porcentaje); 
    Costo USD Quilate (Número calculado) rapaport/porcentaje costo rapaport; 
    Costo Total (Número calculado moneda) costo usd quilate*quilate
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
	'views/add_fields_rapaport_view.xml',
#    'views/new_wizard_view.xml',
	'templates.xml',
	'reports.xml',
    ],
	'demo':[

	],
    'installable':True,
}
