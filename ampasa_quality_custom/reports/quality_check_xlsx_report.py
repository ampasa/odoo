# -*- encoding: utf-8 -*-
from odoo import models

class QualityCheckXlsxReport(models.AbstractModel):
    _name = 'report.ampasa_quality_custom.quality_check_xlsx_report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, recs):              
            # 
            sheet = workbook.add_worksheet("Rechazos")
            bold = workbook.add_format({'bold': True})
            normal = workbook.add_format({'bold': False})
            date_style = workbook.add_format({'text_wrap': True, 'num_format': 'dd-mm-yyyy'})
            
            # Encabezados
            sheet.write(0, 0, 'FOLIO', bold)
            sheet.write(0, 1, 'PO', bold)
            sheet.write(0, 2, 'FECHA DE RECHAZO', bold)
            sheet.write(0, 3, 'MPH', bold)
            sheet.write(0, 4, 'PROVEEDOR', bold)
            sheet.write(0, 5, 'PLANTA', bold)
            sheet.write(0, 6, 'NUM.PLANTA', bold)
            sheet.write(0, 7, 'ESTADO', bold)
            sheet.write(0, 8, 'CIUDAD', bold)
            sheet.write(0, 9, 'CANTIDAD DE RECHAZO', bold)
            sheet.write(0, 10, 'MOTIVO RECHAZO', bold)
            sheet.write(0, 11, 'CANTIDAD', bold)
            sheet.write(0, 12, 'ESTATUS', bold)

            # Para cada registro                        
            for i,check in enumerate(recs,start=1):
                # Contenido
                sheet.write(i, 0, check.name, normal)
                sheet.write(i, 1, check.purchase_id.name or '', normal)
                sheet.write(i, 2, check.rejected_date or '', date_style)
                sheet.write(i, 3, check.lot_id.name, normal)
                sheet.write(i, 4, check.partner_id.name or '', normal)
                sheet.write(i, 5, '', normal)
                sheet.write(i, 6, '', normal)
                sheet.write(i, 7, '', normal)
                sheet.write(i, 8, '', normal)
                sheet.write(i, 9, check.qty_tested, normal)
                sheet.write(i, 10, check.rejected_reason_id.name or '', normal)            
                sheet.write(i, 11, check.qty_line, normal)
                sheet.write(i, 12, check.rejected_status_id.name or '', normal)
