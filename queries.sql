USE HospitalManagement;

/*============================== DELIVERABLE #2 =======================================*/
-- CREATE INDEXES
/* -- create index on Department table */
CREATE INDEX idx_department_branch ON Department(Branch_ID);
SHOW INDEX FROM department;

/* -- create index on Patient table */
CREATE INDEX idx_patient_branch ON Patient(Branch_ID);
CREATE INDEX idx_patient_name ON Patient(LastName);
SHOW INDEX FROM Patient;

/* -- create index on Doctor table */
CREATE INDEX idx_doctor_department ON Doctor(DepartmentID);
CREATE INDEX idx_doctor_branch ON Doctor(Branch_ID);
SHOW INDEX FROM Doctor;

/* -- create index on Nurse table */
CREATE INDEX idx_nurse_branch ON Nurse(Branch_ID);
SHOW INDEX FROM Nurse;

/* -- create index on Appointment table */
CREATE INDEX idx_appointment_patient ON Appointment(PatientID);
CREATE INDEX idx_appointment_doctor ON Appointment(DoctorID);
CREATE INDEX idx_appointment_date ON Appointment(AppointmentDate);
SHOW INDEX FROM Appointment;

/* -- create index on MedicalRecord table */
CREATE INDEX idx_medicalrecord_patient ON MedicalRecord(PatientID);
CREATE INDEX idx_medicalrecord_doctor ON MedicalRecord(DoctorID);
CREATE INDEX idx_medicalrecord_date ON MedicalRecord(DateOfEntry);
SHOW INDEX FROM MedicalRecord;

/* -- create index on Room table */
CREATE INDEX idx_room_branch ON Room(Branch_ID);
CREATE INDEX idx_room_availability ON Room(Availability);
SHOW INDEX FROM Room;

/* -- create index on HospitalStay table */
CREATE INDEX idx_hospitalstay_patient ON HospitalStay(PatientID);
CREATE INDEX idx_hospitalstay_room ON HospitalStay(RoomID);
CREATE INDEX idx_hospitalstay_admitdate ON HospitalStay(AdmitDate);
SHOW INDEX FROM HospitalStay;

/* -- create index on Billing table */
CREATE INDEX idx_billing_patient ON Billing(PatientID);
CREATE INDEX idx_billing_date ON Billing(PaymentDate);
SHOW INDEX FROM Billing;

/*---------------------------------------------------------------------------------*/

-- CREATE VIEWS
-- 1. View for Patient Details in Vetical branch
CREATE OR REPLACE VIEW View_PatientDetailsInVerticalBranch AS
SELECT 
    p.*, 
    hb.Branch_Name, 
    hb.Branch_Address
FROM 
    Patient p
JOIN 
    Hospital_Branch hb USING(Branch_ID)
WHERE 
    hb.Branch_Name = 'Vertical';

SELECT * FROM View_PatientDetailsInVerticalBranch;

-- 2. create a view that contains a list of departments with the most doctors
CREATE OR REPLACE VIEW View_DepartmentsWithMostDoctors AS
SELECT 
    D.DepartmentName, 
    COUNT(DR.DepartmentID) AS NumberOfDoctors
FROM 
    Doctor DR
INNER JOIN 
    Department D USING(DepartmentID)
GROUP BY 
    DR.DepartmentID
HAVING 
    COUNT(DR.DepartmentID) = (
        SELECT MAX(DoctorCount)
        FROM (
            SELECT 
                COUNT(DR1.DepartmentID) AS DoctorCount
            FROM 
                Doctor DR1
            GROUP BY 
                DR1.DepartmentID
        ) AS SubQuery
    );

SELECT * FROM View_DepartmentsWithMostDoctors;

-- 3. create a view for listing doctors specifically in the Dermatology department
CREATE OR REPLACE VIEW View_DoctorsInDermatology AS
SELECT 
    d.*
FROM 
    Doctor d
INNER JOIN 
    Department dept USING(DepartmentID)
WHERE 
    dept.DepartmentName = 'Dermatology';

SELECT * FROM View_DoctorsInDermatology;

-- 4. create a view that identifies the doctor with the most appointments
CREATE OR REPLACE VIEW View_DoctorWithMostAppointments AS
WITH CTE_DoctorAppointmentCount AS (
    SELECT 
        a.DoctorID, 
        COUNT(a.AppointmentID) AS AppointmentCount
    FROM 
        Appointment a
    GROUP BY 
        a.DoctorID
)
SELECT 
    d.DoctorID, 
    d.FirstName, 
    d.LastName, 
    d.Phone, 
    d.Email, 
    dac.AppointmentCount
FROM 
    Doctor d
INNER JOIN 
    CTE_DoctorAppointmentCount dac USING(DoctorID)
WHERE 
    dac.AppointmentCount = (
        SELECT 
            MAX(AppointmentCount) 
        FROM 
            CTE_DoctorAppointmentCount
    );

SELECT * FROM View_DoctorWithMostAppointments;

-- 5. create a view that identifies the busiest branch
CREATE OR REPLACE VIEW View_BusiestBranch AS
WITH CTE_BranchAppointmentCount AS (
    SELECT 
        a.Branch_ID, 
        COUNT(a.AppointmentID) AS AppointmentCount
    FROM 
        Appointment a
    GROUP BY 
        a.Branch_ID
)
SELECT 
    hb.Branch_ID, 
    hb.Branch_Name, 
    hb.Branch_Address, 
    bac.AppointmentCount
FROM 
    Hospital_Branch hb
INNER JOIN 
    CTE_BranchAppointmentCount bac USING(Branch_ID)
WHERE 
    bac.AppointmentCount = (
        SELECT 
            MAX(AppointmentCount) 
        FROM 
            CTE_BranchAppointmentCount
    );

SELECT * FROM View_BusiestBranch;

/*---------------------------------------------------------------------------------*/
-- create temporary tables
-- CASE 1: Using temporary table to find the patient with the highest total stay in the hospital
-- Step 1: Create a temporary table to calculate the total stay duration for each patient
CREATE TEMPORARY TABLE Temp_PatientStayDurations AS
SELECT 
    PatientID, 
    SUM(DATEDIFF(DischargeDate, AdmitDate)) AS TotalStayDays
FROM 
    HospitalStay
GROUP BY 
    PatientID;

-- Display the contents of the temporary table
SELECT * FROM Temp_PatientStayDurations;

-- Step 2: Find the Patient with the Highest Total Stay
SELECT PatientID, CONCAT(FirstName, ' ', LastName) AS PatientName,
        (SELECT TotalStayDays
        FROM Temp_PatientStayDurations
        WHERE Pt.PatientID = PatientID) AS TotalStayDays
FROM Patient Pt
ORDER BY TotalStayDays DESC
LIMIT 1;


DROP TEMPORARY TABLE IF EXISTS Temp_PatientStayDurations;

-- CASE 2: Using temporary table to classify customers by their total spending
-- Step 1: Calculate the Total Payment for Each Patient
CREATE TEMPORARY TABLE Temp_PatientTotalPayments AS
SELECT 
    PatientID, 
    SUM(TotalAmount) AS TotalPayment
FROM 
    Billing
GROUP BY 
    PatientID;

DROP TEMPORARY TABLE IF EXISTS Temp_PatientTotalPayments;
-- Display the contents of the temporary table to verify the total payments
SELECT * FROM Temp_PatientTotalPayments;

-- Step 2: Classify Customers into Tiers Based on Their Total Spending
CREATE TABLE CustomerTier AS
SELECT 
    ptp.PatientID, 
    p.FirstName, 
    p.LastName, 
    ptp.TotalPayment,
    CASE
        WHEN ptp.TotalPayment >= 4000 THEN 'Platinum'
        WHEN ptp.TotalPayment >= 2000 AND ptp.TotalPayment < 4000 THEN 'Gold'
        WHEN ptp.TotalPayment >= 500 AND ptp.TotalPayment < 2000 THEN 'Silver'
        ELSE 'Bronze'
    END AS CustomerTier
FROM 
    Temp_PatientTotalPayments ptp
JOIN 
    Patient p ON ptp.PatientID = p.PatientID;

-- Display the contents of the new table to verify the customer tiers
SELECT * FROM CustomerTier;


/*---------------------------------------------------------------------------------*/
-- CREATE TRIGGER

-- CASE 1: create a trigger that prevents users from inserting an appointment 
-- into the Appointment table if the appointment date is more than 6 months in the future
DROP TRIGGER IF EXISTS PreventFutureAppointmentInsert;
DELIMITER $$

CREATE TRIGGER PreventFutureAppointmentInsert
BEFORE INSERT ON Appointment
FOR EACH ROW
BEGIN
    DECLARE six_months_ahead DATETIME;
    
    -- Calculate the date 6 months ahead from today
    SET six_months_ahead = DATE_ADD(NOW(), INTERVAL 6 MONTH);
    
    -- Check if the new appointment date is more than 6 months in the future
    IF NEW.AppointmentDate > six_months_ahead THEN
        SIGNAL SQLSTATE '12345'
        SET MESSAGE_TEXT = 'Cannot insert appointment with a date more than 6 months in the future';
    END IF;
END$$

DELIMITER ;

-- Example of trigger in action
INSERT INTO Appointment (PatientID, DoctorID, AppointmentDate, AppointmentTime, ReasonForVisit, Branch_ID)
VALUES (1, 2, '2025-06-06', '09:00:00', 'Routine check-up', 1);

-- CASE 2:create a trigger that prevents users from inserting a new doctor into the Obstetrics & Gynaecology department 
DROP TRIGGER IF EXISTS PreventDoctorInsertForObstetricsAndGynaecology;
DELIMITER $$

CREATE TRIGGER PreventDoctorInsertForObstetricsAndGynaecology
BEFORE INSERT ON Doctor
FOR EACH ROW
BEGIN
    DECLARE obstetrics_dept_id TINYINT;
    
    -- Retrieve the DepartmentID for 'Obstetrics & Gynaecology'
    SELECT DepartmentID INTO obstetrics_dept_id
    FROM Department
    WHERE DepartmentName = 'Obstetrics & Gynaecology';
    
    -- Check if the new doctor is being inserted into the 'Obstetrics & Gynaecology' department
    IF NEW.DepartmentID = obstetrics_dept_id THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cannot add more doctors to Obstetrics & Gynaecology; department is full.';
    END IF;
END$$

DELIMITER ;

-- Example of trigger in action
INSERT INTO Doctor (FirstName, LastName, Phone, Email, DepartmentID, Branch_ID)
VALUES ('Jane', 'Doe', '123-456-7890', 'jane.doe@example.com', 7, 1);

-- CASE 3: create a trigger that ensures no more than 9 nurses can be added to each branch
DROP TRIGGER IF EXISTS Trg_CheckNurseLimitInBranch;
DELIMITER $$

CREATE TRIGGER Trg_CheckNurseLimitInBranch
BEFORE INSERT ON Nurse
FOR EACH ROW
BEGIN
    DECLARE var_NurseCountInBranch TINYINT;
    
    -- Retrieve the count of nurses currently in the branch
    SELECT COUNT(NurseID) INTO var_NurseCountInBranch
    FROM Nurse
    WHERE Branch_ID = NEW.Branch_ID;
    
    -- Check if the count exceeds or equals 9
    IF var_NurseCountInBranch >= 9 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cannot add more nurses to this branch because it already has the maximum allowed.';
    END IF;
END$$

DELIMITER ;

-- Example
INSERT INTO Nurse (FirstName, LastName, Phone, Email, Branch_ID)
VALUES ('Jane', 'Doe', '123-456-7890', 'jane.doe@example.com', 1);

-- CASE 4: create trigger to prevent the deletion of a doctor with the email admin@hospital.com.
DROP TRIGGER IF EXISTS trigger_delete_doctor;

DELIMITER $$

CREATE TRIGGER trigger_delete_doctor
BEFORE DELETE ON Doctor
FOR EACH ROW
BEGIN
    DECLARE v_Email VARCHAR(100);
    
    -- Set the specific email that is protected from deletion
    SET v_Email = 'admin@hospital.com';
    
    -- Check if the email of the doctor being deleted matches the protected email
    IF OLD.Email = v_Email THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'This is an Admin Doctor. You cannot delete this doctor!';
    END IF;
END$$

DELIMITER ;

-- Example
DELETE FROM Doctor WHERE Email = 'admin@hospital.com';

-- CASE 5: create a trigger that prevents users from deleting any medical record that was created less than 3 months ago
DROP TRIGGER IF EXISTS PreventRecentMedicalRecordDeletion;
DELIMITER $$

CREATE TRIGGER PreventRecentMedicalRecordDeletion
BEFORE DELETE ON MedicalRecord
FOR EACH ROW
BEGIN
    DECLARE three_months_ago DATE;
    
    -- Calculate the date 3 months before today
    SET three_months_ago = DATE_SUB(CURDATE(), INTERVAL 3 MONTH);
    
    -- Check if the medical record's CreateDate is less than 3 months ago
    IF OLD.CreateDate > three_months_ago THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cannot delete medical records that were created less than 3 months ago';
    END IF;
END$$

DELIMITER ;

-- Example
DELETE FROM MedicalRecord WHERE RecordID = 10;

-- CASE 6: create a trigger that restricts users to creating a maximum of 3 appointments per day
DROP TRIGGER IF EXISTS LimitDailyAppointments;
DELIMITER $$

CREATE TRIGGER LimitDailyAppointments
BEFORE INSERT ON Appointment
FOR EACH ROW
BEGIN
    DECLARE appointment_count INT;
    
    -- Count the number of appointments for the same day
    SELECT COUNT(*) INTO appointment_count
    FROM Appointment
    WHERE AppointmentDate = NEW.AppointmentDate AND PatientID = NEW.PatientID;
    
    -- Check if the number of appointments is already 3
    IF appointment_count >= 3 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'You cannot create more than 3 appointments per day';
    END IF;
END$$

DELIMITER ;

-- Example
INSERT INTO Appointment (PatientID, DoctorID, AppointmentDate, AppointmentTime, ReasonForVisit, Branch_ID)
VALUES (5, 2, '2024-10-06', '09:00:00', 'Routine check-up', 1);

-- CASE 7: create triggers to ensure that Doctor names are in upper-case letters
DROP TRIGGER IF EXISTS UpperCaseDoctorNameInsert;
DROP TRIGGER IF EXISTS UpperCaseDoctorNameUpdate;

-- before inserting
DELIMITER $$

CREATE TRIGGER UpperCaseDoctorNameInsert
BEFORE INSERT ON Doctor
FOR EACH ROW
BEGIN
    -- Convert FirstName and LastName to upper case before inserting
    SET NEW.FirstName = UPPER(NEW.FirstName),
    NEW.LastName = UPPER(NEW.LastName);
END$$

DELIMITER ;


-- before updating 
DELIMITER $$

CREATE TRIGGER UpperCaseDoctorNameUpdate
BEFORE UPDATE ON Doctor
FOR EACH ROW
BEGIN
    -- Convert FirstName and LastName to upper case before updating
    SET NEW.FirstName = UPPER(NEW.FirstName),
    NEW.LastName = UPPER(NEW.LastName);
END$$

DELIMITER ;

-- example: insert
INSERT INTO Doctor (FirstName, LastName, Phone, Email, DepartmentID, Branch_ID)
VALUES ('john', 'doe', '123-456-7890', 'john.doe@example.com', 1, 1);

-- example: update
UPDATE Doctor
SET FirstName = 'max', LastName = 'Padson'
WHERE DoctorID = 14;

SELECT * FROM doctor;

-- CASE 8:create a trigger to track name changes in the Patient table
-- Step 1: Create the Audit Table
DROP TABLE IF EXISTS PatientNameChanges;
CREATE TABLE PatientNameChanges (
    patient_id INT UNSIGNED,
    old_name VARCHAR(200),
    new_name VARCHAR(200),
    change_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES Patient(PatientID) ON DELETE CASCADE
);

-- Step 2: Create the Trigger
DROP TRIGGER IF EXISTS name_change_trigger;
DELIMITER $$

CREATE TRIGGER name_change_trigger
AFTER UPDATE ON Patient
FOR EACH ROW
BEGIN
    -- Check if the FirstName or LastName is being changed
    IF (OLD.FirstName <> NEW.FirstName) OR (OLD.LastName <> NEW.LastName) THEN
        -- Insert the old and new names into the audit table
        INSERT INTO PatientNameChanges (patient_id, old_name, new_name)
        VALUES (
            NEW.PatientID, 
            CONCAT(OLD.FirstName, ' ', OLD.LastName), 
            CONCAT(NEW.FirstName, ' ', NEW.LastName)
        );
    END IF;
END$$

DELIMITER ;

-- Example
UPDATE Patient
SET FirstName = 'Dana', LastName = 'Wu'
WHERE PatientID = 27;

SELECT * FROM PatientNameChanges;



/*---------------------------------------------------------------------------------*/
-- CREATE STORE PROCEDURE

-- CASE 1: create a stored procedure that allows a user to input a department name and 
-- retrieves all the doctors belonging to that department
-- step 1: create stored procedure
DROP PROCEDURE IF EXISTS GetDoctorsByDepartment;
DELIMITER $$

CREATE PROCEDURE GetDoctorsByDepartment(IN deptName VARCHAR(100))
BEGIN
    SELECT 
        d.DoctorID, d.FirstName, d.LastName, 
        d.Phone, d.Email
    FROM 
        Doctor d
    INNER JOIN 
        Department dp USING(DepartmentID)
    WHERE 
        dp.DepartmentName = deptName;
END$$

DELIMITER ;

#Step 2: Call the Stored Procedure
CALL GetDoctorsByDepartment('CARDIOLOGY');

-- CASE 2: create a stored procedure that finds the patient who has made the most payment in the last one month
-- Step 1: Create the Stored Procedure
DROP PROCEDURE IF EXISTS GetTopPayingPatientLastMonth;
DELIMITER $$

CREATE PROCEDURE GetTopPayingPatientLastMonth()
BEGIN
    -- Find the patient who has made the most payment in the last one month
    SELECT 
        p.PatientID, 
        p.FirstName, 
        p.LastName, 
        SUM(b.TotalAmount) AS TotalPayments
    FROM 
        Patient p
    INNER JOIN 
        Billing b USING(PatientID)
    WHERE 
        b.PaymentDate >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)
    GROUP BY 
        p.PatientID, p.FirstName, p.LastName
    ORDER BY 
        TotalPayments DESC
    LIMIT 1;
END$$

DELIMITER ;

-- Step 2: Call the Stored Procedure
CALL GetTopPayingPatientLastMonth();

-- CASE 3: create a stored procedure that calculates the total hospital stay (in days) for each patient
-- Step 1: Create the Stored Procedure
DROP PROCEDURE IF EXISTS CalculateTotalHospitalStay;
DELIMITER $$

CREATE PROCEDURE CalculateTotalHospitalStay()
BEGIN
    -- Calculate the total hospital stay in days for each patient
    SELECT 
        p.PatientID, 
        p.FirstName, 
        p.LastName, 
        SUM(DATEDIFF(hs.DischargeDate, hs.AdmitDate)) AS TotalStayDays
    FROM 
        Patient p
    INNER JOIN 
        HospitalStay hs ON p.PatientID = hs.PatientID
    GROUP BY 
        p.PatientID, p.FirstName, p.LastName;
END$$

DELIMITER ;

-- Step 2: Call the Stored Procedure
CALL CalculateTotalHospitalStay();

-- CASE 4: create a stored procedure that counts the number of available rooms in each branch
-- Step 1: Create the Stored Procedure
DROP PROCEDURE IF EXISTS CountAvailableRoomsPerBranch;
DELIMITER $$

CREATE PROCEDURE CountAvailableRoomsPerBranch()
BEGIN
    -- Count the number of available rooms in each branch
    SELECT 
        hb.Branch_ID, 
        hb.Branch_Name, 
        COUNT(r.RoomID) AS AvailableRooms
    FROM 
        Hospital_Branch hb
    INNER JOIN 
        Room r ON hb.Branch_ID = r.Branch_ID
    WHERE 
        r.Availability = TRUE
    GROUP BY 
        hb.Branch_ID, hb.Branch_Name;
END$$

DELIMITER ;

-- Step 2: Call the Stored Procedure
CALL CountAvailableRoomsPerBranch();

-- CASE 5: create a stored procedure that applies a 10% discount to 
-- all billing records where the payment method is "Debit Card"
-- Step 1: Create the Stored Procedure
DROP PROCEDURE IF EXISTS ApplyDebitCardDiscount;
DELIMITER $$

CREATE PROCEDURE ApplyDebitCardDiscount()
BEGIN
    -- Update the TotalAmount by applying a 10% discount for all records with PaymentMethod = 'Debit Card'
    UPDATE Billing
    SET TotalAmount = TotalAmount * 0.90
    WHERE PaymentMethod = 'Debit Card';
END$$

DELIMITER ;

-- Step 2: Call the Stored Procedure
CALL ApplyDebitCardDiscount();

SELECT * FROM Billing;

/*---------------------------------------------------------------------------------*/
-- CREATE FUNCTION
-- CASE 1: create function to calculate total bill for each patient
DROP FUNCTION IF EXISTS TotalBilledAmount;
CREATE FUNCTION TotalBilledAmount(p_PatientID INT)
RETURNS DECIMAL(10, 2)
DETERMINISTIC
BEGIN
    DECLARE total DECIMAL(10, 2);
    
    SELECT SUM(TotalAmount)
    INTO total
    FROM Billing
    WHERE PatientID = p_PatientID;

    RETURN total;
END;

-- Using the TotalBilledAmount function
SELECT 
    PatientID, CONCAT(FirstName,' ', LastName) AS Patient_FullName,
    TotalBilledAmount(PatientID) AS TotalBilling
FROM Patient
ORDER BY TotalBilling DESC;

-- CASE 2: Calculate Room Occupancy Rate
DROP FUNCTION IF EXISTS CalculateRoomOccupancyRate;
DELIMITER $$

CREATE FUNCTION CalculateRoomOccupancyRate(branchID INT) 
RETURNS DECIMAL(5, 2)
DETERMINISTIC
BEGIN
    DECLARE totalRooms INT;
    DECLARE occupiedRooms INT;
    DECLARE occupancyRate DECIMAL(5, 2);
    
    SELECT COUNT(*) INTO totalRooms 
    FROM Room 
    WHERE Branch_ID = branchID;
    
    SELECT COUNT(*) INTO occupiedRooms 
    FROM Room 
    WHERE Branch_ID = branchID AND Availability = FALSE;
    
    SET occupancyRate = (occupiedRooms / totalRooms) * 100;
    
    RETURN IFNULL(occupancyRate, 0.00);
END$$

DELIMITER ;

SELECT CalculateRoomOccupancyRate(1) AS OccupancyRate_branch1,
        CalculateRoomOccupancyRate(2) AS OccupancyRate_branch2;





/*============================== DELIVERABLE #3 =======================================*/

/* Query: List all patients with their assigned branch and department names */
SELECT p.PatientID, p.FirstName, p.LastName, hb.Branch_Name, d.DepartmentName
FROM Patient p
LEFT JOIN Hospital_Branch hb USING(Branch_ID)
LEFT JOIN Doctor doc ON p.PatientID = doc.DoctorID
LEFT JOIN Department d USING(DepartmentID);

/* Query: Calculate the total number of rooms available by branch */
SELECT hb.Branch_Name, COUNT(r.RoomID) AS AvailableRooms
FROM Room r
INNER JOIN Hospital_Branch hb USING(Branch_ID)
WHERE r.Availability = TRUE
GROUP BY hb.Branch_Name;

/* Query: Find patients who have visited multiple departments */
SELECT  p.PatientID, p.FirstName, p.LastName, 
        COUNT(DISTINCT doc.DepartmentID) AS DepartmentCount
FROM Patient p
INNER JOIN Appointment a USING(PatientID)
INNER JOIN Doctor doc USING(DoctorID)
GROUP BY p.PatientID, p.FirstName, p.LastName
HAVING COUNT(DISTINCT doc.DepartmentID) > 1;

/* Query: Rank patients by their total billing amount */
SELECT  p.PatientID, p.FirstName, p.LastName, 
        SUM(b.TotalAmount) AS TotalBilling,
        RANK() OVER (ORDER BY SUM(b.TotalAmount) DESC) AS BillingRank
FROM Billing b
INNER JOIN Patient p USING(PatientID)
GROUP BY p.PatientID, p.FirstName, p.LastName
ORDER BY BillingRank;

/* Query: Dense rank patients by their total billing amount */
SELECT  p.PatientID, p.FirstName, p.LastName, 
        SUM(b.TotalAmount) AS TotalBilling,
        DENSE_RANK() OVER (ORDER BY SUM(b.TotalAmount) DESC) AS BillingDenseRank
FROM Billing b
INNER JOIN Patient p USING(PatientID)
GROUP BY p.PatientID, p.FirstName, p.LastName
ORDER BY BillingDenseRank;

/* Query: Rank doctors by the number of patients they have attended */
SELECT  doc.DoctorID, doc.FirstName, doc.LastName, 
        COUNT(mr.PatientID) AS PatientCount,
        RANK() OVER (ORDER BY COUNT(mr.PatientID) DESC) AS DoctorRank
FROM Doctor doc
INNER JOIN MedicalRecord mr USING(DoctorID)
GROUP BY doc.DoctorID, doc.FirstName, doc.LastName;

/* Query: Dense Rank of Doctors by Number of Patients Treated */
SELECT doc.DoctorID,
       CONCAT(doc.FirstName, ' ', doc.LastName) AS DoctorName,
       COUNT(DISTINCT mr.PatientID) AS PatientsTreated,
       DENSE_RANK() OVER (ORDER BY COUNT(DISTINCT mr.PatientID) DESC) AS DoctorRank
FROM MedicalRecord mr
INNER JOIN Doctor doc USING(DoctorID)
GROUP BY doc.DoctorID, doc.FirstName, doc.LastName
ORDER BY DoctorRank;

/* Query: Find all appointments that fall within the next 7 days */
SELECT  a.AppointmentID, 
        CONCAT(p.FirstName, ' ', p.LastName) AS PatientFullName, 
        a.AppointmentDate, a.AppointmentTime
FROM Appointment a
INNER JOIN Patient p USING(PatientID)
WHERE a.AppointmentDate BETWEEN CURDATE() AND DATE_ADD(CURDATE(), INTERVAL 7 DAY)
ORDER BY a.AppointmentDate, a.AppointmentTime;

/* Query: Generate a report showing total revenue per branch for the last month */
SELECT hb.Branch_Name, SUM(b.TotalAmount) AS TotalRevenue
FROM Billing b
INNER JOIN Hospital_Branch hb USING(Branch_ID)
WHERE b.PaymentDate BETWEEN DATE_SUB(CURDATE(), INTERVAL 1 MONTH) AND CURDATE()
GROUP BY hb.Branch_Name;

/* Query: Calculate the lead payment amount for each patient */
SELECT p.PatientID, p.FirstName, p.LastName, b.PaymentDate, b.TotalAmount,
       LEAD(b.TotalAmount, 1) OVER (PARTITION BY p.PatientID ORDER BY b.PaymentDate) 
       AS NextPaymentAmount
FROM Billing b
INNER JOIN Patient p USING(PatientID)
ORDER BY p.PatientID, b.PaymentDate;

/* Query: Calculate the lag payment amount for each patient */
SELECT p.PatientID, p.FirstName, p.LastName, b.PaymentDate, b.TotalAmount,
       LAG(b.TotalAmount, 1) OVER (PARTITION BY p.PatientID ORDER BY b.PaymentDate) 
       AS PreviousPaymentAmount
FROM Billing b
INNER JOIN Patient p USING(PatientID)
ORDER BY p.PatientID, b.PaymentDate;

/* Query: List all appointments by daytime */
SELECT
    a.AppointmentDate,
    a.AppointmentTime,
    CONCAT(p.FirstName, ' ', p.LastName) AS PatientFullName,
    p.Gender,
    p.Phone AS PatientPhoneNumber,
    CONCAT(doc.FirstName, ' ', doc.LastName) AS DoctorFullName,
    d.DepartmentName,
    a.ReasonForVisit
FROM
    Appointment a
INNER JOIN
    Patient p USING(PatientID)
INNER JOIN
    Doctor doc USING(DoctorID)
INNER JOIN
    Department d USING(DepartmentID)
ORDER BY
    a.AppointmentDate, a.AppointmentTime;

/* Query: List all appointments for each doctor within a week */
SELECT
    CONCAT(doc.FirstName, ' ', doc.LastName) AS DoctorFullName,
    d.DepartmentName,
    a.AppointmentDate,
    a.AppointmentTime,
    CONCAT(p.FirstName, ' ', p.LastName) AS PatientFullName,
    p.Phone AS PatientPhoneNumber,
    a.ReasonForVisit
FROM
    Appointment a
INNER JOIN
    Doctor doc USING(DoctorID)
INNER JOIN
    Department d USING(DepartmentID)
INNER JOIN
    Patient p USING(PatientID)
WHERE
    YEARWEEK(a.AppointmentDate, 1) = YEARWEEK(CURDATE(), 1)
ORDER BY
    doc.FirstName, doc.LastName, a.AppointmentDate, a.AppointmentTime;

/* Query: Total number of appointments per department with a grand total */
SELECT
    d.DepartmentName,
    COUNT(a.AppointmentID) AS TotalAppointments
FROM
    Appointment a
INNER JOIN
    Doctor doc ON a.DoctorID = doc.DoctorID
INNER JOIN
    Department d ON doc.DepartmentID = d.DepartmentID
GROUP BY
    d.DepartmentName WITH ROLLUP;

#option 2
SELECT
    d.DepartmentName,
    COUNT(a.AppointmentID) AS TotalAppointments
FROM
    Appointment a
INNER JOIN
    Doctor doc ON a.DoctorID = doc.DoctorID
INNER JOIN
    Department d ON doc.DepartmentID = d.DepartmentID
GROUP BY
    d.DepartmentName
UNION ALL
SELECT
    NULL,
    COUNT(a.AppointmentID) AS TotalAppointments
FROM
    Appointment a
INNER JOIN
    Doctor doc ON a.DoctorID = doc.DoctorID
INNER JOIN
    Department d ON doc.DepartmentID = d.DepartmentID;

/* Query: Total number of patients by branch and gender */
SELECT
    hb.Branch_Name,
    p.Gender,
    COUNT(p.PatientID) AS TotalPatients
FROM
    Patient p
INNER JOIN
    Hospital_Branch hb USING(Branch_ID)
GROUP BY
    hb.Branch_Name, p.Gender;

/* Query: Total billing per branch with subtotals*/
SELECT
    hb.Branch_Name,
    SUM(b.TotalAmount) AS TotalBilling
FROM
    Billing b
INNER JOIN
    Hospital_Branch hb USING(Branch_ID)
GROUP BY
    hb.Branch_Name WITH ROLLUP;


/* Query: Total revenue per branch and payment method */
SELECT
    hb.Branch_Name,
    b.PaymentMethod,
    SUM(b.TotalAmount) AS TotalRevenue
FROM
    Billing b
INNER JOIN
    Hospital_Branch hb USING(Branch_ID)
GROUP BY
    hb.Branch_Name, b.PaymentMethod WITH ROLLUP;

/* Query: Total number of patients and appointments by branch */
SELECT
    hb.Branch_Name,
    COUNT(DISTINCT p.PatientID) AS TotalPatients,
    COUNT(a.AppointmentID) AS TotalAppointments
FROM
    Patient p
INNER JOIN
    Appointment a USING(PatientID)
INNER JOIN
    Hospital_Branch hb USING(Branch_ID)
GROUP BY
    hb.Branch_Name;

/* Query: Calculate the total length of stay for each patient */
SELECT
    p.PatientID,
    CONCAT(p.FirstName, ' ', p.LastName) AS PatientFullName,
    SUM(DATEDIFF(hs.DischargeDate, hs.AdmitDate)) AS TotalStayLength
FROM
    HospitalStay hs
INNER JOIN
    Patient p USING(PatientID)
GROUP BY
    p.PatientID, PatientFullName;

/*Query: Room Availability Summary by Branch*/
SELECT
    hb.Branch_ID,
    hb.Branch_Name,
    COUNT(r.RoomID) AS TotalRooms,
    SUM(CASE WHEN r.Availability = TRUE THEN 1 ELSE 0 END) AS AvailableRooms
FROM
    Room r
INNER JOIN
    Hospital_Branch hb USING(Branch_ID)
GROUP BY
    hb.Branch_ID, hb.Branch_Name;


/* Query: Total billing per payment method with subtotals*/
SELECT
    PaymentMethod,
    SUM(TotalAmount) AS TotalBilling
FROM
    Billing
GROUP BY
    PaymentMethod WITH ROLLUP;

/* Query: Availability by Room Type and Branch */
SELECT
    r.RoomType,
    hb.Branch_Name,
    COUNT(r.RoomID) AS TotalRooms,
    SUM(CASE WHEN r.Availability = TRUE THEN 1 ELSE 0 END) AS AvailableRooms
FROM
    Room r
INNER JOIN
    Hospital_Branch hb ON r.Branch_ID = hb.Branch_ID
GROUP BY
    r.RoomType, hb.Branch_Name;


/* Query: Total Billing for Each Patient (Cumulative Sum) */
SELECT
    PatientID,
    PaymentDate,
    TotalAmount,
    SUM(TotalAmount) OVER (PARTITION BY PatientID ORDER BY PaymentDate) 
    AS CumulativeTotalBilling
FROM
    Billing
ORDER BY
    PatientID, PaymentDate;


/* Query: Rank Patients Based on Total Billing Amount in Quartiles */
SELECT
    p.PatientID,
    CONCAT(p.FirstName, ' ', p.LastName) AS PatientFullName,
    SUM(b.TotalAmount) AS TotalBilling,
    NTILE(4) OVER (ORDER BY SUM(b.TotalAmount) DESC) AS BillingQuartile
FROM
    Billing b
INNER JOIN
    Patient p USING(PatientID)
GROUP BY
    p.PatientID, PatientFullName
ORDER BY
    BillingQuartile;


/* Query: Running Total of Appointments by Doctor */
SELECT
    doc.DoctorID,
    CONCAT(doc.FirstName, ' ', doc.LastName) AS DoctorName,
    a.AppointmentDate,
    COUNT(a.AppointmentID) OVER (PARTITION BY doc.DoctorID 
    ORDER BY a.AppointmentDate ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) 
    AS RunningTotalAppointments
FROM
    Appointment a
INNER JOIN
    Doctor doc USING(DoctorID)
ORDER BY
    doc.DoctorID, a.AppointmentDate;

/* Query: Rank Doctors by Number of Appointments */
SELECT
    doc.DoctorID,
    CONCAT(doc.FirstName, ' ', doc.LastName) AS DoctorName,
    COUNT(a.AppointmentID) AS TotalAppointments,
    RANK() OVER (ORDER BY COUNT(a.AppointmentID) DESC) AS AppointmentRank
FROM
    Doctor doc
INNER JOIN
    Appointment a USING(DoctorID)
GROUP BY
    doc.DoctorID, doc.FirstName, doc.LastName
ORDER BY
    AppointmentRank;

/* Query: Combined Use of RANK and DENSE_RANK: Compare Ranking Methods for Billing */
SELECT
    p.PatientID,
    CONCAT(p.FirstName, ' ', p.LastName) AS PatientName,
    SUM(b.TotalAmount) AS TotalBilling,
    RANK() OVER (ORDER BY SUM(b.TotalAmount) DESC) AS RankBilling,
    DENSE_RANK() OVER (ORDER BY SUM(b.TotalAmount) DESC) AS DenseRankBilling
FROM
    Patient p
INNER JOIN
    Billing b USING(PatientID)
GROUP BY
    p.PatientID, p.FirstName, p.LastName
ORDER BY
    RankBilling;

/* Query: Combined Use of RANK and DENSE_RANK: Compare Ranking Methods for Appointment */
SELECT
    doc.DoctorID,
    CONCAT(doc.FirstName, ' ', doc.LastName) AS DoctorFullName,
    COUNT(DISTINCT a.PatientID) AS TotalPatients,
    RANK() OVER (ORDER BY COUNT(DISTINCT a.PatientID) DESC) AS DoctorRank,
    DENSE_RANK() OVER (ORDER BY COUNT(DISTINCT a.PatientID) DESC) AS DoctorDenseRank
FROM
    Appointment a
INNER JOIN
    Doctor doc USING(DoctorID)
GROUP BY
    doc.DoctorID, DoctorFullName
ORDER BY
    DoctorRank;

/* Query: Find Doctors with More Patients than Average */
SELECT
    CONCAT(doc.FirstName, ' ', doc.LastName) AS DoctorName,
    COUNT(a.PatientID) AS PatientCount
FROM
    Doctor doc
INNER JOIN
    Appointment a USING(DoctorID)
GROUP BY
    doc.DoctorID, doc.FirstName, doc.LastName
HAVING
    COUNT(a.PatientID) > (SELECT AVG(PatientCount) FROM
                            (SELECT COUNT(a2.PatientID) AS PatientCount
                             FROM Appointment a2
                             GROUP BY a2.DoctorID) AS avgPatients);

/* Query: List Patients with Appointments in Multiple Departments */
SELECT
    DISTINCT p.PatientID,
    CONCAT(p.FirstName, ' ', p.LastName) AS PatientName
FROM
    Patient p
WHERE
    EXISTS (
        SELECT 1
        FROM Appointment a1
        INNER JOIN Doctor d1 USING(DoctorID)
        WHERE p.PatientID = a1.PatientID
        AND d1.DepartmentID !=
            (SELECT d2.DepartmentID
             FROM Appointment a2
             INNER JOIN Doctor d2 USING(DoctorID)
             WHERE p.PatientID = a2.PatientID
             LIMIT 1)
    );

/* Query: List Doctors with No Appointments in a Specific Month */
SELECT
    doc.DoctorID,
    CONCAT(doc.FirstName, ' ', doc.LastName) AS DoctorName
FROM
    Doctor doc
WHERE
    NOT EXISTS (
        SELECT 1
        FROM Appointment a
        WHERE a.DoctorID = doc.DoctorID
        AND a.AppointmentDate BETWEEN '2024-10-01' AND '2024-10-30'
    );

/* Query: Calculate the Number of Days Since Last Appointment */
SELECT
    p.PatientID,
    CONCAT(p.FirstName, ' ', p.LastName) AS PatientFullName,
    MAX(a.AppointmentDate) AS LastAppointmentDate,
    DATEDIFF(CURDATE(), MAX(a.AppointmentDate)) AS DaysSinceLastAppointment
FROM
    Appointment a
INNER JOIN
    Patient p USING(PatientID)
GROUP BY
    p.PatientID, PatientFullName
HAVING
    DaysSinceLastAppointment > 0
ORDER BY
    DaysSinceLastAppointment DESC;



/* Query: Find Departments with Below-Average Appointment Counts */
SELECT
    d.DepartmentName,
    COUNT(a.AppointmentID) AS AppointmentCount
FROM
    Department d
INNER JOIN
    Doctor doc USING(DepartmentID)
INNER JOIN
    Appointment a USING(DoctorID)
GROUP BY
    d.DepartmentName
HAVING
    COUNT(a.AppointmentID) <    (SELECT AVG(AppointmentCount)
                                FROM
                                (SELECT COUNT(a2.AppointmentID) AS AppointmentCount
                                FROM Department d2
                                INNER JOIN Doctor doc2 USING(DepartmentID)
                                INNER JOIN Appointment a2 USING(DoctorID)
                                GROUP BY d2.DepartmentName) AS avgAppointments);

/* Query: Cumulative Diagnosis Count Over Time */
SELECT
    mr.RecordID,
    mr.Diagnosis,
    mr.CreateDate,
    SUM(1) OVER (PARTITION BY mr.Diagnosis 
    ORDER BY mr.CreateDate ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) 
    AS CumulativeDiagnosisCount
FROM
    MedicalRecord mr
ORDER BY
    mr.CreateDate;
