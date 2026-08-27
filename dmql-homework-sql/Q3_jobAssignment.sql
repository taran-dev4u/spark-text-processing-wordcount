-- Create the Employee table
CREATE TABLE Employee (
    emp_id INT PRIMARY KEY,
    emp_name VARCHAR(100),
    age INT,
    salary REAL
);

-- Create the Project table
CREATE TABLE Project (
    project_id INT PRIMARY KEY,
    project_name VARCHAR(100),
    budget REAL,
    manager_id INT
);

-- Create the Assignment table with ON DELETE CASCADE for project_id
CREATE TABLE Assignment (
    emp_id INT,
    project_id INT,
    hours_worked INT,
    PRIMARY KEY (emp_id, project_id),
    FOREIGN KEY (emp_id) REFERENCES Employee(emp_id),
    FOREIGN KEY (project_id) REFERENCES Project(project_id) ON DELETE CASCADE
);


-- Employees
INSERT INTO Employee (emp_id, emp_name, age, salary) VALUES
    (101, 'Alice Johnson', 30, 60000),
    (102, 'David Brown', 40, 85000),
    (103, 'Carol White', 28, 55000);

-- Projects
INSERT INTO Project (project_id, project_name, budget, manager_id) VALUES
    (10, 'Web Development', 300000, 101),
    (20, 'AI Research', 500000, 102),
    (30, 'Mobile App', 200000, 103);

-- Assignments
INSERT INTO Assignment (emp_id, project_id, hours_worked) VALUES
    (101, 10, 120),
    (102, 20, 150),
    (103, 30, 100),
    (101, 20, 80);  


-- 1. Add a new employee, Bob Smith, with emp_id = 301, age = 35, 
-- and salary = 75,000
INSERT INTO Employee (emp_id, emp_name, age, salary)
VALUES (301, 'Bob Smith', 35, 75000);

-- 2.	Write an SQL statement to give every employee a 15 percent raise.
UPDATE Employee
SET salary = salary * 1.15;


-- 3. delete the “AI Research” project. 
--- explain what happens when this statement is executed.
DELETE FROM Project
WHERE project_name = 'AI Research';



