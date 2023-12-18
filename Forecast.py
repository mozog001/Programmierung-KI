import pandas as pd
from prophet import Prophet  # https://facebook.github.io/prophet/docs/quick_start.html
from prophet.plot import plot_plotly, plot_components_plotly
#  https://peerj.com/preprints/3190.pdf
import Database as StockDB


class Forecast:
    def __init__(self):
        self.stockname = None
        self.stockDB = StockDB.StockDatabase()

    def get_forecast(self, stockname):
        self.stockname = stockname
        data = self.stockDB.getStockCloseData(self.stockname)
        data = pd.DataFrame(data, columns=['ds', 'y'])
        forecast = Prophet()
        forecast.fit(data)
        future = forecast.make_future_dataframe(periods=365)
        predict = forecast.predict(future)
        return predict[["yhat", "yhat_lower", "yhat_upper"]]


if __name__ == "__main__":
    test = Forecast()
    test_data = test.get_forecast("AAPL")
    print(test_data)


# data = pd.read_csv("stock_data.csv")
# data[['date', 'time']] = data['Date'].str.split(' ', expand=True)
# df = data[['date', 'Close']]
# df = df.rename(columns={"date": "ds", "Close": "y"})
# m = Prophet()
# m.fit(df)
# future = m.make_future_dataframe(periods=365)
# forecast = m.predict(future)
# forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
# plot_plotly(m, forecast).show()
# plot_components_plotly(m, forecast).show()
# print(forecast)
