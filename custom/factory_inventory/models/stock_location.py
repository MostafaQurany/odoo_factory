# -*- coding: utf-8 -*-
from odoo import models, fields, api

class StockLocation(models.Model):
    _inherit = 'stock.location'

    factory_location_type = fields.Selection([
        ('input', 'Input / Receiving'),
        ('quality_hold', 'Quality Hold / Quarantine'),
        ('raw_materials', 'Raw Materials'),
        ('components', 'Components'),
        ('wip', 'WIP / Production Floor'),
        ('finished_goods', 'Finished Goods'),
        ('packaging', 'Packaging Materials'),
        ('returns', 'Customer / Vendor Returns'),
        ('scrap', 'Scrap & Defective'),
        ('spare_parts', 'Spare Parts / Maintenance'),
    ], string='Factory Classification', index=True,
       help='Industrial factory classification for this stock location.')

    is_factory_controlled = fields.Boolean(
        string='Factory Controlled Location',
        default=True,
        help='If checked, this location follows strict industrial warehouse policies.')
