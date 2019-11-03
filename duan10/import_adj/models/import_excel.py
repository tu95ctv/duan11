# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.addons.import_adj.models.import_dict import  gen_dict
# from odoo.addons.dai_tgg.models.import_excel_model_dict_folder.model_dict_user_department import  gen_user_department_model_dict

class ImportExcel(models.Model):
    _inherit = 'importexcel.importexcel' 
    app = fields.Char(compute = 'app_', store=True)
    single_app = fields.Selection([('bizapps_medical','bizapps_medical'),('tour_travel','tour_travel')], default = 'bizapps_medical')
    extend_app = fields.Char(default = 'bizapps_client_backend')
    @api.depends('single_app', 'extend_app')
    def app_(self):
        for r in self:
            r.app = r.single_app + ( '|' + r.extend_app) if r.extend_app else ''
            
    def gen_model_dict(self):
        rs = super(ImportExcel, self).gen_model_dict()
        rs.update(gen_dict())
#         rs.update(gen_user_department_model_dict())
        return rs