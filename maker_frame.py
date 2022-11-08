from tkinter import *
from tkinter import ttk

from validator import Validator


class MakerFrame(ttk.Frame):

    def __init__(self, master, font_):
        super().__init__(master)

        self.font = font_

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid(sticky=N + W + S + E)

        self.configure(borderwidth=5, relief='groove')

        self.maker_name_entry = None
        self.maker_cpf_entry = None
        self.maker_address_entry = None

    def create_widgets(self):

        # Setup
        maker_name_label = ttk.Label(self, text='Nome do Emitente: ')
        self.maker_name_entry = ttk.Entry(self)

        maker_cpf_label = ttk.Label(self, text='Nº CPF do Emitente: ')
        self.maker_cpf_entry = ttk.Entry(self, validate='key',
                                         validatecommand=(self.register(Validator.validate_cpf), '%P'))

        maker_address_label = ttk.Label(self, text='Endereço do Emitente: ')
        self.maker_address_entry = ttk.Entry(self)

        # Position
        maker_name_label.grid(row=0, column=0, sticky=E)
        self.maker_name_entry.grid(row=0, column=1)

        maker_cpf_label.grid(row=1, column=0, sticky=E)
        self.maker_cpf_entry.grid(row=1, column=1)

        maker_address_label.grid(row=2, column=0, sticky=E)
        self.maker_address_entry.grid(row=2, column=1)

        # Configure
        maker_name_label.configure(font=self.font)
        self.maker_name_entry.configure(font=self.font)

        maker_cpf_label.configure(font=self.font)
        self.maker_cpf_entry.configure(font=self.font)

        maker_address_label.configure(font=self.font)
        self.maker_address_entry.configure(font=self.font)

        for child in self.winfo_children():
            child.grid(pady=5, padx=5)

    def get_data(self):

        if self.maker_name_entry is None:
            raise ValueError('Call .create_widgets() before calling this method.')

        return {
            'maker_name': self.maker_name_entry.get(),
            'maker_cpf': self.maker_cpf_entry.get(),
            'maker_address': self.maker_address_entry.get()
        }
