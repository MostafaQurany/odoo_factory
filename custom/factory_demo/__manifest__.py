# -*- coding: utf-8 -*-
{
    'name': 'Factory Universal Generic Demo Data',
    'version': '18.0.1.0.0',
    'category': 'Manufacturing/Demo',
    'summary': 'Neutral industrial demo data: raw materials, subassemblies, work centers, and BOMs',
    'author': 'Odoo Factory Platform',
    'license': 'LGPL-3',
    'depends': [
        'product',
        'stock',
        'mrp',
        'purchase',
        'sale_management',
        'factory_base',
    ],
    'data': [
        'data/products_data.xml',
        'data/workcenters_data.xml',
        'data/routing_bom_data.xml',
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}
