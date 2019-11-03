# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import  ValidationError

class IrModelImport(models.Model):
    _inherit = 'ir.model'
    _name = 'ir.model.import'
    
#     @api.constrains('model')
#     def _check_model_name(self):
#         for model in self:
# #             if model.state == 'manual':
# #                 if not model.model.startswith('x_'):
# #                     raise ValidationError(_("The model name must start with 'x_'."))
#             if not models.check_object_name(model.model):
#                 raise ValidationError(_("The model name can only contain lowercase characters, digits, underscores and dots."))
            
# class IrModelFields(models.Model):
#     _inherit = 'ir.model.fields.import'            
#     _name = 'ir.model.fields.import.import'
    
FIELD_TYPES = [(key, key) for key in sorted(fields.Field.by_type)]
class IrModelFields(models.Model):
    _name = 'ir.model.fields.import'
    _description = "Fields"
    _order = "name"
    _rec_name = 'field_description'

    name = fields.Char(string='Field Name', default='x_', required=True, index=True)
    complete_name = fields.Char(index=True)
    model = fields.Char(string='Object Name', required=True, index=True,
                        help="The technical name of the model this field belongs to")
    relation = fields.Char(string='Object Relation',
                           help="For relationship fields, the technical name of the target model")
    relation_field = fields.Char(help="For one2many fields, the field on the target model that implement the opposite many2one relationship")
    model_id = fields.Many2one('ir.model', string='Model', required=True, index=True, ondelete='cascade',
                               help="The model this field belongs to")
    field_description = fields.Char(string='Field Label', default='', required=True, translate=True)
    help = fields.Text(string='Field Help', translate=True)
    ttype = fields.Selection(selection=FIELD_TYPES, string='Field Type', required=True)
    selection = fields.Char(string='Selection Options', default="",
                            help="List of options for a selection field, "
                                 "specified as a Python expression defining a list of (key, label) pairs. "
                                 "For example: [('blue','Blue'),('yellow','Yellow')]")
    copy = fields.Boolean(string='Copied', help="Whether the value is copied when duplicating a record.")
    related = fields.Char(string='Related Field', help="The corresponding related field, if any. This must be a dot-separated list of field names.")
    required = fields.Boolean()
    readonly = fields.Boolean()
    index = fields.Boolean(string='Indexed')
    translate = fields.Boolean(string='Translatable', help="Whether values for this field can be translated (enables the translation mechanism for that field)")
    size = fields.Integer()
    state = fields.Selection([('manual', 'Custom Field'), ('base', 'Base Field')], string='Type', default='manual', required=True, readonly=True, index=True)
    on_delete = fields.Selection([('cascade', 'Cascade'), ('set null', 'Set NULL'), ('restrict', 'Restrict')],
                                 string='On Delete', default='set null', help='On delete property for many2one fields')
    domain = fields.Char(default="[]", help="The optional domain to restrict possible values for relationship fields, "
                                            "specified as a Python expression defining a list of triplets. "
                                            "For example: [('color','=','red')]")
    groups = fields.Many2many('res.groups', 'ir_model_fields_group_rel', 'field_id', 'group_id')
    selectable = fields.Boolean(default=True)
    modules = fields.Char(compute='_in_modules', string='In Apps', help='List of modules in which the field is defined')
    relation_table = fields.Char(help="Used for custom many2many fields to define a custom relation table name")
    column1 = fields.Char(string='Column 1', help="Column referring to the record in the model table")
    column2 = fields.Char(string="Column 2", help="Column referring to the record in the comodel table")
    compute = fields.Text(help="Code to compute the value of the field.\n"
                               "Iterate on the recordset 'self' and assign the field's value:\n\n"
                               "    for record in self:\n"
                               "        record['size'] = len(record.name)\n\n"
                               "Modules time, datetime, dateutil are available.")
    depends = fields.Char(string='Dependencies', help="Dependencies of compute method; "
                                                      "a list of comma-separated field names, like\n\n"
                                                      "    name, partner_id.name")
    store = fields.Boolean(string='Stored', default=True, help="Whether the value is stored in the database.")
    
    
    

class IrModel(models.Model):
    _inherit = 'ir.model'
    
    @api.constrains('model')
    def _check_model_name(self):
        for model in self:
#             if model.state == 'manual':
#                 if not model.model.startswith('x_'):
#                     raise ValidationError(_("The model name must start with 'x_'."))
            if not models.check_object_name(model.model):
                raise ValidationError(_("The model name can only contain lowercase characters, digits, underscores and dots."))
            
            
            
            
            
            
            
            
            
class IrModelFieldsI(models.Model):
    _inherit = 'ir.model.fields'            
    @api.constrains('name', 'state')
    def _check_name(self):
        for  field in self:
#                 if field.state == 'manual' and not field.name.startswith('x_'):
#                     raise ValidationError(_("Custom fields must have a name that starts with 'x_' !"))
            try:
                models.check_pg_name(field.name)
            except ValidationError:
                msg = _("Field names can only contain characters, digits and underscores (up to 63).")
                raise ValidationError(msg)
            
            

            