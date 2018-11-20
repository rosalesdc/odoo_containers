# -*- coding: utf-8 -*-
{
    'name': "Agregar columna Fecha",

    'summary': """
        Agregar la columna de Fecha para reporte (Facturas) productos vendidos
        """,

    'description': """
        Agregar la columna de Fecha para reporte (Facturas) productos vendidos
    """,

    'author': "Soluciones4G",
    'website': "http://www.soluciones4g.com",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base',],

    'data': [
        'views/add_column_date_view.xml',
    ],
    'auto_install':False,
}
