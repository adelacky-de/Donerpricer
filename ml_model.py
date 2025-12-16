import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta

def get_recommendation(df):
    """
    Generates a recommendation based on historical price data using a simple linear regression model.
    Returns a dictionary with recommendation string and confidence score.
    """
    if len(df) < 2:
        return {"recommendation": "Not enough data for a recommendation.", "confidence": 0}

    # Ensure 'date' column is datetime and sort
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by='date')

    # Feature Engineering
    df['day_of_week'] = df['date'].dt.dayofweek
    df['day_of_year'] = df['date'].dt.dayofyear
    
    # Calculate rolling average and volatility
    df['rolling_avg'] = df['price'].rolling(window=min(7, len(df)), min_periods=1).mean()
    df['price_volatility'] = df['price'].rolling(window=min(7, len(df)), min_periods=1).std().fillna(0)

    # One-hot encode brand_name
    df = pd.get_dummies(df, columns=['brand_name'], prefix='brand')

    # Prepare features and target
    features = ['day_of_year', 'day_of_week', 'rolling_avg', 'price_volatility', 'weight_grams']
    # Add brand columns to features
    brand_columns = [col for col in df.columns if col.startswith('brand_')]
    features.extend(brand_columns)
    
    # Ensure all feature columns exist, fill missing with 0
    for col in features:
        if col not in df.columns:
            df[col] = 0

    # Fill NaN values in weight_grams with 0
    df['weight_grams'] = df['weight_grams'].fillna(0)

    X = df[features]
    y = df['price']

    # Train Model
    model = LinearRegression()
    model.fit(X, y)

    # Predict for the next 7 days
    today = datetime.now()
    future_dates = [today + timedelta(days=i) for i in range(7)]
    
    # Create future features, using the last known values for prediction
    last_row = df.iloc[-1]
    future_features_data = {
        'day_of_year': [d.timetuple().tm_yday for d in future_dates],
        'day_of_week': [d.weekday() for d in future_dates],
        'rolling_avg': [last_row['rolling_avg']] * 7,
        'price_volatility': [last_row['price_volatility']] * 7,
        'weight_grams': [last_row['weight_grams']] * 7,
    }
    for col in brand_columns:
        future_features_data[col] = [last_row[col]] * 7

    future_features = pd.DataFrame(future_features_data)
    
    # Ensure future_features has the same columns as X
    for col in X.columns:
        if col not in future_features.columns:
            future_features[col] = 0
    future_features = future_features[X.columns] # Ensure order is the same

    predictions = model.predict(future_features)
    
    # Find best day to buy
    best_day_index = np.argmin(predictions)
    best_day = future_dates[best_day_index].strftime("%A")
    predicted_price = predictions[best_day_index]

    # Basic statistics
    avg_price = df["price"].mean()
    
    # Calculate confidence (simple heuristic: inverse of volatility, scaled)
    # If volatility is 0, set confidence to 100. Otherwise, scale it.
    if df['price_volatility'].mean() == 0:
        confidence = 100
    else:
        confidence = max(0, min(100, int(100 - (df['price_volatility'].mean() * 50)))) # Scale volatility to confidence

    recommendation_str = f"ᝰ.ᐟ\nAverage price: {avg_price:.2f} €\n"
    recommendation_str += f"Predicted best day to buy: {best_day}\n"
    recommendation_str += f"Predicted price: {predicted_price:.2f} €"
    
    return {"recommendation": recommendation_str, "confidence": confidence}
