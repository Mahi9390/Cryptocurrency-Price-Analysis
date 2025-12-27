# predictor.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from datetime import timedelta
from .models import cryptcurrencyratemodel  # Import Django model (adjust path as needed)
import warnings

warnings.filterwarnings("ignore")

def predict_prices(dataset_path, coin_name=None, days=7, min_data_points=30):
    """
    Predicts cryptocurrency prices for the next 7 days.
    Args:
        dataset_path (str): Path to the dataset CSV file.
        coin_name (str, optional): Specific cryptocurrency to predict. If None, predict for all.
        days (int): Number of days to predict (default: 7).
        min_data_points (int): Minimum data points required for training.
    Returns:
        list: List of dictionaries with predictions ({'crypto_name', 'date', 'predicted_price'}).
        dict: RMSE scores for each cryptocurrency.
    """
    try:
        # Load and validate dataset
        df = pd.read_csv(dataset_path)
        required_columns = ['date', 'crypto_name', 'open', 'high', 'low', 'close', 'volume', 'marketcap']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")

        # Convert date to datetime and extract features
        df['date'] = pd.to_datetime(df['date'])
        df['day'] = df['date'].dt.day
        df['month'] = df['date'].dt.month
        df['year'] = df['date'].dt.year
        df['weekday'] = df['date'].dt.weekday

        # Features for Random Forest
        features = ['open', 'high', 'low', 'volume', 'marketcap', 'day', 'month', 'year', 'weekday']
        results = []
        rmse_scores = {}

        # Get unique cryptocurrencies
        crypto_names = [coin_name] if coin_name else df['crypto_name'].unique()

        for crypto in crypto_names:
            crypto_data = df[df['crypto_name'] == crypto].sort_values('date')
            
            if len(crypto_data) < min_data_points:
                print(f"Skipping {crypto} due to insufficient data ({len(crypto_data)} rows).")
                continue

            # Prepare features and target
            X = crypto_data[features]
            y = crypto_data['close']
            
            # Train-test split (no shuffling for time series)
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
            
            # Train Random Forest
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            
            # Calculate RMSE
            y_pred = model.predict(X_test)
            rmse = np.sqrt(mean_squared_error(y_test, y_pred))
            rmse_scores[crypto] = rmse
            print(f"{crypto} RMSE: {rmse:.4f}")

            # Get current price from cryptcurrencyratemodel for scaling
            try:
                current_price = cryptcurrencyratemodel.objects.get(currencytype=crypto).doller
                last_dataset_price = crypto_data['close'].iloc[-1]
                scaling_factor = current_price / last_dataset_price if last_dataset_price != 0 else 1.0
            except cryptcurrencyratemodel.DoesNotExist:
                print(f"No current price found for {crypto} in cryptcurrencyratemodel. Using unscaled predictions.")
                scaling_factor = 1.0

            # Predict next 7 days
            last_row = crypto_data.iloc[-1].copy()
            future_dates = pd.date_range(start=last_row['date'] + timedelta(days=1), periods=days)
            
            for date in future_dates:
                row = last_row.copy()
                row['day'] = date.day
                row['month'] = date.month
                row['year'] = date.year
                row['weekday'] = date.weekday()
                
                # Estimate other features
                row['open'] = last_row['close']  # Assume next day's open is previous close
                row['high'] = last_row['high']  # Keep last known values (improve as needed)
                row['low'] = last_row['low']
                row['volume'] = last_row['volume']
                row['marketcap'] = last_row['marketcap']
                
                # Predict and scale
                pred_price = model.predict([row[features]])[0] * scaling_factor
                results.append({
                    'crypto_name': crypto,
                    'date': date.date(),
                    'predicted_price': pred_price
                })
                
                # Update last_row for sequential prediction
                last_row['close'] = pred_price

        return results, rmse_scores

    except Exception as e:
        print(f"Error processing dataset: {e}")
        return [], {}

def visualize_predictions(results, crypto_name):
    """
    Visualize predictions for a specific cryptocurrency (for debugging).
    Args:
        results (list): List of prediction dictionaries.
        crypto_name (str): Cryptocurrency to visualize.
    """
    import matplotlib.pyplot as plt
    forecast_df = pd.DataFrame(results)
    crypto_forecast = forecast_df[forecast_df['crypto_name'] == crypto_name].sort_values('date')
    
    if not crypto_forecast.empty:
        plt.figure(figsize=(10, 6))
        plt.plot(crypto_forecast['date'], crypto_forecast['predicted_price'], marker='o')
        plt.xlabel('Date')
        plt.ylabel('Predicted Price (USD)')
        plt.title(f'Predicted {crypto_name} Price Over Next 7 Days')
        plt.grid(True)
        plt.show()