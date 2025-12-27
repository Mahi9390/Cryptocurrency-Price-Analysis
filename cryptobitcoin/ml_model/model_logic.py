import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from datetime import timedelta

def predict_future_prices(file_path, crypto_name):
    # Load dataset
    df = pd.read_csv(file_path)
    df = df[df['crypto_name'] == crypto_name]

    # Prepare features
    df = df.sort_values(by='date')
    df['date'] = pd.to_datetime(df['date'])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['target'] = df['close'].shift(-1)
    df.dropna(inplace=True)

    X = df[['open', 'high', 'low', 'volume', 'marketCap']]
    y = df['target']

    # Train RandomForest
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)

    # Predict for next 7 days
    last_row = df.iloc[-1]
    future_dates = [last_row['date'] + timedelta(days=i) for i in range(1, 8)]

    preds = []
    prev_row = last_row.copy()

    for future_date in future_dates:
        X_pred = [[
            prev_row['open'], prev_row['high'], prev_row['low'],
            prev_row['volume'], prev_row['marketCap']
        ]]
        pred_price = model.predict(X_pred)[0]
        preds.append({'date': future_date.date(), 'predicted_price': round(pred_price, 2)})
        prev_row['close'] = pred_price  # update for next day

    return preds
