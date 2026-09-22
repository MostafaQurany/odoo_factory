# -*- coding: utf-8 -*-
from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    factory_po_approval_limit = fields.Monetary(
        string='PO Factory Manager Approval Threshold',
        default=50000.0,
        currency_field='currency_id',
        help='Purchase orders exceeding this amount require Factory Manager approval.')
