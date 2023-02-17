# -*- coding: utf-8 -*-

from odoo import models, api, fields, _

class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    kd_cargo = fields.Date(string="Killing date")
    flete_id = fields.Many2one('flete.rel',string="Flete")
    fecha_entrada = fields.Date(string="Fecha entrada")
    temperature = fields.Float(string="Temperatura")