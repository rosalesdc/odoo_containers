{
    'name': 'Stock Move',
    'description': """
        Módulo de Luis Angel
    """,
    'version': '1.0',
    'author': 'Luis Angel',
    'website': 'http://www.soluciones4g.com',
    'license': 'AGPL-3',
    'summary': '',
    'depends': [
        'base','stock'
        ],
    'data': [
        'report/report_move.xml',
        'report/report_move_qweb.xml',
        'views/stock_move_view_inherit.xml',
        ],
    'installable': True,
}
