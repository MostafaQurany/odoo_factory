# -*- coding: utf-8 -*-
from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    factory_customer_tier = fields.Selection([
        ('key_account', 'Key Industrial Account'),
        ('oem', 'OEM Manufacturer Partner'),
        ('distributor', 'Wholesale Distributor'),
        ('standard', 'Standard Commercial Client'),
    ], string='Factory Customer Category', default='standard', index=True)
