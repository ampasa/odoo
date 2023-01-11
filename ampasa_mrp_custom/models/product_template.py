# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    carcass_product = fields.Boolean(string="Producto carcasa")
    
