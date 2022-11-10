from datetime import datetime

from PIL import ImageFont, ImageDraw, Image
from dateutil.relativedelta import relativedelta

from definitions import FONT_FILE, MODEL_FILE
from utilities.utils import Formatter, NumberUtils, DateUtils

FONT = ImageFont.truetype(font=FONT_FILE, size=40)


class WritableField:

    ANCHOR_MB = 'mb'
    ANCHOR_LB = 'lb'
    ANCHOR_LS = 'ls'
    ANCHOR_MS = 'ms'

    def __init__(self,
                 first_line_text: str,
                 first_line_x_pos: int | float,
                 first_line_y_pos: int | float,
                 anchor: str = ANCHOR_MB,
                 first_line_max_len: int | float | None = None,
                 second_line_x_pos: int | float | None = None,
                 second_line_y_pos: int | float | None = None,
                 second_line_max_len: int | float | None = None,
                 pad_with_dashes=False):

        self.first_line_text: str = first_line_text
        self.second_line_text: str | None = None
        self.first_line_x_pos: int | float = first_line_x_pos
        self.first_line_y_pos: int | float = first_line_y_pos
        self.anchor = anchor
        self.first_line_max_len: int | float | None = first_line_max_len
        self.second_line_x_pos = second_line_x_pos
        self.second_line_y_pos = second_line_y_pos
        self.second_line_max_len: int | float | None = second_line_max_len
        self._validate_state()
        self._resolve_line_breaks()
        if pad_with_dashes:
            self._apply_dash_padding()

    def write_on_model(self, model: ImageDraw.ImageDraw):
        xy = (self.first_line_x_pos, self.first_line_y_pos)
        model.text(xy, str(self.first_line_text), anchor=self.anchor, font=FONT, fill='black')
        if self.second_line_text:
            wrap_xy = (self.second_line_x_pos, self.second_line_y_pos)
            model.text(wrap_xy, str(self.second_line_text), anchor=self.anchor, font=FONT, fill='black')

    def _apply_dash_padding(self):
        dash_length = FONT.getlength('  -')
        value_len = FONT.getlength(self.first_line_text)
        if not self.second_line_text:
            first_line_dif = self.first_line_max_len - value_len
            while first_line_dif > dash_length:
                self.first_line_text += '  -'
                first_line_dif -= dash_length
        if self.second_line_max_len:
            wrap_value = '' if self.second_line_text is None else self.second_line_text
            wrap_len = FONT.getlength(wrap_value)
            second_line_dif = self.second_line_max_len - wrap_len
            while second_line_dif > dash_length:
                wrap_value += '  -'
                second_line_dif -= dash_length
            self.second_line_text = wrap_value

    def _resolve_line_breaks(self):
        if self.first_line_max_len and FONT.getlength(self.first_line_text) >= self.first_line_max_len:
            split_val = self.first_line_text.split()
            word_idx = -1
            while FONT.getlength(' '.join(split_val[:word_idx])) > self.first_line_max_len:
                word_idx -= 1
            value = ' '.join(split_val[:word_idx])
            wrap_value = ' '.join(split_val[word_idx:])
            self.first_line_text = value
            self.second_line_text = wrap_value

    def _validate_state(self):
        required_types = (float, int)
        if type(self.first_line_x_pos) not in required_types or type(self.first_line_y_pos) not in required_types:
            raise TypeError('X and Y positions should be numbers.')
        if self.first_line_max_len is not None:
            if type(self.first_line_max_len) not in required_types:
                raise TypeError('first_line_max_len should be a number.')
            if type(self.second_line_x_pos) not in required_types and \
                    type(self.second_line_y_pos) not in required_types:
                raise ValueError('if first_line_max_len is provided, so should second_line_x_pos and second_line_y_pos')


class PromissoryImage:

    def __init__(self, number, value, due_date, payee_name,
                 payee_cpf, payable_in, maker_name, maker_cpf, maker_address):

        # Promissory Frame
        self.number_field = WritableField(number, 560, 94)
        formatted_value = NumberUtils.to_locale_currency(float(value))
        self.value = WritableField(formatted_value, 1830, 94)

        due_day, due_month_num, due_year = due_date.split('/')
        due_month = DateUtils.get_localized_month_name(int(due_month_num)).upper()
        self.due_date = WritableField(due_day, 905, 94)
        self.due_month = WritableField(due_month, 1175, 94)
        self.due_year = WritableField(due_year, 1465, 94)

        due_date_in_full = DateUtils.get_localized_date_in_full(due_date)
        self.due_date_in_full = WritableField(due_date_in_full, 500, 166,
                                              WritableField.ANCHOR_LB, 1487.0, 415, 241, 444.0)
        self.subject = WritableField('EI', 1090, 241)

        value_in_full = NumberUtils.get_currency_value_in_full(float(value)).upper()
        self.value_in_full = WritableField(value_in_full, 910, 400, WritableField.ANCHOR_LS,
                                           1089.0, 415, 489, 1590.0, pad_with_dashes=True)

        today = datetime.today()
        curr_day, curr_month, curr_year = today.strftime(DateUtils.DATE_FORMAT).split('/')
        self.emission_day = WritableField(curr_day, 1713, 633, WritableField.ANCHOR_MS)
        self.emission_month = WritableField(curr_month, 1828, 633, WritableField.ANCHOR_MS)
        self.emission_year = WritableField(curr_year, 1950, 633, WritableField.ANCHOR_MS)

        # Payee Frame
        self.payee_name = WritableField(payee_name.title(), 893, 316)
        formatted_payee_cpf = Formatter.format_cpf(payee_cpf)
        self.payee_cpf = WritableField(formatted_payee_cpf, 1775, 316)
        self.payable_in = WritableField(payable_in.title(), 1540, 562, WritableField.ANCHOR_MS)

        # Maker Frame
        self.maker_name = WritableField(maker_name.title(), 995, 633, WritableField.ANCHOR_MS)
        formatted_maker_cpf = Formatter.format_cpf(maker_cpf)
        self.maker_cpf = WritableField(formatted_maker_cpf, 843, 709, WritableField.ANCHOR_MS)
        self.maker_address = WritableField(maker_address.title(), 1363, 709, WritableField.ANCHOR_LS,
                                           621.0, 405, 779, 662.0)

    def write_on_model(self, model: ImageDraw.ImageDraw):
        for field in self.__dict__.values():
            if type(field) == WritableField:
                field: WritableField
                field.write_on_model(model)


class PromissoryGenerator:

    @staticmethod
    def generate_from(data, gui):
        quantity = int(data['quantity'])
        if quantity < 1:
            raise ValueError('Value "quantity" should be greater than zero.')
        loading_bar_increment = 100 / quantity
        loading_bar_curr_value = 0
        promissory_images = []
        first_due_date = DateUtils.get_date_from_string(data['due_date'])
        for n in range(quantity):
            due_date = first_due_date + relativedelta(months=n)
            promissory_model = Image.open(MODEL_FILE)
            editable_model = ImageDraw.Draw(promissory_model)
            promissory = PromissoryImage(
                f'{n+1:02}/{quantity:02}',
                data['value'],
                DateUtils.get_string_from_date(due_date),
                data['payee_name'],
                data['payee_cpf'],
                data['payable_in'],
                data['maker_name'],
                data['maker_cpf'],
                data['maker_address']
            )
            promissory.write_on_model(editable_model)
            promissory_images.append(promissory_model)
            loading_bar_curr_value += loading_bar_increment
            gui.loading_bar['value'] = loading_bar_curr_value
            gui.generate_button.configure(text=f'{loading_bar_curr_value:.2f}%')
            gui.master.update_idletasks()
        gui.loading_bar.stop()
        return promissory_images
