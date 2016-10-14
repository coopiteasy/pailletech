# -*- coding: utf-8 -*-
# � 2016 Open Architects Consulting sprl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from datetime import date
from dateutil.relativedelta import relativedelta

from openerp import models, fields, api


class CrmLead(models.Model):
    _inherit = 'crm.lead'
    
    @api.one
    def count_actions(self):
        self.actions_count = len(self.action_ids)
    
    @api.one    
    def compute_actions_in_month(self):
        #for lead in self:
        self.actions_in_month = len(self.env['crm.action'].search(
            [('lead_id', '=', self.id), ('state', '=', 'done')
             ,('date','>=',date.today()+ relativedelta(months=-1))]))
    
                
    actions_in_month = fields.Integer(string='Actions in month',
        compute='compute_actions_in_month', readonly=True)
    
    def log_action(self, state, action_date, user=None):
        assert len(self) == 1, 'This option should only be used for a single id at a time.'
        
        
        if user == None:
            user = self.user_id.id
        ctx = dict(self._context or {}, default_lead_id= self.id,
                   default_partner_id= self.partner_id.id,
                   default_user_id= user,
                   default_date= action_date,
                   default_state = state)
        
        form = self.env.ref('pailletech_crm_action.popup_action_form', False)
        
        return {
            'name': 'Action',
            'res_model': 'crm.action',
            'view_id': form.id,
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'nodestroy':True,
            'context': ctx
            }   
         
    @api.multi
    def action_done(self):
        
        return self.log_action('done', date.today().strftime('%Y-%m-%d'), self.env.uid)
         
    
    @api.multi
    def contact_asap(self):
        
        return self.log_action('draft', date.today().strftime('%Y-%m-%d'), None)
         
    @api.multi
    def contact_one_week(self):
        
        return self.log_action('draft', (date.today()+ relativedelta(weeks=+1)).strftime('%Y-%m-%d'), None)
         
    @api.multi
    def contact_one_month(self):
        
        return self.log_action('draft', (date.today()+ relativedelta(months=+1)).strftime('%Y-%m-%d'), None)
         
    @api.multi
    def contact_three_month(self):
        
        return self.log_action('draft', (date.today()+ relativedelta(months=+3)).strftime('%Y-%m-%d'), None)
        
    