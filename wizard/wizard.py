from odoo import fields, models
from odoo.exceptions import ValidationError
import json
import io
import xlsxwriter
from odoo.tools import date_utils

class Wizard(models.TransientModel):
    _name = 'report.wizard'
    _description = 'wizard'

    report_mode = fields.Selection(selection=[('book', 'Book'), ('customer', 'Customer')], default='customer')
    from_date = fields.Datetime(string='From', default=fields.Datetime.now())
    to_date = fields.Datetime(string='To', default=fields.Datetime.now())
    book_id = fields.Many2many('product.product', domain=[('is_book', '=', 'True')], string='Book')
    customer_id = fields.Many2one('research.management', string='Customer')
    today_date = fields.Datetime()

# pdf report#################

    def action_print_report(self):
        if self.report_mode == 'customer':
            if self.from_date or self.to_date:
                self.today_date = False
            else:
                self.today_date = fields.Datetime.now()
            query = """select br.reference_no, tmpl.name, br.status, br.reserved_date
                        from book_res as br
                        inner join  product_select as ps
                        on ps.book_id = br.id
                        inner join product_product as pd
                        on pd.id = ps.product_name_id
                        inner join product_template as tmpl
                        on pd.product_tmpl_id = tmpl.id """
            if self.customer_id:
                query_a = """where br.scholar_book_ids = '%d' """ % self.customer_id.id
                query += query_a
            if self.from_date:
                query1 = """and br.reserved_date >= '%s' """ % self.from_date
                query += query1
            if self.to_date:
                query2 = """and br.reserved_date <= '%s' """ % self.to_date
                query += query2
            self.env.cr.execute(query)
            data_1 = self.env.cr.dictfetchall()
            if data_1 == []:
                raise ValidationError('There is no data for this customer on this date')
            data = {
                'from_date': self.from_date,
                'to_date': self.to_date,
                'customer_id': self.customer_id.fullname,
                'today': self.today_date,
                'data_1': data_1
            }
            return self.env.ref('research_management.action_cust_report').report_action(self, data=data)

        # book #
        if self.report_mode == 'book':
            if self.from_date or self.to_date:
                self.today_date = False
            else:
                self.today_date = fields.Datetime.now()
            if self.book_id:
                list1 = []
                list1.clear()
                for rec in self.book_id.product_tmpl_id:
                    query = """select br.reference_no, pt.name,rm.fullname,br.status,br.reserved_date
                                from book_res as br
                                inner join product_select as ps
                                on ps.book_id = br.id
                                inner join product_product as pd
                                on pd.id = ps.product_name_id
                                inner join product_template as pt
                                on pd.product_tmpl_id = pt.id
                                inner join research_management as rm
                                on br.scholar_book_ids = rm.id
                                where pt.id = '%d' """ % rec.id
                    if self.from_date:
                        query1 = """and br.reserved_date >= '%s' """ % self.from_date
                        query += query1
                    if self.to_date:
                        query2 = """and br.reserved_date <= '%s' """ % self.to_date
                        query += query2
                    self.env.cr.execute(query)
                    data_1 = self.env.cr.dictfetchall()
                    if data_1 == []:
                        raise ValidationError('Please enter data in the book field on this date')
                    list1.append(data_1)
                    print("BOOK: ", list1)
                    data = {
                        'from_date': self.from_date,
                        'to_date': self.to_date,
                        'today': self.today_date,
                        'data_1': list1
                    }
            else:
                list1 = []
                list1.clear()
                query = """select br.reference_no, pt.name,rm.fullname,br.status,br.reserved_date
                                                from book_res as br
                                                inner join product_select as ps
                                                on ps.book_id = br.id
                                                inner join product_product as pd
                                                on pd.id = ps.product_name_id
                                                inner join product_template as pt
                                                on pd.product_tmpl_id = pt.id
                                                inner join research_management as rm
                                                on br.scholar_book_ids = rm.id """
                if self.from_date:
                    query1 = """where br.reserved_date >= '%s' """ % self.from_date
                    query += query1
                if self.to_date:
                    query2 = """and br.reserved_date <= '%s' """ % self.to_date
                    query += query2
                self.env.cr.execute(query)
                data_1 = self.env.cr.dictfetchall()
                if data_1 == []:
                    raise ValidationError('Please enter data in the book field on this date')
                list1.append(data_1)
                data = {
                    'from_date': self.from_date,
                    'to_date': self.to_date,
                    'today': self.today_date,
                    'data_1': list1
                }
            return self.env.ref('research_management.action_book_report').report_action(self, data=data)

    # excel ##########################

    def action_print_report_XL(self):
        if self.report_mode == 'customer':
            if self.from_date or self.to_date:
                self.today_date = False
            else:
                self.today_date = fields.Datetime.now()
            query = """select br.reference_no, tmpl.name, br.status, br.reserved_date
                        from book_res as br
                        inner join  product_select as ps
                        on ps.book_id = br.id
                        inner join product_product as pd
                        on pd.id = ps.product_name_id
                        inner join product_template as tmpl
                        on pd.product_tmpl_id = tmpl.id """
            if self.customer_id:
                query_a = """where br.scholar_book_ids = '%d' """ % self.customer_id.id
                query += query_a
            if self.from_date:
                query1 = """and br.reserved_date >= '%s' """ % self.from_date
                query += query1
            if self.to_date:
                query2 = """and br.reserved_date <= '%s' """ % self.to_date
                query += query2
            self.env.cr.execute(query)
            data_1 = self.env.cr.dictfetchall()
            if data_1 == []:
                raise ValidationError('There is no data for this customer on this date')
            data = {
                'c_from_date': self.from_date,
                'c_to_date': self.to_date,
                'customer_id': self.customer_id.fullname,
                'c_today': self.today_date,
                'c_data_1': data_1
            }
            return {
                'type': 'ir.actions.report',
                'data': {'model': 'report.wizard',
                         'options': json.dumps(data, default=date_utils.json_default),
                         'output_format': 'xlsx',
                         'report_name': 'Scholar Report',
                         },
                'report_type': 'xlsx',
            }
        # book#

        if self.report_mode == 'book':
            if self.from_date or self.to_date:
                self.today_date = False
            else:
                self.today_date = fields.Datetime.now()
            if self.book_id:
                list1 = []
                list1.clear()
                for rec in self.book_id.product_tmpl_id:
                    query = """select br.reference_no, pt.name,rm.fullname,br.status,br.reserved_date
                                from book_res as br
                                inner join product_select as ps
                                on ps.book_id = br.id
                                inner join product_product as pd
                                on pd.id = ps.product_name_id
                                inner join product_template as pt
                                on pd.product_tmpl_id = pt.id
                                inner join research_management as rm
                                on br.scholar_book_ids = rm.id
                                where pt.id = '%d' """ % rec.id
                    if self.from_date:
                        query1 = """and br.reserved_date >= '%s' """ % self.from_date
                        query += query1
                    if self.to_date:
                        query2 = """and br.reserved_date <= '%s' """ % self.to_date
                        query += query2
                    self.env.cr.execute(query)
                    data_1 = self.env.cr.dictfetchall()
                    if data_1 == []:
                        raise ValidationError('Please enter data in the book field on this date')
                    list1.append(data_1)
                    print("BOOK: ", list1)
                    data = {
                        'from_date': self.from_date,
                        'to_date': self.to_date,
                        'today': self.today_date,
                        'data_1': list1
                    }
            else:
                list1 = []
                list1.clear()
                query = """select br.reference_no, pt.name,rm.fullname,br.status,br.reserved_date
                                                from book_res as br
                                                inner join product_select as ps
                                                on ps.book_id = br.id
                                                inner join product_product as pd
                                                on pd.id = ps.product_name_id
                                                inner join product_template as pt
                                                on pd.product_tmpl_id = pt.id
                                                inner join research_management as rm
                                                on br.scholar_book_ids = rm.id """
                if self.from_date:
                    query1 = """where br.reserved_date >= '%s' """ % self.from_date
                    query += query1
                if self.to_date:
                    query2 = """and br.reserved_date <= '%s' """ % self.to_date
                    query += query2
                self.env.cr.execute(query)
                data_1 = self.env.cr.dictfetchall()
                if data_1 == []:
                    raise ValidationError('Please enter data in the book field on this date')
                list1.append(data_1)
                data = {
                    'from_date': self.from_date,
                    'to_date': self.to_date,
                    'today': self.today_date,
                    'data_1': list1
                }
            return {
                'type': 'ir.actions.report',
                'data': {'model': 'report.wizard',
                         'options': json.dumps(data, default=date_utils.json_default),
                         'output_format': 'xlsx',
                         'report_name': 'Scholar Report',
                         },
                'report_type': 'xlsx',
            }

    def get_xlsx_report(self, data, response):
        # buffer'output'for writing data into excel
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet()
        table_name = workbook.add_format({'align': 'center', 'bold': True, 'font_size': '20px'})
        scholar_name = workbook.add_format({'align': 'center', 'bold': True, 'font_size': '15px'})
        col_name = workbook.add_format({'align': 'center', 'bold': True, 'font_size': '13px'})
        date = workbook.add_format({'align': 'center', 'bold': True, 'font_size': '10px'})
        date_label = workbook.add_format({'align': 'right', 'bold': True, 'font_size': '10px'})
        sheet.merge_range('C1:D2', 'Reserved List', table_name)
        if data.get('customer_id'):
            if data['customer_id']:
                sheet.write(3, 1, 'Scholar: ', date_label)
                sheet.merge_range('C4:D4', data['customer_id'], scholar_name)
        if data.get('c_from_date'):
            if data['c_from_date']:
                sheet.write(4, 1, 'From: ', date_label)
                sheet.merge_range('C5:D5', data['c_from_date'], date)
        if data.get('c_to_date'):
            if data['c_to_date']:
                sheet.write(5, 1, 'To: ', date_label)
                sheet.merge_range('C6:D6', data['c_to_date'], date)
        if data.get('c_today'):
            if data['c_today']:
                sheet.write(4, 1, 'Date: ', date_label)
                sheet.merge_range('C5:D5', data['c_today'], date)

        if data.get('from_date'):
            if data['from_date']:
                sheet.write(3, 1, 'From: ', date_label)
                sheet.merge_range('C4:D4', data['from_date'], date)
        if data.get('to_date'):
            if data['to_date']:
                sheet.write(4, 1, 'To: ', date_label)
                sheet.merge_range('C5:D5', data['to_date'], date)
        if data.get('today'):
            if data['today']:
                sheet.write(3, 1, 'Date: ', date_label)
                sheet.merge_range('C4:D4', data['today'], date)
    ######################################################################
        sheet.set_column('A:A', 20)
        sheet.set_column('B:B', 20)
        sheet.set_column('C:C', 20)
        sheet.set_column('D:D', 20)
        sheet.set_column('E:E', 20)
        sheet.set_column('F:F', 20)
        sheet.set_column('G:G', 20)
        sheet.set_column('H:H', 20)
        sheet.set_column('I:I', 20)
        sheet.set_column('J:J', 20)
        if data.get('c_data_1'):
            c_data_1 = data.get('c_data_1')
            if c_data_1:
                row = 8
                col = 0
                sheet.write(row, col, 'Sl No.', col_name)
                sheet.write(row, col + 1, 'Order Reference', col_name)
                sheet.write(row, col + 2, 'Product', col_name)
                sheet.write(row, col + 3, 'Status', col_name)
                sheet.write(row, col + 4, 'Date', col_name)
                rows = 8
                cols = 0
                sl = 0
                for rec in c_data_1:
                    rows = rows + 1
                    sl = sl + 1
                    sheet.write(rows, cols, sl)
                    sheet.write(rows, cols + 1, rec.get('reference_no'))
                    sheet.write(rows, cols + 2, rec.get('name'))
                    sheet.write(rows, cols + 3, rec.get('status'))
                    sheet.write(rows, cols + 4, rec.get('reserved_date'))
        if data.get('data_1'):
            data_1 = data.get('data_1')
            print(data_1)
            if data_1:
                row = 8
                col = 0
                sheet.write(row, col, 'SL.No', col_name)
                sheet.write(row, col + 1, 'Order Reference', col_name)
                sheet.write(row, col + 2, 'Scholar', col_name)
                sheet.write(row, col + 3, 'Product', col_name)
                sheet.write(row, col + 4, 'Status', col_name)
                sheet.write(row, col + 5, 'Date', col_name)
                rows = 8
                cols = 0
                sl = 0
                for i in data_1:
                    for rec in i:
                        rows = rows + 1
                        sl = sl + 1
                        sheet.write(rows, cols, sl)
                        sheet.write(rows, cols + 1, rec.get('reference_no'))
                        sheet.write(rows, cols + 2, rec.get('fullname'))
                        sheet.write(rows, cols + 3, rec.get('name'))
                        sheet.write(rows, cols + 4, rec.get('status'))
                        sheet.write(rows, cols + 5, rec.get('reserved_date'))
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()
