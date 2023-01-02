from odoo import fields,models

class CrmLead(models.Model):
    _inherit = 'crm.lead'


    def action_sale_quotations_new_one(self):
        if not self.partner_id:
            return self.env["ir.actions.actions"]._for_xml_id("sale_crm.crm_quotation_partner_action")
        else:
            return self.action_new_quotation_new()

    def action_new_quotation_new(self):
        action = self.env["ir.actions.actions"]._for_xml_id("sale_crm.sale_action_quotations_new")
        enquiry_lines = []
        for products in self.enquiry_lines:
            approved_vendor = self.env['res.partner']
            supplier_currency = self.env['res.currency']
            supplier_po = ''
            approved_price = 0
            for each in products.supplier_name:
                pq_approved = self.purchase_ids.filtered(lambda a: a.po_state == 'approve' and a.partner_id == each)
                if pq_approved:
                    supplier_po = pq_approved.name
                    approved_vendor = self.purchase_ids.filtered(
                        lambda a: a.po_state == 'approve' and a.partner_id == each).partner_id.id
                    approved_price = sum(self.purchase_ids.filtered(
                        lambda a: a.po_state == 'approve' and a.partner_id == each).mapped(
                        'order_line').filtered(lambda a: a.product_id == products.product_id and a.name == products.description).mapped('price_unit'))
                    supplier_currency = self.purchase_ids.filtered(
                        lambda
                            a: a.po_state == 'approve' and a.partner_id == each).partner_id.property_purchase_currency_id.id

            if not approved_vendor:
                approved_vendor = products.supplier_name[0].id
                supplier_currency = products.supplier_name[0].property_purchase_currency_id.id
                approved_price = 0

            if products.partner_id:
                vendor_id = products.partner_id.id
            else:
                vendor_id = approved_vendor
            if products.approved_price != 0:
                approved_price = products.approved_price
            lines = (0, 0, {
                'categ_id': products.categ_id.id,
                'product_id': products.product_id.id,
                'iu_ref':products.product_id.product_tmpl_id.internal_unique_no,
                'name': products.description,
                'part_number_mfr': products.part_number_mfr,
                'part_number_one': products.part_number_one,
                'part_number_two': products.part_number_two,
                'c_mfr': products.c_mfr,
                'c_pn': products.c_pn,
                'on_hand': products.product_onhand_qty,
                'product_uom': products.product_uom.id,
                'supplier_currency': supplier_currency,
                'part_number': products.part_number,
                'price_unit': products.product_id.lst_price,
                'product_uom_qty': products.product_uom_qty,
                'supplier_po': supplier_po,
                # 'supplier': products.supplier_name.id,
                'supplier_new': vendor_id,
                # 'supplier_price': products.supplier_price,
                'supplier_price': approved_price,
                'supplier_price_new': approved_price,
                'availability': products.availability,
                'enquiry_line_id':products.id,
            })
            enquiry_lines.append(lines)
        action['context'] = {
            'search_default_opportunity_id': self.id,
            'default_opportunity_id': self.id,
            'search_default_partner_id': self.partner_id.id,
            'default_partner_id': self.partner_id.id,
            'default_team_id': self.team_id.id,
            'default_campaign_id': self.campaign_id.id,
            'default_medium_id': self.medium_id.id,
            'default_origin': self.name,
            'default_rig': self.rig,
            'default_customer_reference': self.customer_reference,
            'default_source_id': self.source_id.id,
            'default_company_id': self.company_id.id or self.env.company.id,
            'default_tag_ids': [(6, 0, self.tag_ids.ids)],
            'default_order_line': enquiry_lines
        }
        # for products in self.enquiry_lines:
        #     for each in products.supplier_name:
        #         pq_approved = self.purchase_ids.filtered(lambda a: a.po_state == 'approve' and a.partner_id == each)
        # for line in pq_approved.order_line:
        #     line.
        return action

