import re

date_regex = re.compile(r"""
    ^((0[1-9])|([1-2]\d)|(3[0-1]))  # Day
    /                               # Separator
    ((0[1-9])|(1[0-2]))             # Month
    /                               # Separator
    (\d{4})$                        # Year
""", re.VERBOSE)

digit_or_null_regex = re.compile(r"^(?![\s\S])|(\d+)$")


class Validator:

    @staticmethod
    def digit_only(value):
        return value.isdigit()

    @staticmethod
    def digit_or_null(value):
        return digit_or_null_regex.match(value) is not None

    @staticmethod
    def validate_cpf(value):
        return Validator.digit_or_null(value) and len(value) <= 11

    @staticmethod
    def is_valid_cpf(cpf: str):
        if len(cpf) != 11:
            return False
        compare_section = str(cpf)[:9]
        result, mult = 0, 10
        for digit in compare_section:
            result += int(digit) * mult
            mult -= 1
        rest = result % 11
        first_digit = 0 if rest < 2 else 11 - rest
        result, mult = 0, 11
        for digit in compare_section + str(first_digit):
            result += int(digit) * mult
            mult -= 1
        rest = result % 11
        second_digit = 0 if rest < 2 else 11 - rest
        return cpf[-2] == str(first_digit) and cpf[-1] == str(second_digit)
