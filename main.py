from plotting import *

def main():
    
    # GUI aufrufen
    app = QtWidgets.QApplication(sys.argv)
    GUI = GUI_Window()
    GUI.text_completer()
    GUI.show_Window(app)

if __name__ == '__main__':
    main()