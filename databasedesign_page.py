import streamlit as st


def show_database_design():
    st.title("Database Design")

    st.write("By **Truc Thi Thanh Vo**")

    # Custom CSS to change the sidebar color
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            background-color: #B0E0E6;  /* Change this to your desired color */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Sidebar with the outline
    st.sidebar.title("Design Document Outline")
    st.sidebar.markdown(
        """
    - **Scope**
    - **Functional Requirements**
    - **Representation**
        - Entities (10)
        - Entity Relationship Diagram (ERD)
    - **Optimizations**
    - **Limitations**
    """
    )

    # Define colors for headers
    header_style = """
        <style>
        .header {
            color: #18b8cc; 
        }
        </style>
        """
    st.markdown(header_style, unsafe_allow_html=True)

    # Custom function to create colored headers
    def colored_header(title):
        st.markdown(f'<h2 class="header">{title}</h2>', unsafe_allow_html=True)

    # Use the custom function for headers
    colored_header("Scope")

    st.subheader("Purpose of the Database")
    st.write(
        """
    The purpose of the Hospital Management database is to manage various operational aspects of a hospital. This includes handling patient management, staff management, appointment scheduling, medical records, room allocation, and billing. The database is designed to ensure efficient data management, reduce administrative burdens, and provide easy access to critical information for both medical and administrative staff.

    Reference website: [lifecarediagnostic](https://lifecarediagnostic.com/)
    """
    )

    st.subheader("Included in the Scope")
    st.write(
        """
    - **People**: Patients, doctors, nurses, administrative staff.
    - **Places**: Hospital branches (Vertical and Horizontal), departments, rooms.
    - **Things**: Appointments, medical records, hospital stays, billing information.
    """
    )

    st.subheader("Outside the Scope")
    st.write(
        """
    - **External Entities**: Insurance companies, suppliers, third-party service providers.
    - **External Locations**: Clinics, pharmacies, other hospitals not part of the main hospital branches.
    - **Inventory Management**: Management of medical supplies, drugs, and other inventory items.
    - **Insurance Claims**: Direct handling of insurance claims or communications with insurance providers.
    """
    )

    colored_header("Functional Requirements")

    st.subheader("What Users Should Be Able to Do")
    st.write(
        """
    - **Patient Management**: Register new patients, update patient details, and track patient history.
    - **Appointment Scheduling**: Schedule, modify, or cancel appointments with doctors.
    - **Medical Records**: Record and retrieve patient diagnoses, treatments, and medical history.
    - **Room Allocation**: Allocate rooms to patients and track room availability.
    - **Hospital Stays**: Manage patient admissions, discharges, and assigned nursing staff.
    - **Billing**: Generate, update, and track billing information for patients.
    """
    )

    st.subheader("Beyond the Scope")
    st.write(
        """
    - **Inventory Management**: The database does not handle the management of medical supplies and inventory.
    - **Insurance Claims Processing**: The database does not directly handle insurance claims or communications with insurance providers.
    - **External Reporting**: Generating reports for external regulatory bodies or other hospitals is not within the scope of this database.
    """
    )

    colored_header("Representation")

    st.subheader("Entities")
    st.write("The following entities are represented in the database:")

    st.subheader("Hospital_Branch Table")
    st.write("The `Hospital_Branch` table includes:")
    st.write(
        """
    - `Branch_ID`: Unique ID for each hospital branch (`TINYINT UNSIGNED`, **Primary Key**).
    - `Branch_Name`: Name of the branch (`ENUM('Vertical', 'Horizontal')`, **NOT NULL**, **Unique**).
    - `Branch_Address`: Address of the branch (`VARCHAR(255)`, **NOT NULL**, **Unique**).
    - `Branch_Phone_Number`: Phone number of the branch (`VARCHAR(20)`, **NOT NULL**, **Unique**).
    - `State`: State where the branch is located (`VARCHAR(50)`, **NOT NULL**).
    - `Zip_Code`: Postal code for the branch (`VARCHAR(10)`, **NOT NULL**).
    """
    )

    st.subheader("Department Table")
    st.write("The `Department` table includes:")
    st.write(
        """
    - `DepartmentID`: Unique ID for each department (`TINYINT UNSIGNED`, **Primary Key**).
    - `DepartmentName`: Name of the department (e.g., 'Cardiology', 'Dermatology') (`ENUM`, **NOT NULL**, **Unique** within branch).
    - `Location`: Location within the branch (`VARCHAR(100)`, **NOT NULL**).
    - `Branch_ID`: ID of the branch (`TINYINT UNSIGNED`, **NOT NULL**, **Foreign Key** references `Hospital_Branch(Branch_ID)`).
    """
    )

    st.subheader("Patient Table")
    st.write("The `Patient` table includes:")
    st.write(
        """
    - `PatientID`: Unique ID for each patient (`INT UNSIGNED`, **Primary Key**).
    - `FirstName`: First name (`VARCHAR(50)`, **NOT NULL**).
    - `LastName`: Last name (`VARCHAR(50)`, **NOT NULL**).
    - `Gender`: Gender (`VARCHAR(10)`, **NOT NULL**).
    - `DateOfBirth`: Date of birth (`DATE`, **NOT NULL**).
    - `Address`: Address (`VARCHAR(255)`, **NOT NULL**).
    - `Phone`: Phone number (`VARCHAR(20)`, **NOT NULL**, **Unique**).
    - `Email`: Email address (`VARCHAR(100)`, **NOT NULL**, **Unique**).
    - `Branch_ID`: Registered branch (`TINYINT UNSIGNED`, **NOT NULL**, **Foreign Key** references `Hospital_Branch(Branch_ID)`).
    """
    )

    st.subheader("Doctor Table")
    st.write("The `Doctor` table includes:")
    st.write(
        """
    - `DoctorID`: Unique ID for each doctor (`TINYINT UNSIGNED`, **Primary Key**).
    - `FirstName`: First name (`VARCHAR(50)`, **NOT NULL**).
    - `LastName`: Last name (`VARCHAR(50)`, **NOT NULL**).
    - `Phone`: Phone number (`VARCHAR(20)`, **NOT NULL**, **Unique**).
    - `Email`: Email address (`VARCHAR(100)`, **NOT NULL**, **Unique**).
    - `DepartmentID`: Department ID (`TINYINT UNSIGNED`, **NOT NULL**, **Foreign Key** references `Department(DepartmentID)`).
    - `Branch_ID`: Employed branch (`TINYINT UNSIGNED`, **NOT NULL**, **Foreign Key** references `Hospital_Branch(Branch_ID)`).
    """
    )

    st.subheader("Nurse Table")
    st.write("The `Nurse` table includes:")
    st.write(
        """
    - `NurseID`: Unique ID for each nurse (`TINYINT UNSIGNED`, **Primary Key**).
    - `FirstName`: First name (`VARCHAR(50)`, **NOT NULL**).
    - `LastName`: Last name (`VARCHAR(50)`, **NOT NULL**).
    - `Phone`: Phone number (`VARCHAR(20)`, **NOT NULL**, **Unique**).
    - `Email`: Email address (`VARCHAR(100)`, **NOT NULL**, **Unique**).
    - `Branch_ID`: Employed branch (`TINYINT UNSIGNED`, **NOT NULL**, **Foreign Key** references `Hospital_Branch(Branch_ID)`).
    """
    )

    st.subheader("Appointment Table")
    st.write("The `Appointment` table includes:")
    st.write(
        """
    - `AppointmentID`: Unique ID for each appointment (`INT UNSIGNED`, **Primary Key**).
    - `PatientID`: Patient ID (`INT`, **NOT NULL**, **Foreign Key** references `Patient(PatientID)`).
    - `DoctorID`: Doctor ID (`TINYINT`, **NOT NULL**, **Foreign Key** references `Doctor(DoctorID)`).
    - `AppointmentDate`: Date of the appointment (`DATE`, **NOT NULL**).
    - `AppointmentTime`: Time of the appointment (`TIME`, **NOT NULL**).
    - `ReasonForVisit`: Reason for the appointment (`TEXT`, **NOT NULL**).
    - `Branch_ID`: Scheduled branch (`TINYINT UNSIGNED`, **NOT NULL**, **Foreign Key** references `Hospital_Branch(Branch_ID)`).
    - **Unique Constraint**: Combination of `PatientID`, `DoctorID`, `AppointmentDate`, and `AppointmentTime` to prevent double-booking.
    """
    )

    st.subheader("MedicalRecord Table")
    st.write("The `MedicalRecord` table includes:")
    st.write(
        """
    - `RecordID`: Unique ID for each medical record (`INT UNSIGNED`, **Primary Key**).
    - `PatientID`: Patient ID (`INT`, **NOT NULL**, **Foreign Key** references `Patient(PatientID)`).
    - `DoctorID`: Doctor ID (`TINYINT`, **NOT NULL**, **Foreign Key** references `Doctor(DoctorID)`).
    - `Diagnosis`: Diagnosis given (`TEXT`, **NOT NULL**).
    - `Treatment`: Treatment prescribed (`TEXT`, **NOT NULL**).
    - `DateOfEntry`: Date and time of entry (`DATETIME`, **NOT NULL**, defaults to current timestamp).
    - `Branch_ID`: Branch where record was created (`TINYINT UNSIGNED`, **NOT NULL**, **Foreign Key** references `Hospital_Branch(Branch_ID)`).
    """
    )

    st.subheader("Room Table")
    st.write("The `Room` table includes:")
    st.write(
        """
    - `RoomID`: Unique ID for each room (`INT UNSIGNED`, **Primary Key**).
    - `RoomNumber`: Room number (`VARCHAR(10)`, **NOT NULL**, **Unique**).
    - `RoomType`: Type of room (e.g., ICU, Private) (`VARCHAR(50)`, **NOT NULL**).
    - `Availability`: Room availability (`BOOLEAN`, **NOT NULL**).
    - `Branch_ID`: Branch where room is located (`TINYINT UNSIGNED`, **NOT NULL**, **Foreign Key** references `Hospital_Branch(Branch_ID)`).
    """
    )

    st.subheader("HospitalStay Table")
    st.write("The `HospitalStay` table includes:")
    st.write(
        """
    - `StayID`: Unique ID for each hospital stay (`INT UNSIGNED`, **Primary Key**).
    - `PatientID`: Patient ID (`INT`, **NOT NULL**, **Foreign Key** references `Patient(PatientID)`).
    - `RoomID`: Room ID (`INT`, **NOT NULL**, **Foreign Key** references `Room(RoomID)`).
    - `AdmitDate`: Date of admission (`DATE`, **NOT NULL**).
    - `DischargeDate`: Date of discharge (`DATE`, **NOT NULL**).
    - `AssignedNurseID`: Assigned nurse ID (`INT`, **NOT NULL**, **Foreign Key** references `Nurse(NurseID)`).
    - `Branch_ID`: Branch of stay (`TINYINT UNSIGNED`, **NOT NULL**, **Foreign Key** references `Hospital_Branch(Branch_ID)`).
    - **Unique Constraint**: Combination of `PatientID`, `RoomID`, and `AdmitDate` to prevent duplicate stays.
    """
    )

    st.subheader("Billing Table")
    st.write("The `Billing` table includes:")
    st.write(
        """
    - `BillID`: Unique ID for each billing record (`INT UNSIGNED`, **Primary Key**).
    - `PatientID`: Patient ID (`INT`, **NOT NULL**, **Foreign Key** references `Patient(PatientID)`).
    - `TotalAmount`: Total amount billed (`DECIMAL(10, 2)`, **NOT NULL**).
    - `PaymentDate`: Date of payment (`DATE`, **NOT NULL**).
    - `PaymentMethod`: Method of payment (`VARCHAR(50)`, **NOT NULL**).
    - `Branch_ID`: Branch where billing was processed (`TINYINT UNSIGNED`, **NOT NULL**, **Foreign Key** references `Hospital_Branch(Branch_ID)`).
    - **Unique Constraint**: Combination of `PatientID` and `PaymentDate` to prevent duplicate billing.
    """
    )

    st.subheader("Relationships")
    st.write(
        "The below entity relationship diagram describes the relationships among the entities in the database."
    )

    st.image("img/ERD.png", caption="ER Diagram")

    st.write("(One-to-many relationship)")
    
    colored_header("Optimizations")

    st.subheader("Indexes")
    st.write(
        """
    - **Primary Keys**: All primary keys (`Branch_ID`, `DepartmentID`, `PatientID`, etc.) are indexed to ensure efficient lookups.
    - **Unique Keys**: Unique constraints on critical fields like `Phone`, `Email`, `DepartmentName`, and others prevent duplicates and ensure data integrity.
    """
    )

    st.subheader("Views")
    st.write(
        """
    No views are defined in this implementation, but could be added for simplified reporting (e.g., a consolidated view of patient history including appointments, medical records, and billing information).
    """
    )

    colored_header("Limitations")

    st.subheader("Design Limitations")
    st.write(
        """
    - **Scalability**: The current design is optimized for a single hospital with multiple branches. Scaling to a larger network of hospitals may require significant redesign.
    - **Complexity**: The database covers core hospital operations but does not handle complex scenarios like advanced inventory management or integration with external systems.
    """
    )

    st.subheader("Representation Limitations")
    st.write(
        """
    - **Granular Permissions**: The design assumes access controls are handled at the application level, not within the database. This limits the ability to enforce fine-grained access restrictions within the database itself.
    - **Detailed Medical Data**: The `MedicalRecord` table is simplified and does not capture more detailed medical data such as lab results, imaging data, or prescription histories.
    """
    )
