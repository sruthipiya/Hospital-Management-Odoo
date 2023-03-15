from odoo import models, fields, api, _
from datetime import datetime


class PatientOP(models.Model):
    _name = "patient.op"
    _description = "Patient OP"
    _rec_name = "name_id"

    name_id = fields.Many2one('patient.card', string="Patient Card",
                              required=True)
    op_id = fields.Many2one(related='name_id.patient_name_id')
    age_op = fields.Integer(related='name_id.age')
    gender_op = fields.Selection(related='name_id.gender')
    blood_op = fields.Selection(related='name_id.blood')
    doctor_op_id = fields.Many2one('hr.employee', domain="[('doct','=',True)]",
                                   string="Doctor")
    date_today = fields.Datetime(string="Date", default=datetime.now())
    token = fields.Char(default=lambda self: _('New'))
    doctor_token = fields.Integer(compute="doctor_token_number")
    company_id = fields.Many2one('res.company',
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  default=lambda self:
                                  self.env.company.currency_id)
    fee = fields.Integer(related='doctor_op_id.fee')
    amount = fields.Monetary()
    # consultation_id = fields.Many2one('patient.consultation')
    # doctor_department_id = fields.Many2one(
    # related='consultation_id.department_id')
    doctor_department_id = fields.Many2one(
        related='doctor_op_id.department_id')
    appointment_id = fields.Many2one('doctor.appointment')
    op_appointment = fields.Boolean(default=False)
    flag = fields.Integer(default=0)
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('op', 'OP')], string="Status", required=True, readonly=True,
        copy=False,
        tracking=True, default='draft')

    def button_in_progress(self):
        self.appointment_id.state = 'op'
        self.state = 'op'

    @api.model
    def create(self, vals):
        if vals.get('token', 'New') == 'New':
            vals['token'] = self.env['ir.sequence'].next_by_code(
                'patient.op') or 'New'
            vals['doctor_token'] = vals['token']
        res = super(PatientOP, self).create(vals)
        return res

    @api.onchange('doctor_op_id')
    def doctor_token_number(self):
        self.doctor_token = self.env['patient.op'].search_count(
            [('doctor_op_id', '=', self.doctor_op_id.id)])

    def button_fee_payment(self):
        self.flag = 1
        invoice = self.env['account.move'].create([{
            'move_type': 'out_invoice',
            'partner_id': self.op_id.id,
            'date': self.date_today,
            'invoice_date': self.date_today,
            'payment_reference': self.id,
            'invoice_line_ids': [(0, 0, {
                'product_id': 28,
                'name': 'product test 1',
                'quantity': 1.0,
                'price_unit': self.fee,
                'tax_ids': [],
            })]
        }])
        return {
            'type': 'ir.actions.act_window',
            'name': 'invoice',
            'view_mode': 'form',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'domain': [('payment_reference', '=', self.id)],
            'context': "{'create': False}"
        }

    def get_payment(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Payment',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'domain': [('payment_reference', '=', self.id)],
            'context': "{'create': False}"
        }
