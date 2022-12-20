# -*- coding: utf-8 -*-

from odoo import models, fields, api


class QualityCheck(models.Model):
    _inherit = 'quality.check'

    def _get_purchase_id(self):
        for rec in self:
            # Se busca la compra con el origen del picking
            purchase_id = self.env['purchase.order'].search([('name','=',rec.picking_id.origin)], limit=1)            
            rec.purchase_id = purchase_id.id if purchase_id else False
        return True

    purchase_id = fields.Many2one(comodel_name='purchase.order', string='Compra', compute='_get_purchase_id')
    rejected_date = fields.Date(string='Fecha de rechazo')
    rejected_reason_id = fields.Many2one(comodel_name='quality.rejected.reason', string='Motivo rechazo') 
    rejected_status_id = fields.Many2one(comodel_name='quality.status', string='Estatus rechazo') 
    
