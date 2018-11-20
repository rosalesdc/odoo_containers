# -*- coding: utf-8 -*-
{
    'name': "Campos para contactos/clientes",

    'summary': """
        Agregado de campos para los contactos
        """,

    'description': """
        * Agregado de campos al modelo res.partner para obtener datos importantes:
        * Codigo del cliente
        * Grupo del cliente
        * Color del grupo del cliente
    """,

    'author': "Soluciones4G OGM",
    'website': "http://www.soluciones4g.com",

    'category': 'Extra Tools',
    'version': '0.1',

    'depends': [
        'base',
        'contacts',
        'web_widget_color',
        'sale',
    ],

    'data': [
        'views/grupos_clientes_view.xml',
        'views/campo_codigo_cliente_view.xml',
        'security/ir.model.access.csv',
    ],

    'installable': True,
    'auto_install': False,
}
