from datetime import datetime as dt
from PIL import ImageFont

# max_len found out with PIL.ImageFont.getlength()


class WritableField:

    ANCHOR_MB = 'mb'
    ANCHOR_LB = 'lb'
    ANCHOR_LS = 'ls'
    ANCHOR_MS = 'ms'

    def __init__(self,
                 value: str,
                 primary_x_pos: int | float,
                 primary_y_pos: int | float,
                 anchor: str = ANCHOR_MB,
                 max_len: int | float | None = None,
                 wrap_x_pos: int | float | None = None,
                 wrap_y_pos: int | float | None = None,
                 wrap_max_len: int | float | None = None):

        self.value = value
        self.x = primary_x_pos
        self.y = primary_y_pos
        self.anchor = anchor
        self.max_len = max_len
        self.x_wrap = wrap_x_pos
        self.y_wrap = wrap_y_pos
        self.wrap_max_len = wrap_max_len  # TODO: Validate this somehow
        self._validate_state()

    def _validate_state(self):
        required_types = (float, int)
        if type(self.x) not in required_types or type(self.y) not in required_types:
            raise AttributeError('X and Y positions should be numbers.')
        if self.max_len is not None:
            if type(self.max_len) not in required_types:
                raise AttributeError('max_len should be a number.')
            if type(self.y_wrap) not in required_types or type(self.x_wrap) not in required_types:
                raise AttributeError('If max_len is provided, wrap_x_pos and wrap_y_pos should be numbers.')

        # TODO: Change validation to accomodate passing in only max_length and throw a warning if it exceeds max space.


class PromissoryImage:

    FONT = ImageFont.truetype(font='Roboto-Light.ttf', size=40)

    # TODO: Sort out writing the date and value in full

    def __init__(self, number, value, due_date, payee_name,
                 payee_cpf, payable_in, maker_name, maker_cpf, maker_address):

        today = dt.today()
        curr_day, curr_month, curr_year = today.strftime('%d/%m/%Y')

        # Promissory Frame
        self.number_field = WritableField(number, 560, 94)
        self.value = WritableField(value, 1830, 94)
        due_day, due_month, due_year = due_date.split('/')
        self.due_date = WritableField(due_day, 905, 94)
        self.due_month = WritableField(due_month, 1175, 94)
        self.due_year = WritableField(due_year, 1465, 94)
        # TODO: Sort out date in full
        self.due_date_in_full = WritableField(None, 500, 166, WritableField.ANCHOR_LB, 1487.0, 415, 241, 444.0)
        self.subject = WritableField('EI', 1090, 241)
        # TODO: Sort out value in full
        self.value_in_full = WritableField(None, 910, 400, WritableField.ANCHOR_LS, 1089.0, 415, 489, 1590.0)
        self.emission_day = WritableField(curr_day, 1713, 633, WritableField.ANCHOR_MS)
        self.emission_month = WritableField(curr_month, 1828, 633, WritableField.ANCHOR_MS)
        self.emission_year = WritableField(curr_year, 1950, 633, WritableField.ANCHOR_MS)

        # Payee Frame
        self.payee_name = WritableField(payee_name, 893, 316, max_len=906.0)
        self.payee_cpf = WritableField(payee_cpf, 1775, 316)
        self.payable_in = WritableField(payable_in, 1540, 562, WritableField.ANCHOR_MS, 913.0)

        # Maker Frame
        self.maker_name = WritableField(maker_name, 995, 633, WritableField.ANCHOR_MS, 773.0)
        self.maker_cpf = WritableField(maker_cpf, 843, 709, WritableField.ANCHOR_MS)
        self.maker_address = WritableField(maker_address, 1363, 709, WritableField.ANCHOR_LS, 621.0, 405, 779, 662.0)
