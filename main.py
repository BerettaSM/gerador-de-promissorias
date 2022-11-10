from ttkthemes import ThemedTk

from view.gui import GUI


def main():
    window = ThemedTk(theme='plastik')
    gui = GUI(window)
    gui.create_widgets()
    gui.register_event_listeners()
    window.mainloop()


if __name__ == '__main__':
    main()
