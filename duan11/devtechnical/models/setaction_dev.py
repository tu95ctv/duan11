# -*- coding: utf-8 -*-
from odoo import models, fields, api,exceptions,tools,_
from odoo.exceptions import UserError
import os.path
import base64

def return_form_action(self):
    return {
                'type': 'ir.actions.act_window',
                'res_model': 'setaction.setaction',
                'view_mode': 'form',
                'view_type': 'form',
                'res_id': self.id,
#                 'context':{'active_model':self.model, 'function_key': self.function_key},
                'views': [(False, 'form')],
                'target': 'new',
            }
def return_form_action_decorator(func):
    def wrapper(*args,**kargs):
        self = args[0]
        func(*args,**kargs)
        return return_form_action(self)
    return wrapper

class Setaction(models.TransientModel):
    _inherit = "setaction.setaction"
    
    
    @api.multi
    @return_form_action_decorator
    def set_depends_is_trig(self):
#         active_ids = self._context.get('active_ids')
#         raise UserError(str(self._context).get('active_model'))
        active_ids = self.env[self._context.get('active_model')].search([])
        self.choosed_object_qty = len(active_ids)
        active_ids.write({'is_trig':True})
#             affected_count = 0
#             for r in self.env['cvi'].browse(active_ids):
#                     r.copy()
#                     affected_count +=1
#             self.affected_object_qty = affected_count
#         else:
#             raise UserError (u'Bạn chưa chọn dòng nào')
        return return_form_action(self)
    
#     
#     @api.multi
#     @return_form_action_decorator
#     def auto_create_import_user(self):
#         active_ids = self._context.get('active_ids')
#         self.choosed_object_qty = len(active_ids)
#         if active_ids:
# #             
#             yourpath = __file__
#             
#             al = [{'key':'User', 'file_name':'Tel-mail-VTHCM-10-2017 gon.xls'}, {'key':u'Thư viện công việc', 'file_name':'01072019_Thu_vien_cong_viec_Dai_HCM_T06.xlsx'}]
#             for adict in al:
#                 print (os.path, os.pardir,type(os.pardir),type(os.path))
# #                 file_name = 'Tel-mail-VTHCM-10-2017 gon.xls'
#                 file_name =adict['file_name']
#                 key = adict['key']
#                 pr =  os.path.abspath(os.path.join(yourpath, os.pardir, os.pardir, os.pardir,'file_import', file_name))
#                 file = open(pr, "rb")
#                 out = file.read()
#                 file.close()
#                 gentextfile = base64.b64encode(out)
#                 self.env['importexcel.importexcel'].create({'import_key':key, 'file':gentextfile, 'filename':file_name})
#          
#         else:
#             raise UserError (u'Bạn chưa chọn dòng nào')
# #         return return_form_action(self)
#     
#     
#     
#     @api.multi
#     @return_form_action_decorator
#     def multi_confirmed(self):
#         active_ids = self._context.get('active_ids')
#         self.choosed_object_qty = len(active_ids)
#         if active_ids:
#             affected_count = 0
#             for r in self.env['cvi'].browse(active_ids):
#                 if r.state in ['draft'] and not r.cam_sua:
#                     affected_count +=1
#                     r.state = 'confirmed'
#             self.affected_object_qty = affected_count
#         else:
#             raise UserError (u'Bạn chưa chọn dòng nào')
#         return return_form_action(self)
#         
#     @api.multi
#     @return_form_action_decorator
#     def multi_approved(self):
#         active_ids = self._context.get('active_ids')
#         self.choosed_object_qty = len(active_ids)
#         if active_ids:
#             affected_count = 0
#             for r in self.env['cvi'].browse(active_ids):
#                 if r.is_sep and r.state in ['confirmed']:
#                     affected_count +=1
#                     r.state = 'approved'
#                 else:
#                     raise UserError (u'Bạn không phải là lãnh đạo của nhân viên tạo record này hoặc trạng thái chưa phải là confirm')
#             self.affected_object_qty = affected_count
#         else:
#             raise UserError (u'Bạn chưa chọn dòng nào')
#         return return_form_action(self)
#     @api.multi
#     @return_form_action_decorator
#     def multi_draft(self):
#         active_ids = self._context.get('active_ids')
#         self.choosed_object_qty = len(active_ids)
#         if active_ids:
#             affected_count = 0
#             for r in self.env['cvi'].browse(active_ids):
#                 state = r.state
#                 if (state in ['mark_delete','confirmed'] and  not r.cam_sua_do_diff_user) or (state =='approved' and r.is_sep) :
#                     affected_count +=1
#                     r.state = 'draft'
#             self.affected_object_qty = affected_count
#         else:
#             raise UserError (u'Bạn chưa chọn dòng nào')
# #         return return_form_action(self)
#     @api.multi
#     @return_form_action_decorator
#     def multi_mark_delete(self):
#         active_ids = self._context.get('active_ids')
#         self.choosed_object_qty = len(active_ids)
#         if active_ids:
#             affected_count = 0
#             for r in self.env['cvi'].browse(active_ids):
#                 state = r.state
#                 if state in ['draft'] and not r.cam_sua_do_diff_user:
#                     affected_count +=1
#                     r.state = 'mark_delete'
#             self.affected_object_qty = affected_count
#         else:
#             raise UserError (u'Bạn chưa chọn dòng nào')
# 
#         