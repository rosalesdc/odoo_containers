# -*- coding: utf-8 -*-
{
    'name': "Agrega opciones EDI/CFDI",

    'summary': """ 
    """,

    'description': """
        Agrega el catálogo de opciones de seleccionar el uso de EDI/CFDI
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
        'sale',
        'contacts'
    ],

    # always loaded
	'data': [
        'views/add_field_catalogo_edi.xml',
    ],
	'demo':[

	],
    'installable':True,
}
