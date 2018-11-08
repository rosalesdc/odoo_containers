# -*- coding: utf-8 -*-
{
    'name': "Wizard Factura de Pedidos",

    'summary': """
    """,

    'description': """
        Wizard para generar una factura general de todos los pedidos de venta
        que no fueron facturados al momento de la compra
    """,

    'author': "Soluciones4G",
    'website': "http://www.soluciones4g.com",

    # Categories can be used to filter modules in modules listing
    # for the full list
    'category': 'Uncategorized',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': [
        'base','purchase','point_of_sale',
    ],

    # always loaded
	'data': [
	'wizard/genera_factura_view.xml'
    ],
	'demo':[

	],
    'installable':True,
}
