# -*- coding: utf-8 -*-
from openerp import api, fields, models, _
from openerp.exceptions import except_orm, Warning

class CrmLead(models.Model):
    _inherit = "crm.lead"

    pre_down_payment_date = fields.Date(string='Pre-down payment date')
    down_payment_date = fields.Date(string='Down payment date')
    building_permit = fields.Boolean(string='Building permit?')
    building_permit_date = fields.Date(string='Building permit date')
    balance_payment_date = fields.Date(string='Balance payment date')
    architect_phone = fields.Char(related="architect.phone", string="Architect phone")
    architect_mobile = fields.Char(related="architect.mobile", string="Architect mobile")
    architect_email = fields.Char(related="architect.email", string="Architect email")
    
    _order = "create_date desc, id desc"
    
    @api.multi
    def write(self, vals):
        super(CrmLead, self).write(vals)
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
        super(CrmLead, self).create(vals)
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