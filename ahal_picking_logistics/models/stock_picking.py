# -*- coding: utf-8 -*-

from odoo import models, api, fields, _
from odoo.exceptions import ValidationError
import time
import json

class StockPicking(models.Model):
    _inherit = 'stock.picking'


    calculo_cargo =  fields.Selection(
        selection=[('calc_diff', 'Calcular diferencias'), 
                   ('no_calc', 'Sin calculo(Pago a Val. De factura)'),],
        string=('Estatus de cálculo'),
    )

    plant_cargo =  fields.Many2one('plant.ampasa', string="PLANT")

    brokers_ampasa = fields.Selection(
        selection=[
                   ('ninguno', 'Ninguno'), 
                   ('landmark', 'Landmark Food'), 
                   ('north', 'North Central'), 
                   ('triple', 'Triple B Food'), 
                   ('tyson', 'Tyson'), 
                   ('sanderson', 'Sanderson'), 
                   ('south', 'Southeastern'), 
                   ('carlos_valle', 'Carlos del Valle'),
                   ('food_suppliers', 'Food Suppliers'),
                   ('s_border_warehouse', 'S. Border Warehouse'),
                   ],
        string=('Brokers'),
    )

    mph_ampasa = fields.Char(string="MPH")
    invoice_ampasa = fields.Integer(string="Invoice")
    caja_mexicana = fields.Char(string="Caja Mexicana")

    kd_cargo = fields.Date(string="KILLING DATE")
    pd_cargo = fields.Date(string="PACKING DATE")
    gw_usa_cargo = fields.Float(string="GROSS WEIGTH SCALE USA")
    tare_cargo = fields.Float(string="TARE")
    water_spill_cargo = fields.Float(string="WATER SPILL")
    rejections_fq_cargo = fields.Float(string="REJECTIONS FOR QUALITY")
    net_weigth_usa_cargo = fields.Float(string="NET WEIGTH SCALE USA", compute="get_net_weigth")
    weigth_in_cargo = fields.Float(string="WEIGTH INVOICED")
    diff_weigth_ampasa_cargo = fields.Float(string="DIFERENCE WEIGTH AMPASA", compute="get_diff_weigth")
    combos_cargo = fields.Float(string="COMBOS")
    price_cargo = fields.Float(string="PRICE", digits=(10,4))
    cost_cargo = fields.Float(string="COST", compute="get_cost")
    obs_cargo = fields.Text(string="OBSERVATIONS")

    flete_id = fields.Many2one('flete.rel',string="Flete", track_visibility='always')

    #CREATE FUNCTION TO GET THE FLETE STATUS DINAMICALLY
    #BUSCA LOS REGISTROS DONDE ESTE SELECCIONADO EL FLETE
    

    #FUNCTION TO CHANGE STATE WHEN THE FLETE IS SELECTED
    @api.onchange('flete_id')
    def get_flete_status(self):
        for rec in self:
            if rec.picking_type_id.sequence_code == 'IN':
                rec.flete_id.flete_status = 'viaje_mp'
            elif rec.picking_type_id.sequence_code == 'OUT':
                rec.flete_id.flete_status = 'viaje_pt'
            else:
                rec.flete_id.flete_status = 'disponible'

    #FUNCTION TO WRITE THE FLETE AS DISPONIBLE WHEN THE STATE IS DONE
    def _compute_state(self):
        res = super(StockPicking, self)._compute_state()
        for rec in self:
            if rec.state == 'done':
                rec.flete_id.write({'flete_status': 'disponible'})
                return res



    
    def get_net_weigth(self):
        for rec in self:
            rec.net_weigth_usa_cargo = rec.gw_usa_cargo - rec.tare_cargo - rec.water_spill_cargo - rec.rejections_fq_cargo
     

    def get_diff_weigth(self):
        for rec in self:
            rec.diff_weigth_ampasa_cargo = rec.net_weigth_usa_cargo - rec.weigth_in_cargo
     

    def get_cost(self):
        for rec in self:
            rec.cost_cargo = rec.diff_weigth_ampasa_cargo * rec.price_cargo


    #FUNCIÓN ACTUALIZAR CAMPOS AL VALIDAR LA ENTRADA
    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        #stp_obj = self.env['stock.production.lot']
        for rec in self.move_ids_without_package:
            move_line_ids = self.env['stock.move.line'].search([('move_id','=',rec.id)])
            for line in move_line_ids:
                if line.lot_id:
                    #lot_id = stp_obj.search([('name','=',rec.lot_name)],limit='1')
                    #if rec.lot_id:
                    line.lot_id.kd_cargo = line.kd_cargo
                    line.lot_id.flete_id = line.flete_id.id
                    line.lot_id.fecha_entrada = line.fecha_entrada
        return res

    def action_show_details(self):
        res = super(StockMove,self).action_show_details()
        for line in self.move_line_ids:
            if line.picking_id:
                line.kd_cargo = line.picking_id.kd_cargo
                line.flete_id = line.picking_id.flete_id
                line.kd_cargo = line.picking_id.fecha_entrada
        return res

    #ADD LOT NUMBER FROM MOVE LINE IDS
    lot_number = fields.Char(string='Lot Number', compute='_compute_lot_number')

    def _compute_lot_number(self):
        for line in self.move_line_ids:
            if line.lot_name:
                self.lot_number = line.lot_name
            else:
                self.lot_number = ''




     

#CREATE NEW MODEL FOR PLANT AMPASA
class PlantAmpasa(models.Model):
    _name = 'plant.ampasa'
    _description = 'Planta Ampasa'
    _rec_name ='name'

    name = fields.Char(string="Nombre de la planta")


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    kd_cargo = fields.Date(string="Killing date")
    flete_id = fields.Many2one('flete.rel',string="Flete")
    fecha_entrada = fields.Date(string="Fecha entrada", default=fields.Date.today)
    qty_done_pass = fields.Float(string="Cantidad hecha USA", related="picking_id.net_weigth_usa_cargo")
    #lot_id_value = fields.Many2one('stock.production.lot', string="Lot/SNumber")
    
    #FUNCTION 
    @api.onchange('qty_done_pass')
    def get_values_qty(self):
        for rec in self:
            if rec.qty_done_pass:
                rec.qty_done = rec.qty_done_pass
 
    #FUNCTION 
    @api.onchange('lot_id')
    def get_values(self):
        for rec in self:
            if rec.lot_id:
                rec.kd_cargo = rec.lot_id.kd_cargo
                rec.flete_id = rec.lot_id.flete_id
                rec.fecha_entrada = rec.lot_id.fecha_entrada

    custom_field = fields.Char(string='Custom Field')


class StockMove(models.Model):
    _inherit = 'stock.move'

    def action_show_details(self):
        res = super(StockMove, self).action_show_details()
        res.update({'context': 
            dict(
                self.env.context,
                show_owner=self.picking_type_id.code != 'incoming',
                show_lots_m2o=self.has_tracking != 'none' and (self.picking_type_id.use_existing_lots or self.state == 'done' or self.origin_returned_move_id.id),  # able to create lots, whatever the value of ` use_create_lots`.
                show_lots_text=self.has_tracking != 'none' and self.picking_type_id.use_create_lots and not self.picking_type_id.use_existing_lots and self.state != 'done' and not self.origin_returned_move_id.id,
                show_source_location=self.picking_type_id.code != 'incoming',
                show_destination_location=self.picking_type_id.code != 'outgoing',
                show_package=not self.location_id.usage == 'supplier',
                show_reserved_quantity=self.state != 'done' and not self.picking_id.immediate_transfer and self.picking_type_id.code != 'incoming',
                default_kd_cargo = self.picking_id.kd_cargo,
                default_flete_id = self.picking_id.flete_id.id,
                default_qty_done = self.picking_id.net_weigth_usa_cargo)

            })
        return res

   
