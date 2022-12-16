# -*- encoding: utf-8 -*-
{
    "name" : 'CFDI Bóveda fiscal',
    'license': 'GPL-3',
    "version" : '15',
    "author" : '...',
    "category" : '',
    "website" : "",
    "description" : """
            Este módulo ...
    """,
    "init_xml" : [],
    "depends" : ['base','account'],
    "data" : [                  
        'security/ir.model.access.csv',
        'views/cfdi_download_request_view.xml',
        'views/cfdi_download_fiel_view.xml',       
        'views/cfdi_download_pack_view.xml',
        'views/cfdi_download_data_view.xml',
        'wizard/request_wizard_view.xml',                        
        'reports/pack_qweb_report_view.xml',                        
    ],
    "demo_xml":[],
    "test":[],
    "installable": True,
    "images": [],
    "auto_install": False,
}
