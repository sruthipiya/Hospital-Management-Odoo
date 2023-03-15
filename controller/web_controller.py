from datetime import datetime, date
from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError


class WebsiteForm(http.Controller):
    @http.route(['/appointment'], type='http', auth="user", website=True)
    def appointment(self):
        doctor = request.env['hr.employee'].sudo().search([("doct", "=", True)])
        patient = request.env['patient.card'].sudo().search([])
        values = {}
        values.update({
            'doctors': doctor,
            'patients': patient,
        })
        return request.render("hospital_management.online_appointment_form",
                              values)

    @http.route(['/appointment/submit/'], type='http', auth="user", website=True)
    def submit_appointment(self, **kwargs):
        request.env['doctor.appointment'].sudo().create({
            'appointment_name_id': kwargs.get('patient_name'),
            'appointment_doctor_id': kwargs.get('doctor_name'),
            'appointment_id': kwargs.get('patient_name'),
            'appointment_date': kwargs.get('date')
        })
        return request.render("hospital_management.appointment_form_success")

    @http.route(['/appointment/create'], type='http', auth="user", website=True)
    def create_form(self):
        return request.render("hospital_management.online_create_patient_form")

    @http.route(['/appointment/created/'], type='http', auth="user",
                website=True)
    def create_patient(self, **kwargs):
        customer = request.env['res.partner'].sudo().create({
            'display_name': kwargs.get('name'),
            'name': kwargs.get('name'),
            'gender': kwargs.get('gender'),
            'dob': kwargs.get('dob'),
            'mobile': kwargs.get('mobile')
        })
        patient_card = request.env['patient.card'].sudo().create({
            'patient_name_id': customer.id,
            'gender': kwargs.get('gender'),
            'dob': kwargs.get('dob'),
            'mob': kwargs.get('mobile')
        })

        values = {}
        values.update({
            'card_id': patient_card.patient
        })
        return request.render("hospital_management.card_number_form", values)
