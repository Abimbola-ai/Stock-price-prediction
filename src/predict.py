import numpy as np 
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from stocks.scraper import get_data


def predict_future_price(ticker, years):
    df = get_data(ticker, years)
    df_new = df[["adjclose"]]
    forecast_out = 1
    df_new["prediction"] = df_new[["adjclose"]].shift(-forecast_out)
    X = np.array(df_new.loc[:,["adjclose"]])
    X = X[:-forecast_out]
    y = np.array(df_new['prediction'])
    y = y[:-forecast_out]
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    lr = LinearRegression()
    # Train the model
    lr.fit(x_train, y_train)
    lr_confidence = lr.score(x_test, y_test)
    x_forecast = np.array(df_new.loc[:,["adjclose"]])[-forecast_out:]
    lr_prediction = lr.predict(x_forecast)
    return lr_prediction, lr_confidence

