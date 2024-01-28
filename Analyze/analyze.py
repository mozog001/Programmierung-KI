import pandas as pd
from prophet import Prophet

class Analyzing_methods:
    """
    Analyzing_methods ist eine Klasse, die verschiedene Methoden für die Analyse von Aktiendaten bereitstellt.
    Die Klasse enthält folgende MEthoden:
    1. calculate_sma(self, stock_data, window_size): Berechnet den einfachen gleitenden Durchschnitt (SMA) für eine gegebene Fenstergröße.
    2. get_forecast_tail(self, data): Erstellt eine Prognose für die nächsten 7 Tage basierend auf den übergebenen Daten.
    3. get_forecast(self, data): Erstellt eine Prognose für die nächsten 7 Tage basierend auf den übergebenen Daten.
    Das Prognosemodell basieren auf der Prophet-Bibliothek von Facebook (https://facebook.github.io/prophet/docs/quick_start.html).
    Die theoretische Motivation für das Modell ist in diesem Paper beschrieben: https://peerj.com/preprints/3190.pdf
    und beruht auf einer statistischen Zeitreihenanalyse mit einem additiven Modell, das aus vier Komponenten besteht:
    1. Einem Sättigungswachstumstrend
    2. Einem jährlichen saisonalen Effekt
    3. Einem wöchentlichen saisonalen Effekt
    4. Einem unregelmäßigen Term.
    """
    def __init__(self):
        pass
    
    def calculate_sma(self, stock_data, window_size):
        """
        Funktion: Berechnet den einfachen gleitenden Durchschnitt (SMA) für eine gegebene Fenstergröße.
        param:
            - stock_data: Liste von Tupeln, die Datenpunkte repräsentieren (Datum, Wert).
            - window_size: Größe des Fensters für den SMA.
        return:
            - Eine Liste von Tupeln, die den SMA für jeden Datenpunkt repräsentieren.
        """
        sma_values = []
        for i in range(len(stock_data) - window_size + 1):
            window = stock_data[i:i + window_size]        
            # Liste mit Daten generieren
            timestamp = window[-1][0]        
            # Liste mit Preisen generieren
            prices = [item[1] for item in window]        
            sma = sum(prices) / len(prices)        
            sma_values.append((timestamp, sma))    
        return sma_values
     
    def get_forecast_tail(self, data):
        """
        Funktion: Erstellt eine Prognose für die nächsten 7 Tage basierend auf den übergebenen Daten.
        param:
            - data: Liste von Tupeln, die Datenpunkte repräsentieren (Datum, Wert).
        return:
            - predict: Gibt nur die die Prognose für die nächsten 7 Tage als DataFrame mit Spalten 'ds' und 'yhat'.
        """
        data = pd.DataFrame(data, columns=['ds', 'y'])
        forecast = Prophet()
        forecast.fit(data)
        future = forecast.make_future_dataframe(periods=7, freq="B")
        predict = forecast.predict(future)
        return predict[["ds", "yhat"]].tail()
    
    def get_forecast(self, data):
        """
        Funktion: Erstellt eine Prognose für die nächsten 7 Tage basierend auf den übergebenen Daten.
        param:
            - data: Liste von Tupeln, die Datenpunkte repräsentieren (Datum, Wert).
            - number_days: Anzahl der Tage für die Prognose.
        return:
            - predict: Die gesamte Prognose als DataFrame mit Spalten 'ds', 'yhat', 'yhat_lower' und 'yhat_upper'.
        """
        data = pd.DataFrame(data, columns=['ds', 'y'])
        forecast = Prophet()
        forecast.fit(data)
        future = forecast.make_future_dataframe(periods=7, freq="B")
        predict = forecast.predict(future)
        return predict[["ds", "yhat", "yhat_lower", "yhat_upper"]]