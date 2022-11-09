from tkinter import *
from tkinter import ttk

from tkcalendar import Calendar

from utilities.validator import Validator


class PromissoryFrame(ttk.Frame):

    def __init__(self, master, font_):
        super().__init__(master)

        self.font = font_

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid(sticky=N+W+S+E)

        self.configure(borderwidth=5, relief='groove')

        self.due_date_calendar = None

        self.inner_frame = None
        self.quantity_entry = None
        self.value_entry = None

    def create_widgets(self):

        # Setup
        calendar_label = ttk.Label(self, text='Data do Primeiro Vencimento')
        self.due_date_calendar = Calendar(self, locale='pt_br', selectmode='day')

        self.inner_frame = ttk.Frame(self)

        quantity_label = ttk.Label(self.inner_frame, text='Nº de Promissórias: ')
        self.quantity_entry = ttk.Entry(self.inner_frame, validate='key',
                                        validatecommand=(self.register(Validator.digit_or_null), '%P'))

        value_label = ttk.Label(self.inner_frame, text='Valor(R$): ')
        self.value_entry = ttk.Entry(self.inner_frame, validate='key',
                                     validatecommand=(self.register(Validator.digit_or_null), '%P'))

        # Position
        calendar_label.grid(row=0, column=0)
        self.due_date_calendar.grid(row=1, column=0)

        self.inner_frame.grid(row=2, column=0)

        quantity_label.grid(row=0, column=0)
        self.quantity_entry.grid(row=0, column=1)

        value_label.grid(row=1, column=0)
        self.value_entry.grid(row=1, column=1)

        # Configure
        self.inner_frame.grid(sticky=N+W+S+E)
        self.inner_frame.grid_rowconfigure(0, weight=1)
        self.inner_frame.grid_columnconfigure(0, weight=1)

        quantity_label.grid(sticky=E)
        self.quantity_entry.grid(sticky=E)
        value_label.grid(sticky=E)
        self.value_entry.grid(sticky=E)
        # TODO: Style the calendar
        calendar_label.configure(font=self.font)
        self.due_date_calendar.configure(font=self.font)

        quantity_label.configure(font=self.font)
        self.quantity_entry.configure(font=self.font)

        value_label.configure(font=self.font)
        self.value_entry.configure(font=self.font)

        for child in self.winfo_children():
            child.grid(pady=5)

        for child in self.inner_frame.winfo_children():
            child.grid(pady=5, padx=5)
            if type(child) == ttk.Entry:
                child: ttk.Entry
                child.configure(justify='center')

    def get_data(self):

        if self.due_date_calendar is None:
            raise ValueError('Call .create_widgets() before calling this method.')

        return {
            'due_date': self.due_date_calendar.get_date(),
            'quantity': self.quantity_entry.get(),
            'value': self.value_entry.get()
        }
