# Ride-Sharing Data Analytics Project

A complete data pipeline project for generating, storing, and analyzing synthetic ride-sharing data using Python, CSV files, and SQLite database.

## 📋 Project Overview

This project generates realistic synthetic ride-sharing datasets, loads them into a SQLite database, and provides SQL-based analytics reports. It includes:

- **Data Generation**: Creates 5 CSV datasets with realistic ride-sharing data
- **Database Loading**: Automatically loads CSVs into SQLite with proper schema and foreign keys
- **Analytics Reports**: Generates 3 business intelligence reports with CSV exports

## 📊 Data Overview

The project generates **5 datasets** with the following structure:

### 1. Drivers (`drivers.csv`)
- **100 drivers** with: ID, name, phone, rating (3.5-5.0), join date, city
- Primary key: `driver_id`

### 2. Riders (`riders.csv`)
- **500 riders** with: ID, name, email, signup date, city
- Primary key: `rider_id`

### 3. Vehicles (`vehicles.csv`)
- **120 vehicles** with: ID, driver ID, make, model, year, plate number
- Primary key: `vehicle_id`
- Foreign key: `driver_id` → `drivers.driver_id`

### 4. Trips (`trips.csv`)
- **2000 trips** with: ID, rider ID, driver ID, vehicle ID, start/end times, locations, distance (km), fare
- Primary key: `trip_id`
- Foreign keys: `rider_id` → `riders.rider_id`, `driver_id` → `drivers.driver_id`, `vehicle_id` → `vehicles.vehicle_id`
- Realistic trip durations: 5-60 minutes
- Distances: 2-50 km with fare calculations

### 5. Payments (`payments.csv`)
- **2000 payments** with: ID, trip ID, amount, method (card/wallet/cash), status (completed/failed), payment time
- Primary key: `payment_id`
- Foreign key: `trip_id` → `trips.trip_id`
- 95% completion rate

## 📁 Project Structure

```
Deligent-Cursor/
│
├── data/                          # CSV data files
│   ├── drivers.csv               # 100 drivers
│   ├── riders.csv                # 500 riders
│   ├── vehicles.csv              # 120 vehicles
│   ├── trips.csv                 # 2000 trips
│   ├── payments.csv              # 2000 payments
│   └── reports/                  # Generated report CSVs
│       ├── top_riders_by_spending.csv
│       ├── driver_performance_summary.csv
│       └── frequent_routes.csv
│
├── scripts/                       # Python scripts
│   ├── load_to_sqlite.py        # Loads CSVs into SQLite database
│   ├── run_query.py              # Executes reports and saves as CSV
│   └── view_tables.py            # Interactive table viewer
│
├── sql/                           # SQL files
│   ├── schema.sql                # Database schema (CREATE TABLE statements)
│   └── report.sql                # 3 SQL report queries
│
├── generate_data.py              # Main data generation script
├── rideshare.db                  # SQLite database (created after loading)
└── README.md                     # This file
```

## 🔧 Files Description

### Data Generation
- **`generate_data.py`**: Generates all 5 CSV datasets with realistic synthetic data. Can be run multiple times to regenerate data with different random values.

### Database Scripts
- **`scripts/load_to_sqlite.py`**: 
  - Creates SQLite database `rideshare.db`
  - Creates tables with proper schema and foreign key constraints
  - Loads all CSV files from `/data` directory
  - Prints summary of loaded records

- **`sql/schema.sql`**: Contains all CREATE TABLE statements with:
  - Appropriate data types (INTEGER, TEXT, REAL, DATETIME)
  - Primary keys
  - Foreign key constraints

### Reporting Scripts
- **`sql/report.sql`**: Contains 3 SQL queries:
  1. **Top Riders by Spending**: Top 20 riders ranked by total spending
  2. **Driver Performance Summary**: All drivers with trip counts, ratings, and earnings
  3. **Frequent Routes**: Top 10 most traveled routes with trip counts and average fares

- **`scripts/run_query.py`**: 
  - Connects to `rideshare.db`
  - Executes all 3 reports from `report.sql`
  - Displays results as formatted tables in terminal
  - Saves each report as CSV in `/data/reports/`

- **`scripts/view_tables.py`**: 
  - Interactive menu to browse database tables
  - View any table with custom row limits
  - View all 3 reports
  - User-friendly table display

## 🚀 Getting Started

### Step 1: Generate Data
```bash
python generate_data.py
```
This creates all 5 CSV files in the `/data` directory.

### Step 2: Load Data into Database
```bash
python scripts/load_to_sqlite.py
```
This creates `rideshare.db` and loads all CSV data with proper relationships.

### Step 3: Generate Reports
```bash
python scripts/run_query.py
```
This executes all 3 reports, displays them in terminal, and saves CSV files.

## 👀 How to View Tables

### Method 1: Run Reports (Recommended)
```bash
python scripts/run_query.py
```
- Displays all 3 reports as formatted tables in terminal
- Automatically saves CSV files to `/data/reports/`

### Method 2: Interactive Table Viewer
```bash
python scripts/view_tables.py
```
- Opens interactive menu
- Browse any table (drivers, riders, vehicles, trips, payments)
- View reports
- Custom row limits

**Menu Options:**
- `1-5`: View raw data tables (first 20 rows)
- `6`: Top riders by spending report
- `7`: Driver performance summary report
- `8`: Frequent routes report
- `9`: View any table with custom row limit
- `0`: Exit

### Method 3: Open CSV Files
Open the report CSV files directly in Excel, Google Sheets, or any spreadsheet application:
- `data/reports/top_riders_by_spending.csv`
- `data/reports/driver_performance_summary.csv`
- `data/reports/frequent_routes.csv`

### Method 4: SQLite Command Line
```bash
sqlite3 rideshare.db
```
Then run SQL queries:
```sql
.headers on
.mode column
SELECT * FROM drivers LIMIT 10;
SELECT * FROM trips LIMIT 10;
```

### Method 5: SQLite Browser (GUI)
1. Download [DB Browser for SQLite](https://sqlitebrowser.org/) (free)
2. Open `rideshare.db`
3. Browse tables visually and run custom queries

## 📈 Reports Generated

### Report 1: Top Riders by Spending
Shows the top 20 riders ranked by total spending:
- Rider ID and name
- Total number of trips
- Total amount spent

### Report 2: Driver Performance Summary
Shows all drivers with performance metrics:
- Driver ID and name
- Total trips completed
- Average rating
- Total earnings

### Report 3: Frequent Routes
Shows the top 10 most traveled routes:
- Start and end locations
- Number of trips on that route
- Average fare for the route

## 🔗 Database Relationships

```
drivers (1) ──→ (many) vehicles
drivers (1) ──→ (many) trips
riders (1) ──→ (many) trips
vehicles (1) ──→ (many) trips
trips (1) ──→ (1) payments
```

## 📝 Requirements

- Python 3.7+
- SQLite3 (included with Python)
- No external dependencies required (uses only Python standard library)

## 🎯 Key Features

✅ Realistic synthetic data generation  
✅ Proper foreign key relationships  
✅ Automatic database schema creation  
✅ SQL-based analytics reports  
✅ CSV export functionality  
✅ Interactive data browsing  
✅ Transaction-safe data loading  

## 📞 Usage Examples

**Regenerate all data:**
```bash
python generate_data.py
python scripts/load_to_sqlite.py
```

**View specific table:**
```bash
python scripts/view_tables.py
# Select option 1-5 or 9
```

**Quick report generation:**
```bash
python scripts/run_query.py
```

---

**Note**: The database file `rideshare.db` is created automatically when you run `scripts/load_to_sqlite.py`. You can delete it and regenerate it anytime by running the load script again.

