from tkinter import *
from tkinter import ttk

from tkcalendar import Calendar

from utilities.validator import Validator


class PromissoryFrame(ttk.Frame):

    PERIODICITY = ['Semanal', 'Quinzenal', 'Mensal', 'Bimensal', 'Trimensal']

    PERIODICITY_DICT = {
        'Semanal': ('days', 7),
        'Quinzenal': ('days', 15),
        'Mensal': ('months', 1),
        'Bimensal': ('months', 2),
        'Trimensal': ('months', 3)
    }

    def __init__(self, master, font_):
        super().__init__(master)

        self.font = font_

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid(sticky=N+W+S+E)

        self.due_date_calendar = None

        self.inner_frame = None
        self.quantity_entry = None
        self.value_entry = None

        self.frequency_var = None
        self.frequency_listbox = None

    def create_widgets(self):

        # Setup
        calendar_label = ttk.Label(self, text='Data do Primeiro Vencimento')
        self.due_date_calendar = Calendar(self, locale='pt_br', selectmode='day')

        self.inner_frame = ttk.Frame(self)

        quantity_label = ttk.Label(self.inner_frame, text='Nº de Promissórias:')
        self.quantity_entry = ttk.Entry(self.inner_frame, validate='key',
                                        validatecommand=(self.register(Validator.validate_quantity), '%P'))

        value_label = ttk.Label(self.inner_frame, text='Valor(R$):')
        self.value_entry = ttk.Entry(self.inner_frame, validate='key',
                                     validatecommand=(self.register(Validator.float_or_null), '%P'))

        frequency_label = ttk.Label(self, text="Frequência")
        self.frequency_var = StringVar(value=PromissoryFrame.PERIODICITY)
        self.frequency_listbox = Listbox(self, listvariable=self.frequency_var)

        # Position
        calendar_label.grid(row=0, column=0)
        self.due_date_calendar.grid(row=1, column=0)

        self.inner_frame.grid(row=2, column=0)

        quantity_label.grid(row=0, column=0)
        self.quantity_entry.grid(row=0, column=1)

        value_label.grid(row=1, column=0)
        self.value_entry.grid(row=1, column=1)

        frequency_label.grid(row=0, column=1)
        self.frequency_listbox.grid(row=1, column=1)

        # Configure
        self.inner_frame.grid(sticky=N+W+S+E)
        self.inner_frame.grid_rowconfigure(0, weight=1)
        self.inner_frame.grid_columnconfigure(0, weight=1)

        quantity_label.grid(sticky=E)
        self.quantity_entry.grid(sticky=S)
        value_label.grid(sticky=E)
        self.value_entry.grid(sticky=S)
        self.frequency_listbox.grid(sticky=N)

        calendar_label.configure(font=self.font)
        self.due_date_calendar.configure(font=self.font)

        quantity_label.configure(font=self.font)
        self.quantity_entry.configure(font=self.font)

        value_label.configure(font=self.font)
        self.value_entry.configure(font=self.font)

        frequency_label.configure(font=self.font)
        self.frequency_listbox.configure(font=self.font, width=8, height=5)

        for child in self.inner_frame.winfo_children():
            child.grid(pady=5, padx=10)
            if type(child) == ttk.Entry:
                child: ttk.Entry
                child.configure(justify='center', width=14)

        self.frequency_listbox.selection_set(2)

    def get_periodicity(self):
        try:
            curr_select_idx = self.frequency_listbox.curselection()[0]
        except IndexError:
            curr_select_idx = 2
        curr_select = PromissoryFrame.PERIODICITY[curr_select_idx]
        curr_select_data = PromissoryFrame.PERIODICITY_DICT[curr_select]
        return curr_select_data

    def get_data(self):

        if self.due_date_calendar is None:
            raise ValueError('Call .create_widgets() before calling this method.')

        return {
            'due_date': self.due_date_calendar.get_date(),
            'quantity': self.quantity_entry.get(),
            'value': self.value_entry.get(),
            'periodicity': self.get_periodicity()
        }
