from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk


from promissory_frame import PromissoryFrame
from payee_frame import PayeeFrame
from maker_frame import MakerFrame


MAIN_FONT = ('Arial', 16)


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

        self.error = None

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
        self.generate_button = ttk.Button(self.buttons_frame, text='Gerar', command=self.generate)

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

    def generate(self):

        data = self.get_data()

        self.error = None

    def get_data(self):

        data = self.promissory_frame.get_data()
        data.update(self.payee_frame.get_data())
        data.update(self.maker_frame.get_data())

        for val in data.values():
            if not val:
                self.error = 'Existe um campo vazio'
                break

        return data
