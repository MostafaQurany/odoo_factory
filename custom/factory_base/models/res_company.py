# -*- coding: utf-8 -*-
from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    factory_code = fields.Char(
        string="Factory Code",
        size=16,
        help="Unique identifier code for this manufacturing facility."
    )
    industrial_license_number = fields.Char(
        string="Industrial License No.",
        help="Official manufacturing and industrial registration license number."
    )
    primary_manufacturing_type = fields.Selection([
        ('discrete', 'Discrete Manufacturing'),
        ('process', 'Process / Batch Manufacturing'),
        ('mixed', 'Mixed / Assembly Mode')
    ], string="Manufacturing Mode", default='discrete')
