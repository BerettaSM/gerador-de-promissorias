from ttkthemes import ThemedTk

from view.gui import GUI


def main():
    window = ThemedTk(theme='breeze')
    gui = GUI(window)
    window.mainloop()


if __name__ == '__main__':
    main()
