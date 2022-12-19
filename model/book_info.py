from odoo import models, fields


class ProductInfo(models.Model):
    _inherit = "product.product"

    is_book = fields.Boolean('Is Book', default=False)


class ProductSelect(models.Model):
    _name = "product.select"

    book_id = fields.Many2one('book.res')
    product_name_id = fields.Many2one('product.product', domain=[('is_book', '=', 'True')])
    description_id = fields.Char(string="Description", related='product_name_id.name')
    price = fields.Float(string="Price", related='product_name_id.list_price')
    def_code = fields.Char(string='Code', related='product_name_id.default_code')



