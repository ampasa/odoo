# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    def _get_performance(self):
        for rec in self:
            #           
            quantity_carcass = 0
            #
            for move in rec.move_raw_ids:
                quantity_carcass += move.quantity_done if move.product_id.carcass_product else 0
            #
            rec.performance = rec.qty_producing / quantity_carcass if quantity_carcass > 0 else 0
            rec.consumed = quantity_carcass
        return True

    performance = fields.Float(string="Rendimiento", compute="_get_performance")
    consumed = fields.Float(string="Consumido", compute="_get_performance")
    
