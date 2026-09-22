# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class ResCompany(models.Model):
    _inherit = 'res.company'

    factory_enable_egp_localization = fields.Boolean(
        string='Egyptian Localization Mode',
        default=True,
        help='If checked, defaults country to Egypt (EG) and currency to EGP.')

    def action_configure_egyptian_defaults(self):
        """Idempotently sets company country to Egypt and currency to EGP if available."""
        self.ensure_one()
        eg_country = self.env['res.country'].search([('code', '=', 'EG')], limit=1)
        egp_currency = self.env['res.currency'].search([('name', '=', 'EGP')], limit=1)

        vals = {}
        if eg_country and self.country_id.id != eg_country.id:
            vals['country_id'] = eg_country.id
        if egp_currency and self.currency_id.id != egp_currency.id:
            egp_currency.write({'active': True})
            vals['currency_id'] = egp_currency.id

        if vals:
            self.write(vals)
        return True
