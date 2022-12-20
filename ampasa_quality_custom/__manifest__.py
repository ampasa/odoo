# -*- coding: utf-8 -*-
{
    'name': "ampasa_quality_custom",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "AMPASA",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','quality','quality_control','report_xlsx'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'wizard/quality_check_wizard_views.xml',
        'views/quality_check_view.xml',
        'views/quality_rejected_reason_view.xml',
        'views/quality_status_view.xml',
        'reports/quality_check_xlsx_report_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
