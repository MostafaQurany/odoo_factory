# -*- coding: utf-8 -*-
{
    'name': 'Factory Equipment Maintenance & Downtime Tracking Engine',
    'version': '18.0.1.0.0',
    'category': 'Manufacturing/Maintenance',
    'summary': 'Industrial machine equipment, work center downtime links, preventive schedules, and failure logging',
    'author': 'Odoo Factory Platform',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mrp',
        'barcodes',
        'factory_base',
        'factory_mrp',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/factory_equipment_views.xml',
        'views/factory_maintenance_request_views.xml',
        'views/factory_maintenance_menus.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
