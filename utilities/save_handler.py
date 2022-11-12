import os

from tkinter import messagebox

USER_DESKTOP = os.path.join(os.environ['USERPROFILE'], 'desktop')


class SaveHandler:

    @staticmethod
    def save_pdf_from(images_list: list, file_name: str):
        if not images_list:
            raise ValueError('List has no images to be saved.')
        pdf_path = os.path.join(USER_DESKTOP, f'{file_name}.pdf')
        if len(images_list) == 1:
            images_list[0].save(pdf_path, 'PDF', resolution=100.0)
        else:
            images_list[0].save(pdf_path, 'PDF', resolution=100.0, save_all=True, append_images=images_list[1:])
        messagebox.showinfo('Êxito', f'PDF salvo na área de trabalho, sob nome "{file_name}.pdf".')
