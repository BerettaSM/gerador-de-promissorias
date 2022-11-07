from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
from tkcalendar import Calendar, DateEntry


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

        calendar = Calendar(self, locale='pt_br', selectmode='day')
        calendar.grid()

        self.create_widgets()

    def create_widgets(self):

        pass

