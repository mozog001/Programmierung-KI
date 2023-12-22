from PyQt5 import QtWidgets
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import pyqtgraph as pg
import Database as db
import graph_utils
import display_data as dd
import helper
import sys
from datetime import datetime, timedelta, timezone

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
        
        #self.StockDB = db.StockDatabase()
        
        self.numberOf_days = helper.NUMB_DAYS()
        
        self.LineABS_Button_clicked = False
        self.SMA_Button_clicked = False 
        self.REGRESSION_Button_clicked = False
        self.stock_ready_flag = False

        self.StockNames = list()
        self.graph_ABS = ()
        self.graph_SMA = ()
        
        self.date = [] 
        self.open_price = []
        self.closed_price = []
        self.sma_date = []
        self.sma_price = []
        self.SymbolNames = []
        
           
    def GUI_components(self):
        
        
        # QLineEdit Objekt für die Such-Textbox erstellen und Eisntellungen vornehmen
        self.textbox = QLineEdit("Suchen...", self)
        self.textbox.setGeometry(10, 10, 150, 40)
        
        #Label für die Error msg, falls in der Textbox etwas falsche eingegeben wurde
        self.err_label = QLabel("", self)
        self.err_label.setGeometry(15, 40, 120, 60) # x, y, Breite, Höhe
        self.err_label.setWordWrap(True)
        
        #Buttons für die Auswahl der Öffnuns- und Schließungskurse definieren
        self.Time_Button_1Week = QPushButton(self)
        #self.Time_Button_1Week.setCheckable(True)
        #self.Time_Button_1Week.toggle()
        self.Time_Button_1Week.setText("1 Woche")
        self.Time_Button_1Week.move(300,10)
        self.Time_Button_1Week.clicked.connect(self.Time_Button_1Week_Action)
        
        self.Time_Button_1month = QPushButton(self)
        self.Time_Button_1month.setText("1 Monat")
        self.Time_Button_1month.move(400,10)
        self.Time_Button_1month.clicked.connect(self.Time_Button_1Month_Action)
        
        self.Time_Button_6month = QPushButton(self)
        self.Time_Button_6month.setText("6 Monate")
        self.Time_Button_6month.move(500,10)
        self.Time_Button_6month.clicked.connect(self.Time_Button_6Month_Action)
        
        self.Time_Button_1year = QPushButton(self)
        self.Time_Button_1year.setText("1 Jahr")
        self.Time_Button_1year.move(600,10)
        self.Time_Button_1year.clicked.connect(self.Time_Button_1Year_Action)
        
        self.Time_Button_3year = QPushButton(self)
        self.Time_Button_3year.setText("3 Jahre")
        self.Time_Button_3year.move(700,10)
        self.Time_Button_3year.clicked.connect(self.Time_Button_3Year_Action)
        
        self.Time_Button_5year = QPushButton(self)
        self.Time_Button_5year.setText("5 Jahre")
        self.Time_Button_5year.move(800,10)
        self.Time_Button_5year.clicked.connect(self.Time_Button_5Year_Action)
        
        self.Time_Button_max = QPushButton(self)
        self.Time_Button_max.setText("max")
        self.Time_Button_max.move(900,10)
        
        #Buttons für die Auswahl der Analysemethoden definieren
        self.Analyse_Button_LineAbs = QPushButton(self)
        self.Analyse_Button_LineAbs.setCheckable(True)
        #self.Analyse_Button_LineAbs.toggle()
        self.Analyse_Button_LineAbs.setText("Linie (Absolut)")
        self.Analyse_Button_LineAbs.move(200,50)
        self.Analyse_Button_LineAbs.clicked.connect(self.Button_LineAbs_state)
        
        self.Analyse_Button_SMA = QPushButton(self)
        self.Analyse_Button_SMA.setCheckable(True)
        #self.Analyse_Button_SMA.toggle()
        self.Analyse_Button_SMA.setText("SMA")
        self.Analyse_Button_SMA.move(300,50)
        self.Analyse_Button_SMA.clicked.connect(self.Button_SMA_state)
        
        self.Analyse_Button_Regression = QPushButton(self)
        self.Analyse_Button_Regression.setCheckable(True)
        #self.Analyse_Button_Regression.toggle()
        self.Analyse_Button_Regression.setText("Regression")
        self.Analyse_Button_Regression.move(400,50)
        self.Analyse_Button_Regression.clicked.connect(self.Button_Regression_state)
        
        #Buttons für die Export-Funktionen
        self.Export_Button_PNG = QPushButton(self)
        self.Export_Button_PNG.setText("Export PNG")
        self.Export_Button_PNG.move(500,700)
        
        self.Export_Button_CSV = QPushButton(self)
        self.Export_Button_CSV.setText("Export PNG")
        self.Export_Button_CSV.move(600,700)
        
        #Rahmen für die News setzen
        #self.news_frame = QFrame(self)
        #self.news_frame.move(10, 80)
        
        #Label für die Error msg, falls in der Textbox etwas falsche eingegeben wurde
        self.info_label = QLabel("", self)
        self.info_label.setGeometry(15, 200, 240, 240) # x, y, Breite, Höhe
        self.info_label.setWordWrap(True)
        
        #Label für die Error msg, falls in der Textbox etwas falsche eingegeben wurde
        self.news_label_headline = QLabel("News", self)
        self.news_label_headline.setGeometry(15, 400, 240, 240) # x, y, Breite, Höhe
        self.news_label_headline.setWordWrap(True)
        self.news_label = QLabel("", self)
        self.news_label.setGeometry(15, 405, 240, 240) # x, y, Breite, Höhe
        self.news_label.setWordWrap(True)
        
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
            self.stock_ready_flag = True
            self.symbol_List = db.StockDatabase().search_symbol(value)
            self.SymbolNames = [SymbolName[1] for SymbolName in self.symbol_List]
        
            Stock_tupple = self.symbol_List[0]
        
            invent_country = Stock_tupple[3]
            invent_year = str(Stock_tupple[4])
            industry = Stock_tupple[5]
            service = Stock_tupple[6]
        
            Stock_Information = 'Invent Country: ' + (invent_country) + '\n' + 'Invent Year: ' + (invent_year) + '\n' + 'Industry: ' + (industry) + '\n' + 'Service: ' + (service)
            self.info_label.setText(Stock_Information)
            
            #date_today = datetime.today()
            #time_offset = timezone(timedelta(hours=-5))
            #end_date_offset = date_today.replace(tzinfo=time_offset)
            #end_date = end_date_offset.strftime('%Y-%m-%d %H:%M:%S%z')
            #Stock_symbol = '' + self.SymbolNames[0]
            #stock_news_list = dd.DisplayData().get_stock_news(Stock_symbol, end_date)
            #stock_news = '\n'.join(stock_news_list)
            #self.news_label.setText(stock_news)
        else:
            self.err_label.setText('Falsche Eingabe')
            self.stock_ready_flag = False
            self.info_label.setText('')
            self.news_label.setText('')
        
        self.symbol_List = [] #Liste leeren aufgrund von Speicherverbrauch
        
    def Time_Button_1Week_Action(self):
        if self.stock_ready_flag:
            number_Days = self.numberOf_days.WEEK_1
            Stock_symbol = '' + self.SymbolNames[0]
            Stock_data = self.qGraph.stock_table_graph(number_Days, Stock_symbol)
            self.date, self.open_price, self.closed_price = helper.listOftupples_to_list(Stock_data)
        
            temp_tuppel = [(tupel[0], tupel[2]) for tupel in Stock_data]
            SMA_data = graph_utils.calculate_sma(temp_tuppel, 5)
            self.sma_date, self.sma_price = helper.listOftupples_to_list(SMA_data)
            
            #self.sma_date = ['2023-11-28 00:00:00-05:00', '2023-11-27 00:00:00-05:00', '2023-11-26 00:00:00-05:00'
             #                , '2023-11-25 00:00:00-05:00','2023-11-24 00:00:00-05:00','2023-11-23 00:00:00-05:00',
              #               '2023-11-22 00:00:00-05:00']
            
            #self.date = ['2023-11-28 00:00:00-05:00', '2023-11-27 00:00:00-05:00', '2023-11-26 00:00:00-05:00'
             #                , '2023-11-25 00:00:00-05:00','2023-11-24 00:00:00-05:00','2023-11-23 00:00:00-05:00',
              #               '2023-11-22 00:00:00-05:00']
            
            #self.sma_price = [122, 150, 176, 200, 25, 30, 250]
            #self.closed_price = [152, 170, 326, 290, 85, 10, 375]
        
            if self.LineABS_Button_clicked:
                self.qGraph.plott_ABS_graph(self.date, self.closed_price)
            else:
                pass
            
            if self.SMA_Button_clicked:
                self.qGraph.plott_SMA_graph(self.sma_date, self.sma_price)
            else:
                pass
        else:
            pass

                
    def Time_Button_1Month_Action(self):
        if self.stock_ready_flag:
            #number_Days = self.numberOf_days.MONTH_1
            #Stock_symbol = '' + self.SymbolNames[0]
            #Stock_data = self.qGraph.stock_table_graph(number_Days, Stock_symbol)
            #self.date, self.open_price, self.closed_price = helper.listOftupples_to_list(Stock_data)
        
            #temp_tuppel = [(tupel[0], tupel[2]) for tupel in Stock_data]
            #SMA_data = graph_utils.calculate_sma(temp_tuppel, 5)
            #self.sma_date, self.sma_price = helper.listOftupples_to_list(SMA_data)
            
            self.sma_date = ['2023-11-28 00:00:00-05:00', '2023-11-27 00:00:00-05:00', '2023-11-26 00:00:00-05:00'
                             , '2023-11-25 00:00:00-05:00']
            
            self.date = ['2023-11-28 00:00:00-05:00', '2023-11-27 00:00:00-05:00', '2023-11-26 00:00:00-05:00'
                             , '2023-11-25 00:00:00-05:00','2023-11-24 00:00:00-05:00','2023-11-23 00:00:00-05:00',
                             '2023-11-22 00:00:00-05:00']
            
            self.sma_price = [12, 15, 17, 20]
            self.closed_price = [102, 100, 36, 80, 75, 60, 375]
        
            if self.LineABS_Button_clicked:
                self.qGraph.plott_ABS_graph(self.date, self.closed_price)
            else:
                pass
            
            if self.SMA_Button_clicked:
                self.qGraph.plott_SMA_graph(self.sma_date, self.sma_price)
            else:
                pass
        else:
            pass
        
    def Time_Button_6Month_Action(self):
        if self.stock_ready_flag:
            #number_Days = self.numberOf_days.MONTH_6
            #Stock_symbol = '' + self.SymbolNames[0]
            #Stock_data = self.qGraph.stock_table_graph(number_Days, Stock_symbol)
            #self.date, self.open_price, self.closed_price = helper.listOftupples_to_list(Stock_data)
        
            #temp_tuppel = [(tupel[0], tupel[2]) for tupel in Stock_data]
            #SMA_data = graph_utils.calculate_sma(temp_tuppel, 5)
            #self.sma_date, self.sma_price = helper.listOftupples_to_list(SMA_data)
            
            self.sma_date = ['2023-11-28 00:00:00-05:00',
                             '2023-11-22 00:00:00-05:00']
            
            self.date = ['2023-11-28 00:00:00-05:00', '2023-11-27 00:00:00-05:00', '2023-11-26 00:00:00-05:00'
                             , '2023-11-25 00:00:00-05:00','2023-11-24 00:00:00-05:00','2023-11-23 00:00:00-05:00',
                             '2023-11-22 00:00:00-05:00']
            
            self.sma_price = [82, 40]
            self.closed_price = [152, 180, 36, 790, 805, 170, 35]
        
            if self.LineABS_Button_clicked:
                self.qGraph.plott_ABS_graph(self.date, self.closed_price)
            else:
                pass
            
            if self.SMA_Button_clicked:
                self.qGraph.plott_SMA_graph(self.sma_date, self.sma_price)
            else:
                pass
        else:
            pass
        
    def Time_Button_1Year_Action(self):
        if self.stock_ready_flag:
            number_Days = self.numberOf_days.YEAR_1
            Stock_symbol = '' + self.SymbolNames[0]
            Stock_data = self.qGraph.stock_table_graph(number_Days, Stock_symbol)
            self.date, self.open_price, self.closed_price = helper.listOftupples_to_list(Stock_data)
        
            temp_tuppel = [(tupel[0], tupel[2]) for tupel in Stock_data]
            SMA_data = graph_utils.calculate_sma(temp_tuppel, 5)
            self.sma_date, self.sma_price = helper.listOftupples_to_list(SMA_data)
        
            if self.LineABS_Button_clicked:
                self.graph_ABS = self.qGraph.plott_graph(self.date, self.closed_price, True)
            #elif self.SMA_Button_clicked:
                #self.qGraph.plott_graph(self.sma_date, self.sma_price, True)
            #elif self.SMA_Button_clicked and self.LineABS_Button_clicked:
                #self.qGraph.plott_graph(self.sma_date, self.sma_price, False)
                #self.qGraph.plott_graph(self.date, self.closed_price, False)
            #elif not (self.SMA_Button_clicked and self.LineABS_Button_clicked):
            #    self.qGraph.plott_graph([], [], True)
            else:
                pass
        else:
            pass
        
    def Time_Button_3Year_Action(self):
        if self.stock_ready_flag:
            number_Days = self.numberOf_days.YEAR_3
            Stock_symbol = '' + self.SymbolNames[0]
            Stock_data = self.qGraph.stock_table_graph(number_Days, Stock_symbol)
            self.date, self.open_price, self.closed_price = helper.listOftupples_to_list(Stock_data)
        
            temp_tuppel = [(tupel[0], tupel[2]) for tupel in Stock_data]
            SMA_data = graph_utils.calculate_sma(temp_tuppel, 5)
            self.sma_date, self.sma_price = helper.listOftupples_to_list(SMA_data)
        
            if self.LineABS_Button_clicked:
                self.graph_ABS = self.qGraph.plott_graph(self.date, self.closed_price, True)
            #elif self.SMA_Button_clicked:
             #   self.qGraph.plott_graph(self.sma_date, self.sma_price, True)
            #elif self.SMA_Button_clicked and self.LineABS_Button_clicked:
                #self.qGraph.plott_graph(self.sma_date, self.sma_price, False)
               # self.qGraph.plott_graph(self.date, self.closed_price, False)
            #elif not (self.SMA_Button_clicked and self.LineABS_Button_clicked):
            #    self.qGraph.plott_graph([], [], True)
            else:
                pass
        else:
            pass
        
    def Time_Button_5Year_Action(self):
        if self.stock_ready_flag:
            number_Days = self.numberOf_days.YEAR_5
            Stock_symbol = '' + self.SymbolNames[0]
            Stock_data = self.qGraph.stock_table_graph(number_Days, Stock_symbol)
            self.date, self.open_price, self.closed_price = helper.listOftupples_to_list(Stock_data)
        
            temp_tuppel = [(tupel[0], tupel[2]) for tupel in Stock_data]
            SMA_data = graph_utils.calculate_sma(temp_tuppel, 5)
            self.sma_date, self.sma_price = helper.listOftupples_to_list(SMA_data)
        
            if self.LineABS_Button_clicked:
                self.graph_ABS = self.qGraph.plott_graph(self.date, self.closed_price, True)
            #elif self.SMA_Button_clicked:
             #   self.graph_SMA = self.qGraph.plott_graph(self.sma_date, self.sma_price, True)
            #elif self.SMA_Button_clicked and self.LineABS_Button_clicked:
             #   self.qGraph.plott_graph(self.sma_date, self.sma_price, False)
              #  self.qGraph.plott_graph(self.date, self.closed_price, False)
            #elif not (self.SMA_Button_clicked and self.LineABS_Button_clicked):
            #    self.qGraph.plott_graph([], [], True)
            else:
                pass
            
            if self.SMA_Button_clicked:
                self.graph_SMA = self.qGraph.plott_graph(self.sma_date, self.sma_price, True)
            else:
                pass
        else:
            pass
        
    def Button_LineAbs_state(self):
    
        if self.Analyse_Button_LineAbs.isChecked():
            self.LineABS_Button_clicked = True
        else:
            self.LineABS_Button_clicked = False
            self.qGraph.remove_ABS_graph()
            #self.qGraph.remove_graph(self.graph_ABS)
            
    def Button_SMA_state(self):
        if self.Analyse_Button_SMA.isChecked():
            self.SMA_Button_clicked = True 
        else:
            self.SMA_Button_clicked = False
            self.qGraph.remove_SMA_graph()
            
    def Button_Regression_state(self):
        if self.Analyse_Button_Regression.isChecked():
            self.REGRESSION_Button_clicked = True
        else:
            self.REGRESSION_Button_clicked = False
            self.qGraph.remove_REGRESSION_graph()

    def text_completer(self):
        self.StockList = db.StockDatabase().get_all_symbols()
        self.StockNames = [StockName[2] for StockName in self.StockList]
        
        self.StockList = [] #Liste leeren aufgrund von Speicherverbrauch
        
        self.completer = QCompleter(self.StockNames)
        self.textbox.setCompleter(self.completer)
            
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
        
        #self.SMA_Line = self.plotWidget.plot()
        self.ABS_Line = self.plotWidget.plot()
        self.SMA_Line = self.plotWidget.plot()
        self.REGRESSION_Line = self.plotWidget.plot()
        
    def plott_ABS_graph(self, time_stamp, price):
        date_dict = dict(enumerate(time_stamp))
        self.ABS_Line.setData(list(date_dict.keys()), price)
        
    def plott_SMA_graph(self, time_stamp, price):
        date_dict = dict(enumerate(time_stamp))
        self.SMA_Line.setData(list(date_dict.keys()), price)
        
    def plott_REGRESSION_graph(self, time_stamp, price):
        date_dict = dict(enumerate(time_stamp))
        self.REGRESSION_Line.setData(list(date_dict.keys()), price)
        
    def remove_ABS_graph(self):
        self.ABS_Line.setData([], [])
        
    def remove_SMA_graph(self):
        self.SMA_Line.setData([], [])
        
    def remove_REGRESSION_graph(self):
        self.REGRESSION_Line.setData([], [])
        
    def stock_table_graph(self, timeframe_days, stock_symbol):
        date_today = datetime.today()
        last_date = datetime.today() - timedelta(days=timeframe_days)

        time_offset = timezone(timedelta(hours=-5))
        
        start_date_offset = last_date.replace(tzinfo=time_offset)
        end_date_offset = date_today.replace(tzinfo=time_offset)
        end_date = end_date_offset.strftime('%Y-%m-%d %H:%M:%S%z')
        start_date = start_date_offset.strftime('%Y-%m-%d %H:%M:%S%z')
       
        stock_data = dd.DisplayData().get_stocks_list(stock_symbol, start_date, end_date)

        return stock_data
    

        
        
        
        