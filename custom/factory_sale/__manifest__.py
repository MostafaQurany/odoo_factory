# -*- coding: utf-8 -*-
{
    'name': 'Factory Sales & Demand Orchestration Engine',
    'version': '18.0.1.0.0',
    'category': 'Sales/Manufacturing',
    'summary': 'Industrial sales orders, MTO/MTS manufacturing demand links, and customer delivery tolerances',
    'author': 'Odoo Factory Platform',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'sale_management',
        'sale_stock',
        'factory_base',
        'factory_inventory',
        'factory_mrp',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'views/res_partner_views.xml',
        'views/factory_sale_menus.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
