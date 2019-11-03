 # -*- coding: utf-8 -*-

from odoo.exceptions import UserError
# from odoo.addons.import_adj.
import re
NOT_IN =  ['__last_update', 'create_date', 'create_uid', 'display_name', 'id', 'write_date', 'write_uid','message_channel_ids','message_follower_ids','message_ids']

def convert_integer(val,needdata):
    try:
        return int(val)
    except:
        return 0
def int_catch_error_(v,n):
    try:
        v = int(v)
    except:
        v = False
    return v

def float_catch_error_(v,n):
    try:
        v = float(v)
    except:
        v = False
    return v

# def start_width_(v,n,self):
#     v = n['vof_dict']['id_char']['val']
#     try:
#         pt = '^%s'%self.app
#         rs  = re.search(pt, v)
#         return bool(rs)
#     except Exception as e:
#         e_notic='%s***********%s'%(e,e)
#         print (pt, v,e_notic)
#         raise ValueError (e_notic)

def initf(self):
    self.want = set(self.app.split('|'))
def is_concern_(v,n,self):
    modules = n['vof_dict']['modules']['val']
    want = self.want
    print ('want', want)
    try:
        modules = modules.split(', ')
        self.module_goc = modules[0]
        modules = set(modules)
    except Exception as e:
        raise ValueError(e)
    du = modules - want
    self.du = du
#     self.du = du
    is_concern = du < modules
    self.active = not du
    return is_concern
   
        
        
        

def start_width_(v,n,self):
    v = n['vof_dict']['id_char']['val']
    try:
        pt = '^%s'%self.app
        rs  = re.search(pt, v)
        return bool(rs)
    except Exception as e:
        e_notic='%s***********%s'%(e,e)
        print (pt, v,e_notic)
        raise ValueError (e_notic)
    
def fields_active_(v,n,self):
    v = n['vof_dict']['id_char']['val']
    fname = n['vof_dict']['name']['val']
    try:
        pt = '^%s'%self.app
        is_concer  = re.search(pt, v)
        is_concer =  bool(is_concer)
        not_in =  fname  in NOT_IN
        is_concer &=not not_in
        return is_concer
    except Exception as e:
        e_notic='%s***********%s'%(e,e)
        print (pt, v,e_notic)
        raise ValueError (e_notic)
    
        
# def active_ham_(v,n,s):
#     modules = n['vof_dict']['modules']['val']
#     print ('**************module*********',modules)
#     abcd =  ',' not in modules
#     print ("abcd",abcd)
# #     if not rs:
# #         raise UserError('akakak')
#     return abcd
# # app = 'bizapps_medical'
# # app = 'tour_travel'
def gen_dict():
    tvcv_dict = {
          u'fields_import': {
                'title_rows' : range(0,1), 
                'begin_data_row_offset_with_title_row' :1,
                'sheet_names':lambda self,wb: [wb.sheet_names()[0]],
                'model':'import_adj.fields_import',
                'offset_write_xl':1,
                'string':'TVCV da co chua',
                'fields' : [
                        ('id_char', {'xl_title':[u'id','External ID'], 'required':True, 'key':True }),
#                         ('start_width', {'required':True, 'for_excel_readonly':True,
#                                           'func': start_width_}),
                        ('name', {'xl_title':[u'name','Field Name'], 'required':True, 'key':True }),
                        ('active', {'write_false':True, 'default_val': False ,
                                          'func': fields_active_}), 
                        ('model_id', {'xl_title':[u'model_id/id','Model'], 'required':False, 'key':True }),
                        ('field_description', {'xl_title':u'field_description','allow_not_match_xl_title':True ,'required':False, 'key':False }),
                        ('ttype', {'xl_title':[u'ttype',u'Field Type'], 'required':False, 'key':True }),
                        ('readonly', {'xl_title':u'readonly', 'required':False, 'key':True }),
                        ('related', {'xl_title':[u'related','Related Field'], 'required':False, 'key':True }),
                        ('relation_field', {'xl_title':[u'relation_field',u'Relation field'], 'required':False, 'key':True }),
                        ('relation_table', {'xl_title':[u'relation_table',u'Relation table'], 'required':False, 'key':True }),
                        ('relation', {'xl_title':[u'relation',u'Object Relation'], 'required':False, 'key':True }),
                        ('modules', {'xl_title':[u'modules',u'In Apps'], 'required':False, 'key':True }),
                      ]
                },#End stock.inventory.line'   
                 
                 
             u'model_import': {
                'title_rows' : range(0,1), 
                'begin_data_row_offset_with_title_row' :1,
                'sheet_names':lambda self,wb: [wb.sheet_names()[0]],
                'model':'import_adj.model_import',
                'offset_write_xl':1,
                'string':'TVCV da co chua',
                'inactive_include_search':True,
                'initf':initf,
                'fields' : [
                    ('id_char', {'xl_title':[u'id',u'External ID'], 'required':True, 'key':True }),
                    ('modules', {'xl_title':[u'modules',u'Ở phân hệ',u'In Apps'], 'required':True, 'key':True }),
                    ('start_width', {'required':True, 'for_excel_readonly':True,
                                      'func':is_concern_}),
#                     ('start_width', {'required':True, 'for_excel_readonly':True, 'func': lambda v,n,self: n['vof_dict']['id_char']['val'].startswith(app) and ',' not in n['vof_dict']['modules']['val']}),
                    ('active', {'required':False,  'func': lambda v,n,self: self.active, 'key':False, 'write_false':True, 'default_val': False }),
                    ('module_goc', {'required':False,  'func': lambda v,n,self: self.module_goc, 'key':False, 'write_false':True, 'default_val': False }),
                    ('du', {'required':False,  'func': lambda v,n,self: self.du, }),
                    ('model', {'xl_title':[u'model',u'Mô hình',u'Model'], 'required':False, 'key':True }),
                    ('name', {'xl_title':[u'Model Description'], 'required':False, 'key':True }),
                    ('transient', {'xl_title':[u'transient',u'Transient Model'], 'required':False, 'key':True, 'allow_not_match_xl_title':True }),
                    
                      ]
                },#End stock.inventory.line'   
                 
            
            u'action_import': {
                'title_rows' : range(0,1), 
                'begin_data_row_offset_with_title_row' :1,
                'sheet_names':lambda self,wb: [wb.sheet_names()[0]],
                'model':'import_adj.action_import',
                'offset_write_xl':1,
                'string':'TVCV da co chua',
                'fields' : [
                    ('id_char', {'xl_title':u'id', 'required':True, 'key':True }),
                    ('start_width', {'required':True, 'for_excel_readonly':True, 'func': start_width_}),
                    ('name', {'xl_title':u'name', 'required':False, 'key':True }),
                    ('type', {'xl_title':u'type', 'required':False, 'key':True }),
                    ('usage', {'xl_title':u'usage', 'required':False, 'key':True }),
                    ('auto_search', {'xl_title':u'auto_search', 'required':False, 'key':True }),
                    ('context', {'xl_title':u'context', 'required':False, 'key':True }),
                    ('res_model', {'xl_title':u'res_model', 'required':False, 'key':True }),
                    ('domain', {'xl_title':u'domain', 'required':False, 'key':True }),
                    ('filter', {'xl_title':u'filter', 'required':False, 'key':True }),
                    ('limit', {'xl_title':u'limit', 'required':False, 'key':True }),
                    ('res_id', {'xl_title':u'res_id', 'required':False, 'key':True }),
                    ('multi', {'xl_title':u'multi', 'required':False, 'key':True }),
                    ('src_model', {'xl_title':u'src_model', 'required':False, 'key':True }),
                    ('target', {'xl_title':u'target', 'required':False, 'key':True }),
                    ('view_mode', {'xl_title':u'view_mode', 'required':False, 'key':True }),
                    ('view_type', {'xl_title':u'view_type', 'required':False, 'key':True }),

                      ]
                },#End stock.inventory.line'   
                 
            u'menu_import': {
                'title_rows' : range(0,1), 
                'begin_data_row_offset_with_title_row' :1,
                'sheet_names':lambda self,wb: [wb.sheet_names()[0]],
                'model':'import_adj.menu_import',
                'offset_write_xl':1,
                'string':'TVCV da co chua',
                'fields' : [
                    ('action', {'xl_title':u'action', 'required':False, 'key':True }),
                    ('id_char', {'xl_title':u'id', 'required':True, 'key':True }),
                    ('start_width', {'required':True, 'for_excel_readonly':True, 'func':start_width_}),
                    ('active', {'xl_title':u'active', 'key':True }),
                    ('name', {'xl_title':u'name', 'required':False, 'key':True }),
                    ('parent_left', {'xl_title':u'parent_left', 'required':False, 'key':True }),
                    ('parent_right', {'xl_title':u'parent_right', 'required':False, 'key':True }),
                    ('sequence', {'xl_title':u'sequence', 'required':False, 'key':True }),
                    ('parent_id', {'xl_title':u'parent_id/id', 'required':False, 'key':True }),



                      ]
                },#End stock.inventory.line'  
                 
                 
                 
                 
        u'view_import': {
                'title_rows' : range(0,1), 
                'begin_data_row_offset_with_title_row' :1,
                'sheet_names':lambda self,wb: [wb.sheet_names()[0]],
                'model':'import_adj.view_import',
                'offset_write_xl':1,
                'string':'TVCV da co chua',
                'fields' : [
                    ('id_char', {'xl_title':[u'External ID','id'], 'required':False, 'key':True }),
                    ('inherit_id', {'xl_title':[u'Inherited View old',u'inherit_id/id',u'Inherited View'], 'required':False, 'key':True }),
#                     ('inherit_id', {'xl_title':u'Inherited View gốc', 'required':False, 'key':True }),
                    ('start_width', {'required':True, 'for_excel_readonly':True, 'func': start_width_}),
                    ('model', {'xl_title':u'Model', 'required':False, 'key':True }),
                    ('priority', {'xl_title':u'Sequence', 'required':False, 'key':True }),
                    ('name', {'xl_title':[u'View Name','name'], 'required':False, 'key':True }),
                    ('type', {'xl_title':[u'View Type','type'], 'required':False, 'key':True }),
                    ('arch_db', {'xl_title':[u'Arch Blob gốc','arch_db',u'Arch Blob'], 'required':False, 'key':True }),
                    ('arch_fs', {'xl_title':[u'Arch Filename','arch_fs'], 'required':False, 'key':True }),
                    ('mode', {'xl_title':[u'View inheritance mode','mode'], 'required':False, 'key':True }),
                      ]
                },#End stock.inventory.line' 
                 
                 
                 
                 
                 
                 
                 
                      
                 
        
         
        }
    return tvcv_dict