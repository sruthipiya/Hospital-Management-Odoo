from odoo import models, fields, api, _
from datetime import datetime


class PatientConsultation(models.Model):
    _name = "patient.consultation"
    _description = "Patient consultation details"
    _rec_name = "card_details_id"

    consultation = fields.Char(default=lambda self: _('New'))
    consultation_doctor_id = fields.Many2one('hr.employee',
                                             domain=[('doct', '=', True)],
                                             string="Doctor")
    card_details_id = fields.Many2one('patient.op', string="Card Number")
    consultation_type = fields.Selection(string="Consultation Type",
                                         selection=[('op', 'OP'),
                                                    ('ip', 'IP')])
    department_id = fields.Many2one(
        related='consultation_doctor_id.department_id')
    consultation_date = fields.Datetime(default=datetime.now())
    disease_id = fields.Many2one('disease.details', string="Disease")
    disease = fields.Char(related='disease_id.name')
    consultation_description = fields.Text(placeholder="Descriptions")
    consultation_details_ids = fields.One2many('patient.treatment',
                                               'treatment_id')
    # op_id = fields.Many2one('patient.op', string="OP")

    token = fields.Char(related='card_details_id.token')

    @api.onchange('consultation_doctor_id')
    def onchange_card_id(self):
        self.write({'card_details_id': [(5, 0)]})
        for rec in self:
            # print(rec.consultation_doctor_id)
            return {'domain': {'card_details_id': [
                ('doctor_op_id', '=', rec.consultation_doctor_id.id)]}}

    @api.model
    def create(self, vals):
        if vals.get('consultation', 'New') == 'New':
            vals['consultation'] = self.env['ir.sequence'].next_by_code(
                'patient.consultation') or 'New'
        res = super(PatientConsultation, self).create(vals)
        return res


class BoolDoctor(models.Model):
    _inherit = "hr.employee"
    fee = fields.Integer(string="Fee")

    doct = fields.Boolean(string='Doctor', default=False)


class PatientTreatment(models.Model):
    _name = "patient.treatment"
    _rec_name = "treatment_id"

    medicine = fields.Char()
    dose = fields.Integer()
    days = fields.Integer()
    description = fields.Text()
    treatment_id = fields.Many2one('patient.consultation')
