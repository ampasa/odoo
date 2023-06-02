from odoo import models, fields,api
from dateutil import parser
from datetime import datetime

class AmpasaPrenomina(models.Model):
    _name = 'ampasa.prenomina'
    _description = 'AmpasaPrenomina'
    
    #AGREGA CAMPOS PRENOMINA
    codigo_empleado = fields.Integer(string='Código',related="nombre_empleado.codigo_empleado")
    start_date = fields.Date(string='Inicio')
    no_semana = fields.Integer(string="Num. Sem.", compute='_compute_week_number',store=True)
    end_date = fields.Date(string='Fin')

    @api.depends('start_date')
    def _compute_week_number(self):
        for record in self:
            start_date = record.start_date
            if start_date:
                week_number = start_date.isocalendar()[1]
                record.no_semana = week_number
            else:
                record.no_semana = 0


    gender = fields.Selection([
        ('male', 'M'),
        ('female', 'F'),
        ('other', 'Otro'),
    ], string='Sexo', related="nombre_empleado.gender")
    nombre_empleado = fields.Many2one('hr.employee', string='Nombre del empleado')
    salario_diario = fields.Float(string='SD')
    puesto = fields.Many2one('hr.job', string='Puesto', compute='_compute_puesto')
    
    @api.depends('nombre_empleado')
    def _compute_puesto(self):
        for record in self:
            record.puesto = record.nombre_empleado.job_id

    departamento = fields.Many2one('hr.department', string='Departamento', compute="_compute_departamento")
    
    @api.depends('nombre_empleado')
    def _compute_departamento(self):
        for record in self:
            record.departamento = record.nombre_empleado.department_id

    supervisor = fields.Many2one('hr.employee', string='Supervisor', compute="_compute_supervisor")

    @api.depends('nombre_empleado')
    def _compute_supervisor(self):
        for record in self:
            record.supervisor = record.nombre_empleado.parent_id.id
    
    turno_empleados = fields.Selection(
        selection=[('01', 'Nocturno'),
                   ('02', 'Matutino'),
                   ('03', 'Vespertino'),
                   ('04', 'Rotativo'),
                   ('05', 'Mixto')],
        string='Turno empleados', related="nombre_empleado.turno_empleados"
    )

    sindicalizado = fields.Boolean(string='Sindicalizado', related="nombre_empleado.sindicalizado")


    #CAMPOS MANUALES
    faltas = fields.Integer(string='Faltas')
    permiso_sin_goce_sueldo = fields.Integer(string='Permiso sin goce de sueldo')
    incapacidad = fields.Integer(string='Incapacidad')
    vacaciones = fields.Integer(string='Vacaciones')
    horas_semanal = fields.Integer(string='Horas semanales')
    horas_semanales_trabajadas = fields.Integer(string='Horas semanales trabajadas')
    prim_dom = fields.Float(string='Prim. Dom')
    descanso_trabajado = fields.Float(string='Descanso trabajado')
    punt_y_assist = fields.Float(string='Punt. y assist.')
    cubiertas_en_num = fields.Float(string='Cubiertas en #')
    t_extra_doble = fields.Float(string='T. Extra Doble')
    t_extra_doble_importe = fields.Float(string='T.E2 Importe', compute="_compute_t_extra_doble_importe")

    @api.depends('salario_diario','t_extra_doble')
    def _compute_t_extra_doble_importe(self):
        for record in self:
            record.t_extra_doble_importe = record.salario_diario / 8 * 2 * record.t_extra_doble



    t_extra_triple = fields.Float(string='T. Extra Triple')
    t_extra_triple_importe = fields.Float(string='T.E.3 Importe', compute="_compute_t_extra_triple_importe")

    @api.depends('salario_diario','t_extra_triple')
    def _compute_t_extra_triple_importe(self):
        for record in self:
            record.t_extra_triple_importe = record.salario_diario / 8 * 3 * record.t_extra_triple


    puntualidad_asistencia = fields.Float(string='Puntualidad y asistencia')
    cubiertas_en_dinero = fields.Float(string='Cubiertas en $$$', compute="_compute_cubiertas_en_dinero")

    @api.depends('cubiertas_en_num')
    def _compute_cubiertas_en_dinero(self):
        for record in self:
            record.cubiertas_en_dinero = record.cubiertas_en_num * 120
    

    premios_eficiencia = fields.Float(string='Premios eficiencia')
    ayuda_transporte = fields.Float(string='Ayuda Transporte')
    gratificacion_fija = fields.Float(string='Gratificación Fija')
    gratificacion_cumpleanios = fields.Float(string='Gratificación Cumpleaños')
    gratificacion_eventual = fields.Float(string='Gratificación eventual')
    combos_paleados = fields.Float(string='Combos Paleados')
    total_gratificacion = fields.Float(string='TOTAL GRATIFICACIÓN', compute="_compute_total_gratificacion")

    @api.depends('cubiertas_en_dinero','gratificacion_fija','gratificacion_cumpleanios','gratificacion_eventual','combos_paleados')
    def _compute_total_gratificacion(self):
        for record in self:
            record.total_gratificacion = record.cubiertas_en_dinero + record.gratificacion_fija + record.gratificacion_cumpleanios + record.gratificacion_eventual + record.combos_paleados

    prestamos = fields.Float(string='PRÉSTAMOS')
    deduccion_general = fields.Float(string='DEDUCCIÓN GRAL.')
    descuentos_adicionales = fields.Float(string='Descuentos adicionales')
    total_deduccion = fields.Float(string='TOTAL DEDUCCIÓN', compute="_compute_total_deduccion")

    @api.depends('prestamos','deduccion_general','descuentos_adicionales')
    def _compute_total_deduccion(self):
        for record in self:
            record.total_deduccion = record.prestamos + record.deduccion_general + record.descuentos_adicionales


    observaciones_deducciones = fields.Text(string='OBSERVACIONES DEDUCCIONES / ADEUDO INFONAVIT')
    observaciones = fields.Text(string='OBSERVACIONES')