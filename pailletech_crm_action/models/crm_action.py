# -*- coding: utf-8 -*-
# � 2015-2016 Savoir-faire Linux (<http://www.savoirfairelinux.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api, _
from openerp.exceptions import Warning

class CrmAction(models.Model):
    _inherit = 'crm.action'
    
    _order = 'date desc'
    
    @api.multi
    @api.depends('subject', 'details')
    def compute_display_name(self):
        for action in self:
            if action.details:
                action.display_name = u'[%s] %s' % (
                    action.subject, action.details)
            else:
                action.display_name = u'[%s]' % action.subject   
    
    subject = fields.Char(string="Subject", required=True)
    
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    
    display_name = fields.Char(
        compute='compute_display_name', readonly=True, store=True)
    
    def default_action_type(self):
        action_type_ids = self.env['crm.action.type'].search([('default','=',True)]).ids
        
        if len(action_type_ids) > 0 :
            return action_type_ids[0]
        else:
            super(CrmAction, self).default_action_type()
    
    action_type_id = fields.Many2one(
        'crm.action.type', string='Type', required=True,
        default=default_action_type)
    
    @api.multi
    def button_confirm(self):
        if not self.details or self.details.strip() == '':
            raise Warning(_('You must give a summary of the action.'))
        self.write({'state': 'done'})
 
    @api.multi
    def view_action(self):
        form = self.env.ref('pailletech_crm_action.popup_action_form', False)

        return {
            'name': 'Action',
            'res_model': 'crm.action',
            'view_id': form.id,
            'res_id': self.id,
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'current',
            'nodestroy':True,
        } 
    
    @api.multi    
    def view_lead_opport(self):
        if self.lead_id.type == 'lead':
            form = self.env.ref('pailletech_crm_action.crm_lead_action_form_pt', False)
            name = "Lead"
        else:
            form = self.env.ref('pailletech_crm_action.crm_oppor_action_form_pt', False)
            name = "Opportunity"
        
        return {
            'name': name,
            'res_model': 'crm.lead',
            'view_id': form.id,
            'res_id': self.id,
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'nodestroy':True,
        } 
                     
class CrmActionType(models.Model):
    _inherit = 'crm.action.type'
    
    default = fields.Boolean(string="Default action type")
    
    @api.one
    def write(self, vals):
        if vals.get('default',False):
            if vals.get('default') == True:
                action_types = self.search([('id','!=',self.id)])
                action_types.write({'default':False})
        super(CrmActionType, self).write(vals)