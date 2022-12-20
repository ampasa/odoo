# -*- coding: utf-8 -*-

from odoo import models, fields, api


class QualityCheckWizard(models.TransientModel):
    _inherit = 'quality.check.wizard'

    purchase_id = fields.Many2one(comodel_name='purchase.order', string='Compra origen', related='current_check_id.purchase_id')
    rejected_date = fields.Date(string='Fecha de rechazo')
    partner_id = fields.Many2one(related='current_check_id.partner_id')
    rejected_reason_id = fields.Many2one(comodel_name='quality.rejected.reason', string='Motivo de rechazo') 
    rejected_status_id = fields.Many2one(comodel_name='quality.status', string='Estatus de rechazo') 

    def do_pass(self):
        res = super(QualityCheckWizard, self).do_pass()
        #
        self.current_check_id.purchase_id = self.purchase_id.id
        self.current_check_id.rejected_date = self.rejected_date
        self.current_check_id.rejected_reason_id = self.rejected_reason_id.id
        self.current_check_id.rejected_status_id = self.rejected_status_id.id
        return res
