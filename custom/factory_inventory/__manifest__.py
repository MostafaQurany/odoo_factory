# -*- coding: utf-8 -*-
{
    'name': 'Factory Inventory & Warehousing Engine',
    'version': '18.0.1.0.0',
    'category': 'Manufacturing/Inventory',
    'summary': 'Industrial warehouse topologies, lot/serial traceability, and no-negative-stock controls',
    'author': 'Odoo Factory Platform',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'stock',
        'stock_no_negative',
        'factory_base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/stock_location_views.xml',
        'views/stock_warehouse_views.xml',
        'views/stock_lot_views.xml',
        'views/factory_inventory_menus.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
