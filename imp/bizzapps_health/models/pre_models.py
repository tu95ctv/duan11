# -*- coding: utf-8 -*-

from odoo import models, fields, api
class AML(models.Model):
    _inherit = 'account.move.line'
    name = fields.Char()
    partner_id = fields.Many2one('res.partner')
    
# class ResPartner(models.Model):
#     _inherit = 'res.partner'
#     birthday = fields.Date()
#     customer_code = fields.Char()
#     district_id = fields.Many2one('res.country.district')



class HrEmployeePre(models.Model):
    _inherit = 'hr.employee'
    calendar_id = fields.Many2one('resource.calendar')
    city = fields.Char()
    last_login = fields.Datetime()
    login = fields.Char()
    name_related = fields.Char()
    resource_type = fields.Selection([('1','1')])
    time_efficiency = fields.Float()


class ProductProductPre(models.Model):
    _inherit = 'product.product'
    delivery_count = fields.Integer()
#     is_bed = fields.Boolean()
#     is_insurance_plan = fields.Boolean()
#     is_medical_supply = fields.Boolean()
#     is_medicine = fields.Boolean()
#     is_vaccine = fields.Boolean()
    property_account_creditor_price_difference = fields.Many2one('account.account')
    property_stock_procurement = fields.Many2one('stock.location')
    purchase_count = fields.Integer()
    purchase_line_warn = fields.Selection([('1','1')])
    purchase_line_warn_msg = fields.Text()
    purchase_method = fields.Selection([('1','1')])
    reception_count = fields.Integer()
    track_service = fields.Selection([('1','1')])
    warranty = fields.Float()


class ProductTemplatePre(models.Model):
    _inherit = 'product.template'
    is_bed = fields.Boolean()
    is_insurance_plan = fields.Boolean()
    is_medical_supply = fields.Boolean()
    is_medicine = fields.Boolean()
    is_vaccine = fields.Boolean()
#     is_bed = fields.Boolean()
#     is_insurance_plan = fields.Boolean()
#     is_medical_supply = fields.Boolean()
#     is_medicine = fields.Boolean()
#     is_vaccine = fields.Boolean()


class ResPartnerPre(models.Model):
    _inherit = 'res.partner'
    birthday = fields.Date()
    customer_code = fields.Char()
    district_id = fields.Many2one('res.country.district')
    estbday = fields.Date()
    fax = fields.Char()
    identify_card = fields.Char()
    is_doctor = fields.Boolean()
    is_institution = fields.Boolean()
    is_insurance_company = fields.Boolean()
    is_patient = fields.Boolean()
    is_person = fields.Boolean()
    is_pharmacy = fields.Boolean()
    issued_total = fields.Monetary(currency_field='property_purchase_currency_id')
    notify_email = fields.Selection([('1','1')])
    payment_next_action = fields.Text()
    payment_next_action_date = fields.Date()
    property_purchase_currency_id = fields.Many2one('res.currency')
    purchase_order_count = fields.Integer()
    purchase_warn = fields.Selection([('1','1')])
    purchase_warn_msg = fields.Text()
    supplier_invoice_count = fields.Integer()
    unreconciled_aml_ids = fields.One2many('account.move.line','partner_id')
    wards_id = fields.Many2one('res.country.wards')
    department = fields.Many2one('medical.health.center.ward')
    institution = fields.Many2one('medical.health.center')
    is_doctor = fields.Boolean()
    is_institution = fields.Boolean()
    is_insurance_company = fields.Boolean()
    is_patient = fields.Boolean()
    is_person = fields.Boolean()
    is_pharmacy = fields.Boolean()
    
    
    