# -*- coding: utf-8 -*-
{
    'name': "Filtro Buscar",

    'summary': """
    """,

    'description': """
        Módulo para agregar el un Filtro para seleccionar las órdenes PAGADAS
        -Para que aparezca como default, se activa el modo desarrollador y se agrega como filtro por default
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
        'point_of_sale'
    ],

    # always loaded
    'data': [
        'views/agregar_filtro_view.xml',
        'views/poner_filtro_default.xml'
    ],
    'installable':True,
    'auto_install':False,
}