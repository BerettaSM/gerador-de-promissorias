import datetime
import locale
from num2words import num2words


class Writer:

    @staticmethod
    def get_localized_date_in_full(date):
        day, month, year = date.split('/')
        date = Writer.get_number_in_full(int(day))
        date += ' dia(s) do mês de '
        date += Writer.get_localized_month_name(int(month))
        date += f' de {year}'
        return date

    @staticmethod
    def get_currency_value_in_full(value):
        return num2words(value, to='currency', lang='pt_BR')

    @staticmethod
    def get_localized_month_name(month_num):
        locale.setlocale(locale.LC_ALL, "")
        d = datetime.datetime(year=1999, month=month_num, day=31)
        return d.strftime("%B")

    @staticmethod
    def get_number_in_full(number):
        return num2words(number, lang='pt_BR')
