# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestFactoryInventory(TransactionCase):

    def setUp(self):
        super(TestFactoryInventory, self).setUp()
        self.warehouse = self.env['stock.warehouse'].search([('company_id', '=', self.env.company.id)], limit=1)
        if not self.warehouse:
            self.warehouse = self.env['stock.warehouse'].create({
                'name': 'Test Factory Warehouse',
                'code': 'TFW',
                'company_id': self.env.company.id,
            })

    def test_01_create_factory_locations(self):
        """Verify action_create_factory_locations generates the standard industrial topology."""
        res = self.warehouse.action_create_factory_locations()
        self.assertTrue(res, "action_create_factory_locations should return True")

        # Verify all 10 location types exist and are bound
        locations = [
            self.warehouse.loc_input_id,
            self.warehouse.loc_quality_hold_id,
            self.warehouse.loc_raw_materials_id,
            self.warehouse.loc_components_id,
            self.warehouse.loc_wip_id,
            self.warehouse.loc_finished_goods_id,
            self.warehouse.loc_packaging_id,
            self.warehouse.loc_returns_id,
            self.warehouse.loc_scrap_id,
            self.warehouse.loc_spare_parts_id,
        ]

        for loc in locations:
            self.assertTrue(loc and loc.exists(), f"Factory location {loc} must exist on warehouse")
            self.assertTrue(loc.is_factory_controlled, "Location must be flagged as factory controlled")

        self.assertEqual(self.warehouse.loc_scrap_id.scrap_location, True, "Scrap location must be marked scrap")
        self.assertEqual(self.warehouse.loc_raw_materials_id.factory_location_type, 'raw_materials')

    def test_02_stock_lot_traceability(self):
        """Verify factory lot traceability extensions."""
        product = self.env['product.product'].create({
            'name': 'Test Raw Steel Sheet',
            'type': 'consu',
            'tracking': 'lot',
        })
        supplier = self.env['res.partner'].create({
            'name': 'Steel Vendor Ltd',
            'supplier_rank': 1,
        })
        lot = self.env['stock.lot'].create({
            'name': 'LOT-STEEL-001',
            'product_id': product.id,
            'company_id': self.env.company.id,
            'supplier_id': supplier.id,
            'vendor_lot_number': 'VEND-LOT-9988',
        })

        self.assertEqual(lot.supplier_id.id, supplier.id)
        self.assertEqual(lot.vendor_lot_number, 'VEND-LOT-9988')
