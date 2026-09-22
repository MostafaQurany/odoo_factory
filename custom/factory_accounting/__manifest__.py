# -*- coding: utf-8 -*-
{
    'name': 'Factory Industrial Accounting & Costing Engine',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Manufacturing',
    'summary': 'Manufacturing cost breakdown (materials, labor, overhead), perpetual valuation, and Egypt localization defaults',
    'author': 'Odoo Factory Platform',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'account',
        'stock_account',
        'factory_base',
        'factory_inventory',
        'factory_mrp',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/mrp_production_views.xml',
        'views/res_company_views.xml',
        'views/factory_accounting_menus.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
