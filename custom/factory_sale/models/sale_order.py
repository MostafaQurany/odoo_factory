# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    factory_demand_type = fields.Selection([
        ('make_to_stock', 'MTS — Make to Stock (Fulfill from Inventory)'),
        ('make_to_order', 'MTO — Make to Order (Trigger Production)'),
    ], string='Industrial Fulfillment Strategy', default='make_to_stock', required=True, index=True)

    customer_delivery_tolerance_days = fields.Integer(
        string='Delivery Tolerance (Days)',
        default=3,
        help='Acceptable delivery window variation agreed with the customer.')

    production_order_count = fields.Integer(
        string='Linked MO Count',
        compute='_compute_production_order_count')

    def _compute_production_order_count(self):
        for order in self:
            # Look up mrp.production where origin is this order name or linked through procurements
            mo_count = self.env['mrp.production'].search_count([('origin', '=', order.name)])
            order.production_order_count = mo_count

    def action_view_manufacturing_orders(self):
        self.ensure_one()
        action = self.env['ir.actions.act_window']._for_xml_id('mrp.mrp_production_action')
        action['domain'] = [('origin', '=', self.name)]
        action['context'] = {'default_origin': self.name}
        return action
