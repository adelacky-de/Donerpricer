import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import RidgeCV
from datetime import datetime, timedelta

def get_recommendation(df):
    """
    Generates a recommendation based on historical price data using a simple linear regression model.
    Returns a dictionary with recommendation string and confidence score.
    """
    # Set random seed for reproducibility
    np.random.seed(42)

    if len(df) < 2:
        return {"recommendation": "Not enough data for a recommendation.", "confidence": 0}

    # Ensure 'date' column is datetime and sort
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by='date')

    # Feature Engineering
    df['day_of_week'] = df['date'].dt.dayofweek
    df['day_of_year'] = df['date'].dt.dayofyear
    df['month'] = df['date'].dt.month
    
    # Calculate rolling average and volatility
    df['rolling_avg'] = df['price'].rolling(window=min(7, len(df)), min_periods=1).mean()
    df['price_volatility'] = df['price'].rolling(window=min(7, len(df)), min_periods=1).std().fillna(0)

    # One-hot encode categorical features
    df = pd.get_dummies(df, columns=['brand_name', 'supermarket', 'location'], prefix=['brand', 'supermarket', 'location'])

    # Prepare features and target
    features = ['day_of_year', 'day_of_week', 'month', 'rolling_avg', 'price_volatility', 'weight_grams']
    # Add one-hot encoded columns to features
    categorical_columns = [col for col in df.columns if col.startswith(('brand_', 'supermarket_', 'location_'))]
    features.extend(categorical_columns)
    
    # Fill NaN values in weight_grams with 0
    df['weight_grams'] = df['weight_grams'].fillna(0)

    # Ensure all feature columns exist, fill missing with 0
    for col in features:
        if col not in df.columns:
            df[col] = 0
    
    # Filter features to only include those present in the DataFrame
    X = df[features].copy()
    y = df['price']

    # Convert boolean columns to integers (0 or 1)
    for col in X.columns:
        if X[col].dtype == 'bool':
            X[col] = X[col].astype(int)

    # Ensure all columns are numeric and handle any remaining non-numeric data
    X = X.apply(pd.to_numeric, errors='coerce').fillna(0)

    # Feature Scaling - Fairness Training (as shown in notebook)
    # Math: z = (x - μ) / σ
    # This ensures all features are on a similar scale, making regularization fair
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Train Ridge Regression with Cross-Validation
    # CV=5 means 5-fold cross-validation to find the best alpha (lambda)
    # The model automatically tests [0.1, 1.0, 10.0] and chooses the best
    model = RidgeCV(alphas=[0.1, 1.0, 10.0], cv=5)
    model.fit(X_scaled, y)

    # Predict for the next 7 days
    today = datetime.now()
    future_dates = [today + timedelta(days=i) for i in range(7)]
    
    # Create future features, using the last known values for prediction
    last_row = df.iloc[-1]
    future_features_data = {
        'day_of_year': [d.timetuple().tm_yday for d in future_dates],
        'day_of_week': [d.weekday() for d in future_dates],
        'month': [d.month for d in future_dates],
        'rolling_avg': [last_row['rolling_avg']] * 7,
        'price_volatility': [last_row['price_volatility']] * 7,
        'weight_grams': [last_row['weight_grams']] * 7,
    }
    
    # Add one-hot encoded columns for future features
    for col in categorical_columns:
        future_features_data[col] = [last_row[col]] * 7

    future_features_df = pd.DataFrame(future_features_data)
    
    # Ensure future_features_df has the same columns as X
    for col in X.columns:
        if col not in future_features_df.columns:
            future_features_df[col] = 0
    future_features_df = future_features_df[X.columns] # Ensure order is the same

    # Ensure all columns in future_features_df are numeric
    future_features_df = future_features_df.apply(pd.to_numeric, errors='coerce').fillna(0)

    # Scale future features and make predictions
    future_features_scaled = scaler.transform(future_features_df)
    predictions = model.predict(future_features_scaled)
    
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
    recommendation_header_str = "Prediction"
    recommendation_str = ""
    recommendation_str += f"Best day to buy: {best_day}\n"
    recommendation_str += f"Best Price: {predicted_price:.2f} €\n"
    recommendation_str += f"Confidence: {confidence:.2f}%"
    return {"recommendation_header":recommendation_header_str, "recommendation": recommendation_str}
