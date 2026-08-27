DROP TABLE IF EXISTS participated;
DROP TABLE IF EXISTS owns;
DROP TABLE IF EXISTS accident;
DROP TABLE IF EXISTS car;
DROP TABLE IF EXISTS person;

CREATE TABLE person (
    driverid INT PRIMARY KEY,
    name VARCHAR(100),
    address VARCHAR(200)
);

CREATE TABLE car (
    license VARCHAR(10),
    plate VARCHAR(10) PRIMARY KEY,
    model VARCHAR(50),
    years INT
);

CREATE TABLE accident (
    report_number INT PRIMARY KEY,
    year INT,
    location VARCHAR(100)
);

CREATE TABLE owns (
    driverid INT,
    license_plate VARCHAR(10),
    PRIMARY KEY (driverid, license_plate),
    FOREIGN KEY (driverid) REFERENCES person(driverid),
    FOREIGN KEY (license_plate) REFERENCES car(plate)
);

CREATE TABLE participated (
    report_number INT,
    license_plate VARCHAR(10),
    driverid INT,
    damage VARCHAR(100),
    amount NUMERIC(10,2),
    PRIMARY KEY (report_number, license_plate, driverid),
    FOREIGN KEY (report_number) REFERENCES accident(report_number),
    FOREIGN KEY (license_plate) REFERENCES car(plate),
    FOREIGN KEY (driverid) REFERENCES person(driverid)
);


-- Inserting data into the person table.
INSERT INTO person (driverid, name, address) VALUES
    (1, 'John Doe', '123 Main St, New York, NY'),
    (2, 'Jane Smith', '456 Maple Ave, Los Angeles, CA'),
    (3, 'Jim Brown', '789 Oak St, Chicago, IL'),
    (4, 'Alice Johnson', '101 Pine Rd, New York, NY'),
    (5, 'Bob Williams', '202 Elm St, San Francisco, CA'),
    (6, 'Chris Evans', '303 Spruce St, New York, NY'),
    (7, 'Emma Stone', '404 Birch Ave, Sacramento, CA'),
    (8, 'Olivia Brown', '505 Cedar St, Boston, MA'),
    (9, 'Liam Miller', '606 Pine St, Houston, TX'),
    (10, 'Noah Davis', '707 Oak Ave, San Diego, CA'),
    (11, 'Sophia Wilson', '808 Maple Blvd, New York, NY'),
    (12, 'Mason Taylor', '909 Walnut St, Los Angeles, CA'),
    (13, 'Isabella Anderson', '1010 Redwood Dr, New York, NY'),
    (14, 'Ethan Thomas', '1111 Cedar Ave, Chicago, IL'),
    (15, 'Ava Martinez', '1212 Oak St, Los Angeles, CA');

-- Inserting data into the car table.
INSERT INTO car (license, plate, model, years) VALUES
    ('NY', 'NY1001', 'Model X', 10),    
    ('CA', 'CA1002', 'Model Y', 8),       
    ('TX', 'TX1003', 'Model Z', 20),      
    ('NY', 'NY1004', 'Model X', 12),      
    ('CA', 'CA1005', 'Model Y', 14),     
    ('FL', 'FL1006', 'Model A', 3),       
    ('NY', 'NY1007', 'Model B', 16),      
    ('CA', 'CA1008', 'Model C', 5),       
    ('NV', 'NV1009', 'Model D', 10),     
    ('CA', 'CA1010', 'Model X', 9); 

-- Inserting data into the accident table.
INSERT INTO accident (report_number, year, location) VALUES
    (2001, 2021, 'Downtown'),
    (2002, 2022, 'Uptown'),
    (2003, 2023, 'Suburb'),
    (2004, 2020, 'Midtown'),
    (2005, 2023, 'Airport');

-- Inserting data into the owns table.
INSERT INTO owns (driverid, license_plate) VALUES
    (1, 'NY1001'),
    (1, 'NY1004'),
    (2, 'CA1002'),
    (3, 'TX1003'),
    (4, 'CA1005'),
    (6, 'FL1006'),
    (7, 'NY1007'),
    (9, 'CA1008'),
    (11, 'CA1010');

-- Inserting data into the participated table.
INSERT INTO participated (report_number, license_plate, driverid, damage, amount) VALUES
    (2001, 'NY1001', 1, 'Front damage', 500.00),
    (2002, 'CA1002', 2, 'Rear damage', 300.00),
    (2003, 'NY1004', 1, 'Side damage', 200.00),
    (2003, 'TX1003', 3, 'Windshield damage', 400.00),
    (2002, 'CA1005', 4, 'Bumper damage', 150.00),
    (2005, 'CA1010', 11, 'Scratch', 50.00),
    (2001, 'FL1006', 6, 'Minor dent', 100.00),
    (2004, 'NY1007', 7, 'Major damage', 600.00),
    (2003, 'CA1002', 2, 'Side mirror damage', 250.00);


-- 2: Find the model number and total number of cars where the year of car is less than 15
-- years and the maker of the license plate belongs to New York or California.
SELECT model, COUNT(*) AS total_cars
FROM car
WHERE years < 15
  AND license IN ('NY', 'CA')
GROUP BY model;
	

-- 3: Find the names of all drivers who own a car that was involved in an accident.
SELECT DISTINCT p.name
FROM person p
JOIN owns o ON p.driverid = o.driverid
JOIN participated pt ON o.license_plate = pt.license_plate;

-- 4: find the number of accidents each driver has been involved in and 
-- the total damage amount they have paid for accidents that occurred in the last 3 years.
SELECT p.driverid, p.name,
       COUNT(DISTINCT a.report_number) AS accident_count,
       SUM(pt.amount) AS total_damage
FROM person p
JOIN participated pt ON p.driverid = pt.driverid
JOIN accident a ON pt.report_number = a.report_number
WHERE a.year >= 2021
GROUP BY p.driverid, p.name;

-- 5: Find all drivers who do not own any cars.
SELECT p.name
FROM person p
WHERE NOT EXISTS (
    SELECT 1
    FROM owns o
    WHERE o.driverid = p.driverid
);