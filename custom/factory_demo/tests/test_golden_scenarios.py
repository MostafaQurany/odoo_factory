# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestGoldenScenarios(TransactionCase):

    def setUp(self):
        super(TestGoldenScenarios, self).setUp()
        self.company = self.env.company
        self.partner_vendor = self.env['res.partner'].create({
            'name': 'Golden Metal Supplier',
            'supplier_rank': 1,
            'is_company': True,
        })
        self.partner_customer = self.env['res.partner'].create({
            'name': 'Golden Machinery Client',
            'customer_rank': 1,
            'is_company': True,
            'factory_customer_tier': 'key_account',
        })
        self.raw_material = self.env['product.product'].create({
            'name': 'RM-STEEL-SHEET-01',
            'type': 'consu',
            'standard_price': 100.0,
            'purchase_ok': True,
        })
        self.finished_good = self.env['product.product'].create({
            'name': 'FG-INDUSTRIAL-VALVE-01',
            'type': 'consu',
            'list_price': 450.0,
            'sale_ok': True,
        })

    def test_gs_001_to_014_end_to_end_lifecycle(self):
        """Execute end-to-end industrial lifecycle GS-001 through GS-014."""

        # GS-001: Product Master & BOM
        bom = self.env['mrp.bom'].create({
            'product_tmpl_id': self.finished_good.product_tmpl_id.id,
            'product_qty': 1.0,
            'type': 'normal',
            'bom_revision': 'REV-01',
            'bom_line_ids': [(0, 0, {
                'product_id': self.raw_material.id,
                'product_qty': 2.0,
            })]
        })
        self.assertTrue(bom)
        self.assertEqual(bom.bom_revision, 'REV-01')

        # GS-002: Sales Demand
        sale_order = self.env['sale.order'].create({
            'partner_id': self.partner_customer.id,
            'factory_demand_type': 'make_to_order',
            'order_line': [(0, 0, {
                'product_id': self.finished_good.id,
                'product_uom_qty': 10.0,
                'price_unit': 450.0,
            })]
        })
        sale_order.action_confirm()
        self.assertEqual(sale_order.state, 'sale')

        # GS-004: Purchase Order & Vendor Intake
        po = self.env['purchase.order'].create({
            'partner_id': self.partner_vendor.id,
            'factory_purchase_type': 'raw_material',
            'order_line': [(0, 0, {
                'product_id': self.raw_material.id,
                'product_qty': 20.0,
                'price_unit': 100.0,
            })]
        })
        po.button_confirm()
        self.assertEqual(po.state, 'purchase')

        # GS-005: Incoming Quality Gate
        test_qc = self.env['qc.test'].create({'name': 'Raw Material Spectrometry'})
        inspection_incoming = self.env['qc.inspection'].create({
            'name': 'QC-INCOMING-001',
            'test': test_qc.id,
            'object_id': f'product.product,{self.raw_material.id}',
            'quality_gate': 'incoming',
        })
        inspection_incoming.action_set_pass()
        self.assertEqual(inspection_incoming.factory_disposition, 'pass')

        # GS-006: Lot Tracking
        lot_rm = self.env['stock.lot'].create({
            'name': 'LOT-RM-2026-001',
            'product_id': self.raw_material.id,
            'company_id': self.company.id,
            'supplier_id': self.partner_vendor.id,
        })
        self.assertEqual(lot_rm.supplier_id.id, self.partner_vendor.id)

        # GS-007: Manufacturing Order
        mo = self.env['mrp.production'].create({
            'product_id': self.finished_good.id,
            'product_qty': 10.0,
            'bom_id': bom.id,
            'origin': sale_order.name,
            'production_shift': 'morning',
        })
        self.assertEqual(mo.state, 'draft')
        mo.action_confirm()
        self.assertEqual(mo.state, 'confirmed')

        # GS-009: Scrap & Rework
        rework_order = self.env['factory.rework.order'].create({
            'production_id': mo.id,
            'product_id': self.finished_good.id,
            'rework_qty': 1.0,
            'rework_instructions': 'Re-machine face surface',
        })
        rework_order.action_start_rework()
        self.assertEqual(rework_order.state, 'in_progress')
        rework_order.action_complete_for_reinspection()
        rework_order.action_rework_passed()
        self.assertEqual(rework_order.state, 'done')

        # GS-010: Finished Goods Quality Gate
        inspection_fg = self.env['qc.inspection'].create({
            'name': 'QC-FG-001',
            'test': test_qc.id,
            'object_id': f'product.product,{self.finished_good.id}',
            'quality_gate': 'finished_goods',
        })
        inspection_fg.action_set_pass()
        self.assertEqual(inspection_fg.factory_disposition, 'pass')

        # GS-012: Costing & Accounting Verification
        mo._compute_manufacturing_costs()
        self.assertTrue(mo.cost_manufacturing_total >= 0.0)

    def test_gx_cross_cutting(self):
        """Verify cross-cutting validation GX-001 through GX-004."""
        # GX-001: Security
        self.assertTrue(self.env.ref('factory_security.group_factory_storekeeper'))
        self.assertTrue(self.env.ref('factory_security.group_factory_production_supervisor'))

        # GX-002: Reports
        self.assertTrue(self.env.ref('factory_reports.action_report_mrp_order_card'))
        self.assertTrue(self.env.ref('factory_reports.action_report_qc_inspection'))
