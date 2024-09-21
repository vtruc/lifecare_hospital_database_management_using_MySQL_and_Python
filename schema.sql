/*============================== CREATE DATABASE =======================================*/
DROP DATABASE IF EXISTS HospitalManagement;
CREATE DATABASE HospitalManagement;
USE HospitalManagement;

/*============================== CREATE TABLES =======================================*/

/* -- create table: Hospital_Branch */
DROP TABLE IF EXISTS Hospital_Branch;
CREATE TABLE Hospital_Branch (
    Branch_ID               TINYINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    Branch_Name             ENUM('Vertical', 'Horizontal') NOT NULL UNIQUE KEY,
    Branch_Address          VARCHAR(255) NOT NULL UNIQUE KEY,
    Branch_Phone_Number     VARCHAR(20) NOT NULL UNIQUE KEY,
    State                   VARCHAR(50) NOT NULL,
    Zip_Code                VARCHAR(10) NOT NULL
);

/* -- create table: Department */
DROP TABLE IF EXISTS Department;
CREATE TABLE Department (
    DepartmentID        TINYINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    DepartmentName      ENUM(
                        'CARDIOLOGY',
                        'DERMATOLOGY',
                        'EAR, NOSE & THROAT',
                        'GASTROENTEROLOGY',
                        'NEUROLOGY',
                        'NEPHROLOGY',
                        'OBSTETRICS & GYNAECOLOGY',
                        'OPHTHALMOLOGY',
                        'ORTHOPAEDIC',
                        'UROLOGY'
                        ) NOT NULL,
    Location            VARCHAR(100) NOT NULL,
    Branch_ID           TINYINT UNSIGNED NOT NULL,
    FOREIGN KEY (Branch_ID) REFERENCES Hospital_Branch(Branch_ID) ON DELETE CASCADE ON UPDATE CASCADE,
    UNIQUE KEY (DepartmentName, Branch_ID) -- Ensures unique department names within each branch
);

/* -- create table: Patient */
DROP TABLE IF EXISTS Patient;
CREATE TABLE Patient (
    PatientID       INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    FirstName       VARCHAR(50) NOT NULL,
    LastName        VARCHAR(50) NOT NULL,
    Gender          VARCHAR(10) NOT NULL,
    DateOfBirth     DATE NOT NULL,
    Address         VARCHAR(255) NOT NULL,
    Phone           VARCHAR(20) UNIQUE KEY NOT NULL,
    Email           VARCHAR(100) UNIQUE KEY NOT NULL,
    Branch_ID       TINYINT UNSIGNED NOT NULL,
    FOREIGN KEY (Branch_ID) REFERENCES Hospital_Branch(Branch_ID) ON DELETE CASCADE ON UPDATE CASCADE
);

/* -- create table: Doctor */
DROP TABLE IF EXISTS Doctor;
CREATE TABLE Doctor (
    DoctorID            TINYINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    FirstName           VARCHAR(50) NOT NULL,
    LastName            VARCHAR(50) NOT NULL,
    Phone               VARCHAR(20) UNIQUE KEY NOT NULL,
    Email               VARCHAR(100) UNIQUE KEY NOT NULL,
    DepartmentID        TINYINT UNSIGNED NOT NULL,
    Branch_ID           TINYINT UNSIGNED NOT NULL,
    FOREIGN KEY (Branch_ID) REFERENCES Hospital_Branch(Branch_ID) ON DELETE CASCADE ON UPDATE CASCADE
);

/* -- create table: Nurse */
DROP TABLE IF EXISTS Nurse;
CREATE TABLE Nurse (
    NurseID         TINYINT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    FirstName       VARCHAR(50) NOT NULL,
    LastName        VARCHAR(50) NOT NULL,
    Phone           VARCHAR(20) UNIQUE KEY NOT NULL,
    Email           VARCHAR(100) UNIQUE KEY NOT NULL,
    Branch_ID       TINYINT UNSIGNED NOT NULL,
    FOREIGN KEY (Branch_ID) REFERENCES Hospital_Branch(Branch_ID) ON DELETE CASCADE ON UPDATE CASCADE
);

/* -- create table: Appointment */
DROP TABLE IF EXISTS Appointment;
CREATE TABLE Appointment (
    AppointmentID       INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    PatientID           INT UNSIGNED NOT NULL,
    DoctorID            TINYINT UNSIGNED NOT NULL,
    AppointmentDate     DATE NOT NULL,
    AppointmentTime     TIME NOT NULL,
    ReasonForVisit      TEXT NOT NULL,
    Branch_ID           TINYINT UNSIGNED NOT NULL,
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (DoctorID) REFERENCES Doctor(DoctorID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (Branch_ID) REFERENCES Hospital_Branch(Branch_ID) ON DELETE CASCADE ON UPDATE CASCADE,
    UNIQUE KEY (PatientID, DoctorID, AppointmentDate, AppointmentTime) -- Unique combination to prevent double-booking
);

/* -- create table: MedicalRecord */
DROP TABLE IF EXISTS MedicalRecord;
CREATE TABLE MedicalRecord (
    RecordID        INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    PatientID       INT UNSIGNED NOT NULL,
    DoctorID        TINYINT UNSIGNED NOT NULL,
    Diagnosis       TEXT NOT NULL,
    Treatment       TEXT NOT NULL,
    CreateDate     DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    Branch_ID       TINYINT UNSIGNED NOT NULL,
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (DoctorID) REFERENCES Doctor(DoctorID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (Branch_ID) REFERENCES Hospital_Branch(Branch_ID) ON DELETE CASCADE ON UPDATE CASCADE
);

/* -- create table: Room */
DROP TABLE IF EXISTS Room;
CREATE TABLE Room (
    RoomID          INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    RoomNumber      VARCHAR(10) UNIQUE KEY NOT NULL,
    RoomType        VARCHAR(50) NOT NULL,
    Availability    BOOLEAN NOT NULL,
    Branch_ID       TINYINT UNSIGNED NOT NULL,
    FOREIGN KEY (Branch_ID) REFERENCES Hospital_Branch(Branch_ID) ON DELETE CASCADE ON UPDATE CASCADE
);

/* -- create table: HospitalStay */
DROP TABLE IF EXISTS HospitalStay;
CREATE TABLE HospitalStay (
    StayID              INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    PatientID           INT UNSIGNED NOT NULL,
    RoomID              INT UNSIGNED NOT NULL,
    AdmitDate           DATE NOT NULL,
    DischargeDate       DATE NOT NULL,
    AssignedNurseID     TINYINT UNSIGNED NOT NULL,
    Branch_ID           TINYINT UNSIGNED NOT NULL,
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (RoomID) REFERENCES Room(RoomID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (AssignedNurseID) REFERENCES Nurse(NurseID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (Branch_ID) REFERENCES Hospital_Branch(Branch_ID) ON DELETE CASCADE ON UPDATE CASCADE,
    UNIQUE KEY (PatientID, RoomID, AdmitDate) -- Prevents duplicate stays
);

/* -- create table: Billing */
DROP TABLE IF EXISTS Billing;
CREATE TABLE Billing (
    BillID              INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    PatientID           INT UNSIGNED NOT NULL,
    TotalAmount         DECIMAL(10, 2) NOT NULL,
    PaymentDate         DATE NOT NULL,
    PaymentMethod       VARCHAR(50) NOT NULL,
    Branch_ID           TINYINT UNSIGNED NOT NULL,
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (Branch_ID) REFERENCES Hospital_Branch(Branch_ID) ON DELETE CASCADE ON UPDATE CASCADE,
    UNIQUE KEY (PatientID, PaymentDate) -- Prevents duplicate billing on the same date
);

/* -- Create table: PatientHistory */
DROP TABLE IF EXISTS PatientHistory;
CREATE TABLE PatientHistory (
    HistoryID       INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    PatientID       INT UNSIGNED NOT NULL,
    FirstName       VARCHAR(50) NOT NULL,
    LastName        VARCHAR(50) NOT NULL,
    Gender          VARCHAR(10) NOT NULL,
    DateOfBirth     DATE NOT NULL,
    Address         VARCHAR(255) NOT NULL,
    Phone           VARCHAR(20) NOT NULL,
    Email           VARCHAR(100) NOT NULL,
    Branch_ID       TINYINT UNSIGNED NOT NULL,
    ChangeDate      DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID) ON DELETE CASCADE ON UPDATE CASCADE
);

DELIMITER $$

CREATE TRIGGER trg_Patient_Phone_Update
BEFORE UPDATE ON Patient
FOR EACH ROW
BEGIN
    IF OLD.Phone <> NEW.Phone THEN
        INSERT INTO PatientHistory (
            PatientID, FirstName, LastName, Gender, DateOfBirth,
            Address, Phone, Email, Branch_ID, ChangeDate
        ) VALUES (
            OLD.PatientID, OLD.FirstName, OLD.LastName, OLD.Gender, OLD.DateOfBirth,
            OLD.Address, OLD.Phone, OLD.Email, OLD.Branch_ID, NOW()
        );
    END IF;
END$$

DELIMITER ;

/*============================== INSERT DATABASE =======================================*/
INSERT INTO Hospital_Branch (Branch_Name,   Branch_Address,                 Branch_Phone_Number, State,     Zip_Code) 
VALUES
                            ('Vertical',    '123 Main St, Springfield',     '123-456-7890',     'Illinois', '62701'),
                            ('Horizontal',  '456 Elm St, Springfield',      '987-654-3210',     'Illinois', '62702');

INSERT INTO Department (DepartmentName, Location, Branch_ID) 
VALUES
                        ('CARDIOLOGY', 'Main Building', 2),
                        ('DERMATOLOGY', 'East Wing', 2),
                        ('EAR, NOSE & THROAT', 'North Block', 2),
                        ('GASTROENTEROLOGY', 'South Wing', 2),
                        ('NEUROLOGY', 'West Block', 2),
                        ('NEPHROLOGY', 'Main Building', 2),
                        ('OBSTETRICS & GYNAECOLOGY', 'East Wing', 1),
                        ('OPHTHALMOLOGY', 'North Block', 1),
                        ('ORTHOPAEDIC', 'South Wing', 2),
                        ('UROLOGY', 'West Block', 1);



INSERT INTO Patient (FirstName, LastName, Gender, DateOfBirth, Address, Phone, Email, Branch_ID) 
VALUES
    ('Quentin', 'Horche', 'Male', '1980-06-19', '927 Kennedy Plaza', '323-790-7357', 'qhorche0@telegraph.co.uk', 1),
    ('Cicely', 'Monsey', 'Female', '1965-07-19', '61 Union Plaza', '737-870-7780', 'cmonsey1@cocolog-nifty.com', 1),
    ('Ansley', 'Vinten', 'Female', '2013-02-18', '50423 Riverside Pass', '282-393-7319', 'avinten2@livejournal.com', 1),
    ('Stacie', 'Raecroft', 'Female', '2005-10-01', '88 Brentwood Way', '112-723-1541', 'sraecroft3@shinystat.com', 2),
    ('Brandtr', 'Cardoo', 'Male', '1987-08-24', '28523 Center Avenue', '135-659-1530', 'bcardoo4@google.ca', 2),
    ('Robyn', 'Bernardotte', 'Female', '1975-11-03', '164 Ludington Lane', '644-736-5718', 'rbernardotte5@mysql.com', 2),
    ('Garey', 'Tuffs', 'Male', '1974-05-28', '7783 Toban Crossing', '698-561-3208', 'gtuffs6@stumbleupon.com', 1),
    ('Alessandra', 'Pallister', 'Female', '1976-11-13', '3 Gerald Road', '206-696-6210', 'apallister7@woothemes.com', 2),
    ('Sibley', 'Sharer', 'Female', '1951-06-20', '4 Valley Edge Center', '974-520-8052', 'ssharer8@ustream.tv', 2),
    ('Myrah', 'Conquer', 'Female', '1994-07-03', '59425 1st Plaza', '220-633-0691', 'mconquer9@goo.ne.jp', 1),
    ('Temp', 'Pashler', 'Male', '1984-02-02', '83 Sutherland Court', '367-694-7131', 'tpashler0@engadget.com', 1),
    ('Jasmine', 'Studholme', 'Female', '1957-03-24', '8741 Manufacturers Place', '734-593-7604', 'jstudholme1@springer.com', 2),
    ('Keelby', 'Stollberg', 'Male', '1995-05-10', '61872 Goodland Road', '482-406-1286', 'kstollberg2@shinystat.com', 2),
    ('Thoma', 'Flippen', 'Male', '1964-06-17', '2717 Muir Circle', '969-820-9950', 'tflippen3@purevolume.com', 2),
    ('Ronald', 'Cottu', 'Male', '2015-06-13', '2653 Brown Terrace', '351-876-2093', 'rcottu4@java.com', 2),
    ('Adella', 'Gribbon', 'Female', '2019-07-13', '92741 Dapin Hill', '692-683-8550', 'agribbon5@independent.co.uk', 1),
    ('Obidiah', 'Wrigglesworth', 'Male', '1998-01-11', '762 Macpherson Street', '102-722-3138', 'owrigglesworth6@diigo.com', 2),
    ('Elva', 'Whaley', 'Female', '1974-03-10', '825 Morrow Plaza', '744-440-5273', 'ewhaley7@ow.ly', 1),
    ('Frieda', 'Simoes', 'Female', '1977-09-09', '6 Milwaukee Place', '328-770-6376', 'fsimoes8@jalbum.net', 1),
    ('Lilia', 'Chetwind', 'Female', '1960-03-13', '2 Ryan Road', '756-696-8467', 'lchetwind9@arizona.edu', 2),
    ('Sapphira', 'Cheesworth', 'Female', '2016-01-13', '72 Buell Place', '566-163-1793', 'scheesworth0@shop-pro.jp', 2),
    ('Stefano', 'Jelf', 'Male', '2015-04-04', '8 Heffernan Alley', '468-526-9546', 'sjelf1@cocolog-nifty.com', 1),
    ('Jan', 'Jacquemet', 'Male', '2009-10-24', '39 Sundown Plaza', '666-575-9331', 'jjacquemet2@people.com.cn', 1),
    ('Edmon', 'Doyle', 'Male', '2018-09-29', '76 Green Trail', '695-982-7672', 'edoyle3@tripadvisor.com', 2),
    ('Alexandre', 'Harkess', 'Male', '2023-08-26', '7 6th Plaza', '942-922-0815', 'aharkess4@npr.org', 2),
    ('Alfons', 'Myrie', 'Male', '1956-05-06', '6510 Annamark Drive', '212-382-2428', 'amyrie5@samsung.com', 1),
    ('Dana', 'Liversley', 'Male', '1976-09-03', '24121 Weeping Birch Center', '851-569-9399', 'dliversley6@w3.org', 2),
    ('Vikki', 'Wheildon', 'Female', '1986-04-03', '89 Granby Parkway', '739-654-9556', 'vwheildon7@ibm.com', 2),
    ('Tadd', 'Epilet', 'Male', '1994-01-25', '67 Sachtjen Street', '109-474-9306', 'tepilet8@godaddy.com', 1),
    ('Leroy', 'Stainland', 'Male', '1996-12-01', '93 Westerfield Alley', '526-384-8829', 'lstainland9@wix.com', 2);



INSERT INTO Doctor (FirstName, LastName, Phone, Email, DepartmentID, Branch_ID) 
VALUES
    ('STEPHI', 'INGLEDEW', '283-505-9368', 'singledew0@mac.com', 5, 2),
    ('MARIJO', 'PURSGLOVE', '156-399-3808', 'mpursglove1@eventbrite.com', 4, 1),
    ('JOSSELYN', 'BRAMSOM', '648-216-7742', 'jbramsom2@ucsd.edu', 1, 1),
    ('UDALL', 'DRINKALL', '459-532-1157', 'admin@hospital.com', 10, 2),
    ('TOME', 'ADAMCZEWSKI', '456-347-5231', 'tadamczewski4@utexas.edu', 9, 1),
    ('AILEY', 'DEVERILL', '387-376-0263', 'adeverill5@amazon.co.jp', 7, 2),
    ('JOHNA', 'FARLAMBE', '782-936-0114', 'jfarlambe6@pcworld.com', 8, 2),
    ('VIDOVIC', 'NEAL', '835-989-6674', 'vneal7@cnn.com', 7, 2),
    ('LARRY', 'SILLETT', '113-100-6950', 'lsillett8@engadget.com', 6, 2),
    ('GOLDI', 'LORKIN', '183-489-3327', 'glorkin9@hubpages.com', 7, 1),
    ('BLAIR', 'PHILLOTT', '910-331-1202', 'bphillotta@gov.uk', 3, 2),
    ('AILSUN', 'L''HOMMEE', '407-518-7463', 'alhommeeb@google.com.br', 2, 2),
    ('GUILLEMA', 'SHRIMPTON', '623-375-8697', 'gshrimptonc@sphinn.com', 10, 1),
    ('MAX', 'PADON', '426-950-7644', 'mpadsond@nytimes.com', 5, 1),
    ('ZACHARIAS', 'AYLETT', '490-530-6412', 'zaylette@salon.com', 2, 2);


INSERT INTO Nurse (FirstName, LastName, Phone, Email, Branch_ID) 
VALUES
    ('Leone', 'Gabites', '414-698-3718', 'lgabites0@pcworld.com', 1),
    ('Conny', 'Denyer', '966-533-3517', 'cdenyer1@1688.com', 1),
    ('Tami', 'Levins', '700-670-4221', 'tlevins2@php.net', 2),
    ('Lorin', 'Ingold', '938-899-4557', 'lingold3@google.it', 1),
    ('Vic', 'Siggin', '648-691-3463', 'vsiggin4@ycombinator.com', 1),
    ('Matelda', 'Garnson', '977-697-2770', 'mgarnson5@netlog.com', 1),
    ('Ebonee', 'Cornfield', '398-408-2855', 'ecornfield6@xrea.com', 2),
    ('Ange', 'O''Henery', '301-682-6501', 'aohenery7@upenn.edu', 2),
    ('Haskel', 'Rosenfeld', '513-371-9907', 'hrosenfeld8@miitbeian.gov.cn', 2),
    ('Sharlene', 'Kleinzweig', '963-404-0333', 'skleinzweig9@seesaa.net', 2),
    ('Bess', 'Hawken', '261-200-8182', 'bhawkena@gnu.org', 1),
    ('Judas', 'Gehricke', '916-367-9053', 'jgehrickeb@wiley.com', 1),
    ('Jorrie', 'Hallihan', '209-490-1808', 'jhallihanc@wiley.com', 2),
    ('Melinda', 'Leicester', '542-533-1757', 'mleicesterd@un.org', 1),
    ('Dori', 'Sherry', '176-245-9028', 'dsherrye@google.ru', 1);


INSERT INTO Appointment (PatientID, DoctorID, AppointmentDate, AppointmentTime, ReasonForVisit, Branch_ID)
VALUES
    (5, 2, '2024-09-01', '09:00:00', 'Routine check-up', 1),
    (12, 4, '2024-09-02', '10:30:00', 'Consultation for skin rash', 2),
    (8, 7, '2024-09-03', '11:00:00', 'ENT consultation', 1),
    (16, 3, '2024-09-04', '13:00:00', 'Gastroenterology consultation', 2),
    (23, 9, '2024-09-05', '14:30:00', 'Follow-up on surgery', 1),
    (2, 1, '2024-09-06', '15:00:00', 'Cardiology consultation', 2),
    (14, 8, '2024-09-07', '09:30:00', 'Neurology follow-up', 1),
    (29, 5, '2024-09-08', '10:00:00', 'Check-up for hypertension', 2),
    (10, 6, '2024-09-09', '11:30:00', 'Orthopaedic consultation', 1),
    (7, 12, '2024-09-10', '12:00:00', 'Urology consultation', 2),
    (18, 10, '2024-09-11', '14:00:00', 'Routine physical', 1),
    (24, 11, '2024-09-12', '15:30:00', 'Consultation for migraine', 2),
    (3, 14, '2024-09-13', '09:15:00', 'Ophthalmology check-up', 1),
    (20, 13, '2024-09-14', '10:45:00', 'ENT follow-up', 2),
    (9, 15, '2024-09-15', '11:45:00', 'Consultation for back pain', 1),
    (2, 5, '2024-10-01', '09:00:00', 'Routine Checkup', 1),
    (8, 3, '2024-10-02', '10:30:00', 'Follow-up', 2),
    (12, 7, '2024-10-03', '11:00:00', 'Consultation', 1),
    (3, 11, '2024-10-04', '14:15:00', 'Lab Results Review', 2),
    (15, 4, '2024-10-05', '13:45:00', 'Routine Checkup', 1),
    (5, 2, '2024-10-06', '08:30:00', 'New Symptoms', 2),
    (7, 9, '2024-10-07', '15:00:00', 'Consultation', 1),
    (9, 2, '2024-11-08', '12:30:00', 'Follow-up', 2),
    (5, 10, '2024-10-06', '10:00:00', 'Routine Checkup', 1),
    (13, 6, '2024-11-10', '11:45:00', 'Lab Results Review', 2),
    (4, 14, '2024-11-11', '14:00:00', 'Consultation', 1),
    (6, 2, '2024-11-12', '09:30:00', 'New Symptoms', 2),
    (10, 15, '2024-12-13', '08:00:00', 'Follow-up', 1),
    (5, 2, '2024-10-06', '13:00:00', 'Routine Checkup', 2),
    (14, 13, '2024-12-15', '15:30:00', 'Lab Results Review', 1);


INSERT INTO MedicalRecord (PatientID, DoctorID, Diagnosis, Treatment, CreateDate, Branch_ID)
VALUES
    (5, 2, 'Hypertension', 'Prescribed blood pressure medication', '2024-09-01 09:30:00', 1),
    (12, 4, 'Skin Rash', 'Prescribed topical cream', '2024-09-02 11:00:00', 2),
    (8, 7, 'Sinusitis', 'Prescribed antibiotics', '2024-09-03 11:30:00', 1),
    (16, 3, 'Gastroesophageal Reflux Disease (GERD)', 'Prescribed proton pump inhibitors', '2024-09-04 13:30:00', 2),
    (23, 9, 'Post-surgery follow-up', 'Advised wound care and scheduled next follow-up', '2024-09-05 15:00:00', 1),
    (2, 1, 'Coronary Artery Disease', 'Prescribed statins and lifestyle changes', '2024-09-06 15:30:00', 2),
    (14, 8, 'Migraine', 'Prescribed migraine medication', '2024-09-07 10:00:00', 1),
    (29, 5, 'Hypertension', 'Adjusted medication dosage', '2024-09-08 10:30:00', 2),
    (10, 6, 'Knee Osteoarthritis', 'Referred to physical therapy', '2024-09-09 12:00:00', 1),
    (7, 12, 'Urinary Tract Infection', 'Prescribed antibiotics', '2024-09-10 12:30:00', 2),
    (18, 10, 'Routine check-up', 'No treatment required', '2024-09-11 14:00:00', 1),
    (24, 11, 'Migraine', 'Prescribed preventive medication', '2024-09-12 15:30:00', 2),
    (7, 3, 'Allergic Rhinitis', 'Prescribed antihistamines and nasal spray', '2024-09-12 16:00:00', 1),
    (9, 1, 'Chronic Bronchitis', 'Prescribed inhalers and pulmonary rehabilitation', '2024-09-12 17:00:00', 2),
    (15, 5, 'Food Allergy', 'Prescribed epinephrine auto-injector and dietary changes', '2024-09-13 8:00:00', 1),
    (3, 14, 'Cataract', 'Scheduled for surgery', '2024-09-13 09:15:00', 1),
    (20, 13, 'Ear Infection', 'Prescribed ear drops', '2024-09-14 10:45:00', 2),
    (9, 15, 'Back Pain', 'Prescribed pain relief medication and referred to physiotherapy', '2024-09-15 11:45:00', 1),
    (1, 10, 'Monkeypox', 'Antiviral medication and supportive care', '2024-09-15', 1),
    (5, 8, 'Measles', 'Vitamin A supplementation and hydration', '2024-09-16', 2),
    (12, 7, 'Monkeypox', 'Symptomatic treatment and isolation', '2024-09-17', 1),
    (18, 12, 'Measles', 'Rest and antipyretics', '2024-09-18', 2),
    (22, 3, 'Monkeypox', 'Supportive care and pain management', '2024-09-19', 1),
    (9, 15, 'Measles', 'Isolation and monitoring for complications', '2024-09-20', 2),
    (28, 2, 'Monkeypox', 'Antiviral drugs and vaccination of close contacts', '2024-09-21', 1),
    (4, 11, 'Measles', 'Hydration and monitoring for secondary infections', '2024-09-22', 2),
    (15, 6, 'Monkeypox', 'Pain management and supportive care', '2024-09-23', 1),
    (30, 4, 'Measles', 'Vitamin A supplementation and rest', '2024-09-24', 2);

INSERT INTO Room (RoomNumber, RoomType, Availability, Branch_ID)
VALUES
    ('101A', 'Single', TRUE, 1),
    ('102B', 'Double', FALSE, 1),
    ('103C', 'Single', TRUE, 2),
    ('104D', 'Suite', FALSE, 2),
    ('105E', 'Single', TRUE, 1),
    ('106F', 'Double', TRUE, 2),
    ('107G', 'Suite', FALSE, 1),
    ('108H', 'Single', TRUE, 2),
    ('109I', 'Double', FALSE, 1),
    ('110J', 'Suite', TRUE, 2),
    ('111K', 'Single', FALSE, 1),
    ('112L', 'Double', TRUE, 2),
    ('113M', 'Suite', FALSE, 1),
    ('114N', 'Single', TRUE, 2),
    ('115O', 'Double', TRUE, 1),
    ('116P', 'ICU', TRUE, 1);


INSERT INTO HospitalStay (PatientID, RoomID, AdmitDate, DischargeDate, AssignedNurseID, Branch_ID)
VALUES
    (3, 5, '2024-08-20', '2024-08-21', 2, 1),
    (6, 10, '2024-08-22', '2024-08-24', 4, 2),
    (8, 12, '2024-08-25', '2024-08-28', 6, 1),
    (1, 3, '2024-08-26', '2024-08-29', 5, 2),
    (14, 7, '2024-08-27', '2024-09-01', 9, 1),
    (2, 6, '2024-08-30', '2024-09-02', 3, 2),
    (9, 4, '2024-08-31', '2024-09-03', 2, 1),
    (12, 8, '2024-09-01', '2024-09-05', 11, 2),
    (4, 11, '2024-09-02', '2024-09-06', 8, 1),
    (10, 2, '2024-09-03', '2024-09-07', 12, 2),
    (5, 9, '2024-09-04', '2024-09-09', 10, 1),
    (7, 1, '2024-09-05', '2024-09-11', 13, 2),
    (15, 14, '2024-09-06', '2024-09-13', 15, 1),
    (11, 13, '2024-09-07', '2024-09-14', 14, 2),
    (13, 15, '2024-09-08', '2024-09-16', 1, 1);


INSERT INTO Billing (PatientID, TotalAmount, PaymentDate, PaymentMethod, Branch_ID)
VALUES
    (5, 1500.00, '2024-09-01', 'Credit Card', 1),
    (12, 2300.50, '2024-09-02', 'Debit Card', 1),
    (8, 1750.75, '2024-09-03', 'Cash', 2),
    (16, 2800.00, '2024-09-04', 'Insurance', 2),
    (23, 3250.25, '2024-09-05', 'Credit Card', 1),
    (2, 2100.50, '2024-09-06', 'Cash', 2),
    (14, 2600.00, '2024-09-07', 'Insurance', 1),
    (29, 1800.75, '2024-09-08', 'Credit Card', 2),
    (10, 2400.00, '2024-09-09', 'Debit Card', 1),
    (7, 1900.50, '2024-09-10', 'Cash', 2),
    (18, 3000.00, '2024-09-11', 'Insurance', 1),
    (24, 2700.25, '2024-09-12', 'Credit Card', 2),
    (3, 2200.50, '2024-09-13', 'Debit Card', 1),
    (20, 2500.75, '2024-09-14', 'Cash', 2),
    (9, 3100.00, '2024-09-15', 'Insurance', 1),
    (5, 1500.50, '2024-09-16', 'Credit Card', 1),
    (6, 200.75, '2024-09-17', 'Cash', 2),
    (7, 1200.00, '2024-09-18', 'Debit Card', 1),
    (8, 850.25, '2024-09-19', 'Insurance', 2),
    (9, 500.00, '2024-09-20', 'Credit Card', 1),
    (10, 950.75, '2024-09-21', 'Cash', 2),
    (11, 300.50, '2024-09-22', 'Debit Card', 1),
    (12, 1800.00, '2024-09-23', 'Insurance', 2),
    (13, 700.25, '2024-09-24', 'Credit Card', 1),
    (14, 400.50, '2024-09-25', 'Cash', 2),
    (15, 600.75, '2024-09-26', 'Debit Card', 1),
    (5, 1100.00, '2024-09-27', 'Insurance', 2),
    (6, 750.25, '2024-09-28', 'Credit Card', 1),
    (7, 1400.50, '2024-09-29', 'Cash', 2),
    (8, 950.75, '2024-09-30', 'Debit Card', 1);
