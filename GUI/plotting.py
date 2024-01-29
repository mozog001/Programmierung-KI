import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import pyqtgraph as pg
import pyqtgraph.exporters
from Low_Level.Database import Database as db
from Analyze import analyze as an
from Controller import display_data as dd
from help_methods import helper
from datetime import datetime, timedelta, timezone
 
class GUI_Window(QtWidgets.QMainWindow): 
    """
    Klasse, um den GUI zu erzeugen
    Die Klasse enthält folgende Methoden:
    1. GUI_components(self):  Diese Methode initialisiert GUI-Komponenten und legt ihre Eigenschaften und Positionen fest.
    2. clearText(self, event): Diese Methode löscht den Text in den Textfeldern
    3. text_completer(self): Diese Methode erstellt einen Text-Vervollständiger.
    4. textBox_Action(self): Diese Methode wird aufgerufen, wenn Enter in der Such-Textbox gedrückt wird.
    5. cal_value_diff(self, data_tupel): Diese Methode berechnet die prozentuale Änderung des Aktienwerts im Vergleich zum vorherigen Tag.
    6. weekly_trend(self, data_tupel): Diese Methode berechnet den wöchentlichen Trend basierend auf den übergebenen Daten.
    7. Time_Button_1Week_Action(self): Diese Methode wird aufgerufen, wenn der Button "1 Woche" in der GUI ausgewählt wird.
    8. Time_Button_1Month_Action(self): Diese Methode wird aufgerufen, wenn der Button "1 Monat" in der GUI ausgewählt wird.
    9. Time_Button_1Month_Action(self): Diese Methode wird aufgerufen, wenn der Button "6 Monate" in der GUI ausgewählt wird.
    10. Time_Button_1Year_Action(self): Diese Methode wird aufgerufen, wenn der Button "1 Jahr" in der GUI ausgewählt wird.
    11. Time_Button_3Year_Action(self): Diese Methode wird aufgerufen, wenn der Button "3 Jahre" in der GUI ausgewählt wird.
    12. Time_Button_5Year_Action(self): Diese Methode wird aufgerufen, wenn der Button "5 Jahre" in der GUI ausgewählt wird.
    13. Button_LineAbs_state(self): Diese Methode wird aufgerufen, wenn der Button "ABS" (Absolutwert) in der GUI ausgewählt oder abgewählt wird.
    14. Button_SMA_state(self): Diese Methode wird aufgerufen, wenn der Button "SMA" (Gleitender Durchschnitt) in der GUI ausgewählt oder abgewählt wird.
    15. Button_Regression_state(self): Diese Methode wird aufgerufen, wenn der Button "TSA" (Regression) in der GUI ausgewählt oder abgewählt wird.
    16. show_Window(self, app): Diese Methode zeigt das GUI-Fenster an und startet die Ausführung der Anwendungsinstanz.
    """  
    def __init__(self):
        super().__init__()
        
        # Titel setzen
        self.setWindowTitle("Aktien-Index-App") 
  
        #Mainwindow Style udn Geometrie definieren
        self.setGeometry(0, 0, 1100, 768) # x, y, Breite, Höhe
        self.setFixedSize(1100, 768)
        self.setStyleSheet("background-color: #fff;")
  
        #Instanziierungen
        self.GUI_components()
        self.numberOf_days = helper.NUMB_DAYS()
       
        #Initialisierung
        self.stock_ready_flag = False

        self.StockNames = []
        self.date = [] 
        self.open_price = []
        self.closed_price = []
        self.sma_date = []
        self.regression_date = []
        self.yhat_avg = []
        self.sma_price = []
        self.SymbolNames = []
        self.StockList = []
        
        self.err_msg = ''
        
        self.mouseReleaseEvent = self.clearText
                  
    def GUI_components(self):
        """
        Funktion:   Diese Methode initialisiert GUI-Komponenten und legt ihre Eigenschaften und Positionen fest.
                    1. Definition von Rahmen mit jeweiligen Geometrien und Style-Einstellungen.
                    2. Erstellung eines QLineEdit-Objekts für die Such-Textbox und Konfiguration der Eigenschaften.
                    3. Definition von Labels für Überschriften, Fehlermeldungen, Aktieninformationen und News.
                    4. Definition von Labels für Aktienpreisänderung, Weekly-Trend und Auswahl von Zeiträumen und Analysemethoden.
                    5. Definition von Buttons für die Auswahl der Zeiträume.
                    6. Definition von Buttons für die Auswahl der Analysemethoden.
                    7. Erzeugung einer Instanz der Klasse Plt_Graph und Einbetten der Graphen im GUI-Mainwindow.

        param: Keine
        return: Keine
        """
        
        #Rahmen definieren mit den jeweiligen Geometrien und Style-Einstellungen
        self.frame = QFrame(self)
        self.frame.setGeometry(235, 5, 800, 110) # x, y, Breite, Höhe
        self.frame.setStyleSheet("border: 2px solid #D3D3D3; border-radius: 10px; padding: 8px")
        
        self.frame2 = QFrame(self)
        self.frame2.setGeometry(10, 130, 215, 250) # x, y, Breite, Höhe
        self.frame2.setStyleSheet("border: 2px solid #D3D3D3; border-radius: 10px; padding: 8px")
        
        self.frame3 = QFrame(self)
        self.frame3.setGeometry(235, 130, 800, 540) # x, y, Breite, Höhe
        self.frame3.setStyleSheet("border: 2px solid #D3D3D3; border-radius: 10px; padding: 8px")
        
        #QLineEdit Objekt für die Such-Textbox erstellen und Eisntellungen vornehmen
        self.textbox = QLineEdit(self)
        self.textbox.setGeometry(10, 10, 150, 30)
        self.textbox.setStyleSheet("border-radius: 8px; border: 2px solid #D3D3D3; padding: 5px 15px;")
        self.textbox.setPlaceholderText('Suchen')
        self.textbox.mouseReleaseEvent = self.clearText
        self.textbox.returnPressed.connect(self.textBox_Action)
        
        #Label für die Überschrift "Stock" definieren
        self.stock_label_headline = QLabel("Stock", self)
        self.stock_label_headline.setGeometry(240, 8, 45, 18) # x, y, Breite, Höhe
        self.stock_label_headline.setWordWrap(True)
        self.stock_label_headline.setStyleSheet("color: #708090; font-weight: 600; font-size: 12px;")
        
        #Label für den Aktiennamen definieren
        self.err_label = QLabel("", self)
        self.err_label.setGeometry(240, 23, 250, 22) # x, y, Breite, Höhe
        self.err_label.setWordWrap(True)
        self.err_label.setStyleSheet("color: #A599B5; font-weight: 600; font-size: 14px;")
        
        #Label für den Aktieninfos definieren
        self.info_label = QLabel("", self)
        self.info_label.setGeometry(240, 55, 300, 50) # x, y, Breite, Höhe
        self.info_label.setWordWrap(True)
        self.info_label.setStyleSheet("color: #2E2F2F; font-weight: 600; font-size: 10px;")
        
        #Label die Überschrift News definieren
        self.news_label_headline = QLabel("News", self)
        self.news_label_headline.setGeometry(600, 8, 45, 15) # x, y, Breite, Höhe
        self.news_label_headline.setWordWrap(True)
        self.news_label_headline.setStyleSheet("color: #708090; font-weight: 600; font-size: 12px;")
        
        #Label für die News-Links definieren
        self.news_label = QLabel("", self)
        self.news_label.setGeometry(600, 30, 430, 50) # x, y, Breite, Höhe
        self.news_label.setWordWrap(True)
        self.news_label.setOpenExternalLinks(True)
        self.news_label.setStyleSheet("color: #2E2F2F; font-weight: 600; font-size: 10px;")
        
        #Label für die Anzeige der Aktienpreisänderung im Vergleich zum Vortag in Prozent
        self.change_label = QLabel("", self)
        self.change_label.setGeometry(30, 75, 80, 15) # x, y, Breite, Höhe
        self.change_label.setWordWrap(True)
        self.change_label.setStyleSheet("font-weight: 600; font-size: 14px;")
        
        #Label die Überschrift "Weekly-Trends"
        self.trend_label_headline = QLabel("Weekly-Trend", self)
        self.trend_label_headline.setGeometry(30, 140, 90, 15) # x, y, Breite, Höhe
        self.trend_label_headline.setWordWrap(True)
        self.trend_label_headline.setStyleSheet("color: #708090; font-weight: 600; font-size: 12px;")
        
        #Label für die Anzeige der Aktienentwicklung in den nächsten Tagen
        self.trend_label = QLabel("", self)
        self.trend_label.setGeometry(30, 160, 180, 180) # x, y, Breite, Höhe
        self.trend_label.setWordWrap(True)
        self.trend_label.setStyleSheet("color: #2E2F2F; font-weight: 600; font-size: 11px;")
        
        #Buttons für die Auswahl der Zeiträume definieren in Form von Time_Button_Zeitraum
        self.Time_Button_1Week = QPushButton(self)
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
        
        #Buttons für die Auswahl der Analysemethoden definieren in Form von Analyse_Button_Analysemethode
        #Absolutwert
        self.Analyse_Button_LineAbs = QPushButton(self)
        self.Analyse_Button_LineAbs.setCheckable(True)
        self.Analyse_Button_LineAbs.setText("ABS")
        self.Analyse_Button_LineAbs.move(50,410)
        self.Analyse_Button_LineAbs.clicked.connect(self.Button_LineAbs_state)
        self.Analyse_Button_LineAbs.setStyleSheet("background-color: #0d6efd; color: #fff; border-radius: 5px; border: 1px solid #0d6efd")
        
        #Gleitender Mittelwert
        self.Analyse_Button_SMA = QPushButton(self)
        self.Analyse_Button_SMA.setCheckable(True)
        self.Analyse_Button_SMA.setText("SMA")
        self.Analyse_Button_SMA.move(50,450)
        self.Analyse_Button_SMA.clicked.connect(self.Button_SMA_state)
        self.Analyse_Button_SMA.setStyleSheet("background-color: #0d6efd; color: #fff; border-radius: 5px; border: 1px solid #0d6efd")
        
        #Zeitreihenanalyse
        self.Analyse_Button_Regression = QPushButton(self)
        self.Analyse_Button_Regression.setCheckable(True)
        self.Analyse_Button_Regression.setText("TSA")
        self.Analyse_Button_Regression.move(50,490)
        self.Analyse_Button_Regression.clicked.connect(self.Button_Regression_state)
        self.Analyse_Button_Regression.setStyleSheet("background-color: #0d6efd; color: #fff; border-radius: 5px; border: 1px solid #0d6efd")
        
        #Instanz der Klasse Plt_Graph erzeugen und Graphen in GUI-Mainwindow einbetten
        self.qGraph = Plt_Graph(self)
        self.qGraph.setGeometry(235, 140, 780, 530) # x, y, Breite, Höhe
     
    def clearText(self, event):
        """
        Funktion:   Methode zum Löschen des Textes in den Textfeldern. 
                    Diese Methode wird aufgerufen, nachdem die Maus außerhalb der Textbox geklickt hat oder eine falsche Eingabe getätigt wurde.
        param: 
            event: Das Event-Objekt, das den Aufruf der Methode ausgelöst hat. 
        return: Keine
        """
        self.textbox.setText("")
        if self.err_msg == "Falsche Eingabe":
            self.err_label.setText('')
            self.change_label.setText('')
        else:
            pass
     
    def text_completer(self):
        """
        Funktion:   Diese Methode erstellt einen Text-Vervollständiger für ein Textfeld basierend auf den Symbolen aus einer Datenbank.
                    1. Alle Aktien aus der Datenbank abrufen und in der Instanzvariable 'self.StockList' speichern.
                    2. Die Aktiennamen in einer separaten Liste 'self.StockNames' extrahieren, indem der dritte Wert jedes Eintrags in 'self.StockList' verwendet wird.
                    3. Die Liste 'self.StockList' leeren, um den Speicherverbrauch zu reduzieren.
                    4. Einen QCompleter erstellen, der die Liste 'self.StockNames' als Vervollständigungsvorschläge verwendet.
                    5. Den erstellten QCompleter dem Textfeld 'self.textbox' hinzufügen, um die Vervollständigung zu aktivieren.
        param: Keine
        return: Keine
        """
        self.StockList = db.StockDatabase().get_all_symbols()
        self.StockNames = [StockName[2] for StockName in self.StockList]
        
        self.StockList = []
        
        self.completer = QCompleter(self.StockNames)
        self.textbox.setCompleter(self.completer)
        
    def textBox_Action(self):
        """
        Funktion:   Diese Methode wird aufgerufen, wenn Enter in der Such-Textbox gedrückt wird.

                    1. Den eingegebenen Wert aus der Textbox abrufen.
                    2. Die Textbox leeren.
                    3. Prüfen, ob der eingegebene Name in der Liste der Aktiennamen ('StockNames') enthalten ist.
                    4. Wenn ja:
                    - Flag ('stock_ready_flag') setzen, um andere Funktionen auszuführen.
                    - Den eingegebenen Namen für die GUI-Ausgabe kürzen.
                    - Das richtige Aktiensymbol basierend auf dem exakt eingetragenen Namen erhalten.
                    - Aktieninformationen extrahieren und in der GUI ausgeben.
                    - Das heutige Datum ermitteln.
                    - Die Überschriften der heutigen Aktiennews der jeweiligen Aktien ausgeben.
                    - Die Entwicklung der Aktie in den letzten 365 Tagen anzeigen.
                    - Den relativen Wert der Aktie im Vergleich zum vorherigen Tag berechnen.
                    5. Wenn nein:
                    - Fehlermeldung setzen und in der GUI ausgeben.
                    - Flag zurücksetzen.
                    - Aktieninformationen, News und Trend in der GUI leeren.
        param: Keine
        :return: Keine
        """
        value = self.textbox.text()
        self.textbox.setText('')
        
        if value in self.StockNames: #Nur ausführen, wenn der eingegebene Name in der Liste enthalten ist
            self.stock_ready_flag = True #Flag setzen, damit andere Funktionen ausgeführt werden können

            shortName = helper.get_first_twoStrings(value) 
            self.err_label.setText(shortName)
            
            self.symbol_List = db.StockDatabase().search_symbol(value) 
            
            Stock_tupple = self.symbol_List[0]
            invent_country = Stock_tupple[3]
            invent_year = str(Stock_tupple[4])
            industry = Stock_tupple[5]
            service = Stock_tupple[6]
            Stock_Information = 'Invent Country: ' + (invent_country) + '\n' + 'Stock Year: ' + (invent_year) + '\n' + 'Industry: ' + (industry) + '\n' + 'Service: ' + (service)
            self.info_label.setText(Stock_Information)
            
            date_today = datetime.today()
            end_date = date_today.strftime('%Y-%m-%d')
            
            self.SymbolNames = [SymbolName[1] for SymbolName in self.symbol_List]
            Stock_symbol = '' + self.SymbolNames[0]
            
            stock_news_list = dd.DisplayData().get_stock_news(Stock_symbol, end_date)
            stock_news_Headers = helper.get_page_headers(stock_news_list)
            News_list = list(zip(stock_news_list, stock_news_Headers))
            
            if len(News_list) > 4:
                News_list = News_list[:5]
            
            html_code = ""
            for link, header in News_list:
                html_code += f'<a href="{link}" style="color: #ACBDBA;">{header}</a><br>'

            self.news_label.setText(html_code)
            
            Stock_data = self.qGraph.stock_table_graph(365, Stock_symbol)
            temp_tuppel = [(tupel[0], tupel[2]) for tupel in Stock_data]
            
            self.weekly_trend(temp_tuppel)
            
            self.cal_value_diff(temp_tuppel)
        else:
            self.err_msg = 'Falsche Eingabe'
            self.err_label.setText(self.err_msg)
            self.stock_ready_flag = False
            self.info_label.setText('')
            self.news_label.setText('')
            self.trend_label.setText('')
        
        self.symbol_List = [] #Liste leeren aufgrund von Speicherverbrauch
      
    def cal_value_diff(self, data_tupel):
        """
        Funktion: Diese Methode berechnet die prozentuale Änderung des Aktienwerts im Vergleich zum vorherigen Tag.
                  1. Überprüfen, ob die Anzahl der Datenpunkte ausreichend ist (mindestens 2 erforderlich).
                  2. Falls ja:
                    - Den Wert des letzten Datenpunkts ('new_tupel') und des vorherigen Datenpunkts ('old_tupel') extrahieren.
                    - Überprüfen, ob der neue Wert ('new_tupel') gleich Null ist; wenn ja, Label 'change_label' leeren.
                    - Die prozentuale Änderung berechnen.
                    - Das Label 'change_label' mit dem prozentualen Änderungswert und entsprechender Textfarbe aktualisieren.
                    3. Falls nein:
                    - Das Label 'change_label' leeren.
        param: 
            data_tupel: Eine Liste von Tupeln, die Datenpunkte repräsentieren (Datum, Wert).
        return: Keine
        """
        if len(data_tupel) >= 2:
            new_tupel = data_tupel[-1][1]
            old_tupel = data_tupel[-2][1]
            if new_tupel == 0:
                self.change_label.setText('')
            valDiff = ((old_tupel - new_tupel) / abs(new_tupel)) * 100
            if valDiff < 0:
                self.change_label.setText(str(round(valDiff,3)) + ' %')
                self.change_label.setStyleSheet("color: red; font-weight: 600; font-size: 14px;")
            else:
                self.change_label.setText(str(round(valDiff,3)) + ' %')
                self.change_label.setStyleSheet("color: green; font-weight: 600; font-size: 14px;")
                    
    def weekly_trend(self, data_tupel):
        """
        Funktion:   Diese Methode berechnet den wöchentlichen Trend basierend auf den übergebenen Daten.
                      1. Überprüfen, ob die Anzahl der Datenpunkte ausreichend ist (mindestens 2 erforderlich).
                      2. Falls ja:
                      - Den wöchentlichen Trend berechnen mithilfe der Methode 'get_forecast_tail'.
                      - Das Ergebnis in eine Liste konvertieren.
                      - Die Liste in einen formatierten String umwandeln.
                      - Den String in der GUI im Label 'trend_label' anzeigen.
                      3. Falls nein:
                      - Das Label 'trend_label' leeren.

        param:
                    data_tupel: Eine Liste von Tupeln, die Datenpunkte repräsentieren (Datum, Wert).
        returns Keine
        """   
        regressionData = []
        if len(data_tupel) >= 2:
            regression_output = an.Analyzing_methods().get_forecast_tail(data_tupel)
            regressionData = regression_output.values.tolist()
            regression_string = helper.ListOfList_to_string(regressionData)
            self.trend_label.setText(regression_string) 
        else:
            self.trend_label.setText("")
   
    def Time_Button_1Week_Action(self):
        """
        Funktion:   Diese Methode wird aufgerufen, wenn der Button "1 Woche" in der GUI ausgewählt wird.
                    1. Überprüfen, ob die Flagge 'stock_ready_flag' gesetzt ist, was bedeutet, dass eine Aktie ausgewählt wurde.
                    2. Falls ja:
                    - Die Anzahl der Tage für die Datenabfrage festlegen ('number_Days').
                    - Das Symbol der ausgewählten Aktie extrahieren.
                    - Die Daten für die ausgewählte Zeitspanne abrufen und in Listen konvertieren.
                    - Die x-Achsen-Ticks für das Diagramm erstellen und setzen. Dient der Beschriftung
                    - Die Daten für den einfachen gleitenden Durchschnitt (SMA) berechnen und in Listen konvertieren.
                    - Abhängig von den ausgewählten Analysemethoden:
                    - Falls "ABS" ausgewählt ist, das ABS-Diagramm plotten.
                    - Falls "SMA" ausgewählt ist, das SMA-Diagramm plotten.
                    - Falls "TSA" (Regression) ausgewählt ist, die Regressionsdaten abrufen und das Regressionsdiagramm plotten.
                    - Andernfalls, wenn keine Analysemethoden ausgewählt sind, nichts tun.
                    3. Falls nein:
                    - Nichts tun.
        param: Keine
        return: Keine
        """
        if self.stock_ready_flag:
            number_Days = self.numberOf_days.WEEK_1
            Stock_symbol = '' + self.SymbolNames[0]
            Stock_data = self.qGraph.stock_table_graph(number_Days, Stock_symbol)
            self.date, self.open_price, self.closed_price = helper.listOftupples_to_list(Stock_data)

            x_Date_ticks = helper.get_time_ticks(self.date)
            self.qGraph.label_X_axis(x_Date_ticks)
        
            temp_tuppel = [(tupel[0], tupel[2]) for tupel in Stock_data]
            SMA_data = an.Analyzing_methods().calculate_sma(temp_tuppel, 2)
            self.sma_date, self.sma_price = helper.listOftupples_to_list(SMA_data)
            
            if self.Analyse_Button_LineAbs.isChecked():
                if len(temp_tuppel) >= 2:
                    self.qGraph.plott_ABS_graph(self.date, self.closed_price)
                else:
                    pass
            else:
                pass
            
            if self.Analyse_Button_SMA.isChecked():
                if len(temp_tuppel) >= 2:
                    self.qGraph.plott_SMA_graph(self.sma_date, self.sma_price)
                else:
                    pass
            else:
                pass
            
            if self.Analyse_Button_Regression.isChecked():
                if len(temp_tuppel) >= 2:
                    regression_output = an.Analyzing_methods().get_forecast(temp_tuppel)
                    self.regression_date = list(regression_output['ds'])
                    self.yhat_avg = list(regression_output['yhat'])
                    self.qGraph.plott_REGRESSION_graph(self.regression_date, self.yhat_avg)
                else:
                    pass
            else:
                pass
        else:
            pass
               
    def Time_Button_1Month_Action(self):
        """
        Funktion:   Diese Methode wird aufgerufen, wenn der Button "1 Monat" in der GUI ausgewählt wird.
                    1. Überprüfen, ob die Flagge 'stock_ready_flag' gesetzt ist, was bedeutet, dass eine Aktie ausgewählt wurde.
                    2. Falls ja:
                    - Die Anzahl der Tage für die Datenabfrage festlegen ('number_Days').
                    - Das Symbol der ausgewählten Aktie extrahieren.
                    - Die Daten für die ausgewählte Zeitspanne abrufen und in Listen konvertieren.
                    - Die x-Achsen-Ticks für das Diagramm erstellen und setzen. Dient der Beschriftung
                    - Die Daten für den einfachen gleitenden Durchschnitt (SMA) berechnen und in Listen konvertieren.
                    - Abhängig von den ausgewählten Analysemethoden:
                    - Falls "ABS" ausgewählt ist, das ABS-Diagramm plotten.
                    - Falls "SMA" ausgewählt ist, das SMA-Diagramm plotten.
                    - Falls "TSA" (Regression) ausgewählt ist, die Regressionsdaten abrufen und das Regressionsdiagramm plotten.
                    - Andernfalls, wenn keine Analysemethoden ausgewählt sind, nichts tun.
                    3. Falls nein:
                    - Nichts tun.
        param: Keine
        return: Keine
        """
        if self.stock_ready_flag:
            number_Days = self.numberOf_days.MONTH_1
            Stock_symbol = '' + self.SymbolNames[0]
            Stock_data = self.qGraph.stock_table_graph(number_Days, Stock_symbol)
            self.date, self.open_price, self.closed_price = helper.listOftupples_to_list(Stock_data)

            x_Date_ticks = helper.get_time_ticks(self.date)
            self.qGraph.label_X_axis(x_Date_ticks)
        
            temp_tuppel = [(tupel[0], tupel[2]) for tupel in Stock_data]
            SMA_data = an.Analyzing_methods().calculate_sma(temp_tuppel, 2)
            self.sma_date, self.sma_price = helper.listOftupples_to_list(SMA_data)
            
            if self.Analyse_Button_LineAbs.isChecked():
                if len(temp_tuppel) >= 2:
                    self.qGraph.plott_ABS_graph(self.date, self.closed_price)
                else:
                    pass
            else:
                pass
            
            if self.Analyse_Button_SMA.isChecked():
                if len(temp_tuppel) >= 2:
                    self.qGraph.plott_SMA_graph(self.sma_date, self.sma_price)
                else:
                    pass
            else:
                pass
            
            if self.Analyse_Button_Regression.isChecked():
                if len(temp_tuppel) >= 2:
                    regression_output = an.Analyzing_methods().get_forecast(temp_tuppel)
                    self.regression_date = list(regression_output['ds'])
                    self.yhat_avg = list(regression_output['yhat'])
                    self.qGraph.plott_REGRESSION_graph(self.regression_date, self.yhat_avg)
                else:
                    pass
            else:
                pass
        else:
            pass
        
    def Time_Button_6Month_Action(self):
        """
        Funktion:   Diese Methode wird aufgerufen, wenn der Button "6 Monate" in der GUI ausgewählt wird.
                    1. Überprüfen, ob die Flagge 'stock_ready_flag' gesetzt ist, was bedeutet, dass eine Aktie ausgewählt wurde.
                    2. Falls ja:
                    - Die Anzahl der Tage für die Datenabfrage festlegen ('number_Days').
                    - Das Symbol der ausgewählten Aktie extrahieren.
                    - Die Daten für die ausgewählte Zeitspanne abrufen und in Listen konvertieren.
                    - Die x-Achsen-Ticks für das Diagramm erstellen und setzen. Dient der Beschriftung
                    - Die Daten für den einfachen gleitenden Durchschnitt (SMA) berechnen und in Listen konvertieren.
                    - Abhängig von den ausgewählten Analysemethoden:
                    - Falls "ABS" ausgewählt ist, das ABS-Diagramm plotten.
                    - Falls "SMA" ausgewählt ist, das SMA-Diagramm plotten.
                    - Falls "TSA" (Regression) ausgewählt ist, die Regressionsdaten abrufen und das Regressionsdiagramm plotten.
                    - Andernfalls, wenn keine Analysemethoden ausgewählt sind, nichts tun.
                    3. Falls nein:
                    - Nichts tun.
        param: Keine
        return: Keine
        """
        if self.stock_ready_flag:
            number_Days = self.numberOf_days.MONTH_6
            Stock_symbol = '' + self.SymbolNames[0]
            Stock_data = self.qGraph.stock_table_graph(number_Days, Stock_symbol)
            self.date, self.open_price, self.closed_price = helper.listOftupples_to_list(Stock_data)

            x_Date_ticks = helper.get_time_ticks(self.date)
            self.qGraph.label_X_axis(x_Date_ticks)
        
            temp_tuppel = [(tupel[0], tupel[2]) for tupel in Stock_data]
            SMA_data = an.Analyzing_methods().calculate_sma(temp_tuppel, 2)
            self.sma_date, self.sma_price = helper.listOftupples_to_list(SMA_data)
            
            if self.Analyse_Button_LineAbs.isChecked():
                if len(temp_tuppel) >= 2:
                    self.qGraph.plott_ABS_graph(self.date, self.closed_price)
                else:
                    pass
            else:
                pass
            
            if self.Analyse_Button_SMA.isChecked():
                if len(temp_tuppel) >= 2:
                    self.qGraph.plott_SMA_graph(self.sma_date, self.sma_price)
                else:
                    pass
            else:
                pass
            
            if self.Analyse_Button_Regression.isChecked():
                if len(temp_tuppel) >= 2:
                    regression_output = an.Analyzing_methods().get_forecast(temp_tuppel)
                    self.regression_date = list(regression_output['ds'])
                    self.yhat_avg = list(regression_output['yhat'])
                    self.qGraph.plott_REGRESSION_graph(self.regression_date, self.yhat_avg)
                else:
                    pass
            else:
                pass
        else:
            pass
        
    def Time_Button_1Year_Action(self):
        """
        Funktion:   Diese Methode wird aufgerufen, wenn der Button "1 Jahr" in der GUI ausgewählt wird.
                    1. Überprüfen, ob die Flagge 'stock_ready_flag' gesetzt ist, was bedeutet, dass eine Aktie ausgewählt wurde.
                    2. Falls ja:
                    - Die Anzahl der Tage für die Datenabfrage festlegen ('number_Days').
                    - Das Symbol der ausgewählten Aktie extrahieren.
                    - Die Daten für die ausgewählte Zeitspanne abrufen und in Listen konvertieren.
                    - Die x-Achsen-Ticks für das Diagramm erstellen und setzen. Dient der Beschriftung
                    - Die Daten für den einfachen gleitenden Durchschnitt (SMA) berechnen und in Listen konvertieren.
                    - Abhängig von den ausgewählten Analysemethoden:
                    - Falls "ABS" ausgewählt ist, das ABS-Diagramm plotten.
                    - Falls "SMA" ausgewählt ist, das SMA-Diagramm plotten.
                    - Falls "TSA" (Regression) ausgewählt ist, die Regressionsdaten abrufen und das Regressionsdiagramm plotten.
                    - Andernfalls, wenn keine Analysemethoden ausgewählt sind, nichts tun.
                    3. Falls nein:
                    - Nichts tun.
        param: Keine
        return: Keine
        """
        if self.stock_ready_flag:
            number_Days = self.numberOf_days.YEAR_1
            Stock_symbol = '' + self.SymbolNames[0]
            Stock_data = self.qGraph.stock_table_graph(number_Days, Stock_symbol)
            self.date, self.open_price, self.closed_price = helper.listOftupples_to_list(Stock_data)

            x_Date_ticks = helper.get_time_ticks(self.date)
            self.qGraph.label_X_axis(x_Date_ticks)
        
            temp_tuppel = [(tupel[0], tupel[2]) for tupel in Stock_data]
            SMA_data = an.Analyzing_methods().calculate_sma(temp_tuppel, 2)
            self.sma_date, self.sma_price = helper.listOftupples_to_list(SMA_data)
            
            if self.Analyse_Button_LineAbs.isChecked():
                if len(temp_tuppel) >= 2:
                    self.qGraph.plott_ABS_graph(self.date, self.closed_price)
                else:
                    pass
            else:
                pass
            
            if self.Analyse_Button_SMA.isChecked():
                if len(temp_tuppel) >= 2:
                    self.qGraph.plott_SMA_graph(self.sma_date, self.sma_price)
                else:
                    pass
            else:
                pass
            
            if self.Analyse_Button_Regression.isChecked():
                if len(temp_tuppel) >= 2:
                    regression_output = an.Analyzing_methods().get_forecast(temp_tuppel)
                    self.regression_date = list(regression_output['ds'])
                    self.yhat_avg = list(regression_output['yhat'])
                    self.qGraph.plott_REGRESSION_graph(self.regression_date, self.yhat_avg)
                else:
                    pass
            else:
                pass
        else:
            pass
        
    def Time_Button_3Year_Action(self):
        """
        Funktion:   Diese Methode wird aufgerufen, wenn der Button "3 Jahre" in der GUI ausgewählt wird.
                    1. Überprüfen, ob die Flagge 'stock_ready_flag' gesetzt ist, was bedeutet, dass eine Aktie ausgewählt wurde.
                    2. Falls ja:
                    - Die Anzahl der Tage für die Datenabfrage festlegen ('number_Days').
                    - Das Symbol der ausgewählten Aktie extrahieren.
                    - Die Daten für die ausgewählte Zeitspanne abrufen und in Listen konvertieren.
                    - Die x-Achsen-Ticks für das Diagramm erstellen und setzen. Dient der Beschriftung
                    - Die Daten für den einfachen gleitenden Durchschnitt (SMA) berechnen und in Listen konvertieren.
                    - Abhängig von den ausgewählten Analysemethoden:
                    - Falls "ABS" ausgewählt ist, das ABS-Diagramm plotten.
                    - Falls "SMA" ausgewählt ist, das SMA-Diagramm plotten.
                    - Falls "TSA" (Regression) ausgewählt ist, die Regressionsdaten abrufen und das Regressionsdiagramm plotten.
                    - Andernfalls, wenn keine Analysemethoden ausgewählt sind, nichts tun.
                    3. Falls nein:
                    - Nichts tun.
        param: Keine
        return: Keine
        """
        if self.stock_ready_flag:
            number_Days = self.numberOf_days.YEAR_3
            Stock_symbol = '' + self.SymbolNames[0]
            Stock_data = self.qGraph.stock_table_graph(number_Days, Stock_symbol)
            self.date, self.open_price, self.closed_price = helper.listOftupples_to_list(Stock_data)

            x_Date_ticks = helper.get_time_ticks(self.date)
            self.qGraph.label_X_axis(x_Date_ticks)
        
            temp_tuppel = [(tupel[0], tupel[2]) for tupel in Stock_data]
            SMA_data = an.Analyzing_methods().calculate_sma(temp_tuppel, 2)
            self.sma_date, self.sma_price = helper.listOftupples_to_list(SMA_data)
            
            if self.Analyse_Button_LineAbs.isChecked():
                if len(temp_tuppel) >= 2:
                    self.qGraph.plott_ABS_graph(self.date, self.closed_price)
                else:
                    pass
            else:
                pass
            
            if self.Analyse_Button_SMA.isChecked():
                if len(temp_tuppel) >= 2:
                    self.qGraph.plott_SMA_graph(self.sma_date, self.sma_price)
                else:
                    pass
            else:
                pass
            
            if self.Analyse_Button_Regression.isChecked():
                if len(temp_tuppel) >= 2:
                    regression_output = an.Analyzing_methods().get_forecast(temp_tuppel)
                    self.regression_date = list(regression_output['ds'])
                    self.yhat_avg = list(regression_output['yhat'])
                    self.qGraph.plott_REGRESSION_graph(self.regression_date, self.yhat_avg)
                else:
                    pass
            else:
                pass
        else:
            pass
        
    def Time_Button_5Year_Action(self):
        """
        Funktion:   Diese Methode wird aufgerufen, wenn der Button "5 Jahre" in der GUI ausgewählt wird.
                    1. Überprüfen, ob die Flagge 'stock_ready_flag' gesetzt ist, was bedeutet, dass eine Aktie ausgewählt wurde.
                    2. Falls ja:
                    - Die Anzahl der Tage für die Datenabfrage festlegen ('number_Days').
                    - Das Symbol der ausgewählten Aktie extrahieren.
                    - Die Daten für die ausgewählte Zeitspanne abrufen und in Listen konvertieren.
                    - Die x-Achsen-Ticks für das Diagramm erstellen und setzen. Dient der Beschriftung
                    - Die Daten für den einfachen gleitenden Durchschnitt (SMA) berechnen und in Listen konvertieren.
                    - Abhängig von den ausgewählten Analysemethoden:
                    - Falls "ABS" ausgewählt ist, das ABS-Diagramm plotten.
                    - Falls "SMA" ausgewählt ist, das SMA-Diagramm plotten.
                    - Falls "TSA" (Regression) ausgewählt ist, die Regressionsdaten abrufen und das Regressionsdiagramm plotten.
                    - Andernfalls, wenn keine Analysemethoden ausgewählt sind, nichts tun.
                    3. Falls nein:
                    - Nichts tun.
        param: Keine
        return: Keine
        """
        if self.stock_ready_flag:
            number_Days = self.numberOf_days.YEAR_5
            Stock_symbol = '' + self.SymbolNames[0]
            Stock_data = self.qGraph.stock_table_graph(number_Days, Stock_symbol)
            self.date, self.open_price, self.closed_price = helper.listOftupples_to_list(Stock_data)

            x_Date_ticks = helper.get_time_ticks(self.date)
            self.qGraph.label_X_axis(x_Date_ticks)
        
            temp_tuppel = [(tupel[0], tupel[2]) for tupel in Stock_data]
            SMA_data = an.Analyzing_methods().calculate_sma(temp_tuppel, 2)
            self.sma_date, self.sma_price = helper.listOftupples_to_list(SMA_data)
            
            if self.Analyse_Button_LineAbs.isChecked():
                if len(temp_tuppel) >= 2:
                    self.qGraph.plott_ABS_graph(self.date, self.closed_price)
                else:
                    pass
            else:
                pass
            
            if self.Analyse_Button_SMA.isChecked():
                if len(temp_tuppel) >= 2:
                    self.qGraph.plott_SMA_graph(self.sma_date, self.sma_price)
                else:
                    pass
            else:
                pass
            
            if self.Analyse_Button_Regression.isChecked():
                if len(temp_tuppel) >= 2:
                    regression_output = an.Analyzing_methods().get_forecast(temp_tuppel)
                    self.regression_date = list(regression_output['ds'])
                    self.yhat_avg = list(regression_output['yhat'])
                    self.qGraph.plott_REGRESSION_graph(self.regression_date, self.yhat_avg)
                else:
                    pass
            else:
                pass
        else:
            pass
        
    def Button_LineAbs_state(self):
        """
        Funktion:   Diese Methode wird aufgerufen, wenn der Button "ABS" (Absolutwert) in der GUI ausgewählt oder abgewählt wird.
                    1. Überprüfen, ob der Button "ABS" ausgewählt ist.
                    2. Falls ja:
                    - Das Erscheinungsbild des Buttons ändern, um den ausgewählten Zustand anzuzeigen.
                    3. Falls nein:
                    - Das Erscheinungsbild des Buttons zurücksetzen und das ABS-Diagramm aus dem Diagramm entfernen.
        param: Keine
        return: Keine
        """    
        if self.Analyse_Button_LineAbs.isChecked():
            self.Analyse_Button_LineAbs.setStyleSheet("background-color: #0b5ed7; color: #fff; border-radius: 5px; border: 1px solid #1C1F33")
        else:
            self.Analyse_Button_LineAbs.setStyleSheet("background-color: #0d6efd; color: #fff; border-radius: 5px; border: 1px solid #0d6efd")
            self.qGraph.remove_ABS_graph()
            
    def Button_SMA_state(self):
        """
        Funktion:   Diese Methode wird aufgerufen, wenn der Button "SMA" (Gleitender Durchschnitt) in der GUI ausgewählt oder abgewählt wird.
                    1. Überprüfen, ob der Button "SMA" ausgewählt ist.
                    2. Falls ja:
                    - Das Erscheinungsbild des Buttons ändern, um den ausgewählten Zustand anzuzeigen.
                    3. Falls nein:
                    - Das Erscheinungsbild des Buttons zurücksetzen und das SMA-Diagramm aus dem Diagramm entfernen.
        param: Keine
        return: Keine
        """ 
        if self.Analyse_Button_SMA.isChecked():
            self.Analyse_Button_SMA.setStyleSheet("background-color: #0b5ed7; color: #fff; border-radius: 5px; border: 1px solid #1C1F33")
        else:
            self.Analyse_Button_SMA.setStyleSheet("background-color: #0d6efd; color: #fff; border-radius: 5px; border: 1px solid #0d6efd")
            self.qGraph.remove_SMA_graph()
            
    def Button_Regression_state(self):
        """
        Funktion:   Diese Methode wird aufgerufen, wenn der Button "TSA" (Regression) in der GUI ausgewählt oder abgewählt wird.
                    1. Überprüfen, ob der Button "TSA" ausgewählt ist.
                    2. Falls ja:
                    - Das Erscheinungsbild des Buttons ändern, um den ausgewählten Zustand anzuzeigen.
                    3. Falls nein:
                    - Das Erscheinungsbild des Buttons zurücksetzen und das TSA-Diagramm aus dem Diagramm entfernen.
        param: Keine
        return: Keine
        """ 
        if self.Analyse_Button_Regression.isChecked():
            self.Analyse_Button_Regression.setStyleSheet("background-color: #0b5ed7; color: #fff; border-radius: 5px; border: 1px solid #1C1F33")
        else:
            self.Analyse_Button_Regression.setStyleSheet("background-color: #0d6efd; color: #fff; border-radius: 5px; border: 1px solid #0d6efd")
            self.qGraph.remove_REGRESSION_graph()
            
    def show_Window(self, app):
        """
        Funktion:   Diese Methode zeigt das GUI-Fenster an und startet die Ausführung der Anwendungsinstanz.
                    1. Das GUI-Fenster anzeigen.
                    2. Die Ausführung der Anwendungsinstanz starten.
                    3. Das Programm beenden, wenn die Anwendung geschlossen wird.

        param:
                    app: Die Anwendungsinstanz, die die GUI steuert (z.B., QApplication).
        returns: Keine
        """
        # GUI Widgets zeigen
        self.show() 
        sys.exit(app.exec())
      
class Plt_Graph(QtWidgets.QWidget):
    """
    Klasse, um den Graphen zu erzeugen
    Die Klasse enthält folgende Methoden:
    1. plott_ABS_graph(self, time_stamp, price): Methode zum Plotten des ABS-Graphen.
    2. plott_SMA_graph(self, time_stamp, price): Methode zum Plotten des SMA-Graphen.
    3. plott_REGRESSION_graph(self, time_stamp, price): Methode zum Plotten des Regressions-Graphen.
    4. remove_ABS_graph(self): Methode zum Entfernen des ABS-Graphen.
    5. remove_SMA_graph(self): Methode zum Entfernen des SMA-Graphen.
    6. remove_REGRESSION_graph(self): Methode zum Entfernen des Regressions-Graphen.
    7. label_X_axis(self, ticks): Methode zum Setzen der X-Achsenticks.
    8. stock_table_graph(self, timeframe_days, stock_symbol): Methode zum Abrufen von Aktiendaten für einen bestimmten Zeitraum.
    """
    def __init__(self, parent=None):
        """
        Funktion: Konstruktor der Klasse zur Initialisierung des Graphen.
                  1. Einen PlotWidget (Graph) erstellen und grundlegende Einstellungen vornehmen.
                  2. Die Achsenbeschriftungen und das Raster konfigurieren.
                  3. Das PlotWidget dem Layout der Klasse hinzufügen.
                  4. Linien für ABS, SMA und Regression initialisieren.
        param: 
                  parent: Das übergeordnete Widget (Standardwert: None).
        return: Keine
        """
        super().__init__(parent)
        
        #Graphen als Widget erzeugen und konfigurieren
        self.plotWidget = pg.PlotWidget()
        self.plotWidget.setBackground('w')
        self.plotWidget.showGrid(x=True, y=True)
        self.plotWidget.getAxis("left").setLabel("Aktienpreis [€]")
        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(self.plotWidget)
        
        # Plotitems für ABS, SMA und Regression initialisieren
        self.ABS_Line = self.plotWidget.plot()
        self.SMA_Line = self.plotWidget.plot()
        self.REGRESSION_Line = self.plotWidget.plot()
        
    def plott_ABS_graph(self, time_stamp, price):
        """
        Funktion:   Diese Methode plottet einen Graphen für den Absolutwert (ABS).
                    1. Die Daten für den ABS-Graphen setzen und die Linienfarbe festlegen.
        param: 
              time_stamp: Die Zeitstempel für die x-Achse.
              price: Die Aktienpreise für die y-Achse.
        return: Keine
        """
        date_dict = dict(enumerate(time_stamp)) #String in ein dict umwandeln, um dann alsa Liste an setData übergeben zu können
        self.ABS_Line.setData(list(date_dict.keys()), price)
        self.ABS_Line.setPen('#003D5B')
        
    def plott_SMA_graph(self, time_stamp, price):
        """
        Funktion:   Diese Methode plottet einen Graphen für den gleitenden Durchschnitt (SMA).
                    1. Die Daten für den SMA-Graphen setzen und die Linienfarbe festlegen.
        param: 
              time_stamp: Die Zeitstempel für die x-Achse.
              price: Die Aktienpreise für die y-Achse.
        return: Keine
        """
        date_dict = dict(enumerate(time_stamp)) #String in ein dict umwandeln, um dann alsa Liste an setData übergeben zu können
        self.SMA_Line.setData(list(date_dict.keys()), price)
        self.SMA_Line.setPen('#44AF69')
        
    def plott_REGRESSION_graph(self, time_stamp, price):
        """
        Funktion:   Diese Methode plottet einen Graphen für die Regression (TSA).
                    1. Die Daten für den TSA-Graphen setzen und die Linienfarbe festlegen.
        param: 
              time_stamp: Die Zeitstempel für die x-Achse.
              price: Die Aktienpreise für die y-Achse.
        return: Keine
        """
        date_dict = dict(enumerate(time_stamp)) #String in ein dict umwandeln, um dann alsa Liste an setData übergeben zu können
        self.REGRESSION_Line.setData(list(date_dict.keys()), price)
        self.REGRESSION_Line.setPen('#D1495B')
        
    def remove_ABS_graph(self):
        """
        Funktion:   Diese Methode entfernt den Graphen für den Absolutwert (ABS).
                    1. Die Daten des ABS-Graphen leeren.
        param: Keine
        returns: Keine
        """
        self.ABS_Line.setData([], [])
        
    def remove_SMA_graph(self):
       """
       Funktion:   Diese Methode entfernt den Graphen für den gleitenden Drschschnitt (SMA).
                    1. Die Daten des SMA-Graphen leeren.
       param: Keine
       returns: Keine
       """
       self.SMA_Line.setData([], [])
        
    def remove_REGRESSION_graph(self):
       """
       Funktion:   Diese Methode entfernt den Graphen für die Regression (TSA).
                    1. Die Daten des SMA-Graphen leeren.
       param: Keine
       returns: Keine
       """
       self.REGRESSION_Line.setData([], [])
        
    def label_X_axis(self,ticks):
        """
        Funktion: Diese Methode setzt die X-Achsenticks des Graphen.
                  1. Die X-Achsenticks setzen.
        param ticks: Eine Liste von Ticks für die X-Achse.
        returns: Keiner
        """
        self.plotWidget.getAxis("bottom").setTicks([ticks])
        
    def stock_table_graph(self, timeframe_days, stock_symbol):
        """
        Funktion:   Diese Methode ruft Aktiendaten für einen bestimmten Zeitraum ab
                    1. Das heutige Datum und das Datum vor der angegebenen Anzahl von Tagen bestimmen.
                    2. Zeitzone für die Daten festlegen.
                    3. Start- und Enddatum für die Daten festlegen.
                    4. Aktiendaten für den angegebenen Zeitraum abrufen und zurückgeben.
        param   timeframe_days: Die Anzahl der Tage, für die Daten abgerufen werden sollen.
                stock_symbol: Das Symbol der Aktie, für die Daten abgerufen werden sollen.
        returns: stock_data: Eine Liste von Aktiendaten.
        """
        date_today = datetime.today()
        last_date = datetime.today() - timedelta(days=timeframe_days)

        time_offset = timezone(timedelta(hours=-5))
        
        start_date_offset = last_date.replace(tzinfo=time_offset)
        end_date_offset = date_today.replace(tzinfo=time_offset)
        end_date = end_date_offset.strftime('%Y-%m-%d')
        start_date = start_date_offset.strftime('%Y-%m-%d')
       
        stock_data = dd.DisplayData().get_stocks_list(stock_symbol, start_date, end_date)

        return stock_data
    

        
        
        
        