# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError

class TestFactoryPurchase(TransactionCase):

    def setUp(self):
        super(TestFactoryPurchase, self).setUp()
        self.vendor = self.env['res.partner'].create({
            'name': 'Primary Industrial Supplier',
            'supplier_rank': 1,
        })
        self.product_steel = self.env['product.product'].create({
            'name': 'Cold Rolled Steel Coil',
            'type': 'consu',
            'purchase_ok': True,
        })
        self.env.company.factory_po_approval_limit = 10000.0

    def test_01_po_approval_tier_trigger(self):
        """Verify that PO above company threshold requires factory manager approval."""
        po = self.env['purchase.order'].create({
            'partner_id': self.vendor.id,
            'factory_purchase_type': 'raw_material',
            'order_line': [(0, 0, {
                'product_id': self.product_steel.id,
                'name': 'Steel Coil',
                'product_qty': 100,
                'price_unit': 200.0, # Total = 20,000 > 10,000 limit
            })]
        })

        self.assertEqual(po.factory_approval_state, 'draft')
        
        # Non-manager user confirm attempts should raise UserError or submit for approval
        user_operator = self.env['res.users'].create({
            'name': 'Test Purchase Officer',
            'login': 'purchase_officer',
            'groups_id': [(6, 0, [self.env.ref('factory_base.group_factory_user').id])]
        })

        with self.assertRaises(UserError):
            po.with_user(user_operator).button_confirm()

        self.assertEqual(po.factory_approval_state, 'to_approve')

        # Manager approves
        po.action_factory_approve()
        self.assertEqual(po.factory_approval_state, 'approved')
        po.button_confirm()
        self.assertEqual(po.state, 'purchase')
