from odoo import models, fields, api, _


class DoctorAppointment(models.Model):
    _name = "doctor.appointment"
    _description = "Doctor's Appointment"
    _rec_name = "appointment_id"
    _inherit = 'mail.thread'

    appointment = fields.Char(default=lambda self: _('New'))
    appointment_id = fields.Many2one('patient.card',
                                             string="Card ID")
    appointment_name_id = fields.Many2one(
        related="appointment_id.patient_name_id")
    appointment_doctor_id = fields.Many2one('hr.employee',
                                            domain=[('doct', '=', True)],
                                            string="Doctor")
    appointment_department_id = fields.Many2one(
        related='appointment_doctor_id.department_id')
    appointment_date = fields.Datetime(string="Date",
                                       default=fields.Date.today())
    state = fields.Selection(
        selection=[('draft', 'Draft'), ('appointment', 'Appointment'),
                   ('op', 'OP')],
        string="Status", required=True, readonly=True, copy=False,
        tracking=True,
        default='draft')
    company_id = fields.Many2one('res.company',
                                 default=lambda self: self.env.company)
    fee = fields.Integer(related='appointment_doctor_id.fee')
    # doctor_token = fields.Integer(compute="doctor_token_number")

    # @api.onchange('appointment_doctor_id')
    # def doctor_token_number(self):
    #     self.doctor_token = self.env['patient.op'].search_count(
    #         [('doctor_op_id', '=',
    #           self.appointment_doctor_id.id)])

    def action_in_appointment(self):
        self.state = "appointment"
        # self.write({'state': "appointment"})

    def action_in_op(self):
        return {
            'name': self.appointment_name_id,
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'patient.op',
            'view_id': self.env.ref(
                'hospital_management.hospital_patient_op_form').id,
            'context': {'default_op_appointment': True,
                        'default_name_id': self.appointment_id.id,
                        'default_appointment_id': self.id,
                        'default_op': self.appointment_name_id.id,
                        'default_doctor_op_id': self.appointment_doctor_id.id,
                        'default_date_today': fields.Date.today(),
                        'default_amount': self.fee,
                        }
        }

    def get_op(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'OP',
            'view_mode': 'tree,form',
            'res_model': 'patient.op',
            'domain': [('appointment_id', '=', self.id)],
            'context': "{'create': False}"
        }

    @api.model
    def create(self, vals):
        if vals.get('appointment', 'New') == 'New':
            vals['appointment'] = self.env['ir.sequence'].next_by_code(
                'doctor.appointment') or 'New'
        res = super(DoctorAppointment, self).create(vals)
        return res
