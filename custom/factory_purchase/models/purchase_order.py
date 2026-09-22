# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    factory_purchase_type = fields.Selection([
        ('raw_material', 'Raw Materials'),
        ('components', 'Components & Hardware'),
        ('packaging', 'Packaging Materials'),
        ('maintenance', 'Maintenance & Spares'),
        ('general', 'General Supplies'),
    ], string='Procurement Category', default='raw_material', required=True, index=True)

    factory_approval_state = fields.Selection([
        ('draft', 'Draft'),
        ('to_approve', 'Waiting Factory Manager Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='Factory Approval Status', default='draft', tracking=True, copy=False)

    factory_approved_by_id = fields.Many2one('res.users', string='Approved By', readonly=True, copy=False)
    factory_approval_date = fields.Datetime(string='Approval Date', readonly=True, copy=False)

    def action_factory_submit_for_approval(self):
        for order in self:
            order.write({'factory_approval_state': 'to_approve'})
        return True

    def action_factory_approve(self):
        if not self.env.user.has_group('factory_base.group_factory_manager'):
            raise UserError(_("Only a Factory Manager can approve high-value purchase orders."))
        for order in self:
            order.write({
                'factory_approval_state': 'approved',
                'factory_approved_by_id': self.env.user.id,
                'factory_approval_date': fields.Datetime.now(),
            })
        return True

    def action_factory_reject(self):
        if not self.env.user.has_group('factory_base.group_factory_manager'):
            raise UserError(_("Only a Factory Manager can reject purchase orders."))
        for order in self:
            order.write({'factory_approval_state': 'rejected'})
        return True

    def button_confirm(self):
        for order in self:
            threshold = order.company_id.factory_po_approval_limit
            if threshold and order.amount_total > threshold:
                if order.factory_approval_state != 'approved':
                    if self.env.user.has_group('factory_base.group_factory_manager'):
                        order.action_factory_approve()
                    else:
                        order.action_factory_submit_for_approval()
                        raise UserError(_(
                            "This purchase order total (%(amount).2f) exceeds the Factory Manager approval threshold (%(threshold).2f). "
                            "It has been submitted for approval.",
                            amount=order.amount_total,
                            threshold=threshold,
                        ))
        return super(PurchaseOrder, self).button_confirm()
