# -*- coding: utf-8 -*-
from openerp import api, fields, models

class CrmLead(models.Model):
    _inherit = "crm.lead"

    pre_down_payment_date = fields.Date(string='Pre-down payment date')
    down_payment_date = fields.Date(string='Down payment date')
    building_permit = fields.Boolean(string='Building permit?')
    building_permit_date = fields.Date(string='Building permit date')
    fifty_percent_payment_date = fields.Date(string='50% advance date')
    architect_phone = fields.Char(related="architect.phone", string="Architect phone")
    architect_mobile = fields.Char(related="architect.mobile", string="Architect mobile")
    architect_email = fields.Char(related="architect.email", string="Architect email")
    
    _order = "create_date desc, id desc"