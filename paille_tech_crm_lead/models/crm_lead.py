# -*- coding: utf-8 -*-
from openerp import api, fields, models, _
from openerp.exceptions import except_orm, Warning

class ResPartner(models.Model):
    _inherit = "res.partner"
    
    is_site = fields.Boolean('Is a construction site')

class CrmLead(models.Model):
    _inherit = "crm.lead"

    pre_down_payment_date = fields.Date(string='Pre-down payment date')
    down_payment_date = fields.Date(string='Down payment date')
    building_permit = fields.Boolean(string='Building permit?')
    has_building_permit = fields.Selection([('yes','Yes'),
                                        ('no','No')],string='Has the building permit')
    has_building_site = fields.Selection([('yes','Yes'),
                                        ('no','No')],string='Has the construction site')
    has_building_architect = fields.Selection([('yes','Yes'),
                                        ('no','No')],string='Has an architect')
    building_permit_date = fields.Date(string='Building permit date')
    balance_payment_date = fields.Date(string='Balance payment date')
    architect_phone = fields.Char(related="architect.phone", string="Architect phone")
    architect_mobile = fields.Char(related="architect.mobile", string="Architect mobile")
    architect_email = fields.Char(related="architect.email", string="Architect email")
    site_id = fields.Many2one('res.partner', string="Construction Site")
    #site_street = fields.Char(related="site.street", string="Site street")

    _order = "create_date desc, id desc"
    
    @api.multi
    def on_change_partner_id(self, partner_id):
        res = super(CrmLead, self).on_change_partner_id(partner_id)
        if partner_id:
            res['value'].update({'site': partner_id})
        return res
        
    @api.multi
    def write(self, vals):
        if self.pre_down_payment_date and self.down_payment_date:
            if self.pre_down_payment_date > self.down_payment_date:
                raise except_orm(
                    _('Error!'),
                    _("Predown payment date can't be greater than the down payment date.")
                )
        if self.pre_down_payment_date and self.balance_payment_date:
            if self.pre_down_payment_date > self.balance_payment_date:
                raise except_orm(
                    _('Error!'),
                    _("Predown payment date can't be greater than the balance payment date.")
                )
        if self.down_payment_date and self.balance_payment_date:
            if self.down_payment_date > self.balance_payment_date:
                raise except_orm(
                    _('Error!'),
                    _("Down payment date can't be greater than the balance payment date.")
                )
        return super(CrmLead, self).write(vals)
    
    @api.model
    def create(self, vals):
        if self.pre_down_payment_date and self.down_payment_date:
            if self.pre_down_payment_date > self.down_payment_date:
                raise except_orm(
                    _('Error!'),
                    _("Predown payment date can't be greater than the down payment date.")
                )
        if self.pre_down_payment_date and self.balance_payment_date:
            if self.pre_down_payment_date > self.balance_payment_date:
                raise except_orm(
                    _('Error!'),
                    _("Predown payment date can't be greater than the balance payment date.")
                )
        if self.down_payment_date and self.balance_payment_date:
            if self.down_payment_date > self.balance_payment_date:
                raise except_orm(
                    _('Error!'),
                    _("Down payment date can't be greater than the balance payment date.")
                )
        return super(CrmLead, self).create(vals)