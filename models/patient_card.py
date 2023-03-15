from odoo import models, fields, api, _
from datetime import date


class PatientCard(models.Model):
    _name = "patient.card"
    _description = "Patient Card"
    _rec_name = 'patient'
    _inherit = 'mail.thread'

    patient = fields.Char(string='Patient ID', required=True, readonly=True,
                          default=lambda self: _('New'))
    patient_name_id = fields.Many2one('res.partner')
    address = fields.Char(related='patient_name_id.contact_address',
                          string="Address")
    dob = fields.Date(related='patient_name_id.dob')
    age = fields.Integer(compute='_compute_age')
    mob = fields.Char(related='patient_name_id.mobile')
    gender = fields.Selection(related='patient_name_id.gender')
    telephone = fields.Char(related='patient_name_id.phone')
    blood = fields.Selection(string="Blood Group",
                             selection=[('A+', 'A+'), ('A-', 'A-'),
                                        ('B+', 'B+'), ('B-', 'B-'),
                                        ('AB+', 'AB+'), ('AB-', 'AB-'),
                                        ('O+', 'O+'), ('O-', 'O-')])
    op_history_ids = fields.One2many('patient.op', 'name_id', readonly=True)

    @api.depends('dob')
    def _compute_age(self):
        print(self)
        for record in self:
            if record.patient_name_id and record.dob:
                today = date.today()
                record.age = today.year - record.dob.year - (
                            (today.month, today.day) < (
                             record.dob.month, record.dob.day))
            self.age = record.age

    @api.model
    def create(self, vals):
        print(self,'aaaaaaaaaaaaaaaaa')
        if vals.get('patient', 'New') == 'New':
            vals['patient'] = self.env['ir.sequence'].next_by_code(
                'patient.card') or 'New'
        res = super(PatientCard, self).create(vals)
        return res
