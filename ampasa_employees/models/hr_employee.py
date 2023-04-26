# -*- coding: utf-8 -*-

from odoo import models, api, fields, _
from odoo.exceptions import ValidationError

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    #Información basica
    codigo_empleado = fields.Integer(string="Código de empleado")
    #nombres = fields.Char(string='Nombres')
    #apellido_paterno = fields.Char(string='Apellido paterno')
    #apellido_materno = fields.Char(string='Apellido materno')

    #@api.onchange('nombres', 'apellido_paterno', 'apellido_materno')
    #def _compute_name(self):
    #    for employee in self:
    #        employee.name = ' '.join(filter(None, [employee.nombres, employee.apellido_paterno, employee.apellido_materno]))

    curp = fields.Char(string="CURP")

    #Revisar length del CURP
    @api.constrains('curp')
    def _check_curp_length(self):
        for record in self:
            if len(record.curp or '') != 18:
                raise ValidationError('El campo CURP debe tener 18 digitos')

    numero_ine = fields.Char(string="Número de INE")
    estado_nacimiento = fields.Many2one('res.country.state', string="Estado de nacimiento")

    #Información nominal
    numero_ss = fields.Integer(string="Número de seguro social")
    factor_descuento_infonavit = fields.Integer(string="Factor de descuento Infonavit")
    #area_asignada = fields.Many2one('area.asignada')
    turno_empleados = fields.Selection(
        selection=[('01', 'Nocturno'),
                   ('02', 'Matutino'),
                   ('03', 'Vespertino')],
        string='My Field',
    )

    inicio_perido = fields.Date()
    fin_periodo = fields.Date()
    
    tipo_empleado = fields.Selection(
        selection=[('01', 'Confianza'),
                   ('02', 'Sindicalizado'),
                   ('03', 'Por ley')],
        string='Tipo empleado',
    )
    
    banco_empleado = fields.Many2one('res.bank', string="Banco")
    numero_tarjeta = fields.Integer(string="Número de tarjeta")

    #Información personal
    nombre_padre = fields.Char(string="Nombre del padre")
    nombre_madre = fields.Char(string="Nombre de la madre")
    hijo_1 = fields.Char(string="Hijo 1")
    hijo_2 = fields.Char(string="Hijo 2")
    hijo_3 = fields.Char(string="Hijo 3")
    hijo_4 = fields.Char(string="Hijo 4")
    fecha_nac_hijo1 = fields.Date(string="Fecha nac. hijo 1")
    fecha_nac_hijo2 = fields.Date(string="Fecha nac. hijo 2")
    fecha_nac_hijo3 = fields.Date(string="Fecha nac. hijo 3")
    fecha_nac_hijo4 = fields.Date(string="Fecha nac. hijo 4")
    nombre_esposo = fields.Char(string="Nombre del esposo/a")
    nombre_beneficiario = fields.Char(string="Nombre del beneficiario")
    telefono_beneficiario = fields.Char(string="Teléfono del beneficiario")
    notas_bajas = fields.Html(string="Notas de bajas")
    fecha_baja = fields.Date(string="Fecha de baja")
    semana_baja = fields.Integer(string="Semana de baja")
    fecha_segundo_ingreso = fields.Date(string="Fecha de segundo ingreso")
    fecha_primer_ingreso = fields.Date(string="Fecha de primer ingreso")
    enfermedad_cronica = fields.Char(string="Enfermedad crónica")
    alergia = fields.Char(string="Alergia")
    covid = fields.Char(string="Covid")
    sindicalizado = fields.Boolean(string="Sindicalizado")
    tipo_sangre = fields.Selection([
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ], string='Tipo de sangre')
    
    leer_escribir = fields.Selection(
        selection=[('1', 'Sí'),
                   ('2', 'No')],
        string='Leer/Escribir',
    )

    observaciones = fields.Html(string="Observaciones")


    #Campos con observaciones
    semana_ingreso = fields.Integer(string="Semana de ingreso")
    fecha_ingreso = fields.Integer(string="Fecha de ingreso")
    clabe_interbancaria = fields.Integer(string="Clabe interbancaria")

