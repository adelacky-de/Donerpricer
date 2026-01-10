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
def get_prices_by_item_and_supermarket(item_name, supermarket=None):
    """Retrieves all price records for a given item and optionally supermarket from Supabase as a Pandas DataFrame."""
    query = supabase.table("receipts").select("*").eq("item_name_en", item_name)
    if supermarket:
        query = query.eq("supermarket", supermarket)
    
    response = query.execute()
    
    if response.data:
        df = pd.DataFrame(response.data)
        # Rename columns to match the schema for compatibility with the rest of the app
        df = df.rename(columns={"purchase_date": "date", "price_eur": "price"})
        return df
    else:
        print("Error fetching data:", response)
        return pd.DataFrame()

# Used in main.py __init__() - Populates the product search dropdown on app startup
def get_all_item_names():
    """Retrieves all unique item names from the Supabase 'receipts' table."""
    response = supabase.table("receipts").select("item_name_en").execute()
    if response.data:
        from collections import Counter
        all_names = [row['item_name_en'] for row in response.data if row['item_name_en']]
        counts = Counter(all_names)
        # Filter for items with count >= 3
        item_names = sorted([name for name, count in counts.items() if count >= 3])
        return item_names
    else:
        print("Error fetching item names:", response)
        return []

# Used in main.py update_supermarket_input() - Dynamically fills supermarket dropdown when user selects a product
def get_supermarkets_for_item(item_name):
    """Retrieves all unique supermarket names for a specific item from the Supabase 'receipts' table."""
    response = supabase.table("receipts").select("supermarket").eq("item_name_en", item_name).execute()
    if response.data:
        supermarkets = sorted(list(set([row['supermarket'] for row in response.data if row['supermarket']])))
        return supermarkets
    else:
        print("Error fetching supermarkets for item:", response)
        return []

