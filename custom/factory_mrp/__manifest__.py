# -*- coding: utf-8 -*-
{
    'name': 'Factory Manufacturing Engine',
    'version': '18.0.1.0.0',
    'category': 'Manufacturing',
    'summary': 'Industrial work center costing, planned vs actual material/labor variance, and BOM revisions',
    'author': 'Odoo Factory Platform',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mrp',
        'stock',
        'factory_base',
        'factory_inventory',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/mrp_workcenter_views.xml',
        'views/mrp_production_views.xml',
        'views/mrp_bom_views.xml',
        'views/factory_mrp_menus.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
