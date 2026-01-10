# The Dönerpricer 🌯

**A Vintage-Themed Grocery Price Tracker & Predictor**

The Dönerpricer is a Python application that tracks grocery price fluctuations and uses Machine Learning to predict the best days to buy. Wrapped in a distinctive vintage newspaper aesthetic, it combines historical data analysis with a local inspiration.

## 🥙 Inspiration
The name "Dönerpricer" comes from a local student saying in Münster, Germany: using the price of a Döner Kebab as a "Döner Index" to benchmark inflation. This project applies that same spirit to everyday groceries, helping you beat price hikes.

## 🚀 Key Features
- **Price Prediction**: Uses Ridge Regression (ML) to forecast the optimal buying day.
- **Smart Search**: Filters history by item and supermarket to show targeted trends.
- **Interactive Maps**: Visualizes purchase locations with custom markers.
- **Vintage UI**: A unique newspaper-style interface powered by PySide6.


## 📚 Build It Yourself (Educational Resources)
This project is also a complete course! The `Helper_notes/` directory contains step-by-step Jupyter Notebooks to build this app from scratch:

1.  **`1. DB_Connection.ipynb`**: Connect Python to a Cloud Database (Supabase).
2.  **`2.1 ML_Donerpricer.ipynb`**: Build the ML Brain (Ridge Regression).
3.  **`3. Plot_Hover_Style.ipynb`**: Create Interactive Charts.
4.  **`4. OSMmap_Label.ipynb`**: Integrate Maps & Geocoding.
5.  **`5. MainFunctions.ipynb`**: Wire it all together.

## 🛠️ Data Origin
- **Real Data**: Unprefixed entries are real data collected over 3 months in Münster.
- **Mock Data**: Entries with prefix `M_` are validation datasets used for testing.
- **Note**: Predictions will become more accurate as the real-world dataset grows over time.

## ⚙️ Tech Stack
- **GUI**: PySide6
- **ML**: scikit-learn (RidgeCV)
- **Data**: Pandas, NumPy, Supabase (PostgreSQL)
- **Viz**: Matplotlib, Leaflet.js

## 📦 Setup
1.  Install dependencies:
    ```bash
    pip install PySide6 pandas numpy scikit-learn supabase matplotlib python-dotenv
    ```
2.  Set up `.env` file with your Supabase credentials: (you can insert the sample data from 'sampledata.json' into your supabase database)
    ```
    SUPABASE_URL=your_url
    SUPABASE_KEY=your_key
    ```
3.  Run the app:
    ```bash
    python main.py
    ```
