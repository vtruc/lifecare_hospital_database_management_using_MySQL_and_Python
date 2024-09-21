# Design Document

By TRUC THI THANH VO


## Scope

### Purpose of the Database
The purpose of the Hospital Management database is to manage various operational aspects of a hospital. This includes handling patient management, staff management, appointment scheduling, medical records, room allocation, and billing. The database is designed to ensure efficient data management, reduce administrative burdens, and provide easy access to critical information for both medical and administrative staff.
Reference website: https://lifecarediagnostic.com/

### Included in the Scope
- **People**: Patients, doctors, nurses, administrative staff.
- **Places**: Hospital branches (Vertical and Horizontal), departments, rooms.
- **Things**: Appointments, medical records, hospital stays, billing information.

### Outside the Scope
- **External Entities**: Insurance companies, suppliers, third-party service providers.
- **External Locations**: Clinics, pharmacies, other hospitals not part of the main hospital branches.
- **Inventory Management**: Management of medical supplies, drugs, and other inventory items.
- **Insurance Claims**: Direct handling of insurance claims or communications with insurance providers.

## Functional Requirements

### What Users Should Be Able to Do
- **Patient Management**: Register new patients, update patient details, and track patient history.
- **Appointment Scheduling**: Schedule, modify, or cancel appointments with doctors.
- **Medical Records**: Record and retrieve patient diagnoses, treatments, and medical history.
- **Room Allocation**: Allocate rooms to patients and track room availability.
- **Hospital Stays**: Manage patient admissions, discharges, and assigned nursing staff.
- **Billing**: Generate, update, and track billing information for patients.

### Beyond the Scope
- **Inventory Management**: The database does not handle the management of medical supplies and inventory.
- **Insurance Claims Processing**: The database does not directly handle insurance claims or communications with insurance providers.
- **External Reporting**: Generating reports for external regulatory bodies or other hospitals is not within the scope of this database.

## Representation

### Entities
The following entities are represented in the database:
### Hospital_Branch Table
The `Hospital_Branch` table includes:

- `Branch_ID`, which specifies the unique ID for each hospital branch as a `TINYINT UNSIGNED`. This column has the `PRIMARY KEY` constraint applied, ensuring that each branch is uniquely identified.
- `Branch_Name`, which is the name of the branch as an `ENUM` with possible values 'Vertical' and 'Horizontal'. This column has the `NOT NULL` constraint applied and the `UNIQUE KEY` constraint to prevent duplicate branch names.
- `Branch_Address`, which specifies the address of the branch as a `VARCHAR(255)`. This column has the `NOT NULL` constraint applied and the `UNIQUE KEY` constraint to ensure each address is unique.
- `Branch_Phone_Number`, which is the phone number of the branch as a `VARCHAR(20)`. This column has the `NOT NULL` constraint applied and the `UNIQUE KEY` constraint to ensure each phone number is unique.
- `State`, which specifies the state where the branch is located as a `VARCHAR(50)`. This column has the `NOT NULL` constraint applied.
- `Zip_Code`, which is the postal code for the branch as a `VARCHAR(10)`. This column has the `NOT NULL` constraint applied.

### Department Table
The `Department` table includes:

- `DepartmentID`, which specifies the unique ID for each department as a `TINYINT UNSIGNED`. This column has the `PRIMARY KEY` constraint applied, ensuring that each department is uniquely identified.
- `DepartmentName`, which specifies the name of the department as an `ENUM` with possible values such as 'Cardiology', 'Dermatology', etc. This column has the `NOT NULL` constraint applied and, combined with `Branch_ID`, has the `UNIQUE KEY` constraint to ensure unique department names within each branch.
- `Location`, which specifies the location of the department within the branch as a `VARCHAR(100)`. This column has the `NOT NULL` constraint applied.
- `Branch_ID`, which is the ID of the branch where the department is located as a `TINYINT UNSIGNED`. This column has the `NOT NULL` constraint and the `FOREIGN KEY` constraint applied, referencing the `Branch_ID` column in the `Hospital_Branch` table to ensure data integrity.

### Patient Table
The `Patient` table includes:

- `PatientID`, which specifies the unique ID for each patient as an `INT UNSIGNED`. This column has the `PRIMARY KEY` constraint applied, ensuring that each patient is uniquely identified.
- `FirstName`, which specifies the first name of the patient as a `VARCHAR(50)`. This column has the `NOT NULL` constraint applied.
- `LastName`, which specifies the last name of the patient as a `VARCHAR(50)`. This column has the `NOT NULL` constraint applied.
- `Gender`, which specifies the gender of the patient as a `VARCHAR(10)`. This column has the `NOT NULL` constraint applied.
- `DateOfBirth`, which specifies the date of birth of the patient as a `DATE`. This column has the `NOT NULL` constraint applied.
- `Address`, which specifies the address of the patient as a `VARCHAR(255)`. This column has the `NOT NULL` constraint applied.
- `Phone`, which specifies the phone number of the patient as a `VARCHAR(20)`. This column has the `NOT NULL` constraint applied and the `UNIQUE KEY` constraint to ensure each phone number is unique.
- `Email`, which specifies the email address of the patient as a `VARCHAR(100)`. This column has the `NOT NULL` constraint applied and the `UNIQUE KEY` constraint to ensure each email is unique.
- `Branch_ID`, which is the ID of the branch where the patient is registered as a `TINYINT UNSIGNED`. This column has the `NOT NULL` constraint and the `FOREIGN KEY` constraint applied, referencing the `Branch_ID` column in the `Hospital_Branch` table to ensure data integrity.

### Doctor Table
The `Doctor` table includes:

- `DoctorID`, which specifies the unique ID for each doctor as a `TINYINT UNSIGNED`. This column has the `PRIMARY KEY` constraint applied, ensuring that each doctor is uniquely identified.
- `FirstName`, which specifies the first name of the doctor as a `VARCHAR(50)`. This column has the `NOT NULL` constraint applied.
- `LastName`, which specifies the last name of the doctor as a `VARCHAR(50)`. This column has the `NOT NULL` constraint applied.
- `Phone`, which specifies the phone number of the doctor as a `VARCHAR(20)`. This column has the `NOT NULL` constraint applied and the `UNIQUE KEY` constraint to ensure each phone number is unique.
- `Email`, which specifies the email address of the doctor as a `VARCHAR(100)`. This column has the `NOT NULL` constraint applied and the `UNIQUE KEY` constraint to ensure each email is unique.
- `DepartmentID`, which is the ID of the department where the doctor works as a `TINYINT UNSIGNED`. This column has the `NOT NULL` constraint and the `FOREIGN KEY` constraint applied, referencing the `DepartmentID` column in the `Department` table to ensure data integrity.
- `Branch_ID`, which is the ID of the branch where the doctor is employed as a `TINYINT UNSIGNED`. This column has the `NOT NULL` constraint and the `FOREIGN KEY` constraint applied, referencing the `Branch_ID` column in the `Hospital_Branch` table to ensure data integrity.

### Nurse Table
The `Nurse` table includes:

- `NurseID`, which specifies the unique ID for each nurse as a `TINYINT UNSIGNED`. This column has the `PRIMARY KEY` constraint applied, ensuring that each nurse is uniquely identified.
- `FirstName`, which specifies the first name of the nurse as a `VARCHAR(50)`. This column has the `NOT NULL` constraint applied.
- `LastName`, which specifies the last name of the nurse as a `VARCHAR(50)`. This column has the `NOT NULL` constraint applied.
- `Phone`, which specifies the phone number of the nurse as a `VARCHAR(20)`. This column has the `NOT NULL` constraint applied and the `UNIQUE KEY` constraint to ensure each phone number is unique.
- `Email`, which specifies the email address of the nurse as a `VARCHAR(100)`. This column has the `NOT NULL` constraint applied and the `UNIQUE KEY` constraint to ensure each email is unique.
- `Branch_ID`, which is the ID of the branch where the nurse is employed as a `TINYINT UNSIGNED`. This column has the `NOT NULL` constraint and the `FOREIGN KEY` constraint applied, referencing the `Branch_ID` column in the `Hospital_Branch` table to ensure data integrity.

### Appointment Table
The `Appointment` table includes:

- `AppointmentID`, which specifies the unique ID for each appointment as an `INT UNSIGNED`. This column has the `PRIMARY KEY` constraint applied, ensuring that each appointment is uniquely identified.
- `PatientID`, which is the ID of the patient attending the appointment as an `INT`. This column has the `NOT NULL` constraint and the `FOREIGN KEY` constraint applied, referencing the `PatientID` column in the `Patient` table to ensure data integrity.
- `DoctorID`, which is the ID of the doctor conducting the appointment as a `TINYINT`. This column has the `NOT NULL` constraint and the `FOREIGN KEY` constraint applied, referencing the `DoctorID` column in the `Doctor` table to ensure data integrity.
- `AppointmentDate`, which specifies the date of the appointment as a `DATE`. This column has the `NOT NULL` constraint applied.
- `AppointmentTime`, which specifies the time of the appointment as a `TIME`. This column has the `NOT NULL` constraint applied.
- `ReasonForVisit`, which specifies the reason for the appointment as `TEXT`. This column has the `NOT NULL` constraint applied.
- `Branch_ID`, which is the ID of the branch where the appointment is scheduled as a `TINYINT UNSIGNED`. This column has the `NOT NULL` constraint and the `FOREIGN KEY` constraint applied, referencing the `Branch_ID` column in the `Hospital_Branch` table to ensure data integrity.
- The combination of `PatientID`, `DoctorID`, `AppointmentDate`, and `AppointmentTime` has the `UNIQUE KEY` constraint applied to prevent double-booking of appointments.

### MedicalRecord Table
The `MedicalRecord` table includes:

- `RecordID`, which specifies the unique ID for each medical record as an `INT UNSIGNED`. This column has the `PRIMARY KEY` constraint applied, ensuring that each medical record is uniquely identified.
- `PatientID`, which is the ID of the patient to whom the record belongs as an `INT`. This column has the `NOT NULL` constraint and the `FOREIGN KEY` constraint applied, referencing the `PatientID` column in the `Patient` table to ensure data integrity.
- `DoctorID`, which is the ID of the doctor who created the record as a `TINYINT`. This column has the `NOT NULL` constraint and the `FOREIGN KEY` constraint applied, referencing the `DoctorID` column in the `Doctor` table to ensure data integrity.
- `Diagnosis`, which specifies the diagnosis given by the doctor as `TEXT`. This column has the `NOT NULL` constraint applied.
- `Treatment`, which specifies the treatment prescribed as `TEXT`. This column has the `NOT NULL` constraint applied.
- `DateOfEntry`, which specifies the date and time when the record was entered as `DATETIME`. This column has the `NOT NULL` constraint applied and defaults to the current timestamp.
- `Branch_ID`, which is the ID of the branch where the record was created as a `TINYINT UNSIGNED`. This column has the `NOT NULL` constraint and the `FOREIGN KEY` constraint applied, referencing the `Branch_ID` column in the `Hospital_Branch` table to ensure data integrity.

### Room Table
The `Room` table includes:

- `RoomID`, which specifies the unique ID for each room as an `INT UNSIGNED`. This column has the `PRIMARY KEY` constraint applied, ensuring that each room is uniquely identified.
- `RoomNumber`, which specifies the room number as a `VARCHAR(10)`. This column has the `NOT NULL` constraint applied and the `UNIQUE KEY` constraint to ensure that each room number is unique within the hospital.
- `RoomType`, which specifies the type of room (e.g., ICU, Private) as a `VARCHAR(50)`. This column has the `NOT NULL` constraint applied.
- `Availability`, which specifies whether the room is available as a `BOOLEAN`. This column has the `NOT NULL` constraint applied.
- `Branch_ID`, which is the ID of the branch where the room is located as a `TINYINT UNSIGNED`. This column has the `NOT NULL` constraint and the `FOREIGN KEY` constraint applied, referencing the `Branch_ID` column in the `Hospital_Branch` table to ensure data integrity.

### HospitalStay Table
The `HospitalStay` table includes:

- `StayID`, which specifies the unique ID for each hospital stay as an `INT UNSIGNED`. This column has the `PRIMARY KEY` constraint applied, ensuring that each stay is uniquely identified.
- `PatientID`, which is the ID of the patient admitted as an `INT`. This column has the `NOT NULL` constraint and the `FOREIGN KEY` constraint applied, referencing the `PatientID` column in the `Patient` table to ensure data integrity.
- `RoomID`, which is the ID of the room where the patient is staying as an `INT`. This column has the `NOT NULL` constraint and the `FOREIGN KEY` constraint applied, referencing the `RoomID` column in the `Room` table to ensure data integrity.
- `AdmitDate`, which specifies the date of admission as a `DATE`. This column has the `NOT NULL` constraint applied.
- `DischargeDate`, which specifies the date of discharge as a `DATE`. This column has the `NOT NULL` constraint applied.
- `AssignedNurseID`, which is the ID of the nurse assigned to the patient as an `INT`. This column has the `NOT NULL` constraint and the `FOREIGN KEY` constraint applied, referencing the `NurseID` column in the `Nurse` table to ensure data integrity.
- `Branch_ID`, which is the ID of the branch where the stay is taking place as a `TINYINT UNSIGNED`. This column has the `NOT NULL` constraint and the `FOREIGN KEY` constraint applied, referencing the `Branch_ID` column in the `Hospital_Branch` table to ensure data integrity.
- The combination of `PatientID`, `RoomID`, and `AdmitDate` has the `UNIQUE KEY` constraint applied to prevent duplicate hospital stays for the same patient.

### Billing Table
The `Billing` table includes:

- `BillID`, which specifies the unique ID for each billing record as an `INT UNSIGNED`. This column has the `PRIMARY KEY` constraint applied, ensuring that each billing record is uniquely identified.
- `PatientID`, which is the ID of the patient being billed as an `INT`. This column has the `NOT NULL` constraint and the `FOREIGN KEY` constraint applied, referencing the `PatientID` column in the `Patient` table to ensure data integrity.
- `TotalAmount`, which specifies the total amount billed as a `DECIMAL(10, 2)`. This column has the `NOT NULL` constraint applied.
- `PaymentDate`, which specifies the date of payment as a `DATE`. This column has the `NOT NULL` constraint applied.
- `PaymentMethod`, which specifies the method of payment as a `VARCHAR(50)`. This column has the `NOT NULL` constraint applied.
- `Branch_ID`, which is the ID of the branch where the billing record was created as a `TINYINT UNSIGNED`. This column has the `NOT NULL` constraint and the `FOREIGN KEY` constraint applied, referencing the `Branch_ID` column in the `Hospital_Branch` table to ensure data integrity.
- The combination of `PatientID` and `PaymentDate` has the `UNIQUE KEY` constraint applied to prevent duplicate billing for the same patient on the same date.

### Relationships

### Relationships

The below entity relationship diagram describes the relationships among the entities in the database.

![ER Diagram](ERdiagram.png)

As detailed by the diagram:

- A hospital branch is associated with one to many departments, with each department being assigned to one and only one branch. This ensures that each department operates under a specific branch of the hospital.
- A hospital branch registers one to many patients, with each patient being registered under one and only one branch. This allows for tracking of patient management at the branch level.
- A hospital branch employs one to many doctors, with each doctor working for one and only one branch. This ensures that doctors are assigned to a specific branch for organizational purposes.
- A hospital branch employs one to many nurses, with each nurse working for one and only one branch. Similar to doctors, this ensures that nurses are assigned to a specific branch.
- A hospital branch is associated with one to many appointments, with each appointment being scheduled at one and only one branch. This allows for proper scheduling and management of appointments within a branch.
- A hospital branch is associated with one to many medical records, with each medical record being created under one and only one branch. This ensures that patient records are managed at the branch level.
- A hospital branch contains one to many rooms, with each room being located within one and only one branch. This allows for efficient room management within a branch.
- A hospital branch is associated with one to many hospital stays, with each hospital stay occurring at one and only one branch. This ensures that patient stays are tracked at the branch level.
- A hospital branch processes one to many billings, with each billing being processed under one and only one branch. This allows for proper financial management within a branch.

- A department employs one to many doctors, with each doctor being employed by one and only one department. This ensures that doctors are associated with a specific department within a branch.

- A patient schedules zero to many appointments, with each appointment being associated with one and only one patient. This allows patients to have multiple appointments, or none, depending on their needs.
- A patient has zero to many medical records, with each medical record being associated with one and only one patient. This allows patients to have multiple medical records, or none, depending on their medical history.
- A patient undergoes one to many hospital stays, with each hospital stay being associated with one and only one patient. This ensures that each patient's hospital stays are properly tracked.
- A patient receives one to many billings, with each billing being associated with one and only one patient. This ensures that each patient's financial transactions are properly tracked.

- A doctor attends zero to many appointments, with each appointment being associated with one and only one doctor. This allows doctors to have multiple appointments, or none, depending on their schedule.
- A doctor creates zero to many medical records, with each medical record being associated with one and only one doctor. This ensures that each patient's medical records are properly attributed to the doctor who provided care.

- A room accommodates zero to many hospital stays, with each hospital stay being associated with one and only one room. This ensures that room usage is properly tracked within the hospital.

- A nurse is assigned to zero to many hospital stays, with each hospital stay being associated with one and only one nurse. This ensures that patient care is properly managed by the nursing staff.


## Optimizations

### Indexes
- **Primary Keys**: All primary keys (`Branch_ID`, `DepartmentID`, `PatientID`, etc.) are indexed to ensure efficient lookups.
- **Unique Keys**: Unique constraints on critical fields like `Phone`, `Email`, `DepartmentName`, and others prevent duplicates and ensure data integrity.
  
### Views
- **No views are defined in this implementation, but could be added for simplified reporting (e.g., a consolidated view of patient history including appointments, medical records, and billing information).**

## Limitations

### Design Limitations
- **Scalability**: The current design is optimized for a single hospital with multiple branches. Scaling to a larger network of hospitals may require significant redesign.
- **Complexity**: The database covers core hospital operations but does not handle complex scenarios like advanced inventory management or integration with external systems.

### Representation Limitations
- **Granular Permissions**: The design assumes access controls are handled at the application level, not within the database. This limits the ability to enforce fine-grained access restrictions within the database itself.
- **Detailed Medical Data**: The `MedicalRecord` table is simplified and does not capture more detailed medical data such as lab results, imaging data, or prescription histories.
