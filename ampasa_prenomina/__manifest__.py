# -*- coding: utf-8 -*-

{
    'name': 'Ampasa Prenomina',
    'version': '1.3',
    'description': ''' Genera una prenomina con la información de los empleados
    ''',
    'category': 'Empleados',
    'author': 'Devs',
    'website': '',
    'depends': [
        'hr'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/ampasa_prenomina_view.xml',
        'wizard/wizard_prenomina_view.xml',
    ],
    'images': [],
    'application': False,
    'installable': True,
    'price': 0.00,
    'currency': 'USD',
    'license': 'OPL-1',
}
