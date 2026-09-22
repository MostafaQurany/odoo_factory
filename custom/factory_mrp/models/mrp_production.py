# -*- coding: utf-8 -*-
from odoo import models, fields, api

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    production_shift = fields.Selection([
        ('morning', 'Shift 1 — Morning (06:00 - 14:00)'),
        ('evening', 'Shift 2 — Evening (14:00 - 22:00)'),
        ('night', 'Shift 3 — Night (22:00 - 06:00)'),
    ], string='Production Shift', default='morning')

    supervisor_id = fields.Many2one('res.users', string='Floor Supervisor')
    has_rework_operations = fields.Boolean(string='Includes Rework Operations', default=False)
    
    actual_vs_planned_material_pct = fields.Float(
        string='Material Consumption Variance %',
        compute='_compute_variances',
        help='Percentage difference between planned and actual raw material consumed.')

    actual_vs_planned_duration_pct = fields.Float(
        string='Labor / Machine Duration Variance %',
        compute='_compute_variances',
        help='Percentage difference between planned work order duration and actual duration.')

    @api.depends('move_raw_ids.quantity', 'move_raw_ids.product_uom_qty', 'workorder_ids.duration', 'workorder_ids.duration_expected')
    def _compute_variances(self):
        for mo in self:
            planned_qty = sum(mo.move_raw_ids.mapped('product_uom_qty'))
            actual_qty = sum(mo.move_raw_ids.mapped('quantity'))
            if planned_qty > 0:
                mo.actual_vs_planned_material_pct = ((actual_qty - planned_qty) / planned_qty) * 100.0
            else:
                mo.actual_vs_planned_material_pct = 0.0

            planned_time = sum(mo.workorder_ids.mapped('duration_expected'))
            actual_time = sum(mo.workorder_ids.mapped('duration'))
            if planned_time > 0:
                mo.actual_vs_planned_duration_pct = ((actual_time - planned_time) / planned_time) * 100.0
            else:
                mo.actual_vs_planned_duration_pct = 0.0
