import pandas as pd
from supabase_client import supabase

def create_receipts_table():
    """
    This function is now a placeholder.
    The table should be created in the Supabase dashboard or via a migration script.
    The required schema is:
    - id: int8 (primary key)
    - item_name: text
    - purchase_date: date
    - weekday: int2
    - price_eur: float4
    - supermarket: text
    - location: text
    """
    print("Please create the 'receipts' table in your Supabase project.")
    print("See the documentation for the required schema.")


def insert_price(item_name, date, price, supermarket, location, brand_name, weight_grams):
    """Inserts a new price record into the Supabase 'receipts' table."""
    # Assuming 'weekday' can be derived from the date
    import datetime
    weekday = datetime.datetime.strptime(date, '%Y-%m-%d').weekday()
    
    data = {
        "item_name": item_name,
        "purchase_date": date,
        "weekday": weekday,
        "price_eur": price,
        "supermarket": supermarket,
        "location": location,
        "brand_name": brand_name,
        "weight_grams": weight_grams,
    }
    
    response = supabase.table("receipts").insert(data).execute()
    
    if response.data:
        print("Inserted data successfully:", response.data)
    else:
        print("Error inserting data:", response)


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

def get_all_item_names():
    """Retrieves all unique item names from the Supabase 'receipts' table."""
    response = supabase.table("receipts").select("item_name").execute()
    if response.data:
        item_names = sorted(list(set([row['item_name'] for row in response.data])))
        return item_names
    else:
        print("Error fetching item names:", response)
        return []

def get_all_brand_names():
    """Retrieves all unique brand names from the Supabase 'receipts' table."""
    response = supabase.table("receipts").select("brand_name").execute()
    if response.data:
        brand_names = sorted(list(set([row['brand_name'] for row in response.data if row['brand_name']])))
        return brand_names
    else:
        print("Error fetching brand names:", response)
        return []

def get_brands_for_item(item_name):
    """Retrieves all unique brand names for a specific item from the Supabase 'receipts' table."""
    response = supabase.table("receipts").select("brand_name").eq("item_name", item_name).execute()
    if response.data:
        brand_names = sorted(list(set([row['brand_name'] for row in response.data if row['brand_name']])))
        return brand_names
    else:
        print("Error fetching brand names for item:", response)
        return []

if __name__ == '__main__':
    # This script is now for manual testing and examples
    # create_receipts_table()
    # insert_price("Oat Milk", "2025-10-17", 1.59, "Super C", "Münster Nord", "Oaty", 1000)
    df = get_prices_by_item_and_brand("Oat Milk", "Oaty")
    print(df)
    all_items = get_all_item_names()
    print("All unique items:", all_items)
    all_brands = get_all_brand_names()
    print("All unique brands:", all_brands)
    oat_milk_brands = get_brands_for_item("Oat Milk")
    print("Oat Milk brands:", oat_milk_brands)