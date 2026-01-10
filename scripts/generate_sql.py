import json
import pathlib

def json_value_to_sql(value):
    if value is None:
        return "NULL"
    if isinstance(value, str):
        # Escape single quotes
        escaped = value.replace("'", "''")
        return f"'{escaped}'"
    return str(value)

def main():
    # Define paths
    input_path = pathlib.Path(__file__).parents[1] / "Data" / "receipts_new.txt"
    output_path = pathlib.Path(__file__).parents[1] / "Data" / "receipts_insert.sql"

    if not input_path.exists():
        print(f"Error: {input_path} not found.")
        return

    # Read JSON
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if not data:
        print("No data found.")
        return

    # Extract columns from the first record
    # Ensure item_name_en is included (it should be in the json)
    first_record = data[0]
    columns = list(first_record.keys())
    
    # Start writing SQL
    with open(output_path, 'w', encoding='utf-8') as sql_file:
        # Add column if not exists
        sql_file.write("-- Ensure the column exists\n")
        sql_file.write("ALTER TABLE receipts ADD COLUMN IF NOT EXISTS item_name_en text;\n\n")
        
        # Write INSERT statement header
        # Postgres supports bulk insert: INSERT INTO x (col1, col2) VALUES (v1, v2), (v3, v4)...
        # We will do batches of 1000 to be safe
        
        batch_size = 1000
        total_records = len(data)
        
        for i in range(0, total_records, batch_size):
            batch = data[i:i+batch_size]
            
            col_names = ", ".join(columns)
            sql_file.write(f"INSERT INTO receipts ({col_names}) VALUES\n")
            
            values_list = []
            for record in batch:
                # Ensure order matches columns
                row_values = []
                for col in columns:
                    val = record.get(col)
                    row_values.append(json_value_to_sql(val))
                
                values_str = "(" + ", ".join(row_values) + ")"
                values_list.append(values_str)
            
            # Join all values with commas
            sql_file.write(",\n".join(values_list))
            
            # End statement
            # Use ON CONFLICT if needed, but for now just ;
            # If IDs might clash, usage of ON CONFLICT (id) DO NOTHING might be better?
            # User just said "insert it", assuming new data or fresh table.
            # Let's add ON CONFLICT DO UPDATE for robustness if ID exists? Or just nothing?
            # Safest is usually DO NOTHING or just standard insert. Let's do standard and let it fail if dupes, 
            # OR we can assume `id` is potentially serial.
            # Given the data has explicit IDs, let's use ON CONFLICT (id) DO UPDATE SET ...
            # Actually, let's just stick to straight INSERT for now as requested.
            sql_file.write("\nON CONFLICT (id) DO UPDATE SET\n")
            # Generate set clause for update
            set_clauses = []
            for col in columns:
                if col != 'id':
                    set_clauses.append(f"{col} = EXCLUDED.{col}")
            sql_file.write("  " + ", ".join(set_clauses))
            sql_file.write(";\n\n")

    print(f"Generated SQL file at: {output_path}")

if __name__ == "__main__":
    main()
