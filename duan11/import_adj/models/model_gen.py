from odoo import models, fields, api
import datetime
# from builtins import filter
from operator import itemgetter
from odoo.addons.base.ir.ir_ui_view import  View
from odoo.exceptions import UserError
import json
import os
import errno
import re
# import xmlrpc

MODULES = 'bizapps_medical'
MODULES = 'tour_travel'
    
NOT_IN =  ['__last_update', 'create_date', 'create_uid', 'display_name', 'id', 'write_date', 'write_uid','message_channel_ids','message_follower_ids','message_ids']
# TYPE = [         ('tree', 'Tree'),
#                              ('form', 'Form'),
#                              ('graph', 'Graph'),
#                              ('pivot', 'Pivot'),
#                              ('calendar', 'Calendar'),
#                              ('diagram', 'Diagram'),
#                              ('gantt', 'Gantt'),
#                              ('kanban', 'Kanban'),
#                              ('search', 'Search'),
#                              ('qweb', 'QWeb')]
# TYPE = [(i[1],i[0]) for i in TYPE]
# TYPE = dict(TYPE)


def domain_(v):
    v = '[]' if (v =='{}' or v =='[]' or v =='False') else v
    return v
#     if v:
#         raise UserError('akakka')
#     v = 'abc' if (v =='False' or '[]' or '{}') else v
#     print ('in domain_***', v)
#     if v :
#         raise UserError(str(v))
    return v

def context_(v):
    v = '{}' if (v =='{}' or v =='[]' or v =='False') else v
    return v
#     if v:
#         raise UserError('akakka')
#     v = 'abc' if (v =='False' or '[]' or '{}') else v
#     print ('in domain_***', v)
#     if v :
#         raise UserError(str(v))
    return v


def escapse_xml(val):  
    return val.replace('&','&amp;')


class Gen():
    def __init__(self, env,app, self_gen_model):
        self.env = env
        self.app = app
        self.self_gen_model = self_gen_model
        begin_func = getattr(self, 'begin_func')
        if begin_func:
            begin_func()
        
        pass
    
    template = '''<record id="%(id_char)s" model="ir.actions.act_window">
         <field name="name">%(name)s</field>
         <field name="res_model">%(res_model)s</field>
         <field name="view_type">%(view_type)s</field>
         <field name="view_mode">%(view_mode)s</field>
         %(src_model)s%(target)s%(multi)s%(view_id)s%(search_view_id)s%(domain)s%(context)s </record>
      '''
   
    @property
    def fieldlist(self):
        fieldlist = ['id_char', 'name', 'res_model', ('view_type',{'func':lambda v: v.lower()}),'view_mode',
                     ('src_model',{'field_template':'        <field name="src_model">%s</field>\n', 'func':lambda v: '' if not v or v =='False' else v}),
                     ('target',{'field_template':'        <field name="target">%s</field>\n', 'func':lambda v: 'new' if v=='New Window' else ''}),
                     ('multi',{'field_template':'        <field name="multi">%s</field>\n', 'func_complete':lambda v,self: True if self.rec.src_model else ''}),
                     ('view_id', {'field_template':'<field name="view_id" ref ="%s"/>\n', 'func':lambda v: '' if v =='False' else v}),
                     ('search_view_id', {'field_template':'        <field name="search_view_id" ref ="%s"/>\n', 'func':lambda v: '' if v =='False' else v}),
                     ('domain', {'field_template':'        <field name="domain">%s</field>\n', 'func':domain_}),
                     ('context', {'field_template':'        <field name="context">%s</field>\n', 'func':context_}),
                      ]
        return fieldlist
    
    model = 'import_adj.action_import'
    @property
    def recs(self):
        recs = self.env[self.model].search([('id_char','=ilike','%s.%%'%self.app)])
        return recs
    def get_a_recfieldval (self, afield):
        

        if isinstance(afield, tuple):
            field_name  = afield[0]
            attrs = afield[1]
        else:
            field_name = afield
            attrs = {}
                
        func_complete = attrs.get('func_complete')
        func = attrs.get('func')
        no_escapse = attrs.get('no_escapse')
        field_template = attrs.get('field_template')
        val =  getattr(self.rec, field_name)
        
        if not no_escapse:
            val = escapse_xml(str(val))
        if func_complete:
            val = func_complete(val, self)
        if func:
            val = func(val)
        
        if field_template and val !='':
            val_last = field_template%val
        else:
            val_last = val
        return (field_name,val_last)


            
    def gen_a_record_xml(self, rec):
            self.rec = rec 
            rs = list(map(self.get_a_recfieldval,  self.fieldlist))
            rs = dict(rs)
            print ("**context", rs)
            return self.template%rs
         
    def gen_xml_of_records(self, recs = None):
        recs = recs or self.recs
        rs = map(self.gen_a_record_xml, recs)
        odoo_xml_tag = '''<odoo>
    <data>
    %s
    </data>
</odoo>'''
        va = odoo_xml_tag% '\n'.join(rs)
        finish_func = getattr(self, 'finish_func')
        if finish_func:
            finish_func()
        return va
        
        

class GenView(Gen):
    template = '''<record id="%(id_char)s" model="ir.ui.view">
         <field name="name">%(name)s</field>
         <field name="model">%(model)s</field>
         <field name="type">%(type)s</field>%(inherit_id)s
         <field name="priority">%(priority)s</field>
         <field name="arch" type="xml">%(arch_db)s
         </field>
</record>'''
    @property
    def finish_func(self):
#         raise UserError('finish_func***')
        self.self_gen_model.log_txt = 'rs: %s'%self.log
        
    def begin_func(self):
        path = r'/mnt/c\Users\tu\Desktop\tour_goc_again\ir.model.data.csv'
        path = path.replace('\\', '/')
        f = open(path,'r')
        r = f.read()
        self.f =r
    def arch_db_func_complete_(self,val,self_gen_model):
#         <button class="oe_inline oe_stat_button" type="action" name="414" 
#         pattern_template = '(button.*?name="%s")'
# #         pattern = 'button.*?name="(\d+)"'
#         pattern = pattern_template%'(\d+)'
        pattern = '''(button.*?name=["'](\d+)["'])'''
        rs = re.findall(pattern,val)
        print ('***rs***', rs)
        action_ids = []
        if rs:
            for match, action_id in rs:
                print ('***action_id', action_id)
                search_rs = re.search('(?<!\s)"(\w*?)","ir.actions.act_window","(.*?)","%s"'%action_id, self.f)
              
                action_name = '%%(%s.%s)d'%(search_rs.group(2), search_rs.group(1))
                repl = match.replace(action_id, action_name)
                val = val.replace(match, repl )
                action_id_return = 'match:%s-repl:%s-action_id:%s-action_name: %s'%(match, repl, action_id, action_name)
                action_ids.append(action_id_return)
            log = getattr(self, 'log',[])
            log.append(action_ids)
            self.log = log
        return val
            
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
                            ('inherit_id',{'func': inherit_id_}),
                            ('arch_db',{'no_escapse':True, 'func_complete': self.arch_db_func_complete_})
                             ]
        return fieldlist1
        
    model = 'import_adj.view_import'
 
class GenMenu(Gen):
    template = '''<menuitem id="%(id_char)s" name="%(name)s" %(parent_id)s %(action)s sequence="%(sequence)s"/>'''
    model = 'import_adj.menu_import'
    @property
    def fieldlist(self):
        fieldlist1 = ['id_char', 'name',('action',{'func':lambda v: '' if v =='False' else v, 'field_template':'action="%s"'}), ('sequence',{'func':lambda v: int(float(v))}),
                      ('parent_id',{'func':lambda v: '' if v =='False' else v, 'field_template':'parent="%s" '})]
        return fieldlist1
    
view_type_sort = {'Form':1,'Tree':2,'Search':11, 'kanban':3,'Qweb':10,'Calendar':4,'Graph':6, 'Gantt':7,'Pivot':8,'Diagram':9 }
class Todo(models.Model):
    _name = 'import_adj.model_gen'
    pre_models = fields.Text()
    models = fields.Text()
    models_ids = fields.Many2many('ir.model')
    test2= fields.Text()
    test = fields.Text()
    log_txt = fields.Text()
    module_inherits = fields.Char()
    relation_not_finds = fields.Char() 
    app = fields.Selection([('bizapps_medical','bizapps_medical'),('tour_travel','tour_travel')], default = 'bizapps_medical')
    
    def gen_model_in_file(self):
        models = self.env['import_adj.model_import'].search(['|', ('active','=',False),('active','=',True)])
    
    def search_file_name_for_model(self):
        models = self.env['import_adj.model_import'].search(['|', ('active','=',False),('active','=',True)])
       
        def search_arch_fs(model):
            model_name  = model.model
            views = self.env['import_adj.view_import'].search([('model','=', model_name)])
            arch_fss =  views.mapped('arch_fs')
            arch_fss = set(arch_fss)
            if arch_fss:
                arch_fs = list(arch_fss)[0]
                arch_fs = arch_fs.split('/')[-1]
                class_model_ = arch_fs.replace('_view.xml','')
                class_model = class_model_.replace('_','.')
                model.filename = class_model_ + '.py'
            else:
                class_model = False
            model.arch_fs_search = set(arch_fss)
            model.class_model = class_model
            return class_model
        
        
        
        class_models = list(map(search_arch_fs, models))
        class_models = filter(lambda i:i, class_models)
        class_models = sorted(class_models, key = lambda i: len(i), reverse=True)
        class_models = set(class_models)
        models_class_model_false = self.env['import_adj.model_import'].search(['|', ('active','=',False),('active','=',True),('class_model','=',False)])
        def search_class_model(model):
            modelname = model.model
            for class_model in class_models:
                class_model_match = False
                template = r'^%s'%class_model.replace('.','\.')
                re_rs = re.search(template, modelname)
                if re_rs:
                    class_model_match = class_model
                    model.class_model = class_model_match
                    break
            filename = class_model_match or modelname
            model.filename = filename.replace('.','_') +'.py'
            return True
        list(map(search_class_model, models_class_model_false)) 
        
                
            
            
        
    def gen_first_last_module(self):
        models = self.env['import_adj.model_import'].search(['|', ('active','=',False),('active','=',True)])
        path = r'/mnt/c\Users\tu\Desktop\tour_goc_again\ir.model.data.csv'
        path = path.replace('\\', '/')
        f = open(path,'r')
        r = f.read()
        def seach_func(model):
            ir_model_data_name = model.ir_model_data_name
            kq = re.findall('_(\d+)_.*(%s.*)'%ir_model_data_name,r)
#             print (kq)
            mapkq = map(lambda i: (int(i[0]),i[1].split(',')[2]),kq)
            mapkq = sorted(mapkq, key = lambda i:i[0])
            model.first_module = mapkq[0][1].replace('"','') + '.' + ir_model_data_name
            model.last_module = mapkq[-1][1].replace('"','') + '.' + ir_model_data_name
            return (mapkq[0], mapkq[-1])

        rs = list(map(lambda i:seach_func(i), models ))
#         raise UserError(list(rs))
#         for module in modules:
#             module.ir_model_data_name
        
        
    
    def gen_view_file(self):
        rs = self.env['import_adj.view_import'].read_group([],['arch_fs'],['arch_fs'],lazy=False)
        arch_fss = map(lambda i: i['arch_fs'],rs)
        arch_fs_and_view_objects = map(lambda arch_fs: (arch_fs, self.env['import_adj.view_import'].search([('arch_fs','=',arch_fs)])) , arch_fss)
        def mk_file(filename_view_objects):
            arch_fs, view_object_olds = filename_view_objects
            view_objects = view_object_olds.sorted(lambda i: view_type_sort.get(i.type,6))
            yourpath = __file__
            filename =  os.path.abspath(os.path.join(yourpath, os.pardir, os.pardir, os.pardir,os.pardir,  'gen_file', arch_fs))
            if not os.path.exists(os.path.dirname(filename)):
                try:
                    os.makedirs(os.path.dirname(filename))
                except OSError as exc: # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
            f= open(filename,"w")
            rs = self._gen_view(view_objects)
            f.write(rs)
            f.close()
            return "'%s'"%arch_fs.replace('tour_travel/','')
        
        write_files = map(mk_file, arch_fs_and_view_objects)
        write_files = list(write_files)
        self.test = ',\n'.join(write_files)
        
        
       
        
        
        
    def gen_view_file_old(self):
        yourpath = __file__
        filename =  os.path.abspath(os.path.join(yourpath, os.pardir, os.pardir, os.pardir,'auto_create/tour_travel/views2', 'view.xml'))
#         filename = "/foo/bar/baz.txt"
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        
        
#         pr = '/home/tour_travel/views/view.xml'
        f= open(filename,"w")
        rs = self.gen_view()
        f.write(rs)
        f.close()
        self.test = filename
        
    def test_rpc(self):
        self.env['import_adj.model_import'].search([]).write ({'active':False})
#         rs = self.env['res.users'].search([('login','=','nguyenductu@gmail.com')])
#         kq =rs.password_crypt
#         raise UserError(kq)
#         
        
#     def search_model_id(self):
#         fields = self.env['import_adj.fields_import'].search([])
#         for field in fields:
#             model_id = self.env['import_adj.model_import'].search(['|', ('active','=',False),('active','=',True),('id_char','=', field.model_id)])
#             field.model_name = model_id.model
    
    def search_model_id(self):
        fields = self.env['import_adj.fields_import'].search([])
        for field in fields:
            model = self.env['import_adj.model_import'].search(['|', ('active','=',False),('active','=',True),('model','=', field.model_look_sum)])
            field.model_name = model
            
        
    def gen_related_model(self):
        read_group_fields_rs = self.env['import_adj.fields_import'].read_group([('field2_name', '=', u'!No exist')], ['field2','field1_model_name','relation','ttype', 'relation_table'], ['field2','field1_model_name','relation','ttype', 'relation_table'],lazy = False)
        for r in read_group_fields_rs:
            print (r)
        raise UserError(str(read_group_fields_rs))
    
    
    def related_deal_new(self):
        fields = self.env['import_adj.fields_import'].search([])
        for field in fields:
            related = field.related
            if related:
                s= related.split('.')
                field1, field2 = s[0],s[1]
                field.field2 = field2
       
    def related_deal(self):
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
        rs = GenMenu(self.env, self.app, self).gen_xml_of_records()
        self.test2 = rs

    def gen_view(self):
        rs = self._gen_view()
        self.test2 = rs
        return rs
    
    def _gen_view(self, recs = None):
        rs = GenView(self.env, self.app, self).gen_xml_of_records(recs)
        return rs
    
    def gen_action(self):
        rs = Gen(self.env,self.app, self).gen_xml_of_records()
        self.test2 = rs
    #############1##################
    
    def declare_python_fields(self, name, ttype, relation,relation_field,related, relation_table):
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
    def comment_if_not_fields(self, declare):
        declare = '#' + declare
        return declare
    def gen_item_model_python(self, model_name, transient, modelclass=None, name_or_inherit = '_name', fields_ids = [],add_mixin = False):
        if not modelclass:
            modelclass =model_name.replace('.',' ').replace('_',' ')
            modelclass = modelclass.title().replace(' ','')
#         pres = []
        model_or_transient ='models.Model' if not transient else  'models.TransientModel'
        class_declare = 'class %s(%s):'%(modelclass, model_or_transient)
        print ('**name_or_inherit',name_or_inherit,'model_name',model_name)
        name_or_inherit_declare = name_or_inherit  + ' = ' +  "'%s'"%model_name 
        if not fields_ids:
            class_declare = '#' + class_declare
            name_or_inherit_declare = '#' + name_or_inherit_declare
        pres = [class_declare, name_or_inherit_declare]
        
#         if not fields_ids:
#             class_declare = '#%s'%class_declare
#             pre = '#%s'%class_declare
            
        if add_mixin and 'name' in name_or_inherit  and fields_ids:
            mix_declare="_inherit = ['mail.thread', 'mail.activity.mixin']" 
            pres.append(mix_declare)
        if fields_ids:
            field_python_list = map(lambda f: self.declare_python_fields(f.name, f.ttype,
                                                                        getattr(f,'relation',None),getattr(f,'relation_field',None),
                                                                        getattr(f,'related',None),getattr(f,'relation_table',None)),fields_ids)
            fields_declare =  '\n\t'.join(field_python_list) 
            pres.append(fields_declare)
        return '\n\t'.join(pres) +'\n\n'


    def add_more_to_model_group(self, read_group_rs):
        for i in read_group_rs:
            model_id = i['model_id']
            model_id_obj = self.env['import_adj.model_import'].search([('id_char','=',model_id)])
            if model_id_obj:
                modelclass = model_id_obj.model
                model_name = model_id_obj.model
                name_or_inherit = '_name'
            else:
                module_name, model_name = model_id.split('.')
                model_in_ir_model_data = self.env['ir.model.data'].search([('name','=',model_name),('model','=','ir.model')])
               
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
    
    
    def gen_model_and_field_old(self):
        domain = [('modules','=ilike','%s'%self.app)]
        model_groups = self.env['import_adj.fields_import'].read_group(domain, ['model_id'],['model_id'], lazy=False)
        self.add_more_to_model_group(model_groups)
        model_groups_adding_more_info = sorted(model_groups, key=itemgetter('name_or_inherit'))
        def gen_a_model(model_group_read_item):    
            fields_ids = self.env['import_adj.fields_import'].search([('model_look_sum','=',model_group_read_item.model),('name','not in', NOT_IN)])
            name_or_inherit = model_group_read_item['name_or_inherit'] 
            modelclass = model_group_read_item['modelclass']
            model_name = model_group_read_item['model_name']
            modelclass = modelclass.replace(' ','').replace('.','')
            transient = model_group_read_item.transient
            item_model_python = self.gen_item_model_python(model_name, transient,  modelclass, name_or_inherit, fields_ids, add_mixin = True)
            return item_model_python
        model_pythons = map(gen_a_model, model_groups_adding_more_info)
        model_pythons_txt = ''.join (model_pythons)
        self.test2 = model_pythons_txt
        return model_pythons_txt
    
    def gen_model_and_field(self):
        domain = ['|', ('active','=',False),('active','=',True)]
        model_groups = self.env['import_adj.model_import'].search(domain)
        model_groups_adding_more_info = sorted(model_groups, key=lambda i: i.active)
        def gen_a_model(model):    
            fields_ids = self.env['import_adj.fields_import'].search([('model_look_sum','=',model['model']),('name','not in', NOT_IN)])
            name_or_inherit = '_name' if model.active else '_inherit'
            model_name = model.model
            modelclass = model_name.replace('.',' ').title().replace(' ','')
            item_model_python = self.gen_item_model_python(model_name, model.transient, modelclass,name_or_inherit, fields_ids, add_mixin = True)
            return item_model_python
        model_pythons = map(gen_a_model, model_groups_adding_more_info)
        model_pythons_txt = ''.join (model_pythons)
        self.test2 = model_pythons_txt
        return model_pythons_txt
    
    
    def gen_declare_model_extend_inherit(self):
        class FieldObj:
            def __init__(self, **entries):
                self.__dict__.update(entries)
        fieldname = FieldObj(**{'name':'name','ttype':'Char'})
        c = '''['res.country.district', 'res.country.wards']'''
        c = c.replace("'",'"')
        rs = json.loads(c)
        def gen_pre_declare_model_default_fields(model_name):
            return self.gen_pre_declare_model(model_name, fields_ids=[fieldname])
        self.test2 = u'\n\n'.join(map(gen_pre_declare_model_default_fields, rs))

    def write(self, vals):
#         print ('dung buon em hoi***********')
        rs = models.Model.write(self, vals)
        return rs
    
  