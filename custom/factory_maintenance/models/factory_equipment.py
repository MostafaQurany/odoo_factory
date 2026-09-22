# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class FactoryEquipment(models.Model):
    _name = 'factory.equipment'
    _description = 'Industrial Factory Equipment & Machinery'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Machine / Equipment Name', required=True, tracking=True)
    code = fields.Char(string='Asset Tag / Code', required=True, index=True)
    barcode = fields.Char(string='Scan Barcode', index=True)
    workcenter_id = fields.Many2one('mrp.workcenter', string='Assigned Work Center / Cell', tracking=True)
    vendor_id = fields.Many2one('res.partner', string='Manufacturer / Vendor')
    model_number = fields.Char(string='Model / Series')
    serial_number = fields.Char(string='Machine Serial Number')
    installation_date = fields.Date(string='Commissioning Date')
    warranty_expiry_date = fields.Date(string='Warranty Expiry Date')

    state = fields.Selection([
        ('operational', 'Operational / Running'),
        ('maintenance', 'Down for Maintenance'),
        ('scrap', 'Decommissioned / Scrapped'),
    ], string='Status', default='operational', tracking=True)

    maintenance_request_ids = fields.One2many(
        'factory.maintenance.request', 'equipment_id', string='Maintenance History')
    maintenance_count = fields.Integer(
        string='Maintenance Count', compute='_compute_maintenance_count')

    def _compute_maintenance_count(self):
        for eq in self:
            eq.maintenance_count = len(eq.maintenance_request_ids)

    def action_view_maintenance_requests(self):
        self.ensure_one()
        action = self.env['ir.actions.act_window']._for_xml_id('factory_maintenance.action_factory_maintenance_request')
        action['domain'] = [('equipment_id', '=', self.id)]
        action['context'] = {'default_equipment_id': self.id}
        return action
