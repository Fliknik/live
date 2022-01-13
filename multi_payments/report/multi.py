from odoo import models, api, fields
from num2words import num2words


class multi_payments_report(models.Model):
    _name = 'report.multi_payments.multi_payments_report'
    _description = "Report"

    @api.model
    def _get_report_values(self, docids, data=None):
        record = self.env['multi.payments'].browse(docids)


        def number_to_spell(attrb):
            word = num2words((attrb))
            word = word.title() + " " + "Only"
            return word

        return {
            'doc_ids': docids,
            'doc_model': 'multi.payments',
            'docs': record,
            'data': data,
            'number_to_spell': number_to_spell,
            # 'company': company,
            # 'warehouse':warehouse,
            }

