# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestFactoryMrp(TransactionCase):

    def setUp(self):
        super(TestFactoryMrp, self).setUp()
        self.workcenter = self.env['mrp.workcenter'].create({
            'name': 'Primary CNC Cell',
            'code': 'WC-CNC-01',
            'factory_section': 'machining',
            'costs_hour': 50.0,
            'hourly_labor_cost': 30.0,
            'hourly_overhead_cost': 20.0,
        })
        self.product_fg = self.env['product.product'].create({
            'name': 'Precision Machined Flange',
            'type': 'consu',
        })
        self.product_rm = self.env['product.product'].create({
            'name': 'Steel Billet 100mm',
            'type': 'consu',
        })

    def test_01_workcenter_costing_aggregation(self):
        """Verify total industrial hourly cost aggregates base, labor, and overhead."""
        self.assertEqual(self.workcenter.total_hourly_rate, 100.0)
        self.assertEqual(self.workcenter.maintenance_status, 'operational')

    def test_02_bom_revision_and_mo(self):
        """Verify BOM revision tracking and manufacturing order creation."""
        bom = self.env['mrp.bom'].create({
            'product_tmpl_id': self.product_fg.product_tmpl_id.id,
            'product_qty': 1.0,
            'type': 'normal',
            'bom_revision': 'REV-02',
            'bom_line_ids': [(0, 0, {
                'product_id': self.product_rm.id,
                'product_qty': 2.0,
            })]
        })
        self.assertEqual(bom.bom_revision, 'REV-02')

        mo = self.env['mrp.production'].create({
            'product_id': self.product_fg.id,
            'product_qty': 10.0,
            'bom_id': bom.id,
            'production_shift': 'morning',
        })
        self.assertEqual(mo.production_shift, 'morning')
        self.assertFalse(mo.has_rework_operations)
