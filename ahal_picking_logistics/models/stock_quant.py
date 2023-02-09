# -*- coding: utf-8 -*-

from odoo import models, api, fields, _
from datetime import date


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    kd_cargo = fields.Date(string="Killing date", related="lot_id.kd_cargo")
    flete_id = fields.Many2one('flete.rel',string="Flete", related="lot_id.flete_id")
    fecha_entrada = fields.Date(string="Fecha entrada", related="lot_id.fecha_entrada")
    custom_field_value = fields.Char(string='Custom Field Value')
    dias_restantes = fields.Integer(string="Días de anaquel", compute="days_between")


    def days_between(self): 
        today = date.today()
        for rec in self:
            if rec.kd_cargo:
                someday = rec.kd_cargo
                diff = someday - today
                rec.dias_restantes = diff.days
            else:
                rec.dias_restantes = 0

    #def create(self, vals):
    #    #Set the value of the custom field
    #    vals['custom_field_value'] = vals['custom_field']
    #    return super(StockQuant, self).create(vals)


    """def create(self,vals):
        vals = super(StockQuant, self).create(vals)
        vals.update({'custom_field_value': vals['custom_field']})
        return vals"""

    @api.model
    def _get_inventory_fields_write(self):    
        fields = super(StockQuant, self)._get_inventory_fields_write()     
        return fields + ['kd_cargo', 'flete_id', 'fecha_entrada','dias_restantes']

