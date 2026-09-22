# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class QcInspection(models.Model):
    _inherit = 'qc.inspection'

    quality_gate = fields.Selection([
        ('incoming', 'Gate 1 — Incoming Receiving Inspection'),
        ('in_process', 'Gate 2 — In-Process Manufacturing Check'),
        ('finished_goods', 'Gate 3 — Final Finished Goods Acceptance'),
        ('return', 'Gate 4 — Customer / Return RMA Inspection'),
    ], string='Quality Gate', default='incoming', required=True, index=True)

    factory_disposition = fields.Selection([
        ('pending', 'Pending Inspection'),
        ('pass', 'PASS — Released to Stock / Next Step'),
        ('hold', 'HOLD — Quarantined for Review'),
        ('rework', 'REWORK — Corrective Action Order'),
        ('scrap', 'SCRAP — Rejected & Scrapped'),
    ], string='Quality Disposition', default='pending', tracking=True, copy=False, index=True)

    inspector_id = fields.Many2one('res.users', string='Quality Inspector', default=lambda self: self.env.user)
    workcenter_id = fields.Many2one('mrp.workcenter', string='Inspected At Work Center')
    lot_id = fields.Many2one('stock.lot', string='Inspected Lot / Serial')
    inspection_notes = fields.Text(string='Inspector Notes & Defects Found')

    rework_order_ids = fields.One2many('factory.rework.order', 'origin_inspection_id', string='Rework Orders')
    scrap_ids = fields.One2many('stock.scrap', 'origin_inspection_id', string='Scrap Orders')

    def action_set_pass(self):
        self.write({
            'factory_disposition': 'pass',
            'state': 'success',
            'date_done': fields.Datetime.now(),
        })
        return True

    def action_set_hold(self):
        self.write({'factory_disposition': 'hold'})
        return True

    def action_set_rework(self):
        self.ensure_one()
        rework_order = self.env['factory.rework.order'].create({
            'origin_inspection_id': self.id,
            'product_id': self.product_id.id,
            'lot_id': self.lot_id.id if self.lot_id else False,
            'rework_qty': self.qty if hasattr(self, 'qty') and self.qty else 1.0,
            'workcenter_id': self.workcenter_id.id if self.workcenter_id else False,
            'rework_instructions': self.inspection_notes or _("Correct defect identified during quality inspection."),
        })
        self.write({'factory_disposition': 'rework'})
        action = self.env['ir.actions.act_window']._for_xml_id('factory_quality.action_factory_rework_order')
        action['res_id'] = rework_order.id
        action['views'] = [(False, 'form')]
        return action

    def action_set_scrap(self):
        self.write({'factory_disposition': 'scrap', 'state': 'failed'})
        return True
