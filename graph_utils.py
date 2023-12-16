import display_data
from datetime import datetime, timedelta

#Diese Funktion generiert eine Liste von Tupeln (Datum, Aktienwert) auf Basis der API (nicht DB!!!)
#Sie benötigt einen Integerwert, der angibt wie alt die Daten sein sollen (Heutiges Datum - Integerwert (in Tagen)) und dem Aktiensymbol.
def populate_graph(timeframe_days, stock_symbol):
    timeframe_start = (datetime.today() - timedelta(days=timeframe_days)).strftime('%Y-%m-%d')
    stock_data = display_data.get_stocks_list(stock_symbol, timeframe_start, datetime.today().strftime('%Y-%m-%d'))
    timeline = [(data[0][:10], data[1]) for data in stock_data if data[0][:10] >= timeframe_start]
    return timeline

#Für den SMA muss eine Liste von Tupeln übergeben werden. An Stelle 0 muss das Datum stehen und an Stelle 1 der Aktienwert
#Darüber hinaus muss ein "Glättungszeitraum" window_size mit übergeben werden (Integer)
def calculate_sma(stock_data, window_size):
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
