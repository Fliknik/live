from odoo import _, api, fields, models, modules, SUPERUSER_ID, tools
from odoo.exceptions import ValidationError, UserError
from odoo import http
import requests
import json
import xmltodict
from datetime import datetime, date


class Integration(models.TransientModel):
    _inherit = 'res.config.settings'

    revmax_port_number = fields.Char('Port Number')

    def set_values(self):
        res = super(Integration, self).set_values()
        self.env['ir.config_parameter'].set_param('revmax_connector.revmax_port_number', self.revmax_port_number)
        return res

    @api.model
    def get_values(self):
        res = super(Integration, self).get_values()
        icpsudo = self.env['ir.config_parameter'].sudo()
        revmax_port_number = icpsudo.get_param('revmax_connector.revmax_port_number')
        res.update(
            revmax_port_number=revmax_port_number
        )
        return res

    def getZreport(self):
        try:
            icpsudo = self.env['ir.config_parameter'].sudo()
            revmax_port_number = icpsudo.get_param('revmax_connector.revmax_port_number')
            headers = {
                'content-type': "application/json",
                'cache-control': "no-cache",
            }
            url = "http://revmax.local:{}/zreport/zreport".format(revmax_port_number)
            response = requests.request("GET", url, headers=headers)
            if response.status_code == 200:
                data = json.loads(response.text)['response']
                reportsData = data.split("#")[1]
                reports = xmltodict.parse(reportsData)['ZRESPONSE']['ZREPORT']
                for report in reports:
                    reportdate = datetime.strptime(report['DATE'], '%Y-%m-%d').date()
                    # regdate = datetime.strptime(report['REGISTRATIONDATE'], '%Y-%m-%d').date()
                    # currency = self.env['res.currency'].search([('display_name', '=', report['CURRENCY'])])
                    odooZReport = self.env['z.report'].search([('z_number', '=', report['Znumber'])])
                    if not odooZReport:
                        self.env['z.report'].create({
                            'date': reportdate,
                            'vat': report['VATNUM'],
                            'bpnumber': report['BPNUM'],
                            'tax_office': report['TAXOFFICE'],
                            'z_number': report['Znumber'],
                            'efd_serial': report['EFDSERIAL'],
                            'registration_date': report['REGISTRATIONDATE'],
                            'user': report['USER'],
                            'currency_id': report['CURRENCY'],
                            'dailytotal': report['TOTALS']['DAILYTOTALAMOUNT'],
                            'gross': report['TOTALS']['GROSS'],
                            'corrections': report['TOTALS']['CORRECTIONS'],
                            'discounts': report['TOTALS']['DISCOUNTS'],
                            'surcharges': report['TOTALS']['SURCHARGES'],
                            'ticketsvoid': report['TOTALS']['TICKETSVOID'],
                            'ticketsvoidtotal': report['TOTALS']['TICKETSVOIDTOTAL'],
                            'ticketsfiscal': report['TOTALS']['TICKETSFISCAL'],
                            'ticketsnonfiscal': report['TOTALS']['TICKETSNONFISCAL'],
                            'vatrate': report['VATTOTALS']['VATRATE'],
                            'netamount': report['VATTOTALS']['NETTAMOUNT'],
                            'taxamount': report['VATTOTALS']['TAXAMOUNT'],
                        })
                    else:
                        odooZReport.write({
                            'date': reportdate,
                            'vat': report['VATNUM'],
                            'bpnumber': report['BPNUM'],
                            'tax_office': report['TAXOFFICE'],
                            'z_number': report['Znumber'],
                            'efd_serial': report['EFDSERIAL'],
                            'registration_date': report['REGISTRATIONDATE'],
                            'user': report['USER'],
                            'currency_id': report['CURRENCY'],
                            'dailytotal': report['TOTALS']['DAILYTOTALAMOUNT'],
                            'gross': report['TOTALS']['GROSS'],
                            'corrections': report['TOTALS']['CORRECTIONS'],
                            'discounts': report['TOTALS']['DISCOUNTS'],
                            'surcharges': report['TOTALS']['SURCHARGES'],
                            'ticketsvoid': report['TOTALS']['TICKETSVOID'],
                            'ticketsvoidtotal': report['TOTALS']['TICKETSVOIDTOTAL'],
                            'ticketsfiscal': report['TOTALS']['TICKETSFISCAL'],
                            'ticketsnonfiscal': report['TOTALS']['TICKETSNONFISCAL'],
                            'vatrate': report['VATTOTALS']['VATRATE'],
                            'netamount': report['VATTOTALS']['NETTAMOUNT'],
                            'taxamount': report['VATTOTALS']['TAXAMOUNT'],
                        })

                self.env.cr.commit()
        except Exception as e:
            raise ValidationError(str(e))

    def getCardDetail(self):
        try:
            icpsudo = self.env['ir.config_parameter'].sudo()
            revmax_port_number = icpsudo.get_param('revmax_connector.revmax_port_number')
            headers = {
                'content-type': "application/json",
                'cache-control': "no-cache",
            }
            url = "http://revmax.local:{}/card/getcarddetails".format(revmax_port_number)
            response = requests.request("GET", url, headers=headers)
            if response.status_code == 200:
                data = json.loads(response.text)['response']
                odooCardDetail = self.env['card.detail'].search([('serialNumber', '=', data['serialNumber'])])
                if not odooCardDetail:
                    self.env['card.detail'].create({
                        'companyName': data['companyName'],
                        'addressLine1': data['addressLine1'],
                        'addressLine2': data['addressLine2'],
                        'addressLine3': data['addressLine3'],
                        'vatNumber': data['vatNumber'],
                        'registrationNumber': data['registrationNumber'],
                        'serialNumber': data['serialNumber'],
                        'BPNumber': data['BPNumber'],
                    })
                else:
                    odooCardDetail.write({
                        'companyName': data['companyName'],
                        'addressLine1': data['addressLine1'],
                        'addressLine2': data['addressLine2'],
                        'addressLine3': data['addressLine3'],
                        'vatNumber': data['vatNumber'],
                        'registrationNumber': data['registrationNumber'],
                        'serialNumber': data['serialNumber'],
                        'BPNumber': data['BPNumber'],
                    })
        except Exception as e:
            raise ValidationError(str(e))
