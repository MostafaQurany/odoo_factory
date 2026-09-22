# -*- coding: utf-8 -*-
from odoo import models, fields

class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    bom_revision = fields.Char(string='Engineering Revision', default='REV-01', index=True)
    engineering_approved_by_id = fields.Many2one('res.users', string='Engineering Sign-off By')
    engineering_approval_date = fields.Date(string='Sign-off Date')
    engineering_notes = fields.Text(string='Revision & Process Notes')
