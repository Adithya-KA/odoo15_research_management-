from odoo import models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"
    is_scholar = fields.Boolean(string="Is Scholar")

    scholar_count = fields.Integer(compute="compute_count")

    def get_related_scholar(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Related Scholar',
            'view_mode': 'tree',
            'res_model': 'research.management',
            'domain': [('related_partner', '=', self.id)],
            'context': "{'create': False}"
        }

    def compute_count(self):
        for record in self:
            record.scholar_count = self.env['research.management']. \
                search_count([('related_partner', '=', self.id)])
