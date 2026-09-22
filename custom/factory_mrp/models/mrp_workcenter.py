# -*- coding: utf-8 -*-
from odoo import models, fields, api

class MrpWorkcenter(models.Model):
    _inherit = 'mrp.workcenter'

    factory_section = fields.Selection([
        ('cutting', 'Cutting / Blanking'),
        ('machining', 'Machining / CNC / Processing'),
        ('welding', 'Welding / Fabrication'),
        ('assembly', 'Assembly / Sub-assembly'),
        ('finishing', 'Finishing / Painting / Treatment'),
        ('packaging', 'Packaging / Boxing'),
        ('qa', 'Inspection / Testing Station'),
    ], string='Factory Section / Cell', default='assembly', index=True)

    hourly_labor_cost = fields.Float(
        string='Operator Labor Rate / Hour',
        default=0.0,
        help='Standard direct labor hourly cost for operators at this work center.')

    hourly_overhead_cost = fields.Float(
        string='Machine & Utility Overhead / Hour',
        default=0.0,
        help='Allocated utility, power, and factory overhead per hour.')

    total_hourly_rate = fields.Float(
        string='Total Industrial Hourly Cost',
        compute='_compute_total_hourly_rate',
        store=True,
        help='Machine base cost + direct labor + overhead rate.')

    maintenance_status = fields.Selection([
        ('operational', 'Operational / Ready'),
        ('maintenance', 'Down for Maintenance'),
        ('restricted', 'Restricted Capacity'),
    ], string='Operating Status', default='operational', tracking=True)

    @api.depends('costs_hour', 'hourly_labor_cost', 'hourly_overhead_cost')
    def _compute_total_hourly_rate(self):
        for wc in self:
            wc.total_hourly_rate = wc.costs_hour + wc.hourly_labor_cost + wc.hourly_overhead_cost
