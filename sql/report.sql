-- Report 1: Top riders by spending
-- Columns: rider_id, rider_name, total_trips, total_spent
-- Order by total_spent DESC, limit top 20

SELECT 
    r.rider_id,
    r.name AS rider_name,
    COUNT(t.trip_id) AS total_trips,
    ROUND(SUM(p.amount), 2) AS total_spent
FROM 
    riders r
    INNER JOIN trips t ON r.rider_id = t.rider_id
    INNER JOIN payments p ON t.trip_id = p.trip_id
WHERE 
    p.status = 'completed'
GROUP BY 
    r.rider_id, r.name
ORDER BY 
    total_spent DESC
LIMIT 20;

-- Report 2: Driver performance summary
-- Columns: driver_id, driver_name, total_trips, avg_rating, total_earnings
-- Order by total_earnings DESC

SELECT 
    d.driver_id,
    d.name AS driver_name,
    COUNT(t.trip_id) AS total_trips,
    ROUND(AVG(d.rating), 2) AS avg_rating,
    ROUND(SUM(p.amount), 2) AS total_earnings
FROM 
    drivers d
    INNER JOIN trips t ON d.driver_id = t.driver_id
    INNER JOIN payments p ON t.trip_id = p.trip_id
WHERE 
    p.status = 'completed'
GROUP BY 
    d.driver_id, d.name
ORDER BY 
    total_earnings DESC;

-- Report 3: Frequent route sample
-- Columns: start_location, end_location, num_trips, avg_fare
-- Group by route (start_location, end_location) and show top 10 routes

SELECT 
    start_location,
    end_location,
    COUNT(trip_id) AS num_trips,
    ROUND(AVG(fare), 2) AS avg_fare
FROM 
    trips
GROUP BY 
    start_location, end_location
ORDER BY 
    num_trips DESC
LIMIT 10;

