# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestFactoryAccounting(TransactionCase):

    def setUp(self):
        super(TestFactoryAccounting, self).setUp()
        self.company = self.env.company

    def test_01_configure_egyptian_defaults(self):
        """Verify Egyptian localization configuration idempotent method."""
        self.company.factory_enable_egp_localization = True
        res = self.company.action_configure_egyptian_defaults()
        self.assertTrue(res)

        eg_country = self.env['res.country'].search([('code', '=', 'EG')], limit=1)
        if eg_country:
            self.assertEqual(self.company.country_id.id, eg_country.id)

    def test_02_manufacturing_cost_breakdown(self):
        """Verify MO cost breakdown computation."""
        product_rm = self.env['product.product'].create({
            'name': 'Raw Aluminum Bar',
            'type': 'consu',
            'standard_price': 15.0,
        })
        product_fg = self.env['product.product'].create({
            'name': 'Aluminum Housing',
            'type': 'consu',
            'standard_price': 0.0,
        })
        mo = self.env['mrp.production'].create({
            'product_id': product_fg.id,
            'product_qty': 2.0,
            'move_raw_ids': [(0, 0, {
                'name': 'Consume Raw Aluminum',
                'product_id': product_rm.id,
                'product_uom_qty': 4.0,
                'product_uom': product_rm.uom_id.id,
                'quantity': 4.0, # 4 * 15.0 = 60.0
                'location_id': self.env.ref('stock.stock_location_stock').id,
                'location_dest_id': self.env.ref('stock.stock_location_stock').id,
            })]
        })

        mo._compute_manufacturing_costs()
        self.assertEqual(mo.cost_raw_materials, 60.0)
        self.assertEqual(mo.cost_manufacturing_total, 60.0)
        self.assertEqual(mo.unit_cost_manufactured, 30.0)
