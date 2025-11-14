"""
Simple script to view tables from the rideshare database.
"""
import sqlite3
import sys
from pathlib import Path

def print_table(cursor, query, title):
    """Execute query and print results as formatted table."""
    try:
        cursor.execute(query)
        columns = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
        
        if not rows:
            print(f"\n{title}: No data found.")
            return
        
        print(f"\n{'='*80}")
        print(f"{title}")
        print('='*80)
        
        # Calculate column widths
        col_widths = []
        for i, col in enumerate(columns):
            max_width = len(str(col))
            for row in rows:
                max_width = max(max_width, len(str(row[i])))
            col_widths.append(min(max_width, 30))  # Cap at 30 chars
        
        # Print header
        header = " | ".join(f"{str(col):<{col_widths[i]}}" for i, col in enumerate(columns))
        print(header)
        print("-" * len(header))
        
        # Print rows
        for row in rows:
            row_str = " | ".join(f"{str(val):<{col_widths[i]}}" for i, val in enumerate(row))
            print(row_str)
        
        print(f"\nTotal rows: {len(rows)}")
        print('='*80)
        
    except sqlite3.Error as e:
        print(f"Error executing query: {e}")

def main():
    """Main function to view database tables."""
    db_path = Path("rideshare.db")
    
    if not db_path.exists():
        print("Error: rideshare.db not found!")
        print("Please run: python scripts/load_to_sqlite.py first")
        return
    
    conn = sqlite3.connect("rideshare.db")
    cursor = conn.cursor()
    
    print("\n" + "="*80)
    print("RIDESHARE DATABASE VIEWER")
    print("="*80)
    
    # Show available tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    
    print("\nAvailable tables:")
    for i, table in enumerate(tables, 1):
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"  {i}. {table} ({count} rows)")
    
    # Menu
    print("\n" + "-"*80)
    print("Options:")
    print("  1. View all drivers (first 20)")
    print("  2. View all riders (first 20)")
    print("  3. View all vehicles (first 20)")
    print("  4. View all trips (first 20)")
    print("  5. View all payments (first 20)")
    print("  6. View top riders by spending (Report 1)")
    print("  7. View driver performance summary (Report 2)")
    print("  8. View frequent routes (Report 3)")
    print("  9. View all data from a specific table")
    print("  0. Exit")
    print("-"*80)
    
    while True:
        try:
            choice = input("\nEnter your choice (0-9): ").strip()
            
            if choice == "0":
                print("Goodbye!")
                break
            elif choice == "1":
                print_table(cursor, "SELECT * FROM drivers LIMIT 20", "DRIVERS (First 20)")
            elif choice == "2":
                print_table(cursor, "SELECT * FROM riders LIMIT 20", "RIDERS (First 20)")
            elif choice == "3":
                print_table(cursor, "SELECT * FROM vehicles LIMIT 20", "VEHICLES (First 20)")
            elif choice == "4":
                print_table(cursor, "SELECT * FROM trips LIMIT 20", "TRIPS (First 20)")
            elif choice == "5":
                print_table(cursor, "SELECT * FROM payments LIMIT 20", "PAYMENTS (First 20)")
            elif choice == "6":
                query = """
                    SELECT r.rider_id, r.name AS rider_name, 
                           COUNT(t.trip_id) AS total_trips,
                           ROUND(SUM(p.amount), 2) AS total_spent
                    FROM riders r
                    INNER JOIN trips t ON r.rider_id = t.rider_id
                    INNER JOIN payments p ON t.trip_id = p.trip_id
                    WHERE p.status = 'completed'
                    GROUP BY r.rider_id, r.name
                    ORDER BY total_spent DESC
                    LIMIT 20
                """
                print_table(cursor, query, "TOP RIDERS BY SPENDING")
            elif choice == "7":
                query = """
                    SELECT d.driver_id, d.name AS driver_name,
                           COUNT(t.trip_id) AS total_trips,
                           ROUND(AVG(d.rating), 2) AS avg_rating,
                           ROUND(SUM(p.amount), 2) AS total_earnings
                    FROM drivers d
                    INNER JOIN trips t ON d.driver_id = t.driver_id
                    INNER JOIN payments p ON t.trip_id = p.trip_id
                    WHERE p.status = 'completed'
                    GROUP BY d.driver_id, d.name
                    ORDER BY total_earnings DESC
                """
                print_table(cursor, query, "DRIVER PERFORMANCE SUMMARY")
            elif choice == "8":
                query = """
                    SELECT start_location, end_location,
                           COUNT(trip_id) AS num_trips,
                           ROUND(AVG(fare), 2) AS avg_fare
                    FROM trips
                    GROUP BY start_location, end_location
                    ORDER BY num_trips DESC
                    LIMIT 10
                """
                print_table(cursor, query, "FREQUENT ROUTES")
            elif choice == "9":
                print("\nAvailable tables:", ", ".join(tables))
                table_name = input("Enter table name: ").strip()
                if table_name in tables:
                    limit = input("Enter number of rows to display (or press Enter for all): ").strip()
                    if limit:
                        query = f"SELECT * FROM {table_name} LIMIT {limit}"
                        print_table(cursor, query, f"{table_name.upper()} (First {limit} rows)")
                    else:
                        query = f"SELECT * FROM {table_name}"
                        print_table(cursor, query, f"{table_name.upper()} (All rows)")
                else:
                    print(f"Error: Table '{table_name}' not found!")
            else:
                print("Invalid choice! Please enter 0-9.")
                
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
    
    conn.close()

if __name__ == "__main__":
    main()

