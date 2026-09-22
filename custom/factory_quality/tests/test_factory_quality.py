# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestFactoryQuality(TransactionCase):

    def setUp(self):
        super(TestFactoryQuality, self).setUp()
        self.product = self.env['product.product'].create({
            'name': 'Machined Piston Ring',
            'type': 'consu',
            'standard_price': 45.0,
        })
        self.test_qc = self.env['qc.test'].create({
            'name': 'Piston Ring Visual & Tolerance Test',
        })

    def test_01_quality_gates_and_pass(self):
        """Verify quality inspection 4-gate workflow and pass disposition."""
        inspection = self.env['qc.inspection'].create({
            'name': 'QC-TEST-001',
            'test': self.test_qc.id,
            'object_id': f'product.product,{self.product.id}',
            'quality_gate': 'incoming',
        })

        self.assertEqual(inspection.quality_gate, 'incoming')
        self.assertEqual(inspection.factory_disposition, 'pending')

        # Pass
        inspection.action_set_pass()
        self.assertEqual(inspection.factory_disposition, 'pass')
        self.assertEqual(inspection.state, 'success')

    def test_02_rework_workflow(self):
        """Verify rework order generation from failed inspection."""
        inspection = self.env['qc.inspection'].create({
            'name': 'QC-TEST-002',
            'test': self.test_qc.id,
            'object_id': f'product.product,{self.product.id}',
            'quality_gate': 'in_process',
            'inspection_notes': 'Surface burrs need deburring',
        })

        action = inspection.action_set_rework()
        self.assertEqual(inspection.factory_disposition, 'rework')
        self.assertTrue(inspection.rework_order_ids)

        rework = inspection.rework_order_ids[0]
        self.assertEqual(rework.state, 'draft')
        self.assertEqual(rework.product_id.id, self.product.id)

        rework.action_start_rework()
        self.assertEqual(rework.state, 'in_progress')

        rework.action_complete_for_reinspection()
        self.assertEqual(rework.state, 'reinspected')

        rework.action_rework_passed()
        self.assertEqual(rework.state, 'done')
        self.assertEqual(inspection.factory_disposition, 'pass')
