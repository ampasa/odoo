# -*- coding: utf-8 -*-
##############################################################################
#                 @author AHAL CONSULTORES
#
##############################################################################

{
    'name': 'Ampasa Employees',
    'version': '1.1',
    'description': ''' Changes for employees info
    ''',
    'category': 'Expenses',
    'author': 'AHAL Consultores',
    'website': '',
    'depends': [
        'hr',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_employee_view.xml',
    ],
    'images': [],
    'application': False,
    'installable': True,
    'price': 0.00,
    'currency': 'USD',
    'license': 'OPL-1',
}
