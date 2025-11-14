"""
Load CSV files into SQLite database rideshare.db
"""
import sqlite3
import csv
from pathlib import Path

# Create necessary directories
Path("sql").mkdir(exist_ok=True)

def create_tables(cursor):
    """Create all tables with proper schema."""
    # Drivers table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS drivers (
            driver_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            phone TEXT,
            rating REAL,
            join_date TEXT,
            city TEXT
        )
    """)
    
    # Riders table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS riders (
            rider_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT,
            signup_date TEXT,
            city TEXT
        )
    """)
    
    # Vehicles table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vehicles (
            vehicle_id INTEGER PRIMARY KEY,
            driver_id INTEGER NOT NULL,
            make TEXT,
            model TEXT,
            year INTEGER,
            plate_number TEXT,
            FOREIGN KEY (driver_id) REFERENCES drivers(driver_id)
        )
    """)
    
    # Trips table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS trips (
            trip_id INTEGER PRIMARY KEY,
            rider_id INTEGER NOT NULL,
            driver_id INTEGER NOT NULL,
            vehicle_id INTEGER NOT NULL,
            start_time TEXT,
            end_time TEXT,
            start_location TEXT,
            end_location TEXT,
            distance_km REAL,
            fare REAL,
            FOREIGN KEY (rider_id) REFERENCES riders(rider_id),
            FOREIGN KEY (driver_id) REFERENCES drivers(driver_id),
            FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id)
        )
    """)
    
    # Payments table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            payment_id INTEGER PRIMARY KEY,
            trip_id INTEGER NOT NULL,
            amount REAL,
            method TEXT,
            status TEXT,
            payment_time TEXT,
            FOREIGN KEY (trip_id) REFERENCES trips(trip_id)
        )
    """)
    
    print("Tables created successfully")

def load_csv_to_table(conn, cursor, csv_file, table_name, columns):
    """Load data from CSV file into SQLite table."""
    filepath = Path("data") / csv_file
    
    if not filepath.exists():
        print(f"Warning: {csv_file} not found, skipping...")
        return 0
    
    # Clear existing data
    cursor.execute(f"DELETE FROM {table_name}")
    
    # Read and insert data
    count = 0
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Prepare values in the correct order
            values = [row.get(col) for col in columns]
            placeholders = ','.join(['?'] * len(values))
            query = f"INSERT INTO {table_name} ({','.join(columns)}) VALUES ({placeholders})"
            cursor.execute(query, values)
            count += 1
    
    conn.commit()
    return count

def main():
    """Main function to load all CSV files into SQLite."""
    # Connect to database (creates if doesn't exist)
    conn = sqlite3.connect("rideshare.db")
    cursor = conn.cursor()
    
    print("Creating database schema...")
    create_tables(cursor)
    
    print("\nLoading data from CSV files...")
    
    # Load drivers
    drivers_count = load_csv_to_table(
        conn, cursor, "drivers.csv", "drivers",
        ["driver_id", "name", "phone", "rating", "join_date", "city"]
    )
    
    # Load riders
    riders_count = load_csv_to_table(
        conn, cursor, "riders.csv", "riders",
        ["rider_id", "name", "email", "signup_date", "city"]
    )
    
    # Load vehicles
    vehicles_count = load_csv_to_table(
        conn, cursor, "vehicles.csv", "vehicles",
        ["vehicle_id", "driver_id", "make", "model", "year", "plate_number"]
    )
    
    # Load trips
    trips_count = load_csv_to_table(
        conn, cursor, "trips.csv", "trips",
        ["trip_id", "rider_id", "driver_id", "vehicle_id", "start_time", "end_time",
         "start_location", "end_location", "distance_km", "fare"]
    )
    
    # Load payments
    payments_count = load_csv_to_table(
        conn, cursor, "payments.csv", "payments",
        ["payment_id", "trip_id", "amount", "method", "status", "payment_time"]
    )
    
    # Print summary
    print("\n" + "="*50)
    print("Data Loading Summary:")
    print("="*50)
    print(f"Inserted {drivers_count} drivers")
    print(f"Inserted {riders_count} riders")
    print(f"Inserted {vehicles_count} vehicles")
    print(f"Inserted {trips_count} trips")
    print(f"Inserted {payments_count} payments")
    print("="*50)
    print("\nSuccessfully loaded all data into rideshare.db!")
    
    # Close connection
    conn.close()

if __name__ == "__main__":
    main()

