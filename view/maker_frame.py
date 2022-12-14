from tkinter import *
from tkinter import ttk

from utilities.validator import Validator


class MakerFrame(ttk.Frame):

    def __init__(self, master, font_):
        super().__init__(master)

        self.font = font_

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid(sticky=N + W + S + E)

        self.maker_name_entry = None
        self.maker_cpf_cnpj_entry = None
        self.maker_address_entry = None

    def create_widgets(self):

        # Setup
        maker_name_label = ttk.Label(self, text='Emitente: ')
        self.maker_name_entry = ttk.Entry(self)

        maker_cpf_label = ttk.Label(self, text='CPF/CNPJ: ')
        self.maker_cpf_cnpj_entry = ttk.Entry(self, validate='key',
                                              validatecommand=(self.register(Validator.validate_cpf_cnpj_entry), '%P'))

        maker_address_label = ttk.Label(self, text='Endereço: ')
        self.maker_address_entry = ttk.Entry(self)

        # Position
        maker_name_label.grid(row=0, column=0, sticky=E + S)
        self.maker_name_entry.grid(row=0, column=1, sticky=S)

        maker_cpf_label.grid(row=1, column=0, sticky=E)
        self.maker_cpf_cnpj_entry.grid(row=1, column=1)

        maker_address_label.grid(row=2, column=0, sticky=E + N)
        self.maker_address_entry.grid(row=2, column=1, sticky=N)

        # Configure
        maker_name_label.configure(font=self.font)
        self.maker_name_entry.configure(font=self.font)

        maker_cpf_label.configure(font=self.font)
        self.maker_cpf_cnpj_entry.configure(font=self.font)

        maker_address_label.configure(font=self.font)
        self.maker_address_entry.configure(font=self.font)

        for child in self.winfo_children():
            child.grid(pady=5, padx=5)
            if type(child) == ttk.Entry:
                child: ttk.Entry
                child.configure(justify='center')

    def get_data(self):

        if self.maker_name_entry is None:
            raise ValueError('Call .create_widgets() before calling this method.')

        return {
            'maker_name': self.maker_name_entry.get(),
            'maker_cpf_cnpj': self.maker_cpf_cnpj_entry.get(),
            'maker_address': self.maker_address_entry.get()
        }
