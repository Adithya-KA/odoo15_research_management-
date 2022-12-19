from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    book_reservation_id = fields.Many2one('book.res')

    @api.onchange('book_reservation_id')
    def onchange_book_reservation_id(self):
        self.order_line = False
        x = self.env['book.res'].search([])
        for rec in x:
            print(rec.scholar_book_ids)
            if rec.scholar_book_ids == self.book_reservation_id.scholar_book_ids:
                sale_partner_id = self.book_reservation_id.scholar_book_ids.related_partner
                self.partner_id = sale_partner_id.id
        reserve = self.book_reservation_id.product_ids
        for i in reserve:
            product = i.product_name_id
            print(product)
            self.write({
                'order_line': [
                    (0, 0, {
                        'product_id': product.id,
                        'name': product.name,
                        'product_uom_qty': 1,
                        'price_unit': i.price,
                    })
                ]
            })
