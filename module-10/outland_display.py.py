"""
Milestone 2: Outland Adventures Data Display Script
Reads data from all primary tables and prints to the console.
"""
import mysql.connector
from mysql.connector import errorcode
from dotenv import dotenv_values
import sys 

# --- 1. Database Configuration Setup ---
secrets = dotenv_values(".env")

# Ensure .env variables are present
if not secrets.get("USER") or not secrets.get("PASSWORD"):
    print("FATAL ERROR: .env file missing or incomplete.")
    sys.exit(1)

config = {
    "user": secrets["USER"],
    "password": secrets["PASSWORD"],
    "host": secrets.get("HOST", "localhost"),
    # Set the database name created in your SQL script
    "database": "outland_adventures", 
    "raise_on_warnings": True
}

# --- 2. Custom Function for Data Display ---

def display_table_data(cursor, table_name, columns, fetch_query):
    """Executes a query and displays the results in a formatted table."""
    
    print("\n" + "=" * 80)
    print(f"--- DISPLAYING DATA FROM TABLE: {table_name} ---")
    print("=" * 80)
    
    try:
        cursor.execute(fetch_query)
        records = cursor.fetchall()
        
        # Print header
        header = " | ".join(columns)
        print(header)
        print("-" * 80)
        
        # Print records
        for record in records:
            # Format output dynamically based on number of columns
            print(" | ".join(str(item) for item in record))
            
    except mysql.connector.Error as err:
        print(f"ERROR displaying {table_name}: {err}")
    finally:
        print("-" * 80)


# --- 3. Main Execution Block ---

db = None
cursor = None
try:
    # Connect to the database
    db = mysql.connector.connect(**config)
    cursor = db.cursor()
    print("Database Connection Successful.")

    # List of tables and their respective SELECT statements
    tables_to_display = [
        ("CUSTOMER", ["ID", "Name", "Email"], "SELECT cust_id, first_name, email FROM CUSTOMER"),
        ("EMPLOYEE", ["ID", "Name", "Role"], "SELECT emp_id, first_name, emp_role FROM EMPLOYEE"),
        ("LOCATION", ["ID", "Name"], "SELECT location_id, location_name FROM LOCATION"),
        ("TRIP", ["ID", "Name", "Start Date", "Location ID"], "SELECT trip_id, trip_name, start_date, location_id FROM TRIP"),
        ("SUPPLIER", ["ID", "Name"], "SELECT supplier_id, supplier_name FROM SUPPLIER"),
        ("INVENTORY_ITEM", ["ID", "Name", "Date"], "SELECT item_id, item_name, purchase_date FROM INVENTORY_ITEM"),
        ("EQUIPMENT_TRANSACTION", ["Customer ID", "Item ID", "Type", "Price"], "SELECT cust_id, item_id, transaction_type, final_price FROM EQUIPMENT_TRANSACTION"),
        ("GUIDE_ASSIGNMENT", ["Trip ID", "Guide ID"], "SELECT trip_id, emp_id FROM GUIDE_ASSIGNMENT")
    ]
    
    # Iterate and display data for each table
    for table_name, columns, query in tables_to_display:
        display_table_data(cursor, table_name, columns, query)

except mysql.connector.Error as err:
    print("\n" + "="*80)
    print("FATAL DATABASE ERROR:")
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Invalid username or password in .env file.")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print(f"Database '{config['database']}' does not exist.")
    else:
        print(err)
    print("="*80)

finally:
    if cursor:
        cursor.close()
    if db and db.is_connected():
        db.close()
        print("\nDatabase connection closed.")
