from PyQt5 import QtWidgets
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import pyqtgraph as pg
import pyqtgraph.exporters
import Database as db
import analyze as an
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
        self.setGeometry(0, 0, 1100, 768) # x, y, Breite, Höhe
        self.setFixedSize(1100, 768)
        self.setStyleSheet("background-color: #fff;")
  
        # GUI Komponenten aufrufen
        self.GUI_components() 
        
        #self.StockDB = db.StockDatabase()
        
        self.numberOf_days = helper.NUMB_DAYS()
        
        self.LineABS_Button_clicked = False
        self.SMA_Button_clicked = False 
        self.REGRESSION_Button_clicked = False
        self.stock_ready_flag = False

        self.StockNames = list()
        self.regressionData = list()
        
        self.date = [] 
        self.open_price = []
        self.closed_price = []
        self.sma_date = []
        self.regression_date = []
        self.yhat_avg = []
        self.sma_price = []
        self.SymbolNames = []
        self.err_msg = ''
        
        self.mouseReleaseEvent = self.setTextboxText
        
           
    def GUI_components(self): 
        
        self.frame = QFrame(self)
        self.frame.setGeometry(235, 5, 800, 110) # x, y, Breite, Höhe
        self.frame.setStyleSheet("border: 2px solid #D3D3D3; border-radius: 10px; padding: 8px")
        
        self.frame2 = QFrame(self)
        self.frame2.setGeometry(10, 130, 215, 250) # x, y, Breite, Höhe
        self.frame2.setStyleSheet("border: 2px solid #D3D3D3; border-radius: 10px; padding: 8px")
        
        self.frame3 = QFrame(self)
        self.frame3.setGeometry(235, 130, 800, 540) # x, y, Breite, Höhe
        self.frame3.setStyleSheet("border: 2px solid #D3D3D3; border-radius: 10px; padding: 8px")
        
        # QLineEdit Objekt für die Such-Textbox erstellen und Eisntellungen vornehmen
        self.textbox = QLineEdit(self)
        self.textbox.setGeometry(10, 10, 150, 30)
        self.textbox.setStyleSheet("border-radius: 8px; border: 2px solid #D3D3D3; padding: 5px 15px;")
        self.textbox.setPlaceholderText('Suchen')
        self.textbox.mouseReleaseEvent = self.clearText
        self.textbox.returnPressed.connect(lambda: self.textBox_Action())
        
        #Label für die Error msg, falls in der Textbox etwas falsche eingegeben wurde

        self.stock_label_headline = QLabel("Stock", self)
        self.stock_label_headline.setGeometry(240, 8, 45, 18) # x, y, Breite, Höhe
        self.stock_label_headline.setWordWrap(True)
        self.stock_label_headline.setStyleSheet("color: #708090; font-weight: 600; font-size: 12px;")
        
        self.err_label = QLabel("", self)
        self.err_label.setGeometry(240, 23, 250, 22) # x, y, Breite, Höhe
        self.err_label.setWordWrap(True)
        self.err_label.setStyleSheet("color: #A599B5; font-weight: 600; font-size: 14px;")
        
        #Label für die Error msg, falls in der Textbox etwas falsche eingegeben wurde
        self.info_label = QLabel("", self)
        self.info_label.setGeometry(240, 55, 300, 50) # x, y, Breite, Höhe
        self.info_label.setWordWrap(True)
        self.info_label.setStyleSheet("color: #2E2F2F; font-weight: 600; font-size: 10px;")
        
        #Label für die Error msg, falls in der Textbox etwas falsche eingegeben wurde
        self.news_label_headline = QLabel("News", self)
        self.news_label_headline.setGeometry(600, 8, 45, 15) # x, y, Breite, Höhe
        self.news_label_headline.setWordWrap(True)
        self.news_label_headline.setStyleSheet("color: #708090; font-weight: 600; font-size: 12px;")
        
        self.news_label = QLabel("", self)
        self.news_label.setGeometry(600, 30, 430, 50) # x, y, Breite, Höhe
        self.news_label.setWordWrap(True)
        self.news_label.setOpenExternalLinks(True)
        self.news_label.setStyleSheet("color: #2E2F2F; font-weight: 600; font-size: 10px;")
        
        self.change_label = QLabel("", self)
        self.change_label.setGeometry(30, 75, 80, 15) # x, y, Breite, Höhe
        self.change_label.setWordWrap(True)
        self.change_label.setStyleSheet("font-weight: 600; font-size: 14px;")
        
        #Label für die Error msg, falls in der Textbox etwas falsche eingegeben wurde
        self.trend_label_headline = QLabel("Weekly-Trend", self)
        self.trend_label_headline.setGeometry(30, 140, 90, 15) # x, y, Breite, Höhe
        self.trend_label_headline.setWordWrap(True)
        self.trend_label_headline.setStyleSheet("color: #708090; font-weight: 600; font-size: 12px;")
        
        self.trend_label = QLabel("", self)
        self.trend_label.setGeometry(30, 160, 180, 180) # x, y, Breite, Höhe
        self.trend_label.setWordWrap(True)
        self.trend_label.setStyleSheet("color: #2E2F2F; font-weight: 600; font-size: 11px;")
        
        #Buttons für die Auswahl der Öffnuns- und Schließungskurse definieren
        self.Time_Button_1Week = QPushButton(self)
        #self.Time_Button_1Week.setCheckable(True) ###
        #self.Time_Button_1Week.toggle() ######
        self.Time_Button_1Week.setText("1 Woche")
        self.Time_Button_1Week.move(300,700)
        self.Time_Button_1Week.clicked.connect(self.Time_Button_1Week_Action)
        self.Time_Button_1Week.setStyleSheet("background-color: #0d6efd; color: #fff; border-radius: 5px; border: 1px solid #0d6efd")
        
        self.Time_Button_1month = QPushButton(self)
        self.Time_Button_1month.setText("1 Monat")
        self.Time_Button_1month.move(420,700)
        self.Time_Button_1month.clicked.connect(self.Time_Button_1Month_Action)
        self.Time_Button_1month.setStyleSheet("background-color: #0d6efd; color: #fff; border-radius: 5px; border: 1px solid #0d6efd")

        self.Time_Button_6month = QPushButton(self)
        self.Time_Button_6month.setText("6 Monate")
        self.Time_Button_6month.move(540,700)
        self.Time_Button_6month.clicked.connect(self.Time_Button_6Month_Action)
        self.Time_Button_6month.setStyleSheet("background-color: #0d6efd; color: #fff; border-radius: 5px; border: 1px solid #0d6efd")
        
        self.Time_Button_1year = QPushButton(self)
        self.Time_Button_1year.setText("1 Jahr")
        self.Time_Button_1year.move(660,700)
        self.Time_Button_1year.clicked.connect(self.Time_Button_1Year_Action)
        self.Time_Button_1year.setStyleSheet("background-color: #0d6efd; color: #fff; border-radius: 5px; border: 1px solid #0d6efd")

        self.Time_Button_3year = QPushButton(self)
        self.Time_Button_3year.setText("3 Jahre")
        self.Time_Button_3year.move(780,700)
        self.Time_Button_3year.clicked.connect(self.Time_Button_3Year_Action)
        self.Time_Button_3year.setStyleSheet("background-color: #0d6efd; color: #fff; border-radius: 5px; border: 1px solid #0d6efd")

        self.Time_Button_5year = QPushButton(self)
        self.Time_Button_5year.setText("5 Jahre")
        self.Time_Button_5year.move(900,700)
        self.Time_Button_5year.clicked.connect(self.Time_Button_5Year_Action)
        self.Time_Button_5year.setStyleSheet("background-color: #0d6efd; color: #fff; border-radius: 5px; border: 1px solid #0d6efd")

        #self.Time_Button_max = QPushButton(self)
        #self.Time_Button_max.setText("max")
        #self.Time_Button_max.move(900,10)
        
        #Buttons für die Auswahl der Analysemethoden definieren
        self.Analyse_Button_LineAbs = QPushButton(self)
        self.Analyse_Button_LineAbs.setCheckable(True)
        #self.Analyse_Button_LineAbs.toggle() #########
        self.Analyse_Button_LineAbs.setText("ABS")
        self.Analyse_Button_LineAbs.move(50,410)
        self.Analyse_Button_LineAbs.clicked.connect(self.Button_LineAbs_state)
        self.Analyse_Button_LineAbs.setStyleSheet("background-color: #0d6efd; color: #fff; border-radius: 5px; border: 1px solid #0d6efd")
        
        self.Analyse_Button_SMA = QPushButton(self)
        self.Analyse_Button_SMA.setCheckable(True)
        #self.Analyse_Button_SMA.toggle() ########
        self.Analyse_Button_SMA.setText("SMA")
        self.Analyse_Button_SMA.move(50,450)
        self.Analyse_Button_SMA.clicked.connect(self.Button_SMA_state)
        self.Analyse_Button_SMA.setStyleSheet("background-color: #0d6efd; color: #fff; border-radius: 5px; border: 1px solid #0d6efd")
        
        self.Analyse_Button_Regression = QPushButton(self)
        self.Analyse_Button_Regression.setCheckable(True)
        #self.Analyse_Button_Regression.toggle()#########
        self.Analyse_Button_Regression.setText("TSA")
        self.Analyse_Button_Regression.move(50,490)
        self.Analyse_Button_Regression.clicked.connect(self.Button_Regression_state)
        self.Analyse_Button_Regression.setStyleSheet("background-color: #0d6efd; color: #fff; border-radius: 5px; border: 1px solid #0d6efd")
        
        #Instanz der Klasse Plt_Graph erzeugen und Graphen in GUI-Mainwindow einbetten
        self.qGraph = Plt_Graph(self)
        self.qGraph.setGeometry(235, 140, 780, 530) # x, y, Breite, Höhe

    def setTextboxText(self, event):
        self.textbox.setText("")
        if self.err_msg == "Falsche Eingabe":
            self.err_label.setText('')
            self.change_label.setText('')
        else:
            pass
        
    def clearText(self,event):
        self.textbox.setText("")
        if self.err_msg == "Falsche Eingabe":
            self.err_label.setText('')
            self.change_label.setText('')
        else:
            pass

    #Methode für Aktionen in der Such-Textbox
    def textBox_Action(self):
        value = self.textbox.text()
        
        self.textbox.setText('')
 
        if value in self.StockNames:
            shortName = helper.get_first_twoStrings(value)
            self.err_label.setText(shortName)
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
            
            date_today = datetime.today()
            time_offset = timezone(timedelta(hours=-5))
            end_date_offset = date_today.replace(tzinfo=time_offset)
            end_date = end_date_offset.strftime('%Y-%m-%d')
            Stock_symbol = '' + self.SymbolNames[0]
            stock_news_list = dd.DisplayData().get_stock_news(Stock_symbol, end_date)
            #print(stock_news_list)
            stock_news_Headers = helper.get_page_headers(stock_news_list)
            tupel_News = list(zip(stock_news_list, stock_news_Headers))
            
            if len(tupel_News) > 4:
                tupel_News = tupel_News[:5]
            
            html_code = ""
            for link, header in tupel_News:
                #html_code += f'<a href="{link}">{header}</a><br>'
                html_code += f'<a href="{link}" style="color: #ACBDBA;">{header}</a><br>'

            self.news_label.setText(html_code)
            
            Stock_symbol = '' + self.SymbolNames[0]
            Stock_data = self.qGraph.stock_table_graph(365, Stock_symbol)
            temp_tuppel = [(tupel[0], tupel[2]) for tupel in Stock_data]
            regression_output = an.Analyzing_methods().get_forecast_tail(temp_tuppel)
            self.regressionData = regression_output.values.tolist()
            regression_string = helper.ListOfList_to_string(self.regressionData)

            self.trend_label.setText(regression_string)
            
            if len(temp_tuppel) >= 2:
                new_tupel = temp_tuppel[-1][1]
                old_tupel = temp_tuppel[-2][1]
                if new_tupel == 0:
                    self.change_label.setText('')
                valDiff = ((old_tupel - new_tupel) / abs(new_tupel)) * 100
                if valDiff < 0:
                    self.change_label.setText(str(round(valDiff,3)) + ' %')
                    self.change_label.setStyleSheet("color: red; font-weight: 600; font-size: 14px;")
                else:
                    self.change_label.setText(str(round(valDiff,3)) + ' %')
                    self.change_label.setStyleSheet("color: green; font-weight: 600; font-size: 14px;") 
            
        else:
            self.err_msg = 'Falsche Eingabe'
            self.err_label.setText(self.err_msg)
            self.stock_ready_flag = False
            self.info_label.setText('')
            self.news_label.setText('')
            self.trend_label.setText('')
        
        self.symbol_List = [] #Liste leeren aufgrund von Speicherverbrauch
        
    def Time_Button_1Week_Action(self):
        if self.stock_ready_flag:
            number_Days = self.numberOf_days.WEEK_1
            Stock_symbol = '' + self.SymbolNames[0]
            Stock_data = self.qGraph.stock_table_graph(number_Days, Stock_symbol)
            self.date, self.open_price, self.closed_price = helper.listOftupples_to_list(Stock_data)

            modified_date = []
            for date_string in self.date:
                date_withoutTime = date_string.replace(' 00:00:00', '')
                modified_date.append(date_withoutTime)
            dates = [datetime.strptime(date_str, '%Y-%m-%d') for date_str in modified_date]
            last_date = dates[-1]
            dates_extended = [last_date + timedelta(days=i) for i in range(1, 11)]
            date_strings_extended = [date.strftime('%Y-%m-%d') for date in dates_extended]
            modified_date.extend(date_strings_extended)
            max_ticks = 10
            numb_ticks = min(len(modified_date), max_ticks)
            ticks_diff = max(1, len(modified_date) // (numb_ticks - 1)) if numb_ticks > 1 else 1
            x_Date_ticks = [(i, modified_date[i]) for i in range(0, len(modified_date), ticks_diff)]
            self.qGraph.label_X_axis(x_Date_ticks)
        
            temp_tuppel = [(tupel[0], tupel[2]) for tupel in Stock_data]
            SMA_data = an.Analyzing_methods().calculate_sma(temp_tuppel, 2)
            self.sma_date, self.sma_price = helper.listOftupples_to_list(SMA_data)
            
        
            if self.LineABS_Button_clicked:
                self.qGraph.plott_ABS_graph(self.date, self.closed_price)
            else:
                pass
            
            if self.SMA_Button_clicked:
                self.qGraph.plott_SMA_graph(self.sma_date, self.sma_price)
            else:
                pass
            
            if self.REGRESSION_Button_clicked:
                regression_output = an.Analyzing_methods().get_forecast(temp_tuppel, number_Days)
                self.regression_date = list(regression_output['ds'])
                self.yhat_avg = list(regression_output['yhat'])
                self.qGraph.plott_REGRESSION_graph(self.regression_date, self.yhat_avg)
            else:
                pass
        else:
            pass

                
    def Time_Button_1Month_Action(self):
        if self.stock_ready_flag:
            number_Days = self.numberOf_days.MONTH_1
            Stock_symbol = '' + self.SymbolNames[0]
            Stock_data = self.qGraph.stock_table_graph(number_Days, Stock_symbol)
            self.date, self.open_price, self.closed_price = helper.listOftupples_to_list(Stock_data)
            
            modified_date = []
            for date_string in self.date:
                date_withoutTime = date_string.replace(' 00:00:00', '')
                modified_date.append(date_withoutTime)
            dates = [datetime.strptime(date_str, '%Y-%m-%d') for date_str in modified_date]
            last_date = dates[-1]
            dates_extended = [last_date + timedelta(days=i) for i in range(1, 11)]
            date_strings_extended = [date.strftime('%Y-%m-%d') for date in dates_extended]
            modified_date.extend(date_strings_extended)
            max_ticks = 10
            numb_ticks = min(len(modified_date), max_ticks)
            ticks_diff = max(1, len(modified_date) // (numb_ticks - 1)) if numb_ticks > 1 else 1
            x_Date_ticks = [(i, modified_date[i]) for i in range(0, len(modified_date), ticks_diff)]
            self.qGraph.label_X_axis(x_Date_ticks)
        
            temp_tuppel = [(tupel[0], tupel[2]) for tupel in Stock_data]
            SMA_data = an.Analyzing_methods().calculate_sma(temp_tuppel, 5)
            self.sma_date, self.sma_price = helper.listOftupples_to_list(SMA_data)
        
            if self.LineABS_Button_clicked:
                self.qGraph.plott_ABS_graph(self.date, self.closed_price)
            else:
                pass
            
            if self.SMA_Button_clicked:
                self.qGraph.plott_SMA_graph(self.sma_date, self.sma_price)
            else:
                pass
            
            if self.REGRESSION_Button_clicked:
                regression_output = an.Analyzing_methods().get_forecast(temp_tuppel, number_Days)
                self.regression_date = list(regression_output['ds'])
                self.yhat_avg = list(regression_output['yhat'])
                self.qGraph.plott_REGRESSION_graph(self.regression_date, self.yhat_avg)
            else:
                pass
        else:
            pass
        
    def Time_Button_6Month_Action(self):
        if self.stock_ready_flag:
            number_Days = self.numberOf_days.MONTH_6
            Stock_symbol = '' + self.SymbolNames[0]
            Stock_data = self.qGraph.stock_table_graph(number_Days, Stock_symbol)
            self.date, self.open_price, self.closed_price = helper.listOftupples_to_list(Stock_data)
            
            modified_date = []
            for date_string in self.date:
                date_withoutTime = date_string.replace(' 00:00:00', '')
                modified_date.append(date_withoutTime)
            dates = [datetime.strptime(date_str, '%Y-%m-%d') for date_str in modified_date]
            last_date = dates[-1]
            dates_extended = [last_date + timedelta(days=i) for i in range(1, 11)]
            date_strings_extended = [date.strftime('%Y-%m-%d') for date in dates_extended]
            modified_date.extend(date_strings_extended)
            max_ticks = 10
            numb_ticks = min(len(modified_date), max_ticks)
            ticks_diff = max(1, len(modified_date) // (numb_ticks - 1)) if numb_ticks > 1 else 1
            x_Date_ticks = [(i, modified_date[i]) for i in range(0, len(modified_date), ticks_diff)]
            self.qGraph.label_X_axis(x_Date_ticks)
        
            temp_tuppel = [(tupel[0], tupel[2]) for tupel in Stock_data]
            SMA_data = an.Analyzing_methods().calculate_sma(temp_tuppel, 5)
            self.sma_date, self.sma_price = helper.listOftupples_to_list(SMA_data)
        
            if self.LineABS_Button_clicked:
                self.qGraph.plott_ABS_graph(self.date, self.closed_price)
            else:
                pass
            
            if self.SMA_Button_clicked:
                self.qGraph.plott_SMA_graph(self.sma_date, self.sma_price)
            else:
                pass
            if self.REGRESSION_Button_clicked:
                regression_output = an.Analyzing_methods().get_forecast(temp_tuppel, number_Days)
                self.regression_date = list(regression_output['ds'])
                self.yhat_avg = list(regression_output['yhat'])
                self.qGraph.plott_REGRESSION_graph(self.regression_date, self.yhat_avg)
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
            
            modified_date = []
            for date_string in self.date:
                date_withoutTime = date_string.replace(' 00:00:00', '')
                modified_date.append(date_withoutTime)
            dates = [datetime.strptime(date_str, '%Y-%m-%d') for date_str in modified_date]
            last_date = dates[-1]
            dates_extended = [last_date + timedelta(days=i) for i in range(1, 11)]
            date_strings_extended = [date.strftime('%Y-%m-%d') for date in dates_extended]
            modified_date.extend(date_strings_extended)
            max_ticks = 10
            numb_ticks = min(len(modified_date), max_ticks)
            ticks_diff = max(1, len(modified_date) // (numb_ticks - 1)) if numb_ticks > 1 else 1
            x_Date_ticks = [(i, modified_date[i]) for i in range(0, len(modified_date), ticks_diff)]
            self.qGraph.label_X_axis(x_Date_ticks)
        
            temp_tuppel = [(tupel[0], tupel[2]) for tupel in Stock_data]
            SMA_data = an.Analyzing_methods().calculate_sma(temp_tuppel, 10)
            self.sma_date, self.sma_price = helper.listOftupples_to_list(SMA_data)
        
            if self.LineABS_Button_clicked:
                self.qGraph.plott_ABS_graph(self.date, self.closed_price)
            else:
                pass
            
            if self.SMA_Button_clicked:
                self.qGraph.plott_SMA_graph(self.sma_date, self.sma_price)
            else:
                pass
            if self.REGRESSION_Button_clicked:
                regression_output = an.Analyzing_methods().get_forecast(temp_tuppel, number_Days)
                self.regression_date = list(regression_output['ds'])
                self.yhat_avg = list(regression_output['yhat'])
                self.qGraph.plott_REGRESSION_graph(self.regression_date, self.yhat_avg)
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
            
            modified_date = []
            for date_string in self.date:
                date_withoutTime = date_string.replace(' 00:00:00', '')
                modified_date.append(date_withoutTime)
            dates = [datetime.strptime(date_str, '%Y-%m-%d') for date_str in modified_date]
            last_date = dates[-1]
            dates_extended = [last_date + timedelta(days=i) for i in range(1, 11)]
            date_strings_extended = [date.strftime('%Y-%m-%d') for date in dates_extended]
            modified_date.extend(date_strings_extended)
            max_ticks = 10
            numb_ticks = min(len(modified_date), max_ticks)
            ticks_diff = max(1, len(modified_date) // (numb_ticks - 1)) if numb_ticks > 1 else 1
            x_Date_ticks = [(i, modified_date[i]) for i in range(0, len(modified_date), ticks_diff)]
            self.qGraph.label_X_axis(x_Date_ticks)
        
            temp_tuppel = [(tupel[0], tupel[2]) for tupel in Stock_data]
            SMA_data = an.Analyzing_methods().calculate_sma(temp_tuppel, 10)
            self.sma_date, self.sma_price = helper.listOftupples_to_list(SMA_data)
        
            if self.LineABS_Button_clicked:
                self.qGraph.plott_ABS_graph(self.date, self.closed_price)
            else:
                pass
            
            if self.SMA_Button_clicked:
                self.qGraph.plott_SMA_graph(self.sma_date, self.sma_price)
            else:
                pass
            if self.REGRESSION_Button_clicked:
                regression_output = an.Analyzing_methods().get_forecast(temp_tuppel, number_Days)
                self.regression_date = list(regression_output['ds'])
                self.yhat_avg = list(regression_output['yhat'])
                self.qGraph.plott_REGRESSION_graph(self.regression_date, self.yhat_avg)
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
            
            modified_date = []
            for date_string in self.date:
                date_withoutTime = date_string.replace(' 00:00:00', '')
                modified_date.append(date_withoutTime)
            dates = [datetime.strptime(date_str, '%Y-%m-%d') for date_str in modified_date]
            last_date = dates[-1]
            dates_extended = [last_date + timedelta(days=i) for i in range(1, 11)]
            date_strings_extended = [date.strftime('%Y-%m-%d') for date in dates_extended]
            modified_date.extend(date_strings_extended)
            max_ticks = 10
            numb_ticks = min(len(modified_date), max_ticks)
            ticks_diff = max(1, len(modified_date) // (numb_ticks - 1)) if numb_ticks > 1 else 1
            x_Date_ticks = [(i, modified_date[i]) for i in range(0, len(modified_date), ticks_diff)]
            self.qGraph.label_X_axis(x_Date_ticks)
        
            temp_tuppel = [(tupel[0], tupel[2]) for tupel in Stock_data]
            SMA_data = an.Analyzing_methods().calculate_sma(temp_tuppel, 10)
            self.sma_date, self.sma_price = helper.listOftupples_to_list(SMA_data)
        
            if self.LineABS_Button_clicked:
                self.qGraph.plott_ABS_graph(self.date, self.closed_price)
            else:
                pass
            
            if self.SMA_Button_clicked:
                self.qGraph.plott_SMA_graph(self.sma_date, self.sma_price)
            else:
                pass
            if self.REGRESSION_Button_clicked:
                regression_output = an.Analyzing_methods().get_forecast(temp_tuppel, number_Days)
                self.regression_date = list(regression_output['ds'])
                self.yhat_avg = list(regression_output['yhat'])
                self.qGraph.plott_REGRESSION_graph(self.regression_date, self.yhat_avg)
            else:
                pass
        else:
            pass
        
    def Button_LineAbs_state(self):
    
        if self.Analyse_Button_LineAbs.isChecked():
            self.LineABS_Button_clicked = True
            self.Analyse_Button_LineAbs.setStyleSheet("background-color: #0b5ed7; color: #fff; border-radius: 5px; border: 1px solid #1C1F33")
        else:
            self.Analyse_Button_LineAbs.setStyleSheet("background-color: #0d6efd; color: #fff; border-radius: 5px; border: 1px solid #0d6efd")
            self.LineABS_Button_clicked = False
            self.qGraph.remove_ABS_graph()
            
    def Button_SMA_state(self):
        if self.Analyse_Button_SMA.isChecked():
            self.SMA_Button_clicked = True
            self.Analyse_Button_SMA.setStyleSheet("background-color: #0b5ed7; color: #fff; border-radius: 5px; border: 1px solid #1C1F33")
        else:
            self.Analyse_Button_SMA.setStyleSheet("background-color: #0d6efd; color: #fff; border-radius: 5px; border: 1px solid #0d6efd")
            self.SMA_Button_clicked = False
            self.qGraph.remove_SMA_graph()
            
    def Button_Regression_state(self):
        if self.Analyse_Button_Regression.isChecked():
            self.REGRESSION_Button_clicked = True
            self.Analyse_Button_Regression.setStyleSheet("background-color: #0b5ed7; color: #fff; border-radius: 5px; border: 1px solid #1C1F33")
        else:
            self.Analyse_Button_Regression.setStyleSheet("background-color: #0d6efd; color: #fff; border-radius: 5px; border: 1px solid #0d6efd")
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
        self.plotWidget.setBackground('w')
        self.plotWidget.showGrid(x=True, y=True)
        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(self.plotWidget)
        
        #self.SMA_Line = self.plotWidget.plot()
        self.ABS_Line = self.plotWidget.plot()
        self.SMA_Line = self.plotWidget.plot()
        self.REGRESSION_Line = self.plotWidget.plot()
        
    def plott_ABS_graph(self, time_stamp, price):
        date_dict = dict(enumerate(time_stamp))
        self.ABS_Line.setData(list(date_dict.keys()), price)
        self.ABS_Line.setPen('#003D5B')
        
    def plott_SMA_graph(self, time_stamp, price):
        date_dict = dict(enumerate(time_stamp))
        self.SMA_Line.setData(list(date_dict.keys()), price)
        self.SMA_Line.setPen('#44AF69')
        
    def plott_REGRESSION_graph(self, time_stamp, price):
        date_dict = dict(enumerate(time_stamp))
        self.REGRESSION_Line.setData(list(date_dict.keys()), price)
        self.REGRESSION_Line.setPen('#D1495B')
        
    def remove_ABS_graph(self):
        self.ABS_Line.setData([], [])
        
    def remove_SMA_graph(self):
        self.SMA_Line.setData([], [])
        
    def remove_REGRESSION_graph(self):
        self.REGRESSION_Line.setData([], [])
        
    def label_X_axis(self,ticks):
        self.plotWidget.getAxis("bottom").setTicks([ticks])
        
    def stock_table_graph(self, timeframe_days, stock_symbol):
        date_today = datetime.today()
        last_date = datetime.today() - timedelta(days=timeframe_days)

        time_offset = timezone(timedelta(hours=-5))
        
        start_date_offset = last_date.replace(tzinfo=time_offset)
        end_date_offset = date_today.replace(tzinfo=time_offset)
        end_date = end_date_offset.strftime('%Y-%m-%d')
        start_date = start_date_offset.strftime('%Y-%m-%d')
       
        stock_data = dd.DisplayData().get_stocks_list(stock_symbol, start_date, end_date)

        return stock_data
    

        
        
        
        