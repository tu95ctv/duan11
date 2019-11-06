# -*- coding: utf-8 -*-

from odoo import models, fields, api

class IrActions(models.Model):
    _inherit = 'ir.actions.actions'
   
    xml_id_add2 = fields.Char(compute='_compute_xml_id_add',store = True)
#     menu_id = fields.Many2one('ir.ui.menu', compute = 'menu_id_',store=True)
    menu_id_char = fields.Char( compute = 'menu_id_', store=True)
    is_trig = fields.Boolean()
    @api.depends('name','is_trig')
    def menu_id_(self):
        for r in self:
            rs= self.env['ir.ui.menu'].search([('action','=','ir.actions.act_window,%s'%r.id)]).mapped('name')
            r.menu_id_char = ', '.join(rs)
#             rs= self.env['ir.ui.menu'].search([('action','=','ir.actions.act_window,%s'%r.id)])
#             rs = map(lambda i: i.name +',' + i.xml_id, )
#             
#             r.menu_id_char = ', '.join(rs)    
            
    @api.depends('name','is_trig')
    def _compute_xml_id_add(self):
        res = self.get_external_id()
        for record in self:
            record.xml_id_add2 = res.get(record.id)
            
            
            
class IrUiMenu(models.Model):
    _inherit = 'ir.ui.menu'
    xml_id = fields.Char(compute='xml_id_', store = True)
    is_trig = fields.Boolean()
    
    @api.depends('is_trig')
    def xml_id_(self):
        res = self.get_external_id()
        for record in self:
            record.xml_id = res.get(record.id)
    