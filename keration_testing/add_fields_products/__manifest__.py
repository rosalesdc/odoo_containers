# -*- coding: utf-8 -*-
{
    'name': "Agrega Campos de Producto",

    'summary': """
    """,

    'description': """
        Módulo creado para agregar campos al formulario de productos
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
    'views/fields_add_product_template.xml'
    ],
    'installable':True,
}
