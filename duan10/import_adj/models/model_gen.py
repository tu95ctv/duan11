from odoo import models, fields, api
import datetime
# from builtins import filter
from operator import itemgetter
from odoo.addons.base.ir.ir_ui_view import  View
from odoo.exceptions import UserError
import json
# import xmlrpc

MODULES = 'bizapps_medical'
MODULES = 'tour_travel'
    
NOT_IN =  ['__last_update', 'create_date', 'create_uid', 'display_name', 'id', 'write_date', 'write_uid','message_channel_ids','message_follower_ids','message_ids']

def convert_to_python_fields(name,ttype, relation,relation_field,related, relation_table):
#             ttype = db_field.ttype
#             tType = ttype.capitalize()
#             relation = db_field.relation # for m2o,m2m,o2m
#             relation_field = db_field.relation_field # for o2m
#             related = db_field.related
            ttype = ttype.capitalize()
            
            tType = 'fields.%s'%ttype
            
            alist = []
            if ttype =='Selection':
                alist.append("[('1','1')]")
            if relation:
                alist.append("'%s'"%relation)
            if relation_field:
                alist.append("'%s'"%relation_field)
            if related:
                alist.append("%s='%s'"%('related', related))
            if relation_table:
                alist.append("%s='%s'"%('relation', relation_table))
            argument = ', '.join(["%s"%x for x in alist])
            declare = '%s = %s(%s)'%(name, tType, argument)
            return declare
        
def gen_pre_declare_model(model_name, modelclass=None,name_or_inherit = '_name', fields_ids = [],add_mixin = False,):
    if not modelclass:
        modelclass =model_name.replace('.',' ').replace('_',' ')
        modelclass = modelclass.title().replace(' ','')
    class_declare = 'class %s(models.Model):'%modelclass
    pre =  class_declare + '\n\t'  + name_or_inherit  + ' = ' +  "'%s'"%model_name + '\n\t'
    
    if add_mixin and 'name' in name_or_inherit:
        pre+="_inherit = ['mail.thread', 'mail.activity.mixin']" + '\n\t' 
    if fields_ids:
        field_python_list = map(lambda f: convert_to_python_fields(f.name, f.ttype,
                                                                    getattr(f,'relation',None),getattr(f,'relation_field',None),
                                                                    getattr(f,'related',None),getattr(f,'relation_table',None)),fields_ids)
        pre +=  '\n\t'.join(field_python_list) +'\n\n'
    return pre


def escapse_xml(val):  
    return val.replace('&','&amp;')


class Gen():
    def __init__(self, env,app):
        self.env = env
        self.app = app
        pass
    
    template = '''<record id="%(id_char)s" model="ir.actions.act_window">
         <field name="name">%(name)s</field>
         <field name="res_model">%(res_model)s</field>
         <field name="view_type">%(view_type)s</field>
         <field name="view_mode">tree,form</field>
      </record>'''
    fieldlist = ['id_char', 'name', 'res_model', ('view_type',{'func':lambda v: v.lower()}), 'domain', 'context'  ]
    model = 'import_adj.action_import'
    @property
    def recs(self):
        recs = self.env[self.model].search([('id_char','=ilike','%s.%%'%self.app)])
        return recs
    
    def get_field_val_of_a_view_record (self, afield):
        if isinstance(afield, tuple):
            field_name  = afield[0]
            attrs = afield[1]
        else:
            field_name = afield
            attrs = {}
        func = attrs.get('func')
        no_escapse = attrs.get('no_escapse')
        field_template = attrs.get('field_template')
        val =  getattr(self.record, field_name)
        if not no_escapse:
            val = escapse_xml(str(val))
        if func:
            val = func(val)
        
        if field_template and val !='':
            val = field_template%val
            print ('akakakaka', (field_name,val))
        return (field_name, val)

    def gen_a_record_xml(self, record):
            self.record = record 
            rs = list(map(self.get_field_val_of_a_view_record, self.fieldlist))
            rs = dict(rs)
            print ("**context", rs)
            return self.template%rs
        
    def gen_xml_of_records(self):
        rs = map(self.gen_a_record_xml, self.recs)
        t2 = '''<odoo>
    <data>
    %s
    </data>
</odoo>'''
        va =t2% '\n'.join(rs)
        return va
        
        

class GenView(Gen):
#     def __init__(self, env):
#         self.env = env
#         pass
    
    template = '''<record id="%(id_char)s" model="ir.ui.view">
         <field name="name">%(name)s</field>
         <field name="model">%(model)s</field>
         <field name="type">%(type)s</field>%(inherit_id)s
         <field name="priority">%(priority)s</field>
         <field name="arch" type="xml">%(arch_db)s
         </field>
</record>'''
   
    
    
   
    @property
    def fieldlist(self):
        TYPE = [         ('tree', 'Tree'),
                             ('form', 'Form'),
                             ('graph', 'Graph'),
                             ('pivot', 'Pivot'),
                             ('calendar', 'Calendar'),
                             ('diagram', 'Diagram'),
                             ('gantt', 'Gantt'),
                             ('kanban', 'Kanban'),
                             ('search', 'Search'),
                             ('qweb', 'QWeb')]
        TYPE = [(i[1],i[0]) for i in TYPE]
        TYPE = dict(TYPE)
        
        def inherit_id_(v):
            tpl_inherit = '''<field name="inherit_id" ref="%s"/>
            '''
            v =  '' if (not v or v=='0' or v=='False') else tpl_inherit%v
            return v
        fieldlist1 = ['id_char', 'name', ('type',{'func':lambda v:TYPE[v]}), ('model',{'func':lambda v: '' if v =='False' else v}), ('priority',{'func':lambda v: int(float(v)) }),
                            ('inherit_id',{'func': inherit_id_}),('arch_db',{'no_escapse':True})]
        return fieldlist1
        
    model = 'import_adj.view_import'
 
class GenMenu(Gen):
    template = '''<menuitem id="%(id_char)s" name="%(name)s" %(parent_id)s %(action)s sequence="%(sequence)s"/>'''
    model = 'import_adj.menu_import'
    @property
    def fieldlist(self):
        fieldlist1 = ['id_char', 'name',('action',{'func':lambda v: '' if v =='False' else v, 'field_template':'`="%s"'}), ('sequence',{'func':lambda v: int(float(v))}),
                      ('parent_id',{'func':lambda v: '' if v =='False' else v, 'field_template':'parent="%s" '})]
        return fieldlist1
    

class Todo(models.Model):
    _name = 'import_adj.model_gen'
    pre_models = fields.Text()
    models = fields.Text()
    models_ids = fields.Many2many('ir.model')
    test2= fields.Text()
    test = fields.Text()
    
    module_inherits = fields.Char()
    relation_not_finds = fields.Char() 
    app = fields.Selection([('bizapps_medical','bizapps_medical'),('tour_travel','tour_travel')], default = 'bizapps_medical')
    def test_rpc(self):
        self.env['import_adj.model_import'].search([]).write ({'active':False})
#         rs = self.env['res.users'].search([('login','=','nguyenductu@gmail.com')])
#         kq =rs.password_crypt
#         raise UserError(kq)
#         
        
        
    def gen_related_model(self):
        read_group_fields_rs = self.env['import_adj.fields_import'].read_group([('field2_name', '=', u'!No exist')], ['field2','field1_model_name','relation','ttype', 'relation_table'], ['field2','field1_model_name','relation','ttype', 'relation_table'],lazy = False)
        for r in read_group_fields_rs:
            print (r)
        raise UserError(str(read_group_fields_rs))
    
    
    def related_deal(self):
        fields = self.env['import_adj.fields_import'].search([])
        for field in fields:
            related = field.related
            if related:
                s= related.split('.')
                field1, field2 = s[0],s[1]
                field.field2 = field2
       
    def related_deal_old(self):
        fields = self.env['import_adj.fields_import'].search([])
        for field in fields:
            related = field.related
            if related:
                print ('***related', related)
                s= related.split('.')
                field1, field2 = s[0],s[1]
                field.field2 = field2
                
                
                
                
                
                field1_obj = self.env['import_adj.fields_import'].search([('model_id','=', field.model_id),('name','=', field1)])\
                or self.env['ir.model.fields'].search([('model_id','=', field.model_look_sum),('name','=', field1)])
                
                if field1_obj:
                    field.field1_model_name = field1_obj.relation
                else:
                    field.field1_model_name = '! NFo field1'
                
                if field1_obj:
                    field1_model_obj = self.env['ir.model'].search([('model','=',field1_obj.relation)]) # model field 1 like res.partner
                    field2_obj = field1_model_obj and self.env['ir.model.fields'].search([('model_id','=',field1_model_obj.id),('name','=',field2)])\
                        or self.env['import_adj.fields_import'].search([('model_look_sum','=', field1_obj.relation),('name','=', field2)])
                if field2_obj:
                    field.field2_name = field2_obj.name
                else:
                    field.field2_name = u'!No exist'
                    
    def model_name_look(self):
#         model_name_look
        fields = self.env['import_adj.fields_import'].search([])
        module_inherits = []
        relation_not_finds = []
        for field in fields:
            model = field.model_id
            module,name = model.split('.')
            field.app_of_model = module# set
            model_look0 = self.env['import_adj.model_import'].search([('id_char','=',model)])
            
            model_name_look = None
            model_look1_name = None
            model_look2_name = None
            if model_look0:
                model_name_look = model_look0[0].model
                field.model_name_look = model_name_look
                is_inherit = False
            else:
                is_inherit = True
                if module not in module_inherits:
                    module_inherits.append(module)
                try:
                    model_look1  = self.env.ref(model)
                    model_look1_name = model_look1.model
                    field.model_look1 = model_look1_name
                except ValueError:
                    res_id_obj  = self.env['ir.model.data'].search([('model','=','ir.model'),(('name','=',name))])
                    if res_id_obj:
                        model_look2_obj = self.env['ir.model'].browse(res_id_obj[0].res_id)
                        model_look2_name = model_look2_obj.model
                        field.model_look2 = model_look2_name
                
            field.is_inherit = is_inherit
            field.model_look_sum = model_name_look or model_look1_name or model_look2_name
            if field.name not in NOT_IN:
                field.is_active = True
                
                
            ########## deal relation
            relation = field.relation
            if relation:
                model_id_obj = self.env['import_adj.model_import'].search([('model','=',relation)])
                if not model_id_obj:
                    model_id_obj = self.env['ir.model'].search([('model','=',relation)])
                
                if model_id_obj:
                    relation_search =   relation
                else:
                    relation_search = u'!relation No find'
                    if relation not in relation_not_finds:
                        relation_not_finds.append(relation)
                field.relation_search = relation_search
                
                
                
        self.module_inherits = module_inherits
        self.relation_not_finds = relation_not_finds
                    
           
                    
                    
                    
    def gen_menu(self):
        rs = GenMenu(self.env, self.app).gen_xml_of_records()
        self.test2 = rs
    def gen_view(self):
        rs = GenView(self.env, self.app).gen_xml_of_records()
        self.test2 = rs
    def gen_action(self):
        rs = Gen(self.env,self.app).gen_xml_of_records()
        self.test2 = rs
    #############1##################
    def find_model_name_from_model_read_group(self, read_group_rs):
        for i in read_group_rs:
            model_id = i['model_id']
            model_id_obj = self.env['import_adj.model_import'].search([('id_char','=',model_id)])
            if model_id_obj:
                modelclass = model_id_obj.model
                model_name = model_id_obj.model
                name_or_inherit = '_name'
            else:
                module_name, model_name = model_id.split('.')
                model_in_ir_model_data = self.env['ir.model.data'].search([('name','=',model_name)])
               
                if model_in_ir_model_data:
                    model_in_ir_model_data = model_in_ir_model_data[0]
                    model_name = self.env['ir.model'].browse(model_in_ir_model_data.res_id).model
                else:
                    raise UserError('model_name:%s NOT exits'%model_name)
                name_or_inherit = '_inherit'
                
            i['name_or_inherit']  = name_or_inherit
            modelclass = model_name.replace('.',' ').title()
            modelclass = modelclass.replace(' ','')
            i['modelclass'] = modelclass
            i['model_name']=model_name
        return read_group_rs   


    def gen_model_and_field(self):
        model_groups = self.env['import_adj.fields_import'].read_group([('modules','=ilike','%s'%self.app)], ['model_id'],['model_id'], lazy=False)
        self.find_model_name_from_model_read_group(model_groups)
        model_groups_adding_more_info = sorted(model_groups, key=itemgetter('name_or_inherit'))
        rt = ''
        for i in model_groups_adding_more_info:
            fields_ids = self.env['import_adj.fields_import'].search([('model_id','=',i['model_id']),('name','not in', NOT_IN)])
            name_or_inherit = i['name_or_inherit'] 
            modelclass = i['modelclass']
            model_name = i['model_name']
            modelclass = modelclass.replace(' ','').replace('.','')
            
            
#             class_declare = 'class %s(models.Model):'%modelclass
#             pre =  class_declare + '\n\t'  + name_or_inherit  + ' = ' +  "'%s'"%model_name + '\n\t'
#             
#             if 'name' in name_or_inherit:
#                 pre+="_inherit = ['mail.thread', 'mail.activity.mixin']" + '\n\t' 
#             field_python_list = map(lambda f: convert_to_python_fields(f.name, f.ttype, f.relation, f.relation_field, f.related),fields_ids)
#             pre += '\n\t'.join(field_python_list) +'\n\n'
#             
            pre = gen_pre_declare_model(model_name, modelclass,name_or_inherit, fields_ids, add_mixin = True)
            rt += pre
            
            
        self.test2 = rt
        
    def gen_declare_model_extend_inherit(self):
        class FieldObj:
            def __init__(self, **entries):
                self.__dict__.update(entries)
        fieldname = FieldObj(**{'name':'name','ttype':'Char'})
        c = '''['res.country.district', 'res.country.wards']'''
        c = c.replace("'",'"')
        rs = json.loads(c)
        def gen_pre_declare_model_default_fields(model_name):
            return gen_pre_declare_model(model_name, fields_ids=[fieldname])
        self.test2 = u'\n\n'.join(map(gen_pre_declare_model_default_fields, rs))

    def write(self,vals):
        print ('dung buon em hoi***********')
        rs = models.Model.write(self, vals)
        return rs
    
  