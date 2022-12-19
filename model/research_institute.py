from odoo import fields, models

class ResearchInstitute(models.Model):
    _name = "research.institute"
    _rec_name = 'institute'
    _description = "Research Management Institutes"

    institute = fields.Char()
    institute_id = fields.One2many("research.management", "res_institute")
    course = fields.Selection(selection=[('cyber security', 'Cyber Security'),
                                         ('language learning', 'Language Learning'),
                                         ('arts and humanities', 'Arts and Humanities'),
                                         ('business', 'Business'),
                                         ('data science', 'Data Science')])
    location = fields.Char(required=True)
