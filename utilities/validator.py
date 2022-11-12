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
    def digit_or_null(value):
        return Validator.DIGIT_OR_NULL_REGEX.match(value) is not None

    @staticmethod
    def float_or_null(value):
        return Validator.FLOAT_OR_NULL_REGEX.match(value) is not None

    @staticmethod
    def is_valid_date_str(date: str):
        return Validator.DATE_REGEX.match(date) is not None

    @staticmethod
    def validate_cpf_cnpj_entry(value):
        return Validator.digit_or_null(value) and len(value) <= 14

    @staticmethod
    def validate_quantity(value):
        return Validator.digit_or_null(value) and int(value) <= 2000 if value != '' else True
