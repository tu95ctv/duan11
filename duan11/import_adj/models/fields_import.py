# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import  ValidationError

# class FieldsImportTestsame(models.Model):
#     _name = 'import_adj.fields.import'
#     _order = 'related desc, ttype'
#     id_char = fields.Char()
#     namekaka = fields.Char()
#     
# class FieldsImportTest(models.Model):
#     _name = 'import_adj.fields.import2'
#     _order = 'related desc, ttype'
#     id_char = fields.Char()
#     name = fields.Char()


    
class FieldsImport(models.Model):
    _name = 'import_adj.fields_import'
    _order = 'related desc, ttype'
    _description = "Field"

    id_char = fields.Char()
    name = fields.Char()
    column1 = fields.Char()
    column2 = fields.Char()
    complete_name = fields.Char()
    compute = fields.Char()
    copy = fields.Char()
    depends = fields.Char()
    domain = fields.Char()
    field_description = fields.Char()
    groups = fields.Char()
    help = fields.Char()
    index = fields.Char()
    model = fields.Char()
    model_id = fields.Char()
    modules = fields.Char()
    on_delete = fields.Char()
    readonly = fields.Char()
    related = fields.Char()
    relation = fields.Char()
    relation_field = fields.Char()
    relation_table = fields.Char()
    required = fields.Char()
    selectable = fields.Char()
    selection = fields.Char()
    size = fields.Char()
    state = fields.Char()
    store = fields.Char()
    translate = fields.Char()
    ttype = fields.Char()
    
    ###
    model_name_look = fields.Char()
    app_of_model = fields.Char()
    model_look1 = fields.Char()
    model_look2 = fields.Char()
    model_look_sum = fields.Char()
    is_inherit = fields.Boolean()
    is_active = fields.Boolean()
    active = fields.Boolean(default = True)
    ##
    relation_search = fields.Char()

    field1_model_name = fields.Char()
    field2_name = fields.Char()
    
    field2 = fields.Char()
    
    test1 = fields.Char()
    model_name = fields.Char()


    
class ModesImport(models.Model):
    _name = 'import_adj.model_import'
    _description = "Model"

    id_char = fields.Char()
    modules = fields.Char()
    module_goc = fields.Char()
    model = fields.Char()
    name = fields.Char()
    transient = fields.Char()
    active = fields.Boolean(default=True)
    du = fields.Char()
    ir_model_data_name = fields.Char(compute ='ir_model_data_name_', store = True )
    @api.depends('id_char')
    def ir_model_data_name_(self):
        for r in self:
            r.ir_model_data_name = r.id_char.split('.')[-1]
    first_module = fields.Char()        
    last_module = fields.Char()  
    arch_fs_search = fields.Char()    
    class_model = fields.Char()
    filename = fields.Char()      
class ActionImport(models.Model):
    _name = 'import_adj.action_import'
    _description = "Action"
    id_char = fields.Char()
    name = fields.Char()
    auto_search = fields.Char()
    context = fields.Char()
    domain = fields.Char()
    filter = fields.Char()
    groups_id = fields.Char()
    limit = fields.Char()
    multi = fields.Char()
    res_id = fields.Char()
    res_model = fields.Char()
    search_view = fields.Char()
    search_view_id = fields.Char()
    src_model = fields.Char()
    target = fields.Char()
    type = fields.Char()
    usage = fields.Char()
    view_id = fields.Char()
    view_ids = fields.Char()
    view_mode = fields.Char()
    view_type = fields.Char()
    views = fields.Char()
    id_number = fields.Integer()

    
class MenuImport(models.Model):
    _name = 'import_adj.menu_import'
    #_name*ir.ui.menu
    _description = "Menu"
    id_char = fields.Char()
    action = fields.Char()
    active = fields.Char()
    child_id = fields.Char()
    complete_name = fields.Char()
    groups_id = fields.Char()
    name = fields.Char()
    parent_id = fields.Char()
    parent_left = fields.Char()
    parent_right = fields.Char()
    sequence = fields.Char()
    web_icon = fields.Char()
    web_icon_data = fields.Char()
    

class ViewImport(models.Model):
    _name = 'import_adj.view_import'
    _description = "View"
    #_name*ir.ui.view
    id_char = fields.Char()
    arch = fields.Char()
    arch_base = fields.Char()
    arch_db = fields.Char()
    arch_fs = fields.Char()
    create_date = fields.Char()
    field_parent = fields.Char()
    groups_id = fields.Char()
    inherit_children_ids = fields.Char()
    inherit_id = fields.Char()
    key = fields.Char()
    mode = fields.Char()
    model = fields.Char()
    model_data_id = fields.Char()
    model_ids = fields.Char()
    name = fields.Char()
    priority = fields.Char()
    type = fields.Char()
    write_date = fields.Char()
    xml_id = fields.Char()
    
    ##
#     model_module = fields.Char()
    

    

    
    
    
    
    
    
    
