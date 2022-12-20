# -*- coding: utf-8 -*-

from odoo import models, fields, api


class QualityRejectedReason(models.Model):
    _name = 'quality.rejected.reason'

    name = fields.Char(string='Motivos de rechazo', required=True) 
    
