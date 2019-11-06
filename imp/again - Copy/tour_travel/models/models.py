# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CrmLead(models.Model):
    _inherit = 'crm.lead'
    product_id = fields.Many2one('product.template')
    tour_date_id = fields.Many2one('tour.date')

class CrmOpportunityReport(models.Model):
    _inherit = 'crm.opportunity.report'
    product_id = fields.Many2one('product.template')
    tour_date_id = fields.Many2one('tour.date')

# class StockQuant(models.Model):
#     _inherit = 'stock.quant'
class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    hotel_reservation_id = fields.Many2one('hotel.reservation')
    tour_date_id = fields.Many2one('tour.date')

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    tour_date_id = fields.Many2one('tour.date')

# class PurchaseOrderLine(models.Model):
#     _inherit = 'purchase.order.line'
class StockMove(models.Model):
    _inherit = 'stock.move'
    tour_date_id = fields.Many2one('tour.date')

class ResPartner(models.Model):
    _inherit = 'res.partner'
    is_hotel = fields.Boolean()
    is_transport = fields.Boolean()
    partner_id = fields.Char()
    passport_number = fields.Char()
    passport_isue_date = fields.Date()
    date_of_birth = fields.Date()
    passport_expiry_date = fields.Date()
    passport_ids = fields.One2many('passport', 'partner_id')
    tour_date_ids = fields.One2many('tour.attendee', 'partner_id')
    gender = fields.Selection([('1','1')])

# class ProductProduct(models.Model):
#     _inherit = 'product.product'
#     transport_ids = fields.One2many('tour.transport', related='product_tmpl_id.transport_ids')
#     tour_type = fields.Many2one('tour.type', related='product_tmpl_id.tour_type')
#     tour_program_ids = fields.One2many('tour.program.line', related='product_tmpl_id.tour_program_ids')
#     tour_destination_ids = fields.One2many('tour.destination', related='product_tmpl_id.tour_destination_ids')
#     specific = fields.Selection([('1','1')], related='product_tmpl_id.specific')
#     product_ids = fields.One2many('tour.product', related='product_tmpl_id.product_ids')
#     hotel_ids = fields.One2many('tour.destination.hotel', related='product_tmpl_id.hotel_ids')
#     duration = fields.Integer(related='product_tmpl_id.duration')
#     departure = fields.Many2one('destination', related='product_tmpl_id.departure')

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    duration = fields.Integer()
    departure = fields.Many2one('destination')
    tour_type = fields.Many2one('tour.type')
    tour_program_ids = fields.One2many('tour.program.line', 'tour_id')
    hotel_ids = fields.One2many('tour.destination.hotel', 'tour_id')
    product_ids = fields.One2many('tour.product', 'tour_id')
    transport_ids = fields.One2many('tour.transport', 'tour_id')
    tour_destination_ids = fields.One2many('tour.destination', 'tour_id')
    specific = fields.Selection([('tour','tour')])

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    is_tour_booking = fields.Boolean()
    attendee_count = fields.Integer()
    tour_date_id = fields.Many2one('tour.date')
    visa_booking_id = fields.Many2one('visa.booking')
    passport_booking_id = fields.Many2one('passport.booking')
    tour_id = fields.Many2one('product.template')
    tour_attendee_ids = fields.One2many('tour.attendee', 'sale_order_id')
    book_date = fields.Datetime(related='tour_date_id.book_date')

class AccountMove(models.Model):
    _inherit = 'account.move'
    tour_date_id = fields.Many2one('tour.date')

# class MailComposeMessage(models.Model):
#     _inherit = 'mail.compose.message'
class IrAttachment(models.Model):
    _inherit = 'ir.attachment'
    document_type_id = fields.Many2one('document.type')
    passport_booking_id = fields.Many2one('passport.booking')
    visa_booking_id = fields.Many2one('visa.booking')

class HotelHotel(models.Model):
    _name = 'hotel.hotel'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    hotel_img3 = fields.Binary()
    hotel_img1 = fields.Binary()
    hotel_img2 = fields.Binary()
    partner_id = fields.Many2one('res.partner')
    hotel_class_id = fields.Many2one('hotel.class')
    hotel_service_ids = fields.One2many('hotel.service', 'hotel_id')
    hotel_room_ids = fields.One2many('hotel.room', 'hotel_id')
    name = fields.Char(related='partner_id.name')

class HotelReservation(models.Model):
    _name = 'hotel.reservation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    name = fields.Char()
    supplier_ref = fields.Char()
    date_order = fields.Datetime()
    amount_untaxed = fields.Float()
    amount_total = fields.Float()
    amount_tax = fields.Float()
    tour_date_id = fields.Many2one('tour.date')
    user_id = fields.Many2one('res.users')
    hotel_id = fields.Many2one('hotel.hotel')
    company_id = fields.Many2one('res.company')
    currency_id = fields.Many2one('res.currency')
    pricelist_id = fields.Many2one('product.pricelist')
    purchase_order_ids = fields.One2many('purchase.order', 'hotel_reservation_id')
    reservation_line = fields.One2many('hotel.reservation.line', 'hotel_reservation_id')
    state = fields.Selection([('1','1')])
    notes = fields.Text()
    invoice_ids = fields.Many2many('account.invoice', related='purchase_order_ids.invoice_ids')

class PassportBooking(models.Model):
    _name = 'passport.booking'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    name = fields.Char()
    passport_number = fields.Char()
    issue_date = fields.Date()
    expiry_date = fields.Date()
    current_date = fields.Date()
    price = fields.Float()
    holder_id = fields.Many2one('res.partner')
    customer_id = fields.Many2one('res.partner')
    currency_id = fields.Many2one('res.currency')
    product_id = fields.Many2one('product.product')
    user_id = fields.Many2one('res.users')
    pricelist_id = fields.Many2one('product.pricelist')
    attachment_ids = fields.One2many('ir.attachment', 'passport_booking_id')
    document_ids = fields.One2many('passport.booking.document', 'passport_booking_id')
    sale_order_ids = fields.One2many('sale.order', 'passport_booking_id')
    state = fields.Selection([('1','1')])
    invoice_ids = fields.Many2many('account.invoice', related='sale_order_ids.invoice_ids')
    mobile = fields.Char(related='customer_id.mobile')
    email = fields.Char(related='customer_id.email')

class TourDate(models.Model):
    _name = 'tour.date'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    name = fields.Char()
    book_date = fields.Datetime()
    end_date = fields.Datetime()
    start_date = fields.Datetime()
    cost_revenue = fields.Float()
    tour_quotation_count = fields.Integer()
    oppor_count = fields.Integer()
    duration = fields.Integer()
    tour_booking_count = fields.Integer()
    attendee_count = fields.Integer()
    available_seat = fields.Integer()
    total_seat = fields.Integer()
    rfq_count = fields.Integer()
    lead_count = fields.Integer()
    purchase_order_count = fields.Integer()
    tour_type = fields.Many2one('tour.type')
    analytic_account_id = fields.Many2one('account.analytic.account')
    tour_id = fields.Many2one('product.template')
    tour_date_transport_ids = fields.One2many('tour.date.transport', 'tour_date_id')
    tour_date_product_ids = fields.One2many('tour.date.product', 'tour_date_id')
    oppor_ids = fields.One2many('crm.lead', 'tour_date_id')
    tour_quotation_ids = fields.One2many('sale.order', 'tour_date_id')
    tour_date_destination_ids = fields.One2many('tour.date.destination', 'tour_date_id')
    purchase_order_ids = fields.One2many('purchase.order', 'tour_date_id')
    tour_date_hotel_ids = fields.One2many('tour.date.destination.hotel', 'tour_date_id')
    lead_ids = fields.One2many('crm.lead', 'tour_date_id')
    tour_booking_ids = fields.One2many('sale.order', 'tour_date_id')
    tour_variant_ids = fields.One2many('tour.date.product.variant', 'tour_date_id')
    rfq_ids = fields.One2many('purchase.order', 'tour_date_id')
    tour_date_program_ids = fields.One2many('tour.date.program.line', 'tour_date_id')
    state = fields.Selection([('1','1')])
    description = fields.Text()

class Transport(models.Model):
    _name = 'transport'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    partner_id = fields.Many2one('res.partner')
    transport_line = fields.One2many('transport.line', 'transport_id')
    name = fields.Char(related='partner_id.name')

class VisaBooking(models.Model):
    _name = 'visa.booking'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    name = fields.Char()
    visa_number = fields.Char()
    issue_date = fields.Date()
    current_date = fields.Date()
    expiry_date = fields.Date()
    price = fields.Float()
    visa_type_id = fields.Many2one('visa.type')
    user_id = fields.Many2one('res.users')
    currency_id = fields.Many2one('res.currency')
    country_id = fields.Many2one('res.country')
    customer_id = fields.Many2one('res.partner')
    holder_id = fields.Many2one('res.partner')
    pricelist_id = fields.Many2one('product.pricelist')
    passport_id = fields.Many2one('passport')
    product_id = fields.Many2one('product.product')
    document_ids = fields.One2many('visa.booking.document', 'visa_booking_id')
    sale_order_ids = fields.One2many('sale.order', 'visa_booking_id')
    attachment_ids = fields.One2many('ir.attachment', 'visa_booking_id')
    state = fields.Selection([('1','1')])
    invoice_ids = fields.Many2many('account.invoice', related='sale_order_ids.invoice_ids')
    mobile = fields.Char(related='customer_id.email')
    email = fields.Char(related='customer_id.email')

class DocumentType(models.Model):
    _name = 'document.type'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    name = fields.Char()
    description = fields.Text()

class HotelClass(models.Model):
    _name = 'hotel.class'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    description = fields.Char()
    name = fields.Char()

class HotelReservationLine(models.Model):
    _name = 'hotel.reservation.line'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    check_out_date = fields.Date()
    check_in_date = fields.Date()
    price = fields.Float()
    no_of_day = fields.Integer()
    no_of_room = fields.Integer()
    tax_ids = fields.Many2many('account.tax', relation='account_tax_hotel_reservation_line_rel')
    hotel_reservation_id = fields.Many2one('hotel.reservation')
    product_id = fields.Many2one('product.product')
    price_subtotal = fields.Monetary()
    price_total = fields.Monetary()
    price_tax = fields.Monetary()
    name = fields.Text()
    currency_id = fields.Many2one('res.currency', related='hotel_reservation_id.currency_id')

class HotelRoom(models.Model):
    _name = 'hotel.room'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    description = fields.Char()
    cost_price = fields.Float()
    sale_price = fields.Float()
    room_type_id = fields.Many2one('product.product')
    hotel_id = fields.Many2one('hotel.hotel')
    name = fields.Char(related='room_type_id.name')

class HotelService(models.Model):
    _name = 'hotel.service'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    description = fields.Char()
    cost_price = fields.Float()
    service_id = fields.Many2one('product.product')
    hotel_id = fields.Many2one('hotel.hotel')
    product_uom = fields.Many2one('product.uom')

class Passport(models.Model):
    _name = 'passport'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    image_medium = fields.Binary()
    image_small = fields.Binary()
    image = fields.Binary()
    name = fields.Char()
    issue_date = fields.Date()
    expiry_date = fields.Date()
    passport_booking_id = fields.Many2one('passport.booking')
    partner_id = fields.Many2one('res.partner')
    visa_ids = fields.One2many('visa', 'passport_id')
    state = fields.Selection([('1','1')])

class PassportBookingDocument(models.Model):
    _name = 'passport.booking.document'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    name = fields.Char()
    original_copy = fields.Integer()
    passport_booking_id = fields.Many2one('passport.booking')
    tour_document_type_id = fields.Many2one('document.type')

class ReportAttendeeDeclaration(models.Model):
    _name = 'report.attendee.declaration'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    is_ascii = fields.Boolean()
    partner_ids = fields.Many2many('res.partner', relation='report_attendee_declaration_rel')

# class ReportTour_TravelReport_Attendee_Declaration(models.Model):
#     _name = 'report.tour_travel.report_attendee_declaration'
#     _inherit = ['mail.thread', 'mail.activity.mixin']
class TourAttendee(models.Model):
    _name = 'tour.attendee'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    sale_order_id = fields.Many2one('sale.order')
    partner_id = fields.Many2one('res.partner')
    name = fields.Char(related='tour_date_id.name')
    tour_date_id = fields.Many2one('tour.date', related='sale_order_id.tour_date_id')
    attendee_id = fields.Char(related='partner_id.partner_id')
    gender = fields.Selection([('1','1')], related='partner_id.gender')
    date_of_birth = fields.Date(related='partner_id.date_of_birth')

class TourDateDestination(models.Model):
    _name = 'tour.date.destination'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    days = fields.Integer()
    tour_date_id = fields.Many2one('tour.date')
    destination_id = fields.Many2one('destination')
    hotel_ids = fields.One2many('tour.date.destination.hotel', 'tour_date_destination_id')
    state_id = fields.Many2one('res.country.state', related='destination_id.state_id')
    name = fields.Char(related='destination_id.name')
    country_id = fields.Many2one('res.country', related='destination_id.country_id')
    city = fields.Char(related='destination_id.city')

class TourDateDestinationHotel(models.Model):
    _name = 'tour.date.destination.hotel'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    auto_booking = fields.Boolean()
    days = fields.Integer()
    hotel_class_id = fields.Many2one('hotel.class')
    hotel_id = fields.Many2one('hotel.hotel')
    tour_date_destination_id = fields.Many2one('tour.date.destination')
    tour_date_id = fields.Many2one('tour.date')
    room_id = fields.Many2one('hotel.room')

class TourDateProduct(models.Model):
    _name = 'tour.date.product'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    product_uom_qty = fields.Float()
    product_id = fields.Many2one('product.product')
    tour_date_id = fields.Many2one('tour.date')
    name = fields.Text()
    product_uom = fields.Many2one('product.uom', related='product_id.product_tmpl_id.uom_id')

class TourDateProductVariant(models.Model):
    _name = 'tour.date.product.variant'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    price = fields.Float()
    qty_booked = fields.Integer()
    product_id = fields.Many2one('product.product')
    tour_date_id = fields.Many2one('tour.date')
    uom_id = fields.Many2one('product.uom')
    name = fields.Text()

class TourDateProgramLine(models.Model):
    _name = 'tour.date.program.line'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    day = fields.Integer()
    tour_date_id = fields.Many2one('tour.date')
    tour_program_id = fields.Many2one('tour.program')
    lunch = fields.Boolean(related='tour_program_id.lunch')
    dinner = fields.Boolean(related='tour_program_id.dinner')
    breakfast = fields.Boolean(related='tour_program_id.breakfast')

class TourDateTransport(models.Model):
    _name = 'tour.date.transport'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    product_name = fields.Char()
    time = fields.Float()
    distance = fields.Float()
    carrier_line = fields.Many2one('product.product')
    transport_id = fields.Many2one('transport')
    carrier_id = fields.Many2one('transport.line')
    to_destination = fields.Many2one('destination')
    tour_date_id = fields.Many2one('tour.date')
    from_destination = fields.Many2one('destination')

class TourDestination(models.Model):
    _name = 'tour.destination'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    days = fields.Integer()
    destination_id = fields.Many2one('destination')
    tour_id = fields.Many2one('product.template')
    hotel_ids = fields.One2many('tour.destination.hotel', 'tour_destination_id')
    state_id = fields.Many2one('res.country.state', related='destination_id.state_id')
    name = fields.Char(related='destination_id.name')
    country_id = fields.Many2one('res.country', related='destination_id.country_id')
    city = fields.Char(related='destination_id.city')

class Destination(models.Model):
    _name = 'destination'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    name = fields.Char()
    code = fields.Char()
    city = fields.Char()
    country_id = fields.Many2one('res.country')
    state_id = fields.Many2one('res.country.state')

class TourDestinationHotel(models.Model):
    _name = 'tour.destination.hotel'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    auto_booking = fields.Boolean()
    days = fields.Integer()
    tour_id = fields.Many2one('product.template')
    hotel_class_id = fields.Many2one('hotel.class')
    hotel_id = fields.Many2one('hotel.hotel')
    room_id = fields.Many2one('hotel.room')
    tour_destination_id = fields.Many2one('tour.destination')

class TourProduct(models.Model):
    _name = 'tour.product'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    product_uom_qty = fields.Float()
    product_id = fields.Many2one('product.product')
    tour_id = fields.Many2one('product.template')
    name = fields.Text()
    product_uom = fields.Many2one('product.uom', related='product_id.product_tmpl_id.uom_id')

class TourProgram(models.Model):
    _name = 'tour.program'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    image_small = fields.Binary()
    image = fields.Binary()
    image_medium = fields.Binary()
    lunch = fields.Boolean()
    dinner = fields.Boolean()
    breakfast = fields.Boolean()
    name = fields.Char()
    description = fields.Html()

class TourProgramLine(models.Model):
    _name = 'tour.program.line'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    day = fields.Integer()
    tour_id = fields.Many2one('product.template')
    tour_program_id = fields.Many2one('tour.program')
    lunch = fields.Boolean(related='tour_program_id.lunch')
    dinner = fields.Boolean(related='tour_program_id.dinner')
    breakfast = fields.Boolean(related='tour_program_id.breakfast')

class TourTransport(models.Model):
    _name = 'tour.transport'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    product_name = fields.Char()
    distance = fields.Float()
    time = fields.Float()
    transport_id = fields.Many2one('transport')
    tour_id = fields.Many2one('product.template')
    carrier_line = fields.Many2one('product.product')
    to_destination = fields.Many2one('destination')
    carrier_id = fields.Many2one('transport.line')
    from_destination = fields.Many2one('destination')

class TourType(models.Model):
    _name = 'tour.type'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    name = fields.Char()

class TransportCarrierLine(models.Model):
    _name = 'transport.carrier.line'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    description = fields.Char()
    cost_price = fields.Float()
    sale_price = fields.Float()
    product_id = fields.Many2one('product.product')
    transport_line_id = fields.Many2one('transport.line')
    name = fields.Char(related='product_id.name')

class TransportLine(models.Model):
    _name = 'transport.line'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    transport_carrier_id = fields.Many2one('res.partner')
    transport_id = fields.Many2one('transport')
    carrier_line = fields.One2many('transport.carrier.line', 'transport_line_id')
    name = fields.Char(related='transport_carrier_id.name')

class Visa(models.Model):
    _name = 'visa'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    visa_img = fields.Binary()
    name = fields.Char()
    issue_date = fields.Date()
    expiry_date = fields.Date()
    type_id = fields.Many2one('visa.type')
    visa_booking_id = fields.Many2one('visa.booking')
    country_id = fields.Many2one('res.country')
    passport_id = fields.Many2one('passport')
    partner_id = fields.Many2one('res.partner')
    state = fields.Selection([('1','1')])

class VisaBookingDocument(models.Model):
    _name = 'visa.booking.document'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    name = fields.Char()
    original_copy = fields.Integer()
    tour_document_type_id = fields.Many2one('document.type')
    visa_booking_id = fields.Many2one('visa.booking')

class VisaType(models.Model):
    _name = 'visa.type'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    name = fields.Char()
    duration = fields.Integer()



