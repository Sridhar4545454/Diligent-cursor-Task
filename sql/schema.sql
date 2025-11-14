-- SQLite schema for rideshare database

-- Drivers table
CREATE TABLE IF NOT EXISTS drivers (
    driver_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT,
    rating REAL,
    join_date TEXT,
    city TEXT
);

-- Riders table
CREATE TABLE IF NOT EXISTS riders (
    rider_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT,
    signup_date TEXT,
    city TEXT
);

-- Vehicles table
CREATE TABLE IF NOT EXISTS vehicles (
    vehicle_id INTEGER PRIMARY KEY,
    driver_id INTEGER NOT NULL,
    make TEXT,
    model TEXT,
    year INTEGER,
    plate_number TEXT,
    FOREIGN KEY (driver_id) REFERENCES drivers(driver_id)
);

-- Trips table
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
);

-- Payments table
CREATE TABLE IF NOT EXISTS payments (
    payment_id INTEGER PRIMARY KEY,
    trip_id INTEGER NOT NULL,
    amount REAL,
    method TEXT,
    status TEXT,
    payment_time TEXT,
    FOREIGN KEY (trip_id) REFERENCES trips(trip_id)
);

