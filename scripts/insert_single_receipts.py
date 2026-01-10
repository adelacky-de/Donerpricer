import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

records = [
    {
        "item_name": "EIER EH M-L",
        "item_name_en": "EGGS M-L",
        "purchase_date": "2025-11-05", # Wednesday
        "weekday": 2, # Monday=0, Wed=2
        "price_eur": 1.99,
        "supermarket": "REWE",
        "location": "Roggenmarkt 15-16, 48143 Münster", # Default location
        "brand_name": "Unknown"
    },
    {
        "item_name": "KAROTTE REGIONAL",
        "item_name_en": "REGIONAL CARROTS",
        "purchase_date": "2025-11-05",
        "weekday": 2,
        "price_eur": 0.69,
        "supermarket": "REWE",
        "location": "Roggenmarkt 15-16, 48143 Münster",
        "brand_name": "Unknown"
    },
    {
        "item_name": "CREME BRULEE",
        "item_name_en": "CREME BRULEE",
        "purchase_date": "2025-11-05",
        "weekday": 2,
        "price_eur": 1.35,
        "supermarket": "REWE",
        "location": "Roggenmarkt 15-16, 48143 Münster",
        "brand_name": "Unknown"
    }
]

response = supabase.table("receipts").insert(records).execute()
print(f"Inserted {len(response.data)} records.")
print(response.data)
