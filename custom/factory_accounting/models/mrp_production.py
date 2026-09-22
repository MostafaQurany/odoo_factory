# -*- coding: utf-8 -*-
from odoo import models, fields, api

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True)

    cost_raw_materials = fields.Monetary(
        string='Actual Raw Materials Cost',
        compute='_compute_manufacturing_costs',
        store=True,
        currency_field='currency_id')

    cost_workcenter_labor = fields.Monetary(
        string='Direct Labor Cost',
        compute='_compute_manufacturing_costs',
        store=True,
        currency_field='currency_id')

    cost_workcenter_overhead = fields.Monetary(
        string='Industrial Overhead Cost',
        compute='_compute_manufacturing_costs',
        store=True,
        currency_field='currency_id')

    cost_manufacturing_total = fields.Monetary(
        string='Total Manufacturing Cost',
        compute='_compute_manufacturing_costs',
        store=True,
        currency_field='currency_id')

    unit_cost_manufactured = fields.Monetary(
        string='Manufactured Unit Cost',
        compute='_compute_manufacturing_costs',
        store=True,
        currency_field='currency_id')

    @api.depends('move_raw_ids.quantity', 'move_raw_ids.product_id.standard_price',
                 'workorder_ids.duration', 'workorder_ids.workcenter_id.hourly_labor_cost',
                 'workorder_ids.workcenter_id.hourly_overhead_cost', 'qty_produced')
    def _compute_manufacturing_costs(self):
        for mo in self:
            # 1. Material cost: sum(move_raw.quantity * standard_price)
            mat_cost = sum(
                move.quantity * move.product_id.standard_price
                for move in mo.move_raw_ids
            )
            mo.cost_raw_materials = mat_cost

            # 2. Labor cost: sum((duration / 60.0) * hourly_labor_cost)
            labor_cost = sum(
                (wo.duration / 60.0) * (wo.workcenter_id.hourly_labor_cost or 0.0)
                for wo in mo.workorder_ids
            )
            mo.cost_workcenter_labor = labor_cost

            # 3. Overhead cost: sum((duration / 60.0) * hourly_overhead_cost)
            overhead_cost = sum(
                (wo.duration / 60.0) * (wo.workcenter_id.hourly_overhead_cost or 0.0)
                for wo in mo.workorder_ids
            )
            mo.cost_workcenter_overhead = overhead_cost

            # 4. Total and unit
            total = mat_cost + labor_cost + overhead_cost
            mo.cost_manufacturing_total = total
            if mo.qty_produced > 0:
                mo.unit_cost_manufactured = total / mo.qty_produced
            elif mo.product_qty > 0:
                mo.unit_cost_manufactured = total / mo.product_qty
            else:
                mo.unit_cost_manufactured = 0.0
