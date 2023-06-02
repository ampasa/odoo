# -*- coding: utf-8 -*-

from odoo import models, fields
from odoo.exceptions import UserError


class WizardPrenomina(models.TransientModel):
    _name = 'wizard.prenomina'
    _description = 'Wizard Prenomina'

    start_date = fields.Date(string='Fecha de inicio')
    end_date = fields.Date(string='Fecha de fin')

    def generate_prenomina(self):
        # Lógica para generar la prenomina
        # Puedes agregar tu propia implementación aquí

        # Obtener los registros de los empleados disponibles
        employee_records = self.env['hr.employee'].search([])

        # Crear un registro en el modelo ampasa.prenomina por cada empleado
        Prenomina = self.env['ampasa.prenomina']
        for employee in employee_records:
            Prenomina.create({
                'nombre_empleado': employee.id,
                'start_date': self.start_date,
                'end_date': self.end_date
                # Agrega los demás campos y sus valores correspondientes aquí
            })
