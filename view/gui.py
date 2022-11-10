from secrets import token_hex
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

from ttkthemes import ThemedTk

from utilities.promissory import PromissoryGenerator
from utilities.save_handler import SaveHandler
from utilities.utils import DateUtils
from utilities.validator import Validator
from view.maker_frame import MakerFrame
from view.payee_frame import PayeeFrame
from view.promissory_frame import PromissoryFrame

# --- CONSTANTS ---
MAIN_FONT = ('Arial', 14)
# -----------------


class GUI(ttk.Frame):

    def __init__(self, master):

        super().__init__(master)

        self.master: ThemedTk = master
        self.master.title('Gerador de Promissórias')
        self.master.resizable(width=False, height=False)

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
        self.loading_bar = None

        self.warnings = []

    def create_widgets(self):

        # Setup
        promissory_frame_label = ttk.Label(self, text='PROMISSÓRIA')
        self.promissory_frame = PromissoryFrame(self, MAIN_FONT)
        payee_frame_label = ttk.Label(self, text='BENEFICIÁRIO')
        self.payee_frame = PayeeFrame(self, MAIN_FONT)
        maker_frame_label = ttk.Label(self, text='EMITENTE')
        self.maker_frame = MakerFrame(self, MAIN_FONT)

        self.promissory_frame.create_widgets()
        self.payee_frame.create_widgets()
        self.maker_frame.create_widgets()

        self.buttons_frame = ttk.Frame(self)
        self.generate_button = ttk.Button(self.buttons_frame, text='Gerar PDF', command=self.proceed)

        self.loading_bar = ttk.Progressbar(self.buttons_frame, orient=HORIZONTAL, length=100, mode='determinate')

        # Position
        promissory_frame_label.grid(row=0, column=0, sticky=W+E)
        self.promissory_frame.grid(row=1, column=0, rowspan=5)

        payee_frame_label.grid(row=0, column=1, sticky=E)
        self.payee_frame.grid(row=1, column=1, rowspan=2)

        maker_frame_label.grid(row=3, column=1, sticky=E)
        self.maker_frame.grid(row=4, column=1, rowspan=2)

        self.buttons_frame.grid(row=6, column=0, columnspan=4)
        self.generate_button.grid(row=0, column=3)

        self.loading_bar.grid(row=0, column=0, columnspan=3)

        # Configure
        promissory_frame_label.configure(font=MAIN_FONT)
        payee_frame_label.configure(font=MAIN_FONT)
        maker_frame_label.configure(font=MAIN_FONT)
        self.buttons_frame.configure(borderwidth=5, relief='flat')
        self.generate_button.configure(width=10)
        promissory_frame_label.grid(pady=(0, 30))
        payee_frame_label.grid(pady=(0, 30))
        self.buttons_frame.grid(sticky=N+W+S+E)
        self.buttons_frame.grid_rowconfigure(0, weight=1)
        self.buttons_frame.grid_columnconfigure(0, weight=1)
        self.generate_button.grid(sticky=N+S, pady=(20, 0))
        self.loading_bar.grid(sticky=N+S+W+E, padx=10,  pady=(20, 0))
        self.loading_bar.grid_remove()

        style = ttk.Style()
        style.configure('TButton', font=MAIN_FONT, anchor=CENTER, foreground='#454545')
        style.configure('TFrame', background='lightgray')
        style.configure('TLabel', background='lightgray', foreground='#454545')

        for child in self.winfo_children():
            if type(child) != ttk.Label:
                child.grid(padx=10)

    def register_event_listeners(self):
        self.master.bind('<Return>', lambda e: self.generate_button.invoke())

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
                messagebox.showinfo('Campo vazio', 'Não deixe nenhum campo vazio.')
                return

        for cpf in (data['payee_cpf'], data['maker_cpf']):
            if len(cpf) != 11:
                messagebox.showinfo('CPF incompleto', 'Os CPFs precisam possuir 11 digitos.')
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

        # disable button and show loading bar
        self.generate_button.state(['disabled'])
        self.loading_bar.grid()

        images = PromissoryGenerator.generate_from(data, gui=self)

        # re-enable button, show loading bar and reset button text
        self.loading_bar.grid_remove()
        self.generate_button.configure(text='Gerar PDF')
        self.generate_button.state(['!disabled'])

        today_string = DateUtils.get_formatted_today_string().replace('/', '-')
        file_name = f'promissórias_{data["maker_name"]}_{today_string}_{token_hex(10)}'

        try:
            SaveHandler.save_pdf_from(images_list=images, file_name=file_name)
        except PermissionError:
            messagebox.showerror('PDF Aberto', f'Feche o PDF "{file_name}".')

    def get_data(self):

        data = self.promissory_frame.get_data()
        data.update(self.payee_frame.get_data())
        data.update(self.maker_frame.get_data())

        return data
