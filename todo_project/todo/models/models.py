# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime

class Todo(models.Model):
    _name = 'todo.todo'
    _rec_name = 'description'
    #Draft --> Waiting for Approval --> Approved or Rejected.
    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting_for_approval', 'Waiting for Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
#         ('cancel', 'Cancel')
        ], default='draft')
    description = fields.Text()
    created_date = fields.Date(default=fields.Date.context_today)
    def offset_date(self):
        today = datetime.date.today()
        print ('today',today,type(today))
        the_day = today + datetime.timedelta(days=7)
        return the_day
    deadline = fields.Date(default= offset_date)
    responsible_id = fields.Many2one('res.users',default=lambda self:self.env.uid)
    manager_id = fields.Many2one('res.users')
    

    @api.multi
    def action_draft(self):
        self.state = 'draft'    
    @api.multi
    def action_waiting_for_approval(self):
        self.state = 'waiting_for_approval'
    @api.multi
    def action_approved(self):
        self.state = 'approved'
    @api.multi
    def action_rejected(self):
        self.state = 'rejected'
#     @api.multi
#     def action_cancel(self):
#         self.state = 'cancel'    
#         
    
    

