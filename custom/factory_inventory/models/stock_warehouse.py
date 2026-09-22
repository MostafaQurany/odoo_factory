# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    loc_input_id = fields.Many2one('stock.location', string='Input / Receiving Location')
    loc_quality_hold_id = fields.Many2one('stock.location', string='Quality Hold Location')
    loc_raw_materials_id = fields.Many2one('stock.location', string='Raw Materials Location')
    loc_components_id = fields.Many2one('stock.location', string='Components Location')
    loc_wip_id = fields.Many2one('stock.location', string='WIP / Production Location')
    loc_finished_goods_id = fields.Many2one('stock.location', string='Finished Goods Location')
    loc_packaging_id = fields.Many2one('stock.location', string='Packaging Location')
    loc_returns_id = fields.Many2one('stock.location', string='Returns Location')
    loc_scrap_id = fields.Many2one('stock.location', string='Scrap Location')
    loc_spare_parts_id = fields.Many2one('stock.location', string='Spare Parts Location')

    def action_create_factory_locations(self):
        """Idempotently generates or verifies standard factory locations under this warehouse."""
        self.ensure_one()
        Location = self.env['stock.location']
        parent_loc = self.lot_stock_id

        factory_structure = [
            ('loc_input_id', 'Input / Receiving', 'input'),
            ('loc_quality_hold_id', 'Quality Hold', 'quality_hold'),
            ('loc_raw_materials_id', 'Raw Materials', 'raw_materials'),
            ('loc_components_id', 'Components', 'components'),
            ('loc_wip_id', 'WIP / Production', 'wip'),
            ('loc_finished_goods_id', 'Finished Goods', 'finished_goods'),
            ('loc_packaging_id', 'Packaging', 'packaging'),
            ('loc_returns_id', 'Returns', 'returns'),
            ('loc_scrap_id', 'Scrap', 'scrap'),
            ('loc_spare_parts_id', 'Spare Parts', 'spare_parts'),
        ]

        vals_update = {}
        for field_name, name_suffix, loc_type in factory_structure:
            current_loc = getattr(self, field_name)
            if not current_loc or not current_loc.exists():
                full_name = f"{self.code}/{name_suffix}"
                # Look for existing location by name or barcode
                existing = Location.search([
                    ('location_id', '=', parent_loc.id),
                    ('factory_location_type', '=', loc_type),
                    ('company_id', '=', self.company_id.id),
                ], limit=1)
                if not existing:
                    existing = Location.create({
                        'name': name_suffix,
                        'location_id': parent_loc.id,
                        'usage': 'inventory' if loc_type == 'scrap' else 'internal',
                        'scrap_location': True if loc_type == 'scrap' else False,
                        'factory_location_type': loc_type,
                        'is_factory_controlled': True,
                        'company_id': self.company_id.id,
                    })
                vals_update[field_name] = existing.id

        if vals_update:
            self.write(vals_update)

        return True
