from odoo import fields, models, api, _


class ResearchManagement(models.Model):
    _name = "research.management"
    _description = "Research Management"
    _rec_name = "fullname"

    sequence_no = fields.Char(string='Order Reference', required=True,
                              readonly=True, default=lambda self: _('New'))
    scholar_id = fields.Char(string="Scholar ID", required=True)
    res_institute = fields.Many2one('research.institute', string='Institute')
    first_name = fields.Char(required=True)
    middle_name = fields.Char()
    last_name = fields.Char(required=True)
    fullname = fields.Char('Name', compute='_compute_name', store="True")
    age = fields.Float(required=True)
    gender = fields.Selection(selection=[('male', 'Male'), ('female', 'Female'), ('others', 'Others')], default='male')
    related_partner = fields.Many2one(
        'res.partner', string='Related Partner', domain="[('is_company', '=', True)]")
    book_res_ids = fields.One2many("book.res", "scholar_book_ids")
    _sql_constraints = [
        ('unique_type', 'unique(scholar_id)', "Scholar ID cannot be duplicated!.")
    ]

    @api.depends('first_name', 'last_name')
    def _compute_name(self):
        for record in self:
            if self.middle_name:
                record.fullname = record.first_name + " " + record.middle_name + " " + record.last_name
            else:
                record.fullname = record.first_name + " " + record.last_name

    @api.model
    def create(self, vals):
        if vals.get('sequence_no', _('New')) == _('New'):
            vals['sequence_no'] = self.env['ir.sequence'].next_by_code(
                'research.management')
        res = super(ResearchManagement, self).create(vals)
        return res
