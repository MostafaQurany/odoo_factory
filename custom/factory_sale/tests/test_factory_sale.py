# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestFactorySale(TransactionCase):

    def setUp(self):
        super(TestFactorySale, self).setUp()
        self.customer = self.env['res.partner'].create({
            'name': 'Strategic OEM Client',
            'customer_rank': 1,
            'factory_customer_tier': 'key_account',
        })
        self.product = self.env['product.product'].create({
            'name': 'Industrial Centrifugal Pump',
            'type': 'consu',
            'list_price': 1500.0,
        })

    def test_01_sale_demand_strategy(self):
        """Verify sales order fulfillment strategy and delivery tolerance."""
        order = self.env['sale.order'].create({
            'partner_id': self.customer.id,
            'factory_demand_type': 'make_to_order',
            'customer_delivery_tolerance_days': 5,
            'order_line': [(0, 0, {
                'product_id': self.product.id,
                'product_uom_qty': 5,
                'price_unit': 1500.0,
            })]
        })

        self.assertEqual(order.factory_demand_type, 'make_to_order')
        self.assertEqual(order.customer_delivery_tolerance_days, 5)
        self.assertEqual(order.partner_id.factory_customer_tier, 'key_account')

        # Test action to view manufacturing orders
        action = order.action_view_manufacturing_orders()
        self.assertEqual(action['domain'], [('origin', '=', order.name)])
