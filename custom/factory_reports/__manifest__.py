# -*- coding: utf-8 -*-
{
    'name': 'Factory Industrial Production Reports Engine',
    'version': '18.0.1.0.0',
    'category': 'Manufacturing/Reporting',
    'summary': '16 industrial production PDF reports for shop floor, quality, warehouse, and costing',
    'author': 'Odoo Factory Platform',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mrp',
        'stock',
        'purchase',
        'factory_base',
        'factory_inventory',
        'factory_mrp',
        'factory_quality',
        'factory_accounting',
    ],
    'data': [
        'report/factory_reports.xml',
        'report/factory_report_templates.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
