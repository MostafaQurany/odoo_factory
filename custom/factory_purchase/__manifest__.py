# -*- coding: utf-8 -*-
{
    'name': 'Factory Procurement & Purchasing Engine',
    'version': '18.0.1.0.0',
    'category': 'Manufacturing/Purchase',
    'summary': 'Industrial procurement, vendor approval tiers, lead times, and factory receiving',
    'author': 'Odoo Factory Platform',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'purchase',
        'purchase_stock',
        'factory_base',
        'factory_inventory',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/purchase_order_views.xml',
        'views/res_company_views.xml',
        'views/factory_purchase_menus.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
