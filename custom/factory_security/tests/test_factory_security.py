# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestFactorySecurity(TransactionCase):

    def test_01_verify_roles_hierarchy(self):
        """Verify all industrial groups exist and maintain proper implied relationships."""
        group_storekeeper = self.env.ref('factory_security.group_factory_storekeeper')
        group_purchase_officer = self.env.ref('factory_security.group_factory_purchase_officer')
        group_purchase_manager = self.env.ref('factory_security.group_factory_purchase_manager')
        group_supervisor = self.env.ref('factory_security.group_factory_production_supervisor')

        self.assertTrue(group_storekeeper)
        self.assertTrue(group_purchase_officer)
        self.assertTrue(group_purchase_manager)
        self.assertTrue(group_supervisor)

        # Purchase manager must imply purchase officer
        self.assertIn(group_purchase_officer, group_purchase_manager.implied_ids)
