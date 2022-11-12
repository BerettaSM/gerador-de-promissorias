import re


class Validator:

    DATE_REGEX = re.compile(r"""
        ^((0[1-9])|([1-2]\d)|(3[0-1]))  # Day
        /                               # Separator
        ((0[1-9])|(1[0-2]))             # Month
        /                               # Separator
        (\d{4})$                        # Year
    """, re.VERBOSE)

    DIGIT_OR_NULL_REGEX = re.compile(r"^(?![\s\S])|(\d+)$")
    FLOAT_OR_NULL_REGEX = re.compile(r"^(?![\s\S])|(\d{1,8}),?(\d{1,2})?$")

    @staticmethod
    def digit_or_null(value: str):
        return Validator.DIGIT_OR_NULL_REGEX.match(value) is not None

    @staticmethod
    def float_or_null(value: str):
        return Validator.FLOAT_OR_NULL_REGEX.match(value) is not None

    @staticmethod
    def is_valid_date_str(date: str):
        return Validator.DATE_REGEX.match(date) is not None

    @staticmethod
    def validate_cpf_cnpj_entry(value: str):
        return Validator.digit_or_null(value) and len(value) <= 14

    @staticmethod
    def validate_quantity(value: str):
        return Validator.digit_or_null(value) and int(value) <= 2000 if value != '' else True

    @staticmethod
    def is_valid_cpf(cpf: str):
        if len(cpf) != 11:
            return False
        stem = cpf[:9]
        mult, res = 10, 0
        for digit in stem:
            res += int(digit) * mult
            mult -= 1
        rest = res % 11
        first_digit = 0 if rest < 2 else 11 - rest
        mult, res = 11, 0
        for digit in stem + str(first_digit):
            res += int(digit) * mult
            mult -= 1
        rest = res % 11
        second_digit = 0 if rest < 2 else 11 - rest
        return cpf[-2] == str(first_digit) and cpf[-1] == str(second_digit)

    @staticmethod
    def is_valid_cnpj(cnpj: str):
        if len(cnpj) != 14:
            return False
        stem, res = cnpj[:12], 0
        stem_mult = (6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)
        for digit, mult in zip(stem, stem_mult[1:]):
            res += int(digit) * mult
        rest, res = res % 11, 0
        first_digit = 0 if rest < 2 else 11 - rest
        for digit, mult in zip(stem + str(first_digit), stem_mult):
            res += int(digit) * mult
        rest = res % 11
        second_digit = 0 if rest < 2 else 11 - rest
        return cnpj[-2] == str(first_digit) and cnpj[-1] == str(second_digit)

    @staticmethod
    def is_valid_cpf_cnpj(cpf_cnpj: str):
        if len(cpf_cnpj) == 11:
            return Validator.is_valid_cpf(cpf_cnpj)
        elif len(cpf_cnpj) == 14:
            return Validator.is_valid_cnpj(cpf_cnpj)
        return False
