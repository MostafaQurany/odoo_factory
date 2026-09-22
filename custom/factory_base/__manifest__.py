# -*- coding: utf-8 -*-
{
    'name': 'Factory Base Engine',
    'version': '18.0.1.0.0',
    'category': 'Manufacturing',
    'summary': 'Foundational settings, industrial security groups, and root factory menus',
    'author': 'Odoo Factory Platform',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',
    ],
    'data': [
        'security/factory_security.xml',
        'security/ir.model.access.csv',
        'views/res_company_views.xml',
        'views/factory_menus.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
