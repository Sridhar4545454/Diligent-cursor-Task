"""
Generate synthetic ride-sharing datasets and save them as CSV files.
"""
import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

# Create data directory if it doesn't exist
Path("data").mkdir(exist_ok=True)

# Set random seed for reproducibility (optional)
random.seed(42)

# Sample data for generation
CITIES = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"]
FIRST_NAMES = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", "William", "Elizabeth", 
               "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica", "Thomas", "Sarah", "Christopher", "Karen"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
              "Hernandez", "Lopez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee"]
MAKES = ["Toyota", "Honda", "Ford", "Chevrolet", "Nissan", "BMW", "Mercedes-Benz", "Audi", "Hyundai", "Kia"]
MODELS = {
    "Toyota": ["Camry", "Corolla", "Prius", "RAV4", "Highlander"],
    "Honda": ["Civic", "Accord", "CR-V", "Pilot", "Odyssey"],
    "Ford": ["F-150", "Escape", "Explorer", "Focus", "Mustang"],
    "Chevrolet": ["Silverado", "Equinox", "Malibu", "Tahoe", "Cruze"],
    "Nissan": ["Altima", "Sentra", "Rogue", "Pathfinder", "Maxima"],
    "BMW": ["3 Series", "5 Series", "X3", "X5", "X1"],
    "Mercedes-Benz": ["C-Class", "E-Class", "GLC", "GLE", "A-Class"],
    "Audi": ["A4", "A6", "Q5", "Q7", "A3"],
    "Hyundai": ["Elantra", "Sonata", "Tucson", "Santa Fe", "Accent"],
    "Kia": ["Optima", "Sorento", "Sportage", "Forte", "Telluride"]
}
PAYMENT_METHODS = ["card", "wallet", "cash"]
PAYMENT_STATUSES = ["completed", "failed"]

LOCATIONS = [
    "Downtown", "Airport", "Train Station", "Shopping Mall", "University", 
    "Hospital", "Stadium", "Beach", "Park", "Business District",
    "Residential Area", "Restaurant District", "Hotel District", "Suburb", "City Center"
]

def generate_phone():
    """Generate a random phone number."""
    return f"{random.randint(200, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"

def generate_email(name):
    """Generate an email from name."""
    name_parts = name.lower().replace(" ", ".")
    domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "icloud.com"]
    return f"{name_parts}@{random.choice(domains)}"

def generate_plate_number():
    """Generate a random license plate number."""
    letters = ''.join(random.choices('ABCDEFGHJKLMNPRSTUVWXYZ', k=3))
    numbers = ''.join(random.choices('0123456789', k=4))
    return f"{letters}-{numbers}"

def generate_date(start_date, end_date):
    """Generate a random date between start_date and end_date."""
    time_between = end_date - start_date
    days_between = time_between.days
    random_days = random.randrange(days_between)
    return start_date + timedelta(days=random_days)

def generate_datetime(start_date, end_date):
    """Generate a random datetime between start_date and end_date."""
    time_between = end_date - start_date
    seconds_between = time_between.total_seconds()
    random_seconds = random.randrange(int(seconds_between))
    return start_date + timedelta(seconds=random_seconds)

def generate_drivers(num_drivers=100):
    """Generate drivers.csv"""
    drivers = []
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2024, 12, 31)
    
    for i in range(1, num_drivers + 1):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        name = f"{first_name} {last_name}"
        phone = generate_phone()
        rating = round(random.uniform(3.5, 5.0), 2)
        join_date = generate_date(start_date, end_date).strftime("%Y-%m-%d")
        city = random.choice(CITIES)
        
        drivers.append({
            "driver_id": i,
            "name": name,
            "phone": phone,
            "rating": rating,
            "join_date": join_date,
            "city": city
        })
    
    return drivers

def generate_riders(num_riders=500):
    """Generate riders.csv"""
    riders = []
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2024, 12, 31)
    
    for i in range(1, num_riders + 1):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        name = f"{first_name} {last_name}"
        email = generate_email(name)
        signup_date = generate_date(start_date, end_date).strftime("%Y-%m-%d")
        city = random.choice(CITIES)
        
        riders.append({
            "rider_id": i,
            "name": name,
            "email": email,
            "signup_date": signup_date,
            "city": city
        })
    
    return riders

def generate_vehicles(num_vehicles=120, num_drivers=100):
    """Generate vehicles.csv"""
    vehicles = []
    # Some drivers have multiple vehicles, some have none
    driver_ids = list(range(1, num_drivers + 1))
    random.shuffle(driver_ids)
    
    for i in range(1, num_vehicles + 1):
        # Assign vehicle to a driver (some drivers may have multiple)
        driver_id = random.choice(driver_ids)
        make = random.choice(MAKES)
        model = random.choice(MODELS[make])
        year = random.randint(2015, 2024)
        plate_number = generate_plate_number()
        
        vehicles.append({
            "vehicle_id": i,
            "driver_id": driver_id,
            "make": make,
            "model": model,
            "year": year,
            "plate_number": plate_number
        })
    
    return vehicles

def generate_trips(num_trips=2000, num_riders=500, num_drivers=100, vehicles_data=None):
    """Generate trips.csv"""
    trips = []
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 12, 31)
    
    # Create a mapping of driver_id to vehicle_ids
    driver_vehicles = {}
    if vehicles_data:
        for vehicle in vehicles_data:
            driver_id = vehicle["driver_id"]
            vehicle_id = vehicle["vehicle_id"]
            if driver_id not in driver_vehicles:
                driver_vehicles[driver_id] = []
            driver_vehicles[driver_id].append(vehicle_id)
    
    # Generate trips
    for i in range(1, num_trips + 1):
        rider_id = random.randint(1, num_riders)
        driver_id = random.randint(1, num_drivers)
        # Assign a vehicle that belongs to this driver
        if driver_id in driver_vehicles and driver_vehicles[driver_id]:
            vehicle_id = random.choice(driver_vehicles[driver_id])
        else:
            # Fallback: assign any vehicle (shouldn't happen if vehicles are properly distributed)
            vehicle_id = random.randint(1, len(vehicles_data) if vehicles_data else 120)
        
        start_time = generate_datetime(start_date, end_date)
        # Trip duration: 5-60 minutes
        duration_minutes = random.randint(5, 60)
        end_time = start_time + timedelta(minutes=duration_minutes)
        
        start_location = random.choice(LOCATIONS)
        end_location = random.choice(LOCATIONS)
        # Ensure end_location is different from start_location
        while end_location == start_location:
            end_location = random.choice(LOCATIONS)
        
        # Distance: 2-50 km (realistic for ride-sharing)
        distance_km = round(random.uniform(2.0, 50.0), 2)
        # Fare: base $2.50 + $1.50/km + $0.25/minute (simplified pricing)
        base_fare = 2.50
        distance_fare = distance_km * 1.50
        time_fare = duration_minutes * 0.25
        fare = round(base_fare + distance_fare + time_fare, 2)
        
        trips.append({
            "trip_id": i,
            "rider_id": rider_id,
            "driver_id": driver_id,
            "vehicle_id": vehicle_id,
            "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
            "start_location": start_location,
            "end_location": end_location,
            "distance_km": distance_km,
            "fare": fare
        })
    
    return trips

def generate_payments(num_trips=2000):
    """Generate payments.csv"""
    payments = []
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 12, 31)
    
    # Generate one payment per trip
    for trip_id in range(1, num_trips + 1):
        # Get the trip to know the fare amount
        # For simplicity, we'll generate payments independently and match amounts
        # In a real scenario, we'd read trips.csv or pass trip data
        amount = round(random.uniform(5.0, 100.0), 2)  # Will be matched with trip fare later
        method = random.choice(PAYMENT_METHODS)
        # 95% success rate
        status = "completed" if random.random() < 0.95 else "failed"
        
        # Payment time is after trip end time (simplified)
        payment_time = generate_datetime(start_date, end_date).strftime("%Y-%m-%d %H:%M:%S")
        
        payments.append({
            "payment_id": trip_id,  # One payment per trip
            "trip_id": trip_id,
            "amount": amount,
            "method": method,
            "status": status,
            "payment_time": payment_time
        })
    
    return payments

def write_csv(filename, data, fieldnames):
    """Write data to CSV file."""
    filepath = Path("data") / filename
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print(f"Generated {filename} with {len(data)} rows")

def main():
    """Generate all datasets."""
    print("Generating synthetic ride-sharing datasets...")
    
    # Generate drivers
    drivers = generate_drivers(100)
    write_csv("drivers.csv", drivers, ["driver_id", "name", "phone", "rating", "join_date", "city"])
    
    # Generate riders
    riders = generate_riders(500)
    write_csv("riders.csv", riders, ["rider_id", "name", "email", "signup_date", "city"])
    
    # Generate vehicles
    vehicles = generate_vehicles(120, 100)
    write_csv("vehicles.csv", vehicles, ["vehicle_id", "driver_id", "make", "model", "year", "plate_number"])
    
    # Generate trips (pass vehicles data to ensure proper foreign keys)
    trips = generate_trips(2000, 500, 100, vehicles)
    write_csv("trips.csv", trips, ["trip_id", "rider_id", "driver_id", "vehicle_id", "start_time", "end_time", 
                                    "start_location", "end_location", "distance_km", "fare"])
    
    # Generate payments (need to match trip fares)
    # First, let's update payments to match trip fares
    payments = []
    for trip in trips:
        amount = trip["fare"]
        method = random.choice(PAYMENT_METHODS)
        status = "completed" if random.random() < 0.95 else "failed"
        # Payment time should be after trip end time
        trip_end = datetime.strptime(trip["end_time"], "%Y-%m-%d %H:%M:%S")
        payment_time = trip_end + timedelta(minutes=random.randint(0, 30))
        
        payments.append({
            "payment_id": trip["trip_id"],
            "trip_id": trip["trip_id"],
            "amount": amount,
            "method": method,
            "status": status,
            "payment_time": payment_time.strftime("%Y-%m-%d %H:%M:%S")
        })
    
    write_csv("payments.csv", payments, ["payment_id", "trip_id", "amount", "method", "status", "payment_time"])
    
    print("\nAll datasets generated successfully!")
    print(f"Generated files in ./data/ directory:")
    print("  - drivers.csv (100 rows)")
    print("  - riders.csv (500 rows)")
    print("  - vehicles.csv (120 rows)")
    print("  - trips.csv (2000 rows)")
    print("  - payments.csv (2000 rows)")

if __name__ == "__main__":
    main()

