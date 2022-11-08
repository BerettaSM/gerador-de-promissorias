class Formatter:

    @staticmethod
    def format_cpf(cpf: str):

        if len(cpf) != 11:
            raise ValueError('cpf len should equal 11.')

        if not cpf.isdigit():
            raise ValueError('cpf should digits only.')

        return cpf[:3] + '.' + cpf[3:6] + '.' + cpf[6:9] + '-' + cpf[9:]
