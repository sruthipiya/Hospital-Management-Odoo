from odoo import models, fields
from datetime import date


class PatientDetails(models.Model):
    _inherit = "res.partner"

    dob = fields.Date(default=date.today())
    gender = fields.Selection(string="Gender", selection=[('male', 'Male'), (
            'female', 'Female')])
