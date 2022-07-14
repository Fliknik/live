from odoo import fields, models, modules, SUPERUSER_ID, tools
from odoo.exceptions import ValidationError
import requests
import json
from lxml import etree


class InheritAM(models.Model):
    _inherit = 'account.move'

    invisible_button = fields.Boolean("Hide/Show Button", default=False)

    def sentInvoice(self):
        try:
            icpsudo = self.env['ir.config_parameter'].sudo()
            revmax_port_number = icpsudo.get_param('revmax_connector.revmax_port_number')
            # url = "http://revmax.local:{}/transactm/transactm".format(revmax_port_number)
            url = "http://45.32.128.52:{}/transactm/transactm".format(revmax_port_number)
            payload = {
                "Currency": self.currency_id.name,
                "BranchName": self.company_id.name,
                "InvoiceNumber": self.name.replace('/', ""),
                "CustomerName": self.partner_id.name,
                "CustomerVatNumber": self.partner_id.vat,
                "CustomerAddress": self.getAddress(),
                "CustomerTelephone": self.partner_id.phone,
                "CustomerBPN": self.partner_id.bpn,
                "InvoiceAmount": self.amount_total,
                "InvoiceTaxAmount": self.amount_tax,
                "Istatus": "01",
                "Cashier": self.user_id.name,
                "InvoiceComment": "Invoice",
                "ItemsXml": str(self.getItems()),
                "CurrenciesXml": str(self.getCurrency())
            }
            headers = {
                'content-type': "application/json",
                'cache-control': "no-cache",
            }
            invoiceNumber = self.name.replace('/', "")
            response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
            responseData = json.loads(response.text)['response']
            checkInvoiceNumber = responseData.split("#")
            if invoiceNumber in checkInvoiceNumber:
                self.invisible_button = True
        except Exception as e:
            raise ValidationError(str(e))

    def getAddress(self):
        street = self.partner_id.street if self.partner_id.street else ''
        street2 = self.partner_id.street2 if self.partner_id.street2 else ''
        city = self.partner_id.city if self.partner_id.city else ''
        state = self.partner_id.state_id.name if self.partner_id.state_id else ''
        country = self.partner_id.country_id.name if self.partner_id.country_id else ''
        return ' '.join([street, street2, city, state, country])

    def getItems(self):
        items = self.invoice_line_ids
        ITEMS = etree.Element("ITEMS")
        count = 0
        for item in items:
            tax, taxrate = self.calculateTaxAndTaxRate(item)
            count +=1
            ITEM = etree.SubElement(ITEMS, "ITEM")
            etree.SubElement(ITEM, "HH").text = str(++count)
            etree.SubElement(ITEM, "ITEMCODE").text = str(item.product_id.product_tmpl_id.default_code)
            etree.SubElement(ITEM, "ITEMNAME1").text = item.product_id.product_tmpl_id.rmFirstName1
            etree.SubElement(ITEM, "ITEMNAME2").text = item.product_id.product_tmpl_id.rmFirstName2
            etree.SubElement(ITEM, "QTY").text = str(item.quantity)
            etree.SubElement(ITEM, "PRICE").text = str(item.price_unit)
            etree.SubElement(ITEM, "AMT").text = str(item.price_total)
            etree.SubElement(ITEM, "TAX").text = tax
            etree.SubElement(ITEM, "TAXR").text = taxrate
        tree = etree.tostring(ITEMS, pretty_print=True)
        return tree.decode()

    def getCurrency(self):
        currencyRoot = etree.Element("CurrenciesReceived")
        currency = etree.SubElement(currencyRoot, "Currency")
        etree.SubElement(currency, "Name").text = self.currency_id.name
        etree.SubElement(currency, "Amount").text = str(self.amount_total)
        etree.SubElement(currency, "Rate").text = str(self.currency_id.rate)
        tree = etree.tostring(currencyRoot, pretty_print=True)
        return tree.decode()

    def calculateTaxAndTaxRate(self, item):
        taxes = item.tax_ids
        rate = 0
        for tax in taxes:
            rate += tax.amount
        totalTax = item.price_subtotal * (rate/100)
        return str(totalTax), str(rate)