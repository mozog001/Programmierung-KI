from PyQt5 import QtWidgets
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import pyqtgraph as pg
import Database as db
import graph_utils as grut
import sys 

## Klasse zur Initialisierung und Beschreibung des GUI   
class GUI_Window(QtWidgets.QMainWindow): 
  
    def __init__(self):
        super().__init__()
        
        # Titel setzen
        self.setWindowTitle("Aktien-Index-App ") 
  
        # Geometrie definieren
        self.setGeometry(100, 100, 1600, 800) # x, y, Breite, Höhe
  
        # GUI Komponenten aufrufen
        self.GUI_components() 
        
    def GUI_components(self):

        self.StockNames = list()
        
        # QLineEdit Objekt für die Such-Textbox erstellen und Eisntellungen vornehmen
        self.textbox = QLineEdit("Suchen...", self)
        self.textbox.setGeometry(10, 10, 150, 40)
        
        #Label für die Error msg, falls in der Textbox etwas falsche eingegeben wurde
        self.err_label = QLabel("", self)
        self.err_label.setGeometry(15, 40, 120, 60) # x, y, Breite, Höhe
        self.err_label.setWordWrap(True)
        
        #Buttons für die Auswahl der Öffnuns- und Schließungskurse definieren
        #self.Time_Button_Intra = QPushButton(self)
        #self.Time_Button_Intra.setText("Intraday")
        #self.Time_Button_Intra.move(200,10)
        
        self.Time_Button_1Week = QPushButton(self)
        self.Time_Button_1Week.setText("1 Woche")
        self.Time_Button_1Week.move(300,10)
        self.Time_Button_1Week.clicked.connect(self.Time_Button_1Week_Action)
        
        self.Time_Button_1month = QPushButton(self)
        self.Time_Button_1month.setText("1 Monat")
        self.Time_Button_1month.move(400,10)
        
        self.Time_Button_6month = QPushButton(self)
        self.Time_Button_6month.setText("6 Monate")
        self.Time_Button_6month.move(500,10)
        
        self.Time_Button_1year = QPushButton(self)
        self.Time_Button_1year.setText("1 Jahr")
        self.Time_Button_1year.move(600,10)
        
        self.Time_Button_3year = QPushButton(self)
        self.Time_Button_3year.setText("3 Jahre")
        self.Time_Button_3year.move(700,10)
        
        self.Time_Button_5year = QPushButton(self)
        self.Time_Button_5year.setText("5 Jahre")
        self.Time_Button_5year.move(800,10)
        
        self.Time_Button_max = QPushButton(self)
        self.Time_Button_max.setText("max")
        self.Time_Button_max.move(900,10)
        
        #Buttons für die Auswahl der Analysemethoden definieren
        self.Analyse_Button_LineAbs = QPushButton(self)
        self.Analyse_Button_LineAbs.setText("Linie (Absolut)")
        self.Analyse_Button_LineAbs.move(200,50)
        
        self.Analyse_Button_SMA = QPushButton(self)
        self.Analyse_Button_SMA.setText("SMA")
        self.Analyse_Button_SMA.move(300,50)
        
        self.Analyse_Button_Regression = QPushButton(self)
        self.Analyse_Button_Regression.setText("Regression")
        self.Analyse_Button_Regression.move(400,50)
        
        #Buttons für die Export-Funktionen
        self.Export_Button_PNG = QPushButton(self)
        self.Export_Button_PNG.setText("Export PNG")
        self.Export_Button_PNG.move(500,700)
        
        self.Export_Button_CSV = QPushButton(self)
        self.Export_Button_CSV.setText("Export PNG")
        self.Export_Button_CSV.move(600,700)
        
        #Rahmen für die News setzen
        self.news_frame = QFrame(self)
        self.news_frame.move(10, 80)
        
        #Instanz der Klasse Plt_Graph erzeugen und Graphen in GUI-Mainwindow einbetten
        self.qGraph = Plt_Graph(self)
        self.qGraph.setGeometry(200, 100, 1100, 600) # x, y, Breite, Höhe
        
        #Aktion ausführen, wenn in der Textbox Enter gedrückt wird
        self.textbox.returnPressed.connect(lambda: self.textBox_Action())
        
    #Methode für Aktionen in der Such-Textbox
    def textBox_Action(self):
        value = self.textbox.text()
        
        self.textbox.setText('Suchen...')
 
        if value in self.StockNames:
            self.err_label.setText(value)
        else:
            self.err_label.setText('Falsche Eingabe')
            
        self.symbol_List = self.StockDB.search_symbol(value)
        print(self.symbol_List)
        self.SymbolNames = [SymbolName[1] for SymbolName in self.symbol_List]
        print(self.SymbolNames)
        
        self.symbol_List = [] #Liste leeren aufgrund von Speicherverbrauch
        
    def Time_Button_1Week_Action(self):
        number_Days = 7
        Stock_symbol = self.SymbolNames[0]
        Stock_data = grut.populate_graph(number_Days, Stock_symbol)
        print(Stock_data)

    def text_completer(self):
        
        self.StockDB = db.StockDatabase()
        
        self.StockList = self.StockDB.get_all_symbols()
        self.StockNames = [StockName[2] for StockName in self.StockList]
        print('Size of StockNames_list',sys.getsizeof(self.StockNames))
        
        self.StockList = [] #Liste leeren aufgrund von Speicherverbrauch
        
        self.completer = QCompleter(self.StockNames)
        self.textbox.setCompleter(self.completer)
        
        #print(self.cleared_StockNames)
            
    def show_Window(self, app):
        # GUI Widgets zeigen
        self.show() 
        sys.exit(app.exec())

## Klasse zur Initialisierung und Beschreibung des Graphen       
class Plt_Graph(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        #Graphen als Widget erzeugen
        self.plotWidget = pg.PlotWidget()
        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(self.plotWidget)
        

        
        
        
        