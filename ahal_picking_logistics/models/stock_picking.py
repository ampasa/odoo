# -*- coding: utf-8 -*-

from odoo import models, api, fields, _
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
    price_cargo = fields.Float(string="PRICE")
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
        if self.state == 'done':
            self.flete_id.write({'flete_status': 'disponible'})
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
    fecha_entrada = fields.Date(string="Fecha entrada")
    #lot_id_value = fields.Many2one('stock.production.lot', string="Lot/SNumber")
    

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
        res = super(StockMove,self).action_show_details()
        for line in self.move_line_ids:
            if line.lot_id:
                line.kd_cargo = line.lot_id.kd_cargo
                line.flete_id = line.lot_id.flete_id
                line.kd_cargo = line.lot_id.fecha_entrada
        return res
