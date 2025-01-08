from flask import Flask, render_template, request
import pandas as pd
import pickle
from statsmodels.tsa.arima.model import ARIMA

app = Flask(__name__)

# Load your preprocessed data (pickled dataframe)
with open('df_agg.pkl', 'rb') as file:
    df_agg = pickle.load(file)

# ARIMA forecasting function
def generate_forecast(p, d, q):
    # Check if 'Date' is the index or a column
    if 'Date' in df_agg.columns:
        df_agg['Date'] = pd.to_datetime(df_agg['Date'])
        df_agg.set_index('Date', inplace=True)
    elif isinstance(df_agg.index, pd.DatetimeIndex):
        pass
    else:
        raise KeyError("Date column or index not found in the DataFrame")

    # ARIMA forecasting logic
    model = ARIMA(df_agg['Revenue'], order=(p, d, q))
    model_fit = model.fit()

    # Generate forecast as a Pandas Series
    forecast_series = model_fit.forecast(steps=10)

    # Convert Pandas Series to dictionary with proper labels
    forecast_dict = {f"Period {i + 1}": revenue for i, revenue in enumerate(forecast_series)}

    return forecast_dict



@app.route("/", methods=["GET", "POST"])
def index():
    forecast = None
    if request.method == "POST":
        p = int(request.form["p"])
        d = int(request.form["d"])
        q = int(request.form["q"])

        # Generate forecast
        forecast = generate_forecast(p, d, q)

    return render_template("index.html", forecast=forecast)

if __name__ == "__main__":
    app.run(debug=True)
