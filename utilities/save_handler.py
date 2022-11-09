import os


USER_DESKTOP = os.path.join(os.environ['USERPROFILE'], 'desktop')


class SaveHandler:

    @staticmethod
    def save_to_pdf(images: list):
        pdf_path = os.path.join(USER_DESKTOP, 'teste.pdf')
        if len(images) == 1:
            images[0].save(pdf_path, 'PDF', resolution=100.0)
        else:
            images[0].save(pdf_path, 'PDF', resolution=100.0, save_all=True, append_images=images[1:])
