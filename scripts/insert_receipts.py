import sys
import pathlib
# Add project root to sys.path for module imports
sys.path.append(str(pathlib.Path(__file__).parents[1]))
from database import add_item_name_en_column, insert_receipts_from_file

def main():
    # Ensure the column exists
    add_item_name_en_column()
    # Path to the data file (relative to project root)
    data_file = pathlib.Path(__file__).parents[1] / "Data" / "receipts_new.txt"
    insert_receipts_from_file(str(data_file))
    print("✅ Finished inserting receipts.")

if __name__ == "__main__":
    main()
