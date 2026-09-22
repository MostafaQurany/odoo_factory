# -*- coding: utf-8 -*-
{
    'name': 'Factory Industrial Security & Access Control Engine',
    'version': '18.0.1.0.0',
    'category': 'Administration/Security',
    'summary': 'Segregation of duties across 12 factory roles, approval authorities, and industrial record rules',
    'author': 'Odoo Factory Platform',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'factory_base',
        'stock',
        'mrp',
        'purchase',
        'sale_management',
        'account',
    ],
    'data': [
        'security/factory_security_groups.xml',
        'security/ir.model.access.csv',
        'security/factory_record_rules.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
