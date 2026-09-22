# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class FactoryReworkOrder(models.Model):
    _name = 'factory.rework.order'
    _description = 'Factory Controlled Rework Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    name = fields.Char(string='Rework Order #', required=True, copy=False, default=lambda self: _('New'))
    origin_inspection_id = fields.Many2one('qc.inspection', string='Origin Quality Inspection', ondelete='cascade')
    production_id = fields.Many2one('mrp.production', string='Source Manufacturing Order')
    product_id = fields.Many2one('product.product', string='Defective Product', required=True)
    lot_id = fields.Many2one('stock.lot', string='Defective Lot / Serial')
    rework_qty = fields.Float(string='Quantity to Rework', default=1.0, required=True)
    workcenter_id = fields.Many2one('mrp.workcenter', string='Assigned Rework Work Center')
    operator_id = fields.Many2one('res.users', string='Assigned Technician', default=lambda self: self.env.user)
    rework_instructions = fields.Text(string='Required Correction Instructions')
    defect_root_cause = fields.Text(string='Defect Root Cause Analysis')

    state = fields.Selection([
        ('draft', 'Draft Rework Plan'),
        ('in_progress', 'Rework in Progress'),
        ('reinspected', 'Pending Quality Re-inspection'),
        ('done', 'Rework Completed & Passed'),
        ('scrapped', 'Rework Unfeasible — Scrapped'),
    ], string='Rework Status', default='draft', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('factory.rework.order') or _('RWK-%04d') % self.env['ir.sequence'].search_count([])
        return super(FactoryReworkOrder, self).create(vals_list)

    def action_start_rework(self):
        self.write({'state': 'in_progress'})

    def action_complete_for_reinspection(self):
        self.write({'state': 'reinspected'})
        # Notify inspector or create re-inspection
        if self.origin_inspection_id:
            self.origin_inspection_id.message_post(body=_("Rework order %s completed. Ready for re-inspection.") % self.name)

    def action_rework_passed(self):
        self.write({'state': 'done'})
        if self.origin_inspection_id:
            self.origin_inspection_id.action_set_pass()

    def action_rework_failed_scrap(self):
        self.write({'state': 'scrapped'})
        if self.origin_inspection_id:
            self.origin_inspection_id.action_set_scrap()
