-- Creating the Departments table
CREATE TABLE Departments (
    department_id INT PRIMARY KEY,
    department_name VARCHAR(50),
    head_doctor_id INT 
);

-- Creating the Doctors table
CREATE TABLE Doctors (
    doctor_id INT PRIMARY KEY,
    name VARCHAR(100),
    specialization VARCHAR(50),
    department_id INT,
    CONSTRAINT fk_doctors_department FOREIGN KEY (department_id)
        REFERENCES Departments(department_id)
);

-- Creating the Patients table
CREATE TABLE Patients (
    patient_id INT PRIMARY KEY,
    name VARCHAR(100),
    date_of_birth DATE,
    gender CHAR(1),
    phone VARCHAR(15)
);

-- Creating the Appointments table
CREATE TABLE Appointments (
    appointment_id INT PRIMARY KEY,
    patient_id INT,
    doctor_id INT,
    appointment_datetime TIMESTAMP,
    status VARCHAR(20),
    CONSTRAINT fk_appointments_patient FOREIGN KEY (patient_id)
        REFERENCES Patients(patient_id),
    CONSTRAINT fk_appointments_doctor FOREIGN KEY (doctor_id)
        REFERENCES Doctors(doctor_id)
);

-- Creating the Prescriptions table
CREATE TABLE Prescriptions (
    prescription_id INT PRIMARY KEY,
    appointment_id INT,
    medication VARCHAR(100),
    dosage VARCHAR(50),
    CONSTRAINT fk_prescriptions_appointment FOREIGN KEY (appointment_id)
        REFERENCES Appointments(appointment_id)
);

-- Creating the MedicalRecords table
CREATE TABLE MedicalRecords (
    record_id INT PRIMARY KEY,
    patient_id INT,
    doctor_id INT,
    diagnosis VARCHAR(200),
    notes VARCHAR(1000),
    CONSTRAINT fk_medicalrecords_patient FOREIGN KEY (patient_id)
        REFERENCES Patients(patient_id),
    CONSTRAINT fk_medicalrecords_doctor FOREIGN KEY (doctor_id)
        REFERENCES Doctors(doctor_id)
);

-- Insert sample data into Departments
INSERT INTO Departments (department_id, department_name, head_doctor_id)
VALUES 
    (101, 'Cardiology', 201),
    (102, 'Neurology', 202);

-- Insert sample data into Doctors
INSERT INTO Doctors (doctor_id, name, specialization, department_id)
VALUES 
    (201, 'Dr. Alice Smith', 'Cardiologist', 101),
    (202, 'Dr. Bob Johnson', 'Neurologist', 102),
    (203, 'Dr. Eva Lee', 'Cardiologist', 101);

-- Insert sample data into Patients
INSERT INTO Patients (patient_id, name, date_of_birth, gender, phone)
VALUES 
    (1, 'Alice Brown', '1985-03-15', 'F', '555-1234'),
    (2, 'Bob Green', '1990-07-22', 'M', '555-5678'),
    (3, 'Charlie White', '1978-11-05', 'M', '555-8765');

-- Insert sample data into Appointments
INSERT INTO Appointments (appointment_id, patient_id, doctor_id, appointment_datetime, status)
VALUES 
    (301, 1, 201, '2023-10-01 09:00:00', 'Completed'),
    (302, 2, 202, '2023-10-02 10:30:00', 'Scheduled'),
    (303, 3, 203, '2023-10-03 14:00:00', 'Completed'),
    (304, 3, 203, '2023-10-03 15:00:00', 'Cancelled');

-- Insert sample data into Prescriptions
INSERT INTO Prescriptions (prescription_id, appointment_id, medication, dosage)
VALUES 
    (401, 301, 'Amlodipine', '10mg/day'),
    (402, 302, 'Ibuprofen', '400mg'),
    (403, 303, 'Aspirin', '81mg/day');

-- Insert sample data into MedicalRecords
INSERT INTO MedicalRecords (record_id, patient_id, doctor_id, diagnosis, notes)
VALUES 
    (501, 1, 201, 'Hypertension', 'Monitor BP weekly'),
    (502, 2, 202, 'Migraine', 'Prescribed rest and fluids'),
    (503, 3, 203, 'Migraine', 'Advised to avoid triggers'),
    (504, 3, 203, 'Hypertension', 'Start low-sodium diet');

-- Question 1: List all patients who have appointments in the "Cardiology" department.
SELECT DISTINCT p.*
FROM Patients p
JOIN Appointments a ON p.patient_id = a.patient_id
JOIN Doctors d ON a.doctor_id = d.doctor_id
JOIN Departments dep ON d.department_id = dep.department_id
WHERE dep.department_name = 'Cardiology';

-- Question 2: Count the number of appointments per month in 2023.
SELECT DATE_TRUNC('month', appointment_datetime) AS month,
       COUNT(*) AS appointment_count
FROM Appointments
WHERE EXTRACT(YEAR FROM appointment_datetime) = 2023
GROUP BY month
ORDER BY month;

-- Question 3: Find doctors who have not had any appointments in the last 30 days.
SELECT d.*
FROM Doctors d
WHERE NOT EXISTS (
    SELECT 1
    FROM Appointments a
    WHERE a.doctor_id = d.doctor_id
      AND a.appointment_datetime >= (CURRENT_DATE - INTERVAL '30 days')
);

-- Question 4: Identify patients with more than one appointment on the same day.
SELECT patient_id,
       DATE(appointment_datetime) AS appt_date,
       COUNT(*) AS num_appointments
FROM Appointments
GROUP BY patient_id, DATE(appointment_datetime)
HAVING COUNT(*) > 1;

-- Question 5: Find the most frequently prescribed medication.
SELECT medication, COUNT(*) AS frequency
FROM Prescriptions
GROUP BY medication
ORDER BY frequency DESC
LIMIT 1;
