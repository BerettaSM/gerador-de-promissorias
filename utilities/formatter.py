import datetime
import locale
from num2words import num2words

from utilities.validator import Validator


class Formatter:

    DATE_FORMAT = "%d/%m/%Y"

    @staticmethod
    def get_currency_value_in_full(value):
        if type(value) not in (int, float):
            raise TypeError('Invalid type for value. Expected is int or float.')
        return num2words(value, to='currency', lang='pt_BR')

    @staticmethod
    def get_date_from_string(date_string: str):
        if type(date_string) != str:
            raise TypeError('Invalid type for date. Expected is str.')
        if not Validator.is_valid_date_str(date_string):
            raise ValueError('Invalid date format. expected -> "DD/MM/YYYY"')
        return datetime.datetime.strptime(date_string, Formatter.DATE_FORMAT)

    @staticmethod
    def get_localized_date_in_full(date_string: str):
        if type(date_string) != str:
            raise TypeError('Invalid type for date. Expected is str.')
        if not Validator.is_valid_date_str(date_string):
            raise ValueError('Invalid date format. expected -> "DD/MM/YYYY"')
        day, month, year = date_string.split('/')
        date = Formatter.get_number_in_full(int(day))
        date += ' dia(s) do mês de '
        date += Formatter.get_localized_month_name(int(month))
        date += f' de {year}'
        return date

    @staticmethod
    def get_localized_month_name(month_num: int):
        if type(month_num) != int:
            raise TypeError('Invalid type for month_num. Expected is int.')
        if not 1 <= month_num <= 12:
            raise ValueError('Invalid value for month_num. Expected a int between 1 and 12.')
        locale.setlocale(locale.LC_ALL, "")
        d = datetime.datetime(year=1999, month=month_num, day=15)
        return d.strftime("%B")

    @staticmethod
    def get_number_in_full(number):
        if type(number) != int:
            raise TypeError('Invalid type for number. Expected is int.')
        return num2words(number, lang='pt_BR')

    @staticmethod
    def get_string_from_date(date: datetime.datetime):
        return date.strftime(Formatter.DATE_FORMAT)

    @staticmethod
    def format_cpf(cpf: str):
        if len(cpf) != 11:
            raise ValueError('cpf len should equal 11.')
        if not cpf.isdigit():
            raise ValueError('cpf should be only digits.')
        return cpf[:3] + '.' + cpf[3:6] + '.' + cpf[6:9] + '-' + cpf[9:]

    @staticmethod
    def to_locale_currency(value: float):
        if type(value) != float:
            raise TypeError('Invalid type for value. Expected is a float.')
        locale.setlocale(locale.LC_ALL, "")
        return locale.currency(value, grouping=True)
