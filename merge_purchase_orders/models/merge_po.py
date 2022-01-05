# -*- coding: utf-8 -*-

from odoo import models, fields, api


from odoo.exceptions import ValidationError


class MrpProductionInh(models.Model):
    _inherit = 'stock.picking'

    purchase_ids = fields.Many2many('purchase.order')
    merged_picking = fields.Char('Merged Pickings')
    picking_status = fields.Selection([
        ('single', 'Single'),
        ('merged', 'Merged')], string='Picking Status', default='single', tracking=True)
    state = fields.Selection(selection_add=[
        ('merge', 'Merged'),
    ], ondelete={'merge': 'cascade'})

    def action_open_wizard(self):
        selected_ids = self.env.context.get('active_ids', [])
        selected_records = self.env['stock.picking'].browse(selected_ids)
        line_vals = []
        names = []
        pickings = []
        if any(res.state == 'done' for res in selected_records) or len(selected_records.mapped('partner_id')) > 1:
            raise ValidationError('Pickings should not be Done state or partner must be same.')
        if selected_records and len(selected_records)>1:
            all_products = selected_records.move_line_ids_without_package.mapped('product_id') 
        

        
        
            line_val1=[]
            for record in selected_records:
                names.append(record.purchase_id.id)
                record.state = 'merge'
                pickings.append(record.name)
            my_string = ','.join(pickings)
                    
            for prd in all_products:
                prd_in_receipt =  selected_records.move_line_ids_without_package.filtered(lambda r,p=prd:r.product_id == p )
                product_rec = prd_in_receipt[0]
                demand_qty = sum(prd_in_receipt.mapped('product_uom_qty'))
                line_val1.append(
                    (0, 0, {
                    # 'picking_id': picking.id,
                    'product_id': product_rec.product_id.id,
                    'name': product_rec.product_id.name,
                    'product_uom': product_rec.product_id.uom_id.id,
                    'location_id': product_rec.location_id.id,
                    'location_dest_id': product_rec.location_dest_id.id,
                    'product_uom_qty': demand_qty,
                    'quantity_done': product_rec.move_id.quantity_done,
                })
                    
                    
            )
            
            
            
            
            
            return {
                'name': 'Requisition',
                'res_model': 'stock.picking',
                'views': [[False, "form"]],
                'type': 'ir.actions.act_window',
                'context': {'default_move_ids_without_package': line_val1,
                            'default_location_dest_id': selected_records[0].location_dest_id.id,
                            'default_location_id': selected_records[0].location_id.id,
                            'default_picking_type_id': selected_records[0].picking_type_id.id,
                            'default_partner_id': selected_records[0].partner_id.id,
                            'default_purchase_ids': names,
                            'default_picking_status': 'merged',
                            'default_merged_picking': my_string,
                            'default_request_date': fields.Date.today(),
                            'default_company_id': self.env.user.company_id.id}}

    # def action_open_wizard(self):
    #     selected_ids = self.env.context.get('active_ids', [])
    #     selected_records = self.env['stock.picking'].browse(selected_ids)
    #     purchase_list = []
    #     for rec in selected_records:
    #         purchase_list.append(rec.id)
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Merge Purchase Order',
    #         'view_id': self.env.ref('merge_purchase_orders.view_merge_purchase_wizard_form', False).id,
    #         'context': {'default_purchase_id': purchase_list},
    #         'target': 'new',
    #         'res_model': 'purchase.merge.wizard',
    #         'view_mode': 'form',
    #     }

