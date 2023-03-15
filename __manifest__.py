{
    'name': 'Hospital Management',
    'version': '16.0.1.0.0',
    'category': 'Hospital Management',
    'summary': 'Managing all operations in a hospital',
    'sequence': -1,
    'installable': True,
    'application': True,
    'depends': ['base', 'contacts', 'hr', 'account', 'website'],
    'data': ['security/hospital_security.xml',
             'security/ir.model.access.csv',
             'wizard/hospital_wizard.xml',
             'report/reports.xml',
             'views/patient_details.xml',
             'views/patient_card.xml',
             'views/patient_op.xml',
             'views/patient_consultation.xml',
             'views/disease.xml',
             'views/doctor_appointment.xml',
             'views/appointment_form.xml',
             'views/website_menu.xml',
             'views/hospital_menu.xml',
             'views/confirmation_form.xml',
             'views/create_patient.xml',
             'views/card_number.xml',
             ],
    'assets': {
        'web.assets_backend': [
            'hospital_management/static/src/js/hospital_report.js'
        ]
    },
}
