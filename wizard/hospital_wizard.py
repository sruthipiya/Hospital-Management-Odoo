from odoo import models, fields
from odoo.exceptions import ValidationError
from odoo.tools import date_utils
import io
import json
from odoo.tools.misc import xlsxwriter


class HospitalWizard(models.TransientModel):
    _name = "hospital.wizard"
    _description = "Hospital wizard"

    from_date = fields.Datetime()
    to_date = fields.Datetime()
    patient_card_id = fields.Many2one('patient.card')
    name = fields.Many2one(related='patient_card_id.patient_name_id')
    doctor_id = fields.Many2one('hr.employee', domain="[('doct','=',True),]",
                                string="Doctor")
    disease_id = fields.Many2one('disease.details')
    department_id = fields.Many2one('hr.department')

    def action_generate(self):
        querry = """select res_partner.name as partner, patient_op.date_today,hr_employee.name as employee, hr_department.name as department, disease_details.name as disease
                                   from patient_card
                                    inner join res_partner
                                    on res_partner.id = patient_card.patient_name_id
                                    inner join patient_op
                                    on patient_op.name_id = patient_card.id
                                    inner join hr_employee
                                    on hr_employee.id = patient_op.doctor_op_id
                                    inner join hr_department
                                    on hr_department.id = hr_employee.department_id
                                    inner join patient_consultation
                                    on patient_consultation.card_details_id = patient_op.id
                                    inner join disease_details
                                    on disease_details.id = patient_consultation.disease where 1=1"""
        # print(self.patient_card_id)
        print(querry,'mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm')

        if self.patient_card_id:
            querry += """ and patient_card.id = '%s'""" % self.patient_card_id.id
        if self.doctor_id:
            querry += """ and patient_op.doctor_op_id = '%s'""" % self.doctor_id.id
        if self.from_date and self.to_date and self.from_date > self.to_date:
            raise ValidationError("From date must be less than To date ")
        if self.from_date and self.to_date:
            querry += """ and patient_op.date_today between '%s' and '%s'""" % (
                self.from_date, self.to_date)
        elif self.from_date:
            querry += """ and patient_op.date_today > '%s'""" % self.from_date
        elif self.to_date:
            querry += """ and patient_op.date_today <= '%s'""" % self.to_date
        if self.disease_id:
            querry += """ and patient_consultation.disease = '%s'""" % self.disease_id.id
        if self.department_id:
            querry += """ and hr_employee.department_id = '%s'""" % self.department_id.id
        self._cr.execute(querry)
        result = self._cr.dictfetchall()
        # print(result)
        data = {
            'model_id': self.id,
            'to_date': self.to_date,
            'from_date': self.from_date,
            'sequence': self.patient_card_id.patient,
            'name': self.name.name,
            'doctor': self.doctor_id.name,
            'disease': self.disease_id,
            'department': self.department_id,
            'data': result

        }
        return self.env.ref(
            'hospital_management.action_report_hospital_management').report_action(
            None, data=data)

    def action_generate_xlsx(self):
        # print('eeeeeeeeee', self)
        if self.from_date and self.to_date and self.from_date > self.to_date:
            raise ValidationError('Start Date must be less than End Date')
        data = {
            'model_id': self.id,
            'from_date': self.from_date,
            'to_date': self.to_date,
            'sequence': self.patient_card_id.patient,
            'name': self.name.name,
            'doctor': self.doctor_id.name,
            'disease': self.disease_id.id,
            'department': self.department_id.id,
        }
        return {
            'type': 'ir.actions.report',
            'data': {
                'model': 'hospital.wizard',
                'output_format': 'xlsx',
                'options': json.dumps(data, default=date_utils.json_default),
                'report_name': 'Excel Report',
            },
            'report_type': 'xlsx',

        }

    def get_xlsx_report(self, data, response):
        # print('inside last function0000000000', data)
        sequence = data['sequence']
        name = data['name']
        doctor = data['doctor']
        from_date = data['from_date']
        to_date = data['to_date']
        disease = data['disease']
        department = data['department']
        # print(sequence,name,doctor,from_date,to_date,disease,department)
        querry = """select res_partner.name as partner, patient_op.date_today,hr_employee.name as employee, hr_department.name as department, disease_details.name as disease
                                           from patient_card
                                            inner join res_partner
                                            on res_partner.id = patient_card.patient_name_id
                                            inner join patient_op
                                            on patient_op.name_id = patient_card.id
                                            inner join hr_employee
                                            on hr_employee.id = patient_op.doctor_op_id
                                            inner join hr_department
                                            on hr_department.id = hr_employee.department_id
                                            inner join patient_consultation
                                            on patient_consultation.card_details_id = patient_op.id
                                            inner join disease_details
                                            on disease_details.id = patient_consultation.disease_id where 1=1"""
        # print(querry,'000000000000000')

        # print(self.id)
        db = self.env['hospital.wizard'].search([])[-1]
        print(db)
        if sequence:
            querry += """ and patient_card.id = '%s'""" % db.patient_card_id.id
        if doctor:
            querry += """ and patient_op.doctor_op_id = '%s'""" % db.doctor_id.id
        if from_date and to_date:
            querry += """ and patient_op.date_today between '%s' and '%s'""" % (
                from_date, to_date)
        elif from_date:
            querry += """ and patient_op.date_today > '%s'""" % from_date
        elif to_date:
            querry += """ and patient_op.date_today <= '%s'""" % to_date
        if department:
            querry += """ and hr_employee.department_id = %s""" % db.department_id.id
        if disease:
            querry += """ and patient_consultation.disease_id = %s""" % db.disease_id.id

        self._cr.execute(querry)
        result = self._cr.dictfetchall()
        # print(result,'0000000000')
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '18px'})
        cell_format = workbook.add_format(
            {'font_size': '14px', 'align': 'center'})
        txt_head = workbook.add_format(
            {'align': 'center', 'bold': True, 'font_size': '10px'})
        txt = workbook.add_format({'font_size': '10px', 'align': 'center'})
        sheet.merge_range('B2:I3', 'EXCEL REPORT', head)
        sheet.set_column(1, 7, 20)
        sheet.write(11, 2, 'Serial No.', txt_head)
        sheet.write(11, 3, 'Date', txt_head)
        sheet.write(11, 4, 'Department', txt_head)
        sheet.write(11, 5, 'Disease', txt_head)
        val = 5
        if sequence:
            sheet.merge_range('A6:B6', 'Patient ID : ' + sequence, cell_format)
            sheet.merge_range('D6:E6', 'Patient : ' + name, cell_format)
        else:
            val += 1
            sheet.write(11, val, 'Patient', txt_head)
        if doctor:
            sheet.merge_range('A8:B8', 'Doctor : ' + doctor, cell_format)
        else:
            val += 1
            sheet.write(11, val, 'Doctor', txt_head)
        if from_date:
            sheet.merge_range('A10:B10', 'From : ' + from_date, cell_format)
        if to_date:
            sheet.merge_range('D10:E10', 'To : ' + to_date, cell_format)

        row = 12
        number = 1
        print(result)
        for res in result:
            sheet.write(row, 2, number, txt)
            sheet.write(row, 3, str(res['date_today']), txt)
            sheet.write(row, 4, res['department'], txt)
            sheet.write(row, 5, res['disease'], txt)
            i = 5
            if not sequence:
                i += 1
                sheet.write(row, i, res['partner'], txt)
            if not doctor:
                i += 1
                sheet.write(row, i, res['employee'], txt)
            row += 1
            number += 1

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
