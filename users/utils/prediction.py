# users/utils/prediction.py

import os
import gc
import pandas as pd
import numpy as np
import yfinance as yf

from datetime import datetime, timedelta
from django.conf import settings

from tensorflow.keras.models import load_model
import tensorflow as tf
import joblib

import plotly.graph_objects as go

# --------------------------------------------------
# TensorFlow silent mode
# --------------------------------------------------
tf.get_logger().setLevel("ERROR")

# --------------------------------------------------
# Configuration
# --------------------------------------------------
MODEL_PATH = os.path.join(settings.BASE_DIR, "ml_models", "lstm_bitcoin_model.keras")
SCALER_PATH = os.path.join(settings.BASE_DIR, "ml_models", "minmax_scaler.joblib")
LOOK_BACK = 60

# --------------------------------------------------
# Lazy-loaded global objects
# --------------------------------------------------
_model = None
_scaler = None


def get_model_and_scaler():
    global _model, _scaler

    if _model is None:
        _model = load_model(MODEL_PATH)

    if _scaler is None:
        _scaler = joblib.load(SCALER_PATH)

    return _model, _scaler


# --------------------------------------------------
# Supported cryptocurrencies
# --------------------------------------------------
CRYPTO_SYMBOLS = {
    "Bitcoin": "BTC-USD",
    "Ethereum": "ETH-USD",
    "Binance Coin": "BNB-USD",
    "Ripple": "XRP-USD",
    "Solana": "SOL-USD",
    "Cardano": "ADA-USD",
    "Dogecoin": "DOGE-USD",
    "Shiba Inu": "SHIB-USD",
    "Polkadot": "DOT-USD",
    "TRON": "TRX-USD",
    "Litecoin": "LTC-USD",
}


# --------------------------------------------------
# Data Fetching
# --------------------------------------------------
def fetch_data(symbol, start_date, end_date):
    df = yf.download(
        symbol,
        start=start_date,
        end=end_date,
        progress=False,
        auto_adjust=False
    )

    if df is None or df.empty:
        raise ValueError("Yahoo Finance returned no data")

    # Flatten MultiIndex columns
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    if "Close" not in df.columns:
        raise ValueError("Close price not found in data")

    df["Close"] = pd.to_numeric(df["Close"], errors="coerce")
    df.dropna(subset=["Close"], inplace=True)

    return df


# --------------------------------------------------
# Forecast logic
# --------------------------------------------------
def forecast_next_n_days(last_sequence_scaled, n_days):
    model, scaler = get_model_and_scaler()

    current_seq = last_sequence_scaled.copy()
    predictions = []

    for _ in range(n_days):
        pred = model.predict(current_seq, verbose=0)

        if pred is None or np.isnan(pred).any():
            raise ValueError("Model returned NaN predictions")

        predictions.append(pred[0, 0])

        current_seq = np.roll(current_seq, -1, axis=1)
        current_seq[0, -1, 0] = pred[0, 0]

    predictions = np.array(predictions).reshape(-1, 1)
    return scaler.inverse_transform(predictions).flatten()


# --------------------------------------------------
# Main Prediction Function
# --------------------------------------------------
def predict_crypto(coin_name, start_date_str, end_date_str, forecast_days=7):

    if not start_date_str or not end_date_str:
        raise ValueError("Start date and End date are required")

    if coin_name not in CRYPTO_SYMBOLS:
        raise ValueError("Invalid cryptocurrency selected")

    symbol = CRYPTO_SYMBOLS[coin_name]

    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    if start_date >= end_date:
        raise ValueError("Start date must be before end date")

    # --------------------------------------------------
    # Fetch data
    # --------------------------------------------------
    df = fetch_data(symbol, start_date, end_date + timedelta(days=1))

    if len(df) < LOOK_BACK:
        raise ValueError(f"At least {LOOK_BACK} days of data required")

    df.index = pd.to_datetime(df.index).normalize()

    prices = df["Close"].astype(float).values.reshape(-1)
    dates = df.index

    # --------------------------------------------------
    # Prepare LSTM input
    # --------------------------------------------------
    model, scaler = get_model_and_scaler()

    last_prices = prices[-LOOK_BACK:]
    scaled_last = scaler.transform(last_prices.reshape(-1, 1))
    last_sequence = scaled_last.reshape(1, LOOK_BACK, 1)

    # --------------------------------------------------
    # Forecast
    # --------------------------------------------------
    forecasted_prices = forecast_next_n_days(last_sequence, forecast_days)

    forecasted_prices = np.nan_to_num(
        forecasted_prices,
        nan=prices[-1],
        posinf=prices[-1],
        neginf=prices[-1],
    )

    # --------------------------------------------------
    # Future dates
    # --------------------------------------------------
    last_date = dates[-1]

    future_dates = pd.date_range(
        start=last_date + timedelta(days=1),
        periods=forecast_days,
        freq="D",
    )

    # --------------------------------------------------
    # Plotly chart
    # --------------------------------------------------
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dates,
        y=prices,
        mode="lines",
        name="Historical"
    ))

    fig.add_trace(go.Scatter(
        x=future_dates,
        y=forecasted_prices,
        mode="lines",
        name="Forecast",
        line=dict(dash="dash")
    ))

    fig.update_layout(
        title=f"{coin_name} ({symbol}) Price Forecast",
        xaxis_title="Date",
        yaxis_title="USD",
        template="plotly_white",
    )

    chart_html = fig.to_html(full_html=True, include_plotlyjs=True)

    # --------------------------------------------------
    # Forecast table
    # --------------------------------------------------
    forecast_table = [
        {
            "date": d.strftime("%Y-%m-%d"),
            "price": f"{float(p):.2f}",
        }
        for d, p in zip(future_dates, forecasted_prices)
    ]

    gc.collect()

    return {
        "chart": chart_html,
        "forecast_table": forecast_table,
        "symbol": symbol,
        "coin_name": coin_name,
        "feedback": "Model trained on BTC historical data. Best accuracy for Bitcoin.",
        "color": "orange",
    }
