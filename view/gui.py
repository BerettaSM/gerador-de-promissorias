import os
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

from PIL import ImageDraw, Image
from ttkthemes import ThemedTk

from definitions import MODEL_FILE
from utilities.promissory import PromissoryGenerator
from utilities.validator import Validator
from view.maker_frame import MakerFrame
from view.payee_frame import PayeeFrame
from view.promissory_frame import PromissoryFrame

# --- CONSTANTS ---
MAIN_FONT = ('Arial', 16)
PRINT_FONT_COLOR = (0, 0, 0)
UI_BG_COLOR = '#ffffff'
UI_LABEL_FONT_COLOR = '#000000'
ENTRY_BG_COLOR = '#c0c0c0'
USER_DESKTOP = os.path.join(os.environ['USERPROFILE'], 'desktop')
# -----------------


class GUI(ttk.Frame):

    def __init__(self, master):

        super().__init__(master)

        self.master: ThemedTk = master
        self.master.title('Gerador de Promissórias')
        # self.master.resizable(width=False, height=False)

        # icon = ImageTk.PhotoImage(Image.open(io.BytesIO(ICON)))
        # self.master.wm_iconphoto(False, icon)

        self.grid(row=0, column=0, sticky=N + W + E + S)
        self.configure(padding=30)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.promissory_frame = None
        self.payee_frame = None
        self.maker_frame = None
        self.buttons_frame = None
        self.generate_button = None

        self.warnings = []

        self.create_widgets()

    def create_widgets(self):

        # Setup
        self.promissory_frame = PromissoryFrame(self, MAIN_FONT)
        self.payee_frame = PayeeFrame(self, MAIN_FONT)
        self.maker_frame = MakerFrame(self, MAIN_FONT)

        self.promissory_frame.create_widgets()
        self.payee_frame.create_widgets()
        self.maker_frame.create_widgets()

        self.buttons_frame = ttk.Frame(self)
        self.generate_button = ttk.Button(self.buttons_frame, text='Gerar', command=self.proceed)

        # Position
        self.promissory_frame.grid(row=0, column=0)
        self.payee_frame.grid(row=1, column=0)
        self.maker_frame.grid(row=2, column=0)
        self.buttons_frame.grid(row=3, column=0)
        self.generate_button.grid(row=0, column=0)

        # Configure
        self.buttons_frame.grid(sticky=N+W+S+E)
        self.buttons_frame.grid_rowconfigure(0, weight=1)
        self.buttons_frame.grid_columnconfigure(0, weight=1)

        self.buttons_frame.configure(borderwidth=5, relief='groove')

        self.generate_button.grid(sticky=N+W+S+E)

        style = ttk.Style()

        style.configure('TButton', font=MAIN_FONT)

    def check_data_for_warnings(self, data):

        if not Validator.is_valid_cpf(data['payee_cpf']):
            self.warnings.append('CPF do Beneficiário aparenta não ser válido.')

        if not Validator.is_valid_cpf(data['maker_cpf']):
            self.warnings.append('CPF do Emitente aparenta não ser válido.')

    def proceed(self):

        self.warnings = []  # Remove errors

        data = self.get_data()

        for val in data.values():
            if not val:
                messagebox.showerror('Campo vazio', 'Não deixe nenhum campo vazio.')
                return

        for cpf in (data['payee_cpf'], data['maker_cpf']):
            if len(cpf) != 11:
                messagebox.showerror('CPF incompleto', 'Os CPFs precisam possuir 11 digitos.')
                return

        self.check_data_for_warnings(data)

        if self.warnings:
            warning_str = 'Avisos: \n'
            for n, warning in enumerate(self.warnings):
                warning_str += f'\n{n+1}) {warning}'
            warning_str += '\n\n Prosseguir mesmo assim?'
            cancel = not messagebox.askyesno('Aviso', warning_str)
            if cancel:
                return

        PromissoryGenerator.generate(data)

    def get_data(self):

        data = self.promissory_frame.get_data()
        data.update(self.payee_frame.get_data())
        data.update(self.maker_frame.get_data())

        return data
