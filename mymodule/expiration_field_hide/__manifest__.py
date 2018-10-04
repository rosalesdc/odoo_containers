# -*- coding: utf-8 -*-
{
    'name': "Modulo Ocultar Expiration",

    'summary': """
    """,

    'description': """
        
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
        'contacts',
    ],

    # always loaded
    'data': [
        'views/expiration_hide_view.xml'
    ],
    'installable':True,
    'auto_install':False,
}