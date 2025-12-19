import os
import pandas as pd
from supabase import create_client, Client
from dotenv import load_dotenv

# Initialize Supabase client
load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

if not url or not key:
    raise ValueError("Supabase URL and Key must be set in the .env file.")

supabase: Client = create_client(url, key)

# Used in main.py search_item() - Fetches complete historical data for ML prediction, table, chart, and map
def get_prices_by_item_and_brand(item_name, brand_name=None):
    """Retrieves all price records for a given item and optionally brand from Supabase as a Pandas DataFrame."""
    query = supabase.table("receipts").select("*").eq("item_name", item_name)
    if brand_name:
        query = query.eq("brand_name", brand_name)
    
    response = query.execute()
    
    if response.data:
        df = pd.DataFrame(response.data)
        # Rename columns to match the old schema for compatibility with the rest of the app
        df = df.rename(columns={"purchase_date": "date", "price_eur": "price"})
        return df
    else:
        print("Error fetching data:", response)
        return pd.DataFrame()

# Used in main.py __init__() - Populates the product search dropdown on app startup
def get_all_item_names():
    """Retrieves all unique item names from the Supabase 'receipts' table."""
    response = supabase.table("receipts").select("item_name").execute()
    if response.data:
        item_names = sorted(list(set([row['item_name'] for row in response.data])))
        return item_names
    else:
        print("Error fetching item names:", response)
        return []

# Used in main.py update_brand_input() - Dynamically fills brand dropdown when user selects a product
def get_brands_for_item(item_name):
    """Retrieves all unique brand names for a specific item from the Supabase 'receipts' table."""
    response = supabase.table("receipts").select("brand_name").eq("item_name", item_name).execute()
    if response.data:
        brand_names = sorted(list(set([row['brand_name'] for row in response.data if row['brand_name']])))
        return brand_names
    else:
        print("Error fetching brand names for item:", response)
        return []