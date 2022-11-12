import os
import sys
import datetime
import locale

from num2words import num2words

from utilities.validator import Validator


class DateUtils:

    DATE_FORMAT = "%d/%m/%Y"

    @staticmethod
    def get_formatted_today_string():
        today = datetime.datetime.today()
        return DateUtils.get_string_from_date(today)

    @staticmethod
    def get_date_from_string(date_string: str):
        if type(date_string) != str:
            raise TypeError('Invalid type for date. Expected is str.')
        if not Validator.is_valid_date_str(date_string):
            raise ValueError('Invalid date format. expected -> "DD/MM/YYYY"')
        return datetime.datetime.strptime(date_string, DateUtils.DATE_FORMAT)

    @staticmethod
    def get_localized_date_in_full(date_string: str):
        if type(date_string) != str:
            raise TypeError('Invalid type for date. Expected is str.')
        if not Validator.is_valid_date_str(date_string):
            raise ValueError('Invalid date format. expected -> "DD/MM/YYYY"')
        day, month, year = date_string.split('/')
        date = Formatter.get_number_in_full(int(day))
        date += ' dia(s) do mês de '
        date += DateUtils.get_localized_month_name(int(month))
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
    def get_string_from_date(date: datetime.datetime):
        return date.strftime(DateUtils.DATE_FORMAT)


class Formatter:

    @staticmethod
    def get_number_in_full(number: int):
        if type(number) != int:
            raise TypeError('Invalid type for number. Expected is int.')
        return num2words(number, lang='pt_BR')

    @staticmethod
    def format_cpf_cnpj(cpf_cnpj: str):
        if type(cpf_cnpj) != str:
            raise TypeError('cpf should be a string.')
        if not cpf_cnpj.isdigit():
            raise ValueError('cpf should be only digits.')
        if len(cpf_cnpj) == 11:  # CPF
            return cpf_cnpj[:3] + '.' + cpf_cnpj[3:6] + '.' + cpf_cnpj[6:9] + '-' + cpf_cnpj[9:]
        elif len(cpf_cnpj) == 14:  # CNPJ
            return cpf_cnpj[:2] + '.' + cpf_cnpj[2:5] + '.' + cpf_cnpj[5:8] + '/' + cpf_cnpj[8:12] + '-' + cpf_cnpj[12:]
        raise ValueError('cpf_cnpj arg should have len of 11 or 14.')


class NumberUtils:

    @staticmethod
    def get_currency_value_in_full(value: int | float):
        if type(value) not in (int, float):
            raise TypeError('Invalid type for value. Expected is int or float.')
        return num2words(value, to='currency', lang='pt_BR')

    @staticmethod
    def to_locale_currency(value: float):
        if type(value) != float:
            raise TypeError('Invalid type for value. Expected is a float.')
        locale.setlocale(locale.LC_ALL, "")
        return locale.currency(value, grouping=True)


def get_true_filepath(filepath):
    try:
        base_path = sys._MEIPASS
        filepath = os.path.basename(filepath)
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, filepath)
