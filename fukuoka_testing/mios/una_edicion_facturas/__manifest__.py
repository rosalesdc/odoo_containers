# -*- coding: utf-8 -*-
{
    'name': "Edición de facturas",

    'summary': """
        Edición de la vista de arbol de las facturas
        """,

    'description': """
        Agregado empresa o compañia relacionada en las facturas del cliente
    """,

    'author': "Soluciones4G OGM",
    'website': "http://www.soluciones4g.com",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': [
        'base',
        'account_accountant',
        'account_invoicing',
        'edicion_contactos',
        'web_widget_color',
    ],

    'data': [
        'views/empresa_enfacturacion_view.xml',
        'reports/edicion_facturas_report.xml',
        'views/invoice_lines_view_extended.xml',
    ],
    'installable':True,
    'auto_install':False,
}
