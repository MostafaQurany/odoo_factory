# -*- coding: utf-8 -*-
from odoo import models, fields

class ProductSupplierinfo(models.Model):
    _inherit = 'product.supplierinfo'

    moq_strict = fields.Boolean(
        string='Strict MOQ Enforcement',
        default=True,
        help='If true, purchase orders cannot order less than the minimum quantity.')
    supplier_rating = fields.Selection([
        ('tier_1', 'Tier 1 — Strategic / Certified'),
        ('tier_2', 'Tier 2 — Approved Standard'),
        ('tier_3', 'Tier 3 — Conditional / New'),
    ], string='Vendor Quality Tier', default='tier_2')
