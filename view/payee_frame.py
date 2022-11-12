from tkinter import *
from tkinter import ttk

from utilities.validator import Validator


class PayeeFrame(ttk.Frame):

    def __init__(self, master, font_):
        super().__init__(master)

        self.font = font_

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid(sticky=N + W + S + E)

        self.payee_name_entry = None
        self.payee_cpf_cnpj_entry = None
        self.payable_in_entry = None

    def create_widgets(self):

        # Setup
        payee_name_label = ttk.Label(self, text='Beneficiário: ')
        self.payee_name_entry = ttk.Entry(self)

        payee_cpf_label = ttk.Label(self, text='CPF/CNPJ: ')
        self.payee_cpf_cnpj_entry = ttk.Entry(self, validate='key',
                                              validatecommand=(self.register(Validator.validate_cpf_cnpj_entry), '%P'))

        payable_in_label = ttk.Label(self, text='Pagável em: ')
        self.payable_in_entry = ttk.Entry(self)

        # Position
        payee_name_label.grid(row=0, column=0, sticky=E + S)
        self.payee_name_entry.grid(row=0, column=1, sticky=S)

        payee_cpf_label.grid(row=1, column=0, sticky=E)
        self.payee_cpf_cnpj_entry.grid(row=1, column=1)

        payable_in_label.grid(row=2, column=0, sticky=E + N)
        self.payable_in_entry.grid(row=2, column=1, sticky=N)

        # Configure
        payee_name_label.configure(font=self.font)
        self.payee_name_entry.configure(font=self.font)

        payee_cpf_label.configure(font=self.font)
        self.payee_cpf_cnpj_entry.configure(font=self.font)

        payable_in_label.configure(font=self.font)
        self.payable_in_entry.configure(font=self.font)

        for child in self.winfo_children():
            child.grid(pady=5, padx=5)
            if type(child) == ttk.Entry:
                child: ttk.Entry
                child.configure(justify='center')

    def get_data(self):

        if self.payee_name_entry is None:
            raise ValueError('Call .create_widgets() before calling this method.')

        return {
            'payee_name': self.payee_name_entry.get(),
            'payee_cpf_cnpj': self.payee_cpf_cnpj_entry.get(),
            'payable_in': self.payable_in_entry.get()
        }
