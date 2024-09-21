import streamlit as st
import mysql.connector
import re  # For email and phone validation
import pandas as pd
import datetime
import decimal
from streamlit_lottie import st_lottie
import json

db_host = st.secrets["DB_HOST"]
db_user = st.secrets["DB_USER"]
db_password = st.secrets["DB_PASSWORD"]
db_name = st.secrets["DB_NAME"]

# Function to load a Lottie animation from a file
def load_lottie_file(filepath: str):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


# Load the Lottie animation
lottie_animation_4 = load_lottie_file(r"img/department.json")

# CREATE A RECORD --------------------------------------------------------------------------------------
def create_record_in_db(table_name, data):
    try:
        # Connect to MySQL database
        mydb = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = mydb.cursor()
        # Insert statement for the "Patient" table
        if table_name == "Patient":
            query = """
                INSERT INTO Patient (FirstName, LastName, Gender, DateOfBirth, Address, Phone, Email, Branch_ID)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(
                query,
                (
                    data["FirstName"],
                    data["LastName"],
                    data["Gender"],
                    data["DateOfBirth"],
                    data["Address"],
                    data["Phone"],
                    data["Email"],
                    data["Branch_ID"],
                ),
            )

        # Insert statement for the "Hospital_Branch" table
        elif table_name == "Hospital_Branch":
            query = """
                INSERT INTO Hospital_Branch (Branch_Name, Branch_Address, Branch_Phone_Number, State, Zip_Code)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(
                query,
                (
                    data["Branch_Name"],
                    data["Branch_Address"],
                    data["Branch_Phone_Number"],
                    data["State"],
                    data["Zip_Code"],
                ),
            )

        # Insert statement for the "Department" table
        elif table_name == "Department":
            query = """
                INSERT INTO Department (DepartmentName, Location, Branch_ID)
                VALUES (%s, %s, %s)
            """
            cursor.execute(
                query, (data["DepartmentName"], data["Location"], data["Branch_ID"])
            )

        # Insert statement for the "Doctor" table
        elif table_name == "Doctor":
            query = """
                INSERT INTO Doctor (FirstName, LastName, Phone, Email, DepartmentID, Branch_ID)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(
                query,
                (
                    data["FirstName"],
                    data["LastName"],
                    data["Phone"],
                    data["Email"],
                    data["DepartmentID"],
                    data["Branch_ID"],
                ),
            )

        # Insert statement for the "Nurse" table
        elif table_name == "Nurse":
            query = """
                INSERT INTO Nurse (FirstName, LastName, Phone, Email, Branch_ID)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(
                query,
                (
                    data["FirstName"],
                    data["LastName"],
                    data["Phone"],
                    data["Email"],
                    data["Branch_ID"],
                ),
            )

        # Insert statement for the "Appointment" table
        elif table_name == "Appointment":
            query = """
                INSERT INTO Appointment (PatientID, DoctorID, AppointmentDate, AppointmentTime, ReasonForVisit, Branch_ID)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(
                query,
                (
                    data["PatientID"],
                    data["DoctorID"],
                    data["AppointmentDate"],
                    data["AppointmentTime"],
                    data["ReasonForVisit"],
                    data["Branch_ID"],
                ),
            )

        # Insert statement for the "MedicalRecord" table
        elif table_name == "MedicalRecord":
            query = """
                INSERT INTO MedicalRecord (PatientID, DoctorID, Diagnosis, Treatment, Branch_ID)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(
                query,
                (
                    data["PatientID"],
                    data["DoctorID"],
                    data["Diagnosis"],
                    data["Treatment"],
                    data["Branch_ID"],
                ),
            )

        # Insert statement for the "Room" table
        elif table_name == "Room":
            query = """
                INSERT INTO Room (RoomNumber, RoomType, Availability, Branch_ID)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(
                query,
                (
                    data["RoomNumber"],
                    data["RoomType"],
                    data["Availability"],
                    data["Branch_ID"],
                ),
            )

        # Insert statement for the "HospitalStay" table
        elif table_name == "HospitalStay":
            query = """
                INSERT INTO HospitalStay (PatientID, RoomID, AdmitDate, DischargeDate, AssignedNurseID, Branch_ID)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(
                query,
                (
                    data["PatientID"],
                    data["RoomID"],
                    data["AdmitDate"],
                    data["DischargeDate"],
                    data["AssignedNurseID"],
                    data["Branch_ID"],
                ),
            )

        # Insert statement for the "Billing" table
        elif table_name == "Billing":
            query = """
                INSERT INTO Billing (PatientID, TotalAmount, PaymentDate, PaymentMethod, Branch_ID)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(
                query,
                (
                    data["PatientID"],
                    data["TotalAmount"],
                    data["PaymentDate"],
                    data["PaymentMethod"],
                    data["Branch_ID"],
                ),
            )

        # Commit the transaction
        mydb.commit()
        st.success(f"Record successfully created in the {table_name} table.")
    except mysql.connector.Error as err:
        # Provide more detailed error messages for specific errors
        if err.errno == 1062:
            st.error(
                "Error: Duplicate entry. A record with the same unique field value already exists."
            )
        elif err.errno == 1452:
            st.error(
                "Error: Foreign key constraint fails. Make sure related records exist in the referenced table."
            )
        else:
            st.error(f"Error: {err}")
    finally:
        if mydb.is_connected():
            cursor.close()
            mydb.close()


# READ records ----------------------------------------------------------------------------------------
def read_table_from_db(table_name):
    try:
        # Connect to MySQL database
        mydb = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = mydb.cursor()
        # SQL query to read the entire table
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)

        # Fetch all rows and column names
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        # Create a DataFrame for better display in Streamlit
        df = pd.DataFrame(rows, columns=columns)

        # Display the data
        st.write(f"Displaying data from {table_name} table:")
        st.dataframe(df)

    except mysql.connector.Error as err:
        st.error(f"Error: {err}")

    finally:
        if mydb.is_connected():
            cursor.close()
            mydb.close()


# UPDATE a record ------------------------------------------------------------------------------------
def get_record_data(table_name, primary_key_column, record_id):
    try:
        # Connect to the MySQL database
        mydb = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = mydb.cursor(
            dictionary=True
        )  # Use dictionary=True to get column names with values

        # Create a dynamic query to fetch the record data
        query = f"SELECT * FROM {table_name} WHERE {primary_key_column} = %s"
        cursor.execute(query, (record_id,))
        record_data = cursor.fetchone()

        return record_data

    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return None
    finally:
        if mydb.is_connected():
            cursor.close()
            mydb.close()


def update_record_in_db(table_name, record_id, updated_data):
    if table_name == "Please choose a table":
        st_lottie(lottie_animation_4, height=300, width=300)
        return  # Exit the function early if the table is not selected
    try:
        # Connect to MySQL database
        mydb = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = mydb.cursor()

        # Update statement for the "Patient" table
        if table_name == "Patient":
            query = """
                UPDATE Patient
                SET FirstName = %s, LastName = %s, Gender = %s, DateOfBirth = %s, 
                    Address = %s, Phone = %s, Email = %s, Branch_ID = %s
                WHERE PatientID = %s
            """
            cursor.execute(
                query,
                (
                    updated_data["FirstName"],
                    updated_data["LastName"],
                    updated_data["Gender"],
                    updated_data["DateOfBirth"],
                    updated_data["Address"],
                    updated_data["Phone"],
                    updated_data["Email"],
                    updated_data["Branch_ID"],
                    record_id,
                ),
            )

        # Update statement for the "Doctor" table
        elif table_name == "Doctor":
            query = """
                UPDATE Doctor
                SET FirstName = %s, LastName = %s, Phone = %s, Email = %s, DepartmentID = %s, Branch_ID = %s
                WHERE DoctorID = %s
            """
            cursor.execute(
                query,
                (
                    updated_data["FirstName"],
                    updated_data["LastName"],
                    updated_data["Phone"],
                    updated_data["Email"],
                    updated_data["DepartmentID"],
                    updated_data["Branch_ID"],
                    record_id,
                ),
            )

        # Update statement for the "Appointment" table
        elif table_name == "Appointment":
            query = """
                UPDATE Appointment
                SET PatientID = %s, DoctorID = %s, AppointmentDate = %s, AppointmentTime = %s, ReasonForVisit = %s, Branch_ID = %s
                WHERE AppointmentID = %s
            """
            cursor.execute(
                query,
                (
                    updated_data["PatientID"],
                    updated_data["DoctorID"],
                    updated_data["AppointmentDate"],
                    updated_data["AppointmentTime"],
                    updated_data["ReasonForVisit"],
                    updated_data["Branch_ID"],
                    record_id,
                ),
            )

        # Update statement for the "Hospital_Branch" table
        elif table_name == "Hospital_Branch":
            query = """
                UPDATE Hospital_Branch
                SET Branch_Name = %s, Branch_Address = %s, Branch_Phone_Number = %s, State = %s, Zip_Code = %s
                WHERE Branch_ID = %s
            """
            cursor.execute(
                query,
                (
                    updated_data["Branch_Name"],
                    updated_data["Branch_Address"],
                    updated_data["Branch_Phone_Number"],
                    updated_data["State"],
                    updated_data["Zip_Code"],
                    record_id,
                ),
            )

        # Update statement for the "Department" table
        elif table_name == "Department":
            query = """
                UPDATE Department
                SET DepartmentName = %s, Location = %s, Branch_ID = %s
                WHERE DepartmentID = %s
            """
            cursor.execute(
                query,
                (
                    updated_data["DepartmentName"],
                    updated_data["Location"],
                    updated_data["Branch_ID"],
                    record_id,
                ),
            )

        # Update statement for the "Nurse" table
        elif table_name == "Nurse":
            query = """
                UPDATE Nurse
                SET FirstName = %s, LastName = %s, Phone = %s, Email = %s, Branch_ID = %s
                WHERE NurseID = %s
            """
            cursor.execute(
                query,
                (
                    updated_data["FirstName"],
                    updated_data["LastName"],
                    updated_data["Phone"],
                    updated_data["Email"],
                    updated_data["Branch_ID"],
                    record_id,
                ),
            )

        # Update statement for the "MedicalRecord" table
        elif table_name == "MedicalRecord":
            query = """
                UPDATE MedicalRecord
                SET PatientID = %s, DoctorID = %s, Diagnosis = %s, Treatment = %s, Branch_ID = %s
                WHERE RecordID = %s
            """
            cursor.execute(
                query,
                (
                    updated_data["PatientID"],
                    updated_data["DoctorID"],
                    updated_data["Diagnosis"],
                    updated_data["Treatment"],
                    updated_data["Branch_ID"],
                    record_id,
                ),
            )

        # Update statement for the "Room" table
        elif table_name == "Room":
            query = """
                UPDATE Room
                SET RoomNumber = %s, RoomType = %s, Availability = %s, Branch_ID = %s
                WHERE RoomID = %s
            """
            cursor.execute(
                query,
                (
                    updated_data["RoomNumber"],
                    updated_data["RoomType"],
                    updated_data["Availability"],
                    updated_data["Branch_ID"],
                    record_id,
                ),
            )

        # Update statement for the "HospitalStay" table
        elif table_name == "HospitalStay":
            query = """
                UPDATE HospitalStay
                SET PatientID = %s, RoomID = %s, AdmitDate = %s, DischargeDate = %s, AssignedNurseID = %s, Branch_ID = %s
                WHERE StayID = %s
            """
            cursor.execute(
                query,
                (
                    updated_data["PatientID"],
                    updated_data["RoomID"],
                    updated_data["AdmitDate"],
                    updated_data["DischargeDate"],
                    updated_data["AssignedNurseID"],
                    updated_data["Branch_ID"],
                    record_id,
                ),
            )

        # Update statement for the "Billing" table
        elif table_name == "Billing":
            query = """
                UPDATE Billing
                SET PatientID = %s, TotalAmount = %s, PaymentDate = %s, PaymentMethod = %s, Branch_ID = %s
                WHERE BillID = %s
            """
            cursor.execute(
                query,
                (
                    updated_data["PatientID"],
                    updated_data["TotalAmount"],
                    updated_data["PaymentDate"],
                    updated_data["PaymentMethod"],
                    updated_data["Branch_ID"],
                    record_id,
                ),
            )

        # Commit the transaction
        mydb.commit()
        st.success(f"Record in the {table_name} table successfully updated.")
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
    finally:
        if mydb.is_connected():
            cursor.close()
            mydb.close()


# DELETE a record ------------------------------------------------------------------------------------
def delete_record_in_db(table_name, record_id):
    try:
        # Connect to MySQL database
        mydb = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        cursor = mydb.cursor()

        # Define the primary keys for different tables
        primary_keys = {
            "Doctor": "DoctorID",
            "Patient": "PatientID",
            "Appointment": "AppointmentID",
            "Hospital_Branch": "Branch_ID",
            "Department": "DepartmentID",
            "Nurse": "NurseID",
            "MedicalRecord": "RecordID",
            "Room": "RoomID",
            "HospitalStay": "StayID",
            "Billing": "BillID",
        }

        # Ensure the table has a defined primary key
        if table_name in primary_keys:
            primary_key_column = primary_keys[table_name]

            # Create the delete query
            query = f"DELETE FROM {table_name} WHERE {primary_key_column} = %s"
            cursor.execute(query, (record_id,))

            # Commit the transaction
            mydb.commit()

            # Check if any rows were affected (to verify deletion)
            if cursor.rowcount > 0:
                st.success(
                    f"Record with ID {record_id} successfully deleted from the {table_name} table."
                )
            else:
                st.warning(
                    f"No record found with ID {record_id} in the {table_name} table."
                )

        else:
            st.error(
                "Invalid table selected or table does not have a defined primary key."
            )

    except mysql.connector.Error as err:
        st.error(f"Error: {err}")

    finally:
        if mydb.is_connected():
            cursor.close()
            mydb.close()


# -----------------------------------------------------------------------------------------------------


def show_crud_operations():
    # Create two columns for layout
    col1, col2 = st.columns(
        [1, 2]
    )  # Adjust the proportions as needed, left column is for Lottie

    with col1:
        # Load Lottie animation from a file
        def load_lottiefile(filepath: str):
            with open(filepath, "r") as f:
                return json.load(f)

        # Display the Lottie animation
        if lottie_animation_4:
            st_lottie(lottie_animation_4, height=230, width=230, speed=0.5)

    with col2:
        # Title and description text on the right
        st.title("CRUD Operations")
        st.write(
            "This page allows you to perform CRUD operations for the Hospital Management Application."
        )

    # Custom CSS to change the sidebar color
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"] {
            background-color: #B0E0E6;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Function to reset the selected table
    def reset_selected_table():
        st.session_state.selected_table = "Please choose a table"

    # Sidebar 1: CRUD Operations
    st.sidebar.markdown("## Select CRUD Operation")
    crud_operations = [
        "Please choose an operation",
        "Create a new record",
        "Read records",
        "Update an existing record",
        "Delete a record",
    ]

    # Use st.session_state to keep track of the selected operation
    selected_operation = st.sidebar.selectbox(
        "Choose an operation:",
        crud_operations,
        key="selected_operation",
        on_change=reset_selected_table,  # Call the reset function when the operation changes
    )

    # Sidebar 2: Table Selection
    st.sidebar.markdown("## Select Table")
    tables = [
        "Please choose a table",
        "Patient",
        "Doctor",
        "Appointment",
        "Department",
        "Hospital_Branch",
        "HospitalStay",
        "Billing",
        "Nurse",
        "Room",
        "MedicalRecord",
    ]

    # Initialize selected_table if it doesn't exist
    if "selected_table" not in st.session_state:
        st.session_state.selected_table = "Please choose a table"

    # Use st.session_state to keep track of the selected table
    selected_table = st.sidebar.selectbox(
        "Choose a table to operate on:",
        tables,
        key="selected_table",
    )

    # Create two columns to display the selected options
    col3, col4 = st.columns(2)

    with col3:
        st.write(f"**Selected Operation:** {selected_operation}")

    with col4:
        st.write(f"**Selected Table:** {selected_table}")

    # CREATE a new record in the selected table --------------------------------------------------------

    if selected_operation == "Create a new record":
        if selected_table == "Please choose a table":
            return

        # Input fields for "Patient" table
        elif selected_table == "Patient":
            st.markdown(f"### Create a new record in the {selected_table} table")
            first_name = st.text_input("First Name").capitalize()
            valid_first_name = first_name.isalpha()
            if not valid_first_name:
                st.error("First name must contain only alphabetic characters.")

            last_name = st.text_input("Last Name").capitalize()
            valid_last_name = last_name.isalpha()
            if not valid_last_name:
                st.error("Last name must contain only alphabetic characters.")

            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            date_of_birth = st.date_input("Date of Birth")
            address = st.text_input("Address")

            phone = st.text_input("Phone (Format: 123-456-7890)")
            phone_pattern = r"^\d{3}-\d{3}-\d{4}$"
            valid_phone = re.match(phone_pattern, phone) is not None
            if not valid_phone:
                st.error("Phone number must be in the format: 123-456-7890.")

            email = st.text_input("Email")
            valid_email = re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None
            if not valid_email:
                st.error("Invalid email format.")

            branch_id = st.number_input(
                "Branch ID (1 or 2)", min_value=1, max_value=2, step=1
            )

            if (
                st.button("Create Record")
                and valid_first_name
                and valid_last_name
                and valid_phone
                and valid_email
            ):
                data = {
                    "FirstName": first_name,
                    "LastName": last_name,
                    "Gender": gender,
                    "DateOfBirth": date_of_birth,
                    "Address": address,
                    "Phone": phone,
                    "Email": email,
                    "Branch_ID": branch_id,
                }
                create_record_in_db(selected_table, data)

        # Input fields for "Hospital_Branch" table
        elif selected_table == "Hospital_Branch":
            st.markdown(f"### Create a new record in the {selected_table} table")
            branch_name = st.text_input("Branch Name")
            valid_branch_name = bool(re.match(r"^[a-zA-Z\s]+$", branch_name))
            if not valid_branch_name and branch_name:
                st.error(
                    "Branch name must contain only alphabetic characters and spaces."
                )

            branch_address = st.text_input("Branch Address")
            branch_phone_number = st.text_input(
                "Branch Phone Number (Format: 123-456-7891)"
            )
            phone_pattern = r"^\d{3}-\d{3}-\d{4}$"
            valid_branch_phone_number = (
                re.match(phone_pattern, branch_phone_number) is not None
            )
            if not valid_branch_phone_number and branch_phone_number:
                st.error("Phone number must be in the format: 123-456-7891.")

            state = st.text_input("State")
            valid_state = state.isalpha() if state else False
            if not valid_state and state:
                st.error("State must contain only alphabetic characters.")

            zip_code = st.text_input("Zip Code")
            valid_zip_code = zip_code.isdigit() if zip_code else False
            if not valid_zip_code and zip_code:
                st.error("Zip code must be numeric.")

            if (
                st.button("Create Record")
                and valid_branch_name
                and valid_branch_phone_number
                and valid_state
                and valid_zip_code
            ):
                data = {
                    "Branch_Name": branch_name,
                    "Branch_Address": branch_address,
                    "Branch_Phone_Number": branch_phone_number,
                    "State": state,
                    "Zip_Code": zip_code,
                }
                create_record_in_db(selected_table, data)

        # Input fields for "Department" table
        elif selected_table == "Department":
            st.markdown(f"### Create a new record in the {selected_table} table")
            department_name = st.text_input("Department Name").upper()
            valid_department_name = bool(re.match(r"^[A-Z\s]+$", department_name))
            if not valid_department_name and department_name:
                st.error("Department name must contain only alphabetic characters.")

            location = st.text_input("Location")
            valid_location = location.isalpha() if location else False
            if not valid_location and location:
                st.error("Location must contain only alphabetic characters.")

            branch_id = st.number_input(
                "Branch ID (1 or 2)", min_value=1, max_value=2, step=1
            )

            if st.button("Create Record") and valid_department_name and valid_location:
                data = {
                    "DepartmentName": department_name,
                    "Location": location,
                    "Branch_ID": branch_id,
                }
                create_record_in_db(selected_table, data)

        # Input fields for the "Doctor" table
        elif selected_table == "Doctor":
            st.markdown(f"### Create a new record in the {selected_table} table")
            # Container for First Name
            with st.container():
                first_name = st.text_input("First Name")
                if first_name:
                    first_name = first_name.capitalize()
                valid_first_name = first_name.isalpha() if first_name else False
                if not valid_first_name and first_name:
                    st.error("First name must contain only alphabetic characters.")

            # Container for Last Name
            with st.container():
                last_name = st.text_input("Last Name")
                if last_name:
                    last_name = last_name.capitalize()
                valid_last_name = last_name.isalpha() if last_name else False
                if not valid_last_name and last_name:
                    st.error("Last name must contain only alphabetic characters.")

            # Container for Phone Number with validation
            with st.container():
                phone = st.text_input("Phone (Format: 123-456-7890)")
                phone_pattern = r"^\d{3}-\d{3}-\d{4}$"
                valid_phone = re.match(phone_pattern, phone) is not None
                if not valid_phone and phone:
                    st.error("Phone number must be in the format: 123-456-7890.")

            # Container for Email with validation
            with st.container():
                email = st.text_input("Email")
                valid_email = re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None
                if not valid_email and email:
                    st.error("Invalid email format.")

            # Container for Department ID (1 to 10)
            with st.container():
                department_id = st.number_input(
                    "Department ID (1 to 10)", min_value=1, max_value=10, step=1
                )

            # Container for Branch ID (1 or 2)
            with st.container():
                branch_id = st.number_input(
                    "Branch ID (1 or 2)", min_value=1, max_value=2, step=1
                )

            # Check if all fields are valid before allowing record creation
            if (
                st.button("Create Record")
                and valid_first_name
                and valid_last_name
                and valid_phone
                and valid_email
            ):
                data = {
                    "FirstName": first_name,
                    "LastName": last_name,
                    "Phone": phone,
                    "Email": email,
                    "DepartmentID": department_id,
                    "Branch_ID": branch_id,
                }
                # Call the function to create the record in the database
                create_record_in_db(selected_table, data)

        # Input fields for the "Nurse" table
        elif selected_table == "Nurse":
            st.markdown(f"### Create a new record in the {selected_table} table")
            # Container for First Name
            with st.container():
                first_name = st.text_input("First Name")
                if first_name:
                    first_name = first_name.capitalize()
                valid_first_name = first_name.isalpha() if first_name else False
                if not valid_first_name and first_name:
                    st.error("First name must contain only alphabetic characters.")

            # Container for Last Name
            with st.container():
                last_name = st.text_input("Last Name")
                if last_name:
                    last_name = last_name.capitalize()
                valid_last_name = last_name.isalpha() if last_name else False
                if not valid_last_name and last_name:
                    st.error("Last name must contain only alphabetic characters.")

            # Container for Phone Number with validation
            with st.container():
                phone = st.text_input("Phone (Format: 123-456-7890)")
                phone_pattern = r"^\d{3}-\d{3}-\d{4}$"
                valid_phone = re.match(phone_pattern, phone) is not None
                if not valid_phone and phone:
                    st.error("Phone number must be in the format: 123-456-7890.")

            # Container for Email with validation
            with st.container():
                email = st.text_input("Email")
                valid_email = re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None
                if not valid_email and email:
                    st.error("Invalid email format.")

            # Container for Branch ID (1 or 2)
            with st.container():
                branch_id = st.number_input(
                    "Branch ID (1 or 2)", min_value=1, max_value=2, step=1
                )

            # Check if all fields are valid before allowing record creation
            if (
                st.button("Create Record")
                and valid_first_name
                and valid_last_name
                and valid_phone
                and valid_email
            ):
                data = {
                    "FirstName": first_name,
                    "LastName": last_name,
                    "Phone": phone,
                    "Email": email,
                    "Branch_ID": branch_id,
                }
                # Call the function to create the record in the database
                create_record_in_db(selected_table, data)

        # Input fields for the "Appointment" table
        elif selected_table == "Appointment":
            st.markdown(f"### Create a new record in the {selected_table} table")
            # Container for Patient ID with validation
            with st.container():
                patient_id = st.text_input("Patient ID")
                valid_patient_id = patient_id.isdigit() and int(patient_id) > 0
                if not valid_patient_id and patient_id:
                    st.error("Patient ID must be a positive number.")

            # Container for Doctor ID with validation
            with st.container():
                doctor_id = st.text_input("Doctor ID")
                valid_doctor_id = doctor_id.isdigit() and int(doctor_id) > 0
                if not valid_doctor_id and doctor_id:
                    st.error("Doctor ID must be a positive number.")

            # Container for Appointment Date
            with st.container():
                appointment_date = st.date_input("Appointment Date")

            # Container for Appointment Time
            with st.container():
                appointment_time = st.time_input("Appointment Time")

            # Container for Reason for Visit
            with st.container():
                reason_for_visit = st.text_area("Reason for Visit")
                if not reason_for_visit.strip():
                    st.error("Reason for visit cannot be empty.")
                valid_reason = bool(reason_for_visit.strip())

            # Container for Branch ID (1 or 2)
            with st.container():
                branch_id = st.number_input(
                    "Branch ID (1 or 2)", min_value=1, max_value=2, step=1
                )

            # Check if all fields are valid before allowing record creation
            if (
                st.button("Create Record")
                and valid_patient_id
                and valid_doctor_id
                and valid_reason
            ):
                data = {
                    "PatientID": int(patient_id),
                    "DoctorID": int(doctor_id),
                    "AppointmentDate": appointment_date,
                    "AppointmentTime": appointment_time,
                    "ReasonForVisit": reason_for_visit,
                    "Branch_ID": branch_id,
                }
                # Call the function to create the record in the database
                create_record_in_db(selected_table, data)

        # Input fields for the "MedicalRecord" table
        elif selected_table == "MedicalRecord":
            st.markdown(f"### Create a new record in the {selected_table} table")
            # Container for Patient ID with validation
            with st.container():
                patient_id = st.text_input("Patient ID")
                valid_patient_id = patient_id.isdigit() and int(patient_id) > 0
                if not valid_patient_id and patient_id:
                    st.error("Patient ID must be a positive number.")

            # Container for Doctor ID with validation
            with st.container():
                doctor_id = st.text_input("Doctor ID")
                valid_doctor_id = doctor_id.isdigit() and int(doctor_id) > 0
                if not valid_doctor_id and doctor_id:
                    st.error("Doctor ID must be a positive number.")

            # Container for Diagnosis
            with st.container():
                diagnosis = st.text_area("Diagnosis")
                if not diagnosis.strip():
                    st.error("Diagnosis cannot be empty.")
                valid_diagnosis = bool(diagnosis.strip())

            # Container for Treatment
            with st.container():
                treatment = st.text_area("Treatment")
                if not treatment.strip():
                    st.error("Treatment cannot be empty.")
                valid_treatment = bool(treatment.strip())

            # Container for Branch ID (1 or 2)
            with st.container():
                branch_id = st.number_input(
                    "Branch ID (1 or 2)", min_value=1, max_value=2, step=1
                )

            # Check if all fields are valid before allowing record creation
            if (
                st.button("Create Record")
                and valid_patient_id
                and valid_doctor_id
                and valid_diagnosis
                and valid_treatment
            ):
                data = {
                    "PatientID": int(patient_id),
                    "DoctorID": int(doctor_id),
                    "Diagnosis": diagnosis,
                    "Treatment": treatment,
                    "Branch_ID": branch_id,
                }
                # Call the function to create the record in the database
                create_record_in_db(selected_table, data)

        # Input fields for the "Room" table
        elif selected_table == "Room":
            st.markdown(f"### Create a new record in the {selected_table} table")
            # Container for Room Number
            with st.container():
                room_number = st.text_input("Room Number")
                valid_room_number = bool(room_number.strip())
                if not valid_room_number:
                    st.error("Room number cannot be empty.")

            # Container for Room Type
            with st.container():
                room_type = st.text_input("Room Type")
                valid_room_type = room_type.isalpha() if room_type else False
                if not valid_room_type:
                    st.error("Room type must contain only alphabetic characters.")

            # Container for Availability
            with st.container():
                availability = st.selectbox("Availability", [True, False])

            # Container for Branch ID
            with st.container():
                branch_id = st.number_input(
                    "Branch ID (1 or 2)", min_value=1, max_value=2, step=1
                )

            # Check if all fields are valid before allowing record creation
            if st.button("Create Record") and valid_room_number and valid_room_type:
                data = {
                    "RoomNumber": room_number,
                    "RoomType": room_type,
                    "Availability": availability,
                    "Branch_ID": branch_id,
                }
                create_record_in_db(selected_table, data)

        # Input fields for the "HospitalStay" table
        elif selected_table == "HospitalStay":
            st.markdown(f"### Create a new record in the {selected_table} table")
            # Container for Patient ID with validation
            with st.container():
                patient_id = st.text_input("Patient ID")
                valid_patient_id = patient_id.isdigit() and int(patient_id) > 0
                if not valid_patient_id and patient_id:
                    st.error("Patient ID must be a positive number.")

            # Container for Room ID with validation
            with st.container():
                room_id = st.text_input("Room ID")
                valid_room_id = room_id.isdigit() and int(room_id) > 0
                if not valid_room_id and room_id:
                    st.error("Room ID must be a positive number.")

            # Container for Admit Date
            with st.container():
                admit_date = st.date_input("Admit Date")

            # Container for Discharge Date
            with st.container():
                discharge_date = st.date_input("Discharge Date")
                if discharge_date < admit_date:
                    st.error("Discharge date cannot be earlier than the admit date.")
                valid_dates = discharge_date >= admit_date

            # Container for Assigned Nurse ID with validation
            with st.container():
                assigned_nurse_id = st.text_input("Assigned Nurse ID")
                valid_nurse_id = (
                    assigned_nurse_id.isdigit() and int(assigned_nurse_id) > 0
                )
                if not valid_nurse_id and assigned_nurse_id:
                    st.error("Assigned Nurse ID must be a positive number.")

            # Container for Branch ID
            with st.container():
                branch_id = st.number_input(
                    "Branch ID (1 or 2)", min_value=1, max_value=2, step=1
                )

            # Check if all fields are valid before allowing record creation
            if (
                st.button("Create Record")
                and valid_patient_id
                and valid_room_id
                and valid_dates
                and valid_nurse_id
            ):
                data = {
                    "PatientID": int(patient_id),
                    "RoomID": int(room_id),
                    "AdmitDate": admit_date,
                    "DischargeDate": discharge_date,
                    "AssignedNurseID": int(assigned_nurse_id),
                    "Branch_ID": branch_id,
                }
                # Call the function to create the record in the database
                create_record_in_db(selected_table, data)

        # Input fields for the "Billing" table
        elif selected_table == "Billing":
            st.markdown(f"### Create a new record in the {selected_table} table")
            # Container for Patient ID with validation
            with st.container():
                patient_id = st.text_input("Patient ID")
                valid_patient_id = patient_id.isdigit() and int(patient_id) > 0
                if not valid_patient_id and patient_id:
                    st.error("Patient ID must be a positive number.")

            # Container for Total Amount with validation
            with st.container():
                total_amount = st.text_input("Total Amount")
                try:
                    total_amount = float(total_amount)
                    valid_total_amount = total_amount > 0
                    if not valid_total_amount:
                        st.error("Total amount must be a positive number.")
                except ValueError:
                    valid_total_amount = False
                    if total_amount:
                        st.error("Total amount must be a valid decimal number.")

            # Container for Payment Date
            with st.container():
                payment_date = st.date_input("Payment Date")

            # Container for Payment Method (Dropdown with four options)
            with st.container():
                payment_method = st.selectbox(
                    "Payment Method", ["Cash", "Credit", "Debit", "Insurance"]
                )
                valid_payment_method = payment_method in [
                    "Cash",
                    "Credit",
                    "Debit",
                    "Insurance",
                ]

            # Container for Branch ID
            with st.container():
                branch_id = st.number_input(
                    "Branch ID (1 or 2)", min_value=1, max_value=2, step=1
                )

            # Check if all fields are valid before allowing record creation
            if (
                st.button("Create Record")
                and valid_patient_id
                and valid_total_amount
                and valid_payment_method
            ):
                data = {
                    "PatientID": int(patient_id),
                    "TotalAmount": total_amount,
                    "PaymentDate": payment_date,
                    "PaymentMethod": payment_method,
                    "Branch_ID": branch_id,
                }
                # Call the function to create the record in the database
                create_record_in_db(selected_table, data)

    # READ records-----------------------------------------------------------------------------
    elif selected_operation == "Read records":
        if selected_table == "Please choose a table":
            return
        else:
            st.markdown(f"### Displaying records from the {selected_table} table")
            read_table_from_db(selected_table)

    # UPDATE a record---------------------------------------------------------------------------
    elif selected_operation == "Update an existing record":
        if selected_table == "Please choose a table":
            return
        else:
            st.markdown(f"### Update a record in the {selected_table} table")

            # Specify the ID of the record to update
            record_id = st.text_input(
                f"Enter the ID of the {selected_table} record to update"
            )

            # Define primary keys for different tables
            primary_keys = {
                "Doctor": "DoctorID",
                "Patient": "PatientID",
                "Appointment": "AppointmentID",
                "Hospital_Branch": "Branch_ID",
                "Department": "DepartmentID",
                "Nurse": "NurseID",
                "MedicalRecord": "RecordID",
                "Room": "RoomID",
                "HospitalStay": "StayID",
                "Billing": "BillID",
            }

            if selected_table in primary_keys and record_id:
                primary_key_column = primary_keys[selected_table]
                record_data = get_record_data(
                    selected_table, primary_key_column, record_id
                )

                if record_data:
                    if selected_table == "Doctor":
                        # Pre-populate the fields with existing doctor data
                        first_name = st.text_input(
                            "First Name", value=record_data["FirstName"]
                        ).capitalize()
                        last_name = st.text_input(
                            "Last Name", value=record_data["LastName"]
                        ).capitalize()
                        phone = st.text_input(
                            "Phone (Format: 123-456-7890)", value=record_data["Phone"]
                        )
                        email = st.text_input("Email", value=record_data["Email"])
                        department_id = st.number_input(
                            "Department ID (1 to 10)",
                            min_value=1,
                            max_value=10,
                            step=1,
                            value=record_data["DepartmentID"],
                        )
                        branch_id = st.number_input(
                            "Branch ID (1 or 2)",
                            min_value=1,
                            max_value=2,
                            step=1,
                            value=record_data["Branch_ID"],
                        )

                        if st.button("Update Record"):
                            updated_data = {
                                "FirstName": first_name,
                                "LastName": last_name,
                                "Phone": phone,
                                "Email": email,
                                "DepartmentID": department_id,
                                "Branch_ID": branch_id,
                            }
                            update_record_in_db("Doctor", record_id, updated_data)

                    elif selected_table == "Patient":
                        # Pre-populate the fields with existing patient data
                        first_name = st.text_input(
                            "First Name", value=record_data["FirstName"]
                        ).capitalize()
                        last_name = st.text_input(
                            "Last Name", value=record_data["LastName"]
                        ).capitalize()
                        gender = st.selectbox(
                            "Gender",
                            ["Male", "Female", "Other"],
                            index=["Male", "Female", "Other"].index(
                                record_data["Gender"]
                            ),
                        )
                        date_of_birth = st.date_input(
                            "Date of Birth",
                            value=pd.to_datetime(record_data["DateOfBirth"]),
                        )
                        address = st.text_input("Address", value=record_data["Address"])
                        phone = st.text_input(
                            "Phone (Format: 123-456-7890)", value=record_data["Phone"]
                        )
                        email = st.text_input("Email", value=record_data["Email"])
                        branch_id = st.number_input(
                            "Branch ID (1 or 2)",
                            min_value=1,
                            max_value=2,
                            step=1,
                            value=record_data["Branch_ID"],
                        )

                        if st.button("Update Record"):
                            updated_data = {
                                "FirstName": first_name,
                                "LastName": last_name,
                                "Gender": gender,
                                "DateOfBirth": date_of_birth,
                                "Address": address,
                                "Phone": phone,
                                "Email": email,
                                "Branch_ID": branch_id,
                            }
                            update_record_in_db("Patient", record_id, updated_data)

                    elif selected_table == "Hospital_Branch":
                        # Pre-populate the fields with existing hospital branch data
                        branch_name = st.text_input(
                            "Branch Name", value=record_data["Branch_Name"]
                        )
                        branch_address = st.text_input(
                            "Branch Address", value=record_data["Branch_Address"]
                        )
                        branch_phone_number = st.text_input(
                            "Branch Phone Number",
                            value=record_data["Branch_Phone_Number"],
                        )
                        state = st.text_input("State", value=record_data["State"])
                        zip_code = st.text_input(
                            "Zip Code", value=record_data["Zip_Code"]
                        )

                        if st.button("Update Record"):
                            updated_data = {
                                "Branch_Name": branch_name,
                                "Branch_Address": branch_address,
                                "Branch_Phone_Number": branch_phone_number,
                                "State": state,
                                "Zip_Code": zip_code,
                            }
                            update_record_in_db(
                                "Hospital_Branch", record_id, updated_data
                            )

                    elif selected_table == "Department":
                        # Pre-populate the fields with existing department data
                        department_name = st.text_input(
                            "Department Name", value=record_data["DepartmentName"]
                        )
                        location = st.text_input(
                            "Location", value=record_data["Location"]
                        )
                        branch_id = st.number_input(
                            "Branch ID", min_value=1, value=record_data["Branch_ID"]
                        )

                        if st.button("Update Record"):
                            updated_data = {
                                "DepartmentName": department_name,
                                "Location": location,
                                "Branch_ID": branch_id,
                            }
                            update_record_in_db("Department", record_id, updated_data)

                    elif selected_table == "Nurse":
                        # Pre-populate the fields with existing nurse data
                        first_name = st.text_input(
                            "First Name", value=record_data["FirstName"]
                        ).capitalize()
                        last_name = st.text_input(
                            "Last Name", value=record_data["LastName"]
                        ).capitalize()
                        phone = st.text_input(
                            "Phone (Format: 123-456-7890)", value=record_data["Phone"]
                        )
                        email = st.text_input("Email", value=record_data["Email"])
                        branch_id = st.number_input(
                            "Branch ID",
                            min_value=1,
                            max_value=2,
                            value=record_data["Branch_ID"],
                        )

                        if st.button("Update Record"):
                            updated_data = {
                                "FirstName": first_name,
                                "LastName": last_name,
                                "Phone": phone,
                                "Email": email,
                                "Branch_ID": branch_id,
                            }
                            update_record_in_db("Nurse", record_id, updated_data)

                    elif selected_table == "Appointment":
                        # Pre-populate the fields with existing appointment data
                        patient_id = st.number_input(
                            "Patient ID", min_value=1, value=record_data["PatientID"]
                        )
                        doctor_id = st.number_input(
                            "Doctor ID", min_value=1, value=record_data["DoctorID"]
                        )
                        appointment_date = st.date_input(
                            "Appointment Date",
                            value=pd.to_datetime(record_data["AppointmentDate"]),
                        )

                        # Handle the AppointmentTime conversion
                        appointment_time = record_data["AppointmentTime"]
                        if isinstance(appointment_time, pd.Timedelta):
                            # Convert Timedelta to time
                            appointment_time = (
                                pd.Timestamp("1970-01-01") + appointment_time
                            ).time()
                        elif isinstance(appointment_time, pd.Timestamp):
                            # Convert Timestamp to time
                            appointment_time = appointment_time.time()
                        elif isinstance(appointment_time, str):
                            # Convert string to time
                            appointment_time = pd.to_datetime(appointment_time).time()
                        elif not isinstance(appointment_time, datetime.time):
                            # Default to None if the type is unexpected
                            appointment_time = datetime.time(
                                7, 0
                            )  # Default to 7:00 AM if none provided

                        # Use the time input with the corrected time value and restrict time range between 7 AM and 7 PM
                        appointment_time = st.time_input(
                            "Appointment Time (7:00 AM - 7:00 PM)",
                            value=appointment_time,
                            step=60,
                        )

                        # Ensure selected time is within the 7:00 AM to 7:00 PM range
                        if appointment_time < datetime.time(
                            7, 0
                        ) or appointment_time > datetime.time(19, 0):
                            st.error(
                                "Please select a time between 7:00 AM and 7:00 PM."
                            )
                        else:
                            reason_for_visit = st.text_input(
                                "Reason for Visit", value=record_data["ReasonForVisit"]
                            )
                            branch_id = st.number_input(
                                "Branch ID",
                                min_value=1,
                                max_value=2,
                                value=record_data["Branch_ID"],
                            )

                            if st.button("Update Record"):
                                updated_data = {
                                    "PatientID": patient_id,
                                    "DoctorID": doctor_id,
                                    "AppointmentDate": appointment_date,
                                    "AppointmentTime": appointment_time,
                                    "ReasonForVisit": reason_for_visit,
                                    "Branch_ID": branch_id,
                                }
                                update_record_in_db(
                                    "Appointment", record_id, updated_data
                                )

                    elif selected_table == "MedicalRecord":
                        # Pre-populate the fields with existing medical record data
                        patient_id = st.number_input(
                            "Patient ID", min_value=1, value=record_data["PatientID"]
                        )
                        doctor_id = st.number_input(
                            "Doctor ID", min_value=1, value=record_data["DoctorID"]
                        )
                        diagnosis = st.text_area(
                            "Diagnosis", value=record_data["Diagnosis"]
                        )
                        treatment = st.text_area(
                            "Treatment", value=record_data["Treatment"]
                        )
                        branch_id = st.number_input(
                            "Branch ID",
                            min_value=1,
                            max_value=2,
                            value=record_data["Branch_ID"],
                        )

                        if st.button("Update Record"):
                            updated_data = {
                                "PatientID": patient_id,
                                "DoctorID": doctor_id,
                                "Diagnosis": diagnosis,
                                "Treatment": treatment,
                                "Branch_ID": branch_id,
                            }
                            update_record_in_db(
                                "MedicalRecord", record_id, updated_data
                            )

                    elif selected_table == "Room":
                        # Pre-populate the fields with existing room data
                        room_number = st.text_input(
                            "Room Number", value=record_data["RoomNumber"]
                        )

                        # Room type selection from predefined options
                        room_types = ["Single", "Double", "Suite", "ICU"]
                        current_room_type = record_data["RoomType"]

                        # Set the default index for the room type if it exists in the list
                        try:
                            room_type_index = room_types.index(current_room_type)
                        except ValueError:
                            room_type_index = 0  # Default to the first option if the current room type is not in the list

                        room_type = st.selectbox(
                            "Room Type", room_types, index=room_type_index
                        )

                        availability = st.selectbox(
                            "Availability",
                            [True, False],
                            index=int(record_data["Availability"]),
                        )
                        branch_id = st.number_input(
                            "Branch ID",
                            min_value=1,
                            max_value=2,
                            value=record_data["Branch_ID"],
                        )

                        if st.button("Update Record"):
                            updated_data = {
                                "RoomNumber": room_number,
                                "RoomType": room_type,
                                "Availability": availability,
                                "Branch_ID": branch_id,
                            }
                            update_record_in_db("Room", record_id, updated_data)

                    elif selected_table == "HospitalStay":
                        # Pre-populate the fields with existing hospital stay data
                        patient_id = st.number_input(
                            "Patient ID", min_value=1, value=record_data["PatientID"]
                        )
                        room_id = st.number_input(
                            "Room ID", min_value=1, value=record_data["RoomID"]
                        )
                        admit_date = st.date_input(
                            "Admit Date", value=pd.to_datetime(record_data["AdmitDate"])
                        )
                        discharge_date = st.date_input(
                            "Discharge Date",
                            value=pd.to_datetime(record_data["DischargeDate"]),
                        )
                        assigned_nurse_id = st.number_input(
                            "Assigned Nurse ID",
                            min_value=1,
                            value=record_data["AssignedNurseID"],
                        )
                        branch_id = st.number_input(
                            "Branch ID",
                            min_value=1,
                            max_value=2,
                            value=record_data["Branch_ID"],
                        )

                        if st.button("Update Record"):
                            updated_data = {
                                "PatientID": patient_id,
                                "RoomID": room_id,
                                "AdmitDate": admit_date,
                                "DischargeDate": discharge_date,
                                "AssignedNurseID": assigned_nurse_id,
                                "Branch_ID": branch_id,
                            }
                            update_record_in_db("HospitalStay", record_id, updated_data)

                    elif selected_table == "Billing":
                        # Pre-populate the fields with existing billing data
                        patient_id = st.number_input(
                            "Patient ID", min_value=1, value=record_data["PatientID"]
                        )

                        # Convert `TotalAmount` to float to ensure compatibility with `st.number_input`
                        total_amount = (
                            float(record_data["TotalAmount"])
                            if isinstance(record_data["TotalAmount"], decimal.Decimal)
                            else record_data["TotalAmount"]
                        )
                        total_amount = st.number_input(
                            "Total Amount", min_value=0.0, value=total_amount, step=0.01
                        )

                        payment_date = st.date_input(
                            "Payment Date",
                            value=pd.to_datetime(record_data["PaymentDate"]),
                        )

                        # Define possible payment methods and get the current payment method
                        payment_methods = [
                            "Credit Card",
                            "Debit Card",
                            "Cash",
                            "Insurance",
                        ]
                        current_payment_method = record_data["PaymentMethod"]

                        # Use try...except to handle cases where current_payment_method is not in payment_methods
                        try:
                            payment_method_index = payment_methods.index(
                                current_payment_method
                            )
                        except ValueError:
                            payment_method_index = 0  # Default to the first option if the value is not in the list

                        payment_method = st.selectbox(
                            "Payment Method",
                            payment_methods,
                            index=payment_method_index,
                        )

                        branch_id = st.number_input(
                            "Branch ID",
                            min_value=1,
                            max_value=2,
                            value=record_data["Branch_ID"],
                        )

                        if st.button("Update Record"):
                            updated_data = {
                                "PatientID": patient_id,
                                "TotalAmount": total_amount,
                                "PaymentDate": payment_date,
                                "PaymentMethod": payment_method,
                                "Branch_ID": branch_id,
                            }
                            update_record_in_db("Billing", record_id, updated_data)
                else:
                    st.error(f"No record found with ID: {record_id}")

    # DELETE a records ---------------------------------------------------------------------------
    elif selected_operation == "Delete a record":
        if selected_table == "Please choose a table":
            return
        else:
            st.markdown(f"### Delete a record in the {selected_table} table")

            # Specify the ID of the record to delete
            record_id = st.text_input(
                f"Enter the ID of the {selected_table} record to delete"
            )

            # Button to delete the record
            if st.button("Delete Record"):
                if record_id:
                    delete_record_in_db(selected_table, record_id)
                else:
                    st.error("Please provide a valid record ID.")
