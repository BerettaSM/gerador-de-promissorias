from PIL import Image, ImageFont, ImageDraw
from ttkthemes import ThemedTk

from gui import GUI
from utils import PromissoryImage

# --- CONSTANTS ---
PRINT_FONT_COLOR = (0, 0, 0)
UI_BG_COLOR = '#ffffff'
UI_LABEL_FONT_COLOR = '#000000'
ENTRY_BG_COLOR = '#c0c0c0'
# -----------------

promissory_model = Image.open('model.jpg')
title_font = ImageFont.truetype(font='Roboto-Light.ttf', size=40)
# promissory = PromissoryImage(
#     number='01/17',
#     value='1.000,00',
#     due_date='25/06/2018',
#     payee_name='Fulano de Tal',
#     payee_cpf='123.456.789-10',
#     payable_in='Belo Horizonte/MG',
#     maker_name='Beltrano de Tal',
#     maker_cpf='987.654.321-09',
#     maker_address='Rua da Esperança, 234'
# )

editable_model = ImageDraw.Draw(promissory_model)


promissory_model.save("result.jpg")


# HIGH LEVEL IDEA

# READ INPUTS FROM FIELDS
# BASIC VALIDATION
# OVERLAY DATA AS TEXT INTO IMAGE(s)
# THROW ALL IMAGES IN A .DOCX FILE FOR PRINTING

def main():
    window = ThemedTk(theme='breeze')
    gui = GUI(window)
    window.mainloop()


if __name__ == '__main__':
    main()
