# -*- coding: utf-8 -*-

from odoo import models, fields, api


class QualityStatus(models.Model):
    _name = 'quality.status'
    _description = "  "

    name = fields.Char(string='Estatus de rechazo', required=True) 
    
