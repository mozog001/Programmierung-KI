import pandas as pd
from prophet import Prophet

class Analyzing_methods:
    def __init__(self):
        pass
    
    def calculate_sma(self, stock_data, window_size):
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
        data = pd.DataFrame(data, columns=['ds', 'y'])
        forecast = Prophet()
        forecast.fit(data)
        future = forecast.make_future_dataframe(periods=7)
        predict = forecast.predict(future)
        return predict[["ds", "yhat"]].tail()
    
    def get_forecast(self, data, number_days):
        data = pd.DataFrame(data, columns=['ds', 'y'])
        forecast = Prophet()
        forecast.fit(data)
        future = forecast.make_future_dataframe(periods=7)
        predict = forecast.predict(future)
        return predict[["ds", "yhat", "yhat_lower", "yhat_upper"]]