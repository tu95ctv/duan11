# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResCountryDistrict(models.Model):
    _name = 'res.country.district'
    name = fields.Char()

class ResCountryWards(models.Model):
    _name = 'res.country.wards'
    name = fields.Char()



    
# 'account.move.line', related='partner_id.unreconciled_aml_ids')