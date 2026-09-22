# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class StockLot(models.Model):
    _inherit = 'stock.lot'

    supplier_id = fields.Many2one('res.partner', string='Origin Supplier', domain=[('supplier_rank', '>', 0)])
    vendor_lot_number = fields.Char(string='Vendor Lot / Batch Ref', index=True)
    manufacturing_date = fields.Date(string='Production Date', default=fields.Date.context_today)
    inspection_certificate = fields.Char(string='COA / Inspection Cert #')

    def action_trace_production_chain(self):
        """Returns traceability report or moves linked to this lot."""
        self.ensure_one()
        action = self.env['ir.actions.act_window']._for_xml_id('stock.action_stock_report_lot_traceability')
        action['res_id'] = self.id
        return action
