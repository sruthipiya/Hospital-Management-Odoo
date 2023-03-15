from odoo import models, fields


class DiseaseDetails(models.Model):
    _name = "disease.details"
    _description = "Disease Details"
    _rec_name = "name"

    name = fields.Char(string="Disease", required=True)

