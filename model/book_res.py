from odoo import fields, models, api, _

class BookRes(models.Model):
    _name = "book.res"
    _description = "Book reservation"
    _rec_name = "reference_no"

    reference_no = fields.Char(string='Order Reference', required=True,
                               readonly=True, default=lambda self: _('New'))

    scholar_book_ids = fields.Many2one("research.management", string="Scholars")
    reserved_date = fields.Datetime(string='Reserved On', default=fields.Datetime.now())
    # ############################################
    product_ids = fields.One2many("product.select", 'book_id')
    product_name_ids = fields.One2many("product.select", 'product_name_id')
    description_id = fields.Char(string="Description")
    price = fields.Float(string="Price")
    def_code = fields.Char(string="Product code")
    # ############################################
    responsible_id = fields.Many2one('res.users', 'Responsible', default=lambda self: self.env.user)
    book_reservation_ids = fields.One2many('sale.order', 'book_reservation_id')
    status = fields.Selection(string="Status", copy=False,
                              selection=[('draft', 'Draft'), ('submitted', 'Submitted'), ('approved', 'Approved'),
                                         ('invoiced', 'Invoiced'), ('rejected', 'Rejected')], default='draft')
    create_invoice = fields.Char(string="Create Invoice")
    is_visibility = fields.Boolean(string="Visibility")

    @api.model
    def create(self, vals):
        if vals.get('reference_no', _('New')) == _('New'):
            vals['reference_no'] = self.env['ir.sequence'].next_by_code(
                'book.res')
        res = super(BookRes, self).create(vals)
        return res

    def button_submitted(self):
        self.write({
            'status': "submitted"
        })

    def button_approved(self):
        self.write({
            'status': "approved"
        })

    def button_rejected(self):
        self.write({
            'status': "rejected"
        })

    def invoice_smart_tab(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'context': "{'create': False}"
        }

    def button_invoice(self):
        self.is_visibility = True

        self.write({'status': "invoiced"})
        reserve = self.product_ids.product_name_id
        invoice = self.env['account.move'].create([
            {
                'move_type': 'out_invoice',
                'partner_id': self.scholar_book_ids.related_partner.id,
                'ref': self.reference_no,
                'invoice_date': fields.date.today(),
                'invoice_line_ids': [(0, 0, {
                    'product_id': i.id,
                    'name': i.name,
                    'quantity': 1,
                    'price_unit': i.list_price,
                }) for i in reserve],
            }])
        return {
            'res_model': 'account.move',
            'res_id': invoice.id,
            'view_mode': 'form',
            'view_type': 'form',
            'type': 'ir.actions.act_window',

        }
