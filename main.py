from GUI import plotting as pl
import sys

def main():

    # GUI aufrufen
    app = pl.QtWidgets.QApplication(sys.argv)
    UI = pl.GUI_Window()
    UI.text_completer()
    UI.show_Window(app)

if __name__ == '__main__':
    main()