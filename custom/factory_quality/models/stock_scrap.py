# -*- coding: utf-8 -*-
from odoo import models, fields, api

class StockScrap(models.Model):
    _inherit = 'stock.scrap'

    origin_inspection_id = fields.Many2one('qc.inspection', string='Quality Inspection Origin')
    rework_order_id = fields.Many2one('factory.rework.order', string='Origin Rework Order')
    scrap_cost_loss = fields.Float(
        string='Estimated Material Loss Value',
        compute='_compute_scrap_cost_loss',
        store=True,
        help='Financial loss computed from product standard cost times scrapped quantity.')

    @api.depends('product_id', 'scrap_qty')
    def _compute_scrap_cost_loss(self):
        for scrap in self:
            cost = scrap.product_id.standard_price if scrap.product_id else 0.0
            scrap.scrap_cost_loss = cost * scrap.scrap_qty
