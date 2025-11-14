"""
Execute SQL reports and save results as CSV files.
"""
import sqlite3
import csv
from pathlib import Path

# Create reports directory
Path("data/reports").mkdir(parents=True, exist_ok=True)

def execute_query(cursor, query, description):
    """Execute a query and return results."""
    cursor.execute(query)
    columns = [description[0] for description in cursor.description]
    rows = cursor.fetchall()
    return columns, rows

def print_table(columns, rows, title):
    """Print query results as a formatted table."""
    print(f"\n{'='*80}")
    print(f"{title}")
    print('='*80)
    
    # Print header
    header = " | ".join(f"{col:>15}" for col in columns)
    print(header)
    print("-" * len(header))
    
    # Print rows
    for row in rows:
        row_str = " | ".join(f"{str(val):>15}" for val in row)
        print(row_str)
    
    print(f"\nTotal rows: {len(rows)}")
    print('='*80)

def save_to_csv(columns, rows, filename):
    """Save query results to CSV file."""
    filepath = Path("data/reports") / filename
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        writer.writerows(rows)
    
    print(f"Saved to: {filepath}")

def main():
    """Main function to execute all reports."""
    # Connect to database
    conn = sqlite3.connect("rideshare.db")
    cursor = conn.cursor()
    
    # Read SQL file
    sql_file = Path("sql/report.sql")
    if not sql_file.exists():
        print(f"Error: {sql_file} not found!")
        return
    
    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    # Split SQL into individual queries (separated by semicolons)
    # Remove comments and empty lines
    queries = []
    current_query = []
    
    for line in sql_content.split('\n'):
        line = line.strip()
        # Skip empty lines and comment-only lines
        if not line or line.startswith('--'):
            continue
        current_query.append(line)
        if line.endswith(';'):
            query = ' '.join(current_query)
            queries.append(query)
            current_query = []
    
    # Execute each query
    report_names = [
        "Top Riders by Spending",
        "Driver Performance Summary",
        "Frequent Route Sample"
    ]
    
    report_files = [
        "top_riders_by_spending.csv",
        "driver_performance_summary.csv",
        "frequent_routes.csv"
    ]
    
    for i, query in enumerate(queries):
        if i < len(report_names):
            print(f"\n{'#'*80}")
            print(f"Executing Report {i+1}: {report_names[i]}")
            print('#'*80)
            
            columns, rows = execute_query(cursor, query, report_names[i])
            print_table(columns, rows, report_names[i])
            save_to_csv(columns, rows, report_files[i])
    
    print(f"\n{'#'*80}")
    print("All reports generated successfully!")
    print('#'*80)
    
    # Close connection
    conn.close()

if __name__ == "__main__":
    main()

