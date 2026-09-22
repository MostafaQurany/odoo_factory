# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestFactoryMaintenance(TransactionCase):

    def setUp(self):
        super(TestFactoryMaintenance, self).setUp()
        self.workcenter = self.env['mrp.workcenter'].create({
            'name': 'Extrusion Line 01',
            'code': 'WC-EXT-01',
            'maintenance_status': 'operational',
        })
        self.equipment = self.env['factory.equipment'].create({
            'name': 'Plastic Extruder Machine',
            'code': 'EQ-EXT-01',
            'workcenter_id': self.workcenter.id,
            'barcode': 'EQ990011',
        })

    def test_01_maintenance_workflow_and_workcenter_status(self):
        """Verify that starting maintenance updates equipment and workcenter status."""
        req = self.env['factory.maintenance.request'].create({
            'equipment_id': self.equipment.id,
            'maintenance_type': 'corrective',
            'failure_reason': 'mechanical',
        })

        self.assertEqual(req.workcenter_id.id, self.workcenter.id)
        self.assertEqual(req.state, 'draft')

        # Start repair
        req.action_start_repair()
        self.assertEqual(req.state, 'in_progress')
        self.assertEqual(self.equipment.state, 'maintenance')
        self.assertEqual(self.workcenter.maintenance_status, 'maintenance')

        # Finish repair
        req.action_finish_repair()
        self.assertEqual(req.state, 'done')
        self.assertEqual(self.equipment.state, 'operational')
        self.assertEqual(self.workcenter.maintenance_status, 'operational')
