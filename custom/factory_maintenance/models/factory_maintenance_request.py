# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class FactoryMaintenanceRequest(models.Model):
    _name = 'factory.maintenance.request'
    _description = 'Factory Maintenance Request & Downtime Log'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(string='Maintenance Work Order #', required=True, copy=False, default=lambda self: _('New'))
    equipment_id = fields.Many2one('factory.equipment', string='Target Equipment', required=True, tracking=True)
    workcenter_id = fields.Many2one('mrp.workcenter', string='Affected Work Center', compute='_compute_workcenter', store=True)
    
    maintenance_type = fields.Selection([
        ('preventive', 'Preventive Scheduled Maintenance'),
        ('corrective', 'Corrective Emergency Repair'),
    ], string='Maintenance Classification', default='preventive', required=True)

    technician_id = fields.Many2one('res.users', string='Assigned Maintenance Engineer', default=lambda self: self.env.user)
    planned_date = fields.Datetime(string='Scheduled Date', default=fields.Datetime.now)
    completion_date = fields.Datetime(string='Actual Completion Date')
    downtime_hours = fields.Float(string='Machine Downtime (Hours)', default=0.0, help='Total operational downtime logged during this repair.')

    failure_reason = fields.Selection([
        ('mechanical', 'Mechanical Wear / Jam'),
        ('electrical', 'Electrical / Motor / Wiring'),
        ('sensor', 'Sensor / Limit Switch'),
        ('hydraulic', 'Hydraulic / Pneumatic Pressure Loss'),
        ('tooling', 'Tooling Wear / Broken Cutter'),
        ('preventive', 'Standard Preventive Cycle / Lubrication'),
    ], string='Primary Root Cause', default='preventive')

    work_summary = fields.Text(string='Work Log & Parts Replaced')

    state = fields.Selection([
        ('draft', 'Scheduled'),
        ('in_progress', 'Under Repair'),
        ('done', 'Repaired & Verified'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)

    @api.depends('equipment_id.workcenter_id')
    def _compute_workcenter(self):
        for req in self:
            req.workcenter_id = req.equipment_id.workcenter_id.id if req.equipment_id else False

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('factory.maintenance.request') or _('MNT-%04d') % self.env['ir.sequence'].search_count([])
        return super(FactoryMaintenanceRequest, self).create(vals_list)

    def action_start_repair(self):
        self.write({'state': 'in_progress'})
        if self.equipment_id:
            self.equipment_id.write({'state': 'maintenance'})
        if self.workcenter_id:
            self.workcenter_id.write({'maintenance_status': 'maintenance'})

    def action_finish_repair(self):
        self.write({
            'state': 'done',
            'completion_date': fields.Datetime.now(),
        })
        if self.equipment_id:
            self.equipment_id.write({'state': 'operational'})
        if self.workcenter_id:
            # Check if other ongoing maintenance requests exist for this workcenter
            ongoing = self.search([
                ('workcenter_id', '=', self.workcenter_id.id),
                ('state', '=', 'in_progress'),
                ('id', '!=', self.id),
            ])
            if not ongoing:
                self.workcenter_id.write({'maintenance_status': 'operational'})
