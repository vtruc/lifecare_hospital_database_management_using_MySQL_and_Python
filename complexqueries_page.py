import streamlit as st
import mysql.connector
import pandas as pd
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

lottiedb3 = load_lottie_file(r"img/dbgreen.json")

def show_complex_queries():
    # Create two columns for layout
    col1, col2 = st.columns([1, 2])  

    with col1:
        # Display Lottie animation
        if lottiedb3:
            st_lottie(lottiedb3, height=270, width=270)

    with col2:
        # Right column: Title and description text
        st.title("Complex Queries")
        st.write(
            "This page allows you to run complex queries on the Hospital Management Database."
        )

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

    # Create a sidebar with 7 main categories, including "Other Query"
    categories = [
        "Please select a category",
        "Set Operations",
        "Set Membership",
        "Set Comparison",
        "Subqueries using the WITH clause",
        "Advanced Aggregate Functions",
        "OLAP",
        "Other Query",  # New option for custom queries
    ]

    selected_category = st.sidebar.selectbox("Select a category:", categories)

    if selected_category == "Please select a category":
        st.markdown(
            """
            <div style="display: flex; justify-content: center;">
                <div style="width: 300px;">
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        return  # Exit the function early if no category is selected

    # Initialize `queries` with a default value
    queries = []

    # Create a selectbox for specific queries based on the selected category
    if selected_category == "Set Operations":
        st.sidebar.markdown(
            " **Set operations** in SQL include `UNION`, `UNION ALL`, `INTERSECT`, and `EXCEPT` (or `MINUS` in some databases). These operations are used to combine the results of two or more SELECT queries."
        )
        queries = [
            "Identify Patients Who Have Either Allergies or Chronic Conditions",
            "List Patients Who Have Had an Appointment but No Medical Records",
            "Compile a List of All Medical Personnel Involved in Patient Care",
            "Identify Patients Who Have Both Inpatient and Outpatient Services",
        ]
    elif selected_category == "Set Membership":
        st.sidebar.markdown(
            " **Set membership** queries check if certain elements exist within a specified set, using `IN`, `NOT IN`, `EXISTS`, or `NOT EXISTS`."
        )
        queries = [
            "List patients who have appointments with doctors specializing in CARDIOLOGY",
            "Find Doctors Who Specialize in Digestive and Renal Health",
            "List Nurses Who Have Worked in ICU Rooms",
            "List Patients with Appointments in Multiple Departments",
            "List Doctors with No Appointments in a Specific Month",
        ]
    elif selected_category == "Set Comparison":
        st.sidebar.markdown(
            " **Set comparison**: Compares sets of rows using operations like `EXCEPT`, `INTERSECT`, or subqueries to find similarities or differences between two result sets."
        )
        queries = [
            "Find Departments That Have More Appointments Than the Average",
            "Compare Availability of Rooms Across Branches",
            "Find Nurses Who Have Not Been Assigned Any Patients Recently",
            "Identify Patients Who Have Consulted Multiple Specialists"
            "Compare Appointment Schedules to Identify Overlaps",
            "Identify Patients Who Have Changed Their Phone Numbers",
            "Identify High-Risk Patients Based on Multiple Admissions",
        ]
    elif selected_category == "Subqueries using the WITH clause":
        st.sidebar.markdown(
            " **Subquery using WITH clause**: The `WITH` clause (Common Table Expression, CTE) defines a temporary result set that can be referenced in a main query, making complex queries easier to read and maintain."
        )
        queries = [
            "Total Revenue per Branch and Department",
            "Doctors Who Treated More Patients Than the Average per Department",
            "List the Patients with the Longest Stay per Branch",
            "Total Number of Appointments per Patient Over the Last 6 Months",
            "List Nurses Who Have Assisted in More Stays Than the Average Nurse in Their Branch",
        ]
    elif selected_category == "Advanced Aggregate Functions":
        st.sidebar.markdown(
            " **Advanced aggregate function**: Includes functions like `SUM()`, `AVG()`, `COUNT()`, and window functions (`ROW_NUMBER()`, `RANK()`), used for performing calculations on sets of rows for analytical purposes."
        )
        queries = [
            "Calculate the total number of rooms available by branch",
            "Find patients who have visited multiple departments",
            "Generate a report showing total revenue per branch for the last month",
            "Total number of patients by branch and gender",
            "Calculate the total length of stay for each patient",
            "Room Availability Summary by Branch",
            "Availability by Room Type and Branch",
            "Calculate the Number of Days Since Last Appointment",
        ]
    elif selected_category == "OLAP":
        st.sidebar.markdown(
            " **OLAP**: Online Analytical Processing functions (`ROLLUP`, `CUBE`, window functions) in SQL are used for complex data analysis, allowing multidimensional views and aggregations in reports."
        )
        queries = [
            "Calculate the next payment amount for each patient",
            "Calculate the previous payment amount for each patient",
            "Total number of appointments per department with a grand total",
            "Total billing per branch with subtotals",
            "Total revenue per branch and payment method",
            "Total billing per payment method with subtotals",
            "Total Billing for Each Patient (Cumulative Sum)",
            "Rank Patients Based on Total Billing Amount in Quartiles",
            "Running Total of Appointments by Doctor",
            "Compare Ranking Methods for Billing",
            "Compare Ranking Methods for Appointment",
            "Rank doctors by the number of patients they have attended",
        ]
    elif selected_category == "Other Query":
        st.write("Write your own SQL query and execute it on the database.")
        custom_query = st.text_area("Enter your SQL query here:")
    else:
        # Handle unexpected cases
        st.warning(
            "Invalid category selected. Please choose a valid category from the sidebar."
        )
        return  # Exit the function if an invalid category is selected

    # If the "Other Query" option is selected
    if selected_category == "Other Query":
        if st.button("Run Custom Query"):
            # Execute custom query
            try:
                mydb = mysql.connector.connect(
                    host=db_host,
                    user=db_user,
                    password=db_password,
                    database=db_name
                )
                mycursor = mydb.cursor()

                mycursor.execute(custom_query)
                results = mycursor.fetchall()
                columns = [
                    desc[0] for desc in mycursor.description
                ]  # Extract column names
                df = pd.DataFrame(results, columns=columns)
                st.write(df)

            except mysql.connector.Error as err:
                st.error(f"Error: {err}")
            finally:
                if mydb.is_connected():
                    mycursor.close()
                    mydb.close()
    else:
        # Now, `queries` is always defined
        selected_query = st.selectbox("Select a query:", queries)

        # Placeholder to show the query
        st.write(f"Selected query: **{selected_query}**")

        # Database connection
        try:
            mydb = mysql.connector.connect(
                host=db_host,
                user=db_user,
                password=db_password,
                database=db_name
            )
            mycursor = mydb.cursor()

            # Execute the selected query on button click
            if st.button("Run Query"):
                # 1. set operation
                if (
                    selected_query
                    == "Identify Patients Who Have Either Allergies or Chronic Conditions"
                ):
                    query = """
                        SELECT PatientID, Diagnosis
                        FROM MedicalRecord
                        WHERE
                            Diagnosis LIKE '%Allerg%'
                        UNION
                        SELECT PatientID, Diagnosis
                        FROM MedicalRecord
                        WHERE
                            Diagnosis LIKE '%Chronic%';
                        """

                    mycursor.execute(query)
                    results = mycursor.fetchall()
                    df = pd.DataFrame(results, columns=["PatientID", "Diagnosis"])
                    st.write(df)

                    # Display the query using st.code
                    st.code(query, language="sql")

                if (
                    selected_query
                    == "List Patients Who Have Had an Appointment but No Medical Records"
                ):
                    query = """
                    SELECT PatientID
                    FROM Appointment EXCEPT
                    SELECT PatientID
                    FROM MedicalRecord;
                    """
                    mycursor.execute(query)
                    results = mycursor.fetchall()
                    df = pd.DataFrame(results, columns=["PatientID"])
                    st.write(df)

                    st.code(query, language="sql")

                if (
                    selected_query
                    == "Compile a List of All Medical Personnel Involved in Patient Care"
                ):
                    query = """
                    SELECT
                        DoctorID AS StaffID,
                        CONCAT(FirstName, ' ', LastName) AS FullName,
                        'Doctor' AS Role
                    FROM Doctor
                    WHERE
                        DoctorID IN (
                            SELECT DoctorID
                            FROM MedicalRecord
                        )
                    UNION
                    SELECT
                        NurseID AS StaffID,
                        CONCAT(FirstName, ' ', LastName) AS FullName,
                        'Nurse' AS Role
                    FROM Nurse
                    WHERE
                        NurseID IN (
                            SELECT AssignedNurseID
                            FROM HospitalStay
                        );
                    """
                    mycursor.execute(query)
                    results = mycursor.fetchall()
                    df = pd.DataFrame(results, columns=["StaffID", "FullName", "Role"])
                    st.write(df)

                    st.code(query, language="sql")

                if (
                    selected_query
                    == "Identify Patients Who Have Both Inpatient and Outpatient Services"
                ):
                    query = """
                    SELECT PatientID FROM HospitalStay
                    INTERSECT
                    SELECT PatientID FROM Appointment;
                    """
                    mycursor.execute(query)
                    results = mycursor.fetchall()
                    df = pd.DataFrame(results, columns=["PatientID"])
                    st.write(df)

                    st.code(query, language="sql")

                # 2. set membership-------------------------------------------------------------------
                if (
                    selected_query
                    == "List patients who have appointments with doctors specializing in CARDIOLOGY"
                ):
                    query = """
                    SELECT DISTINCT p.PatientID, p.FirstName, p.LastName
                    FROM Patient p
                    WHERE p.PatientID IN (
                        SELECT a.PatientID
                        FROM Appointment a
                        JOIN Doctor d ON a.DoctorID = d.DoctorID
                        WHERE d.DepartmentID = (
                            SELECT DepartmentID FROM Department WHERE DepartmentName = 'CARDIOLOGY'
                        )
                    );
                    """
                    mycursor.execute(query)
                    results = mycursor.fetchall()
                    df = pd.DataFrame(
                        results,
                        columns=[
                            "PatientID",
                            "FirstName",
                            "LastName",
                        ],
                    )
                    st.write(df)

                    st.code(query, language="sql")

                if selected_query == "-- List Nurses Who Have Worked in ICU Rooms":
                    query = """
                    SELECT DISTINCT n.NurseID, n.FirstName, n.LastName
                    FROM Nurse n
                    WHERE n.NurseID IN (
                        SELECT hs.AssignedNurseID
                        FROM HospitalStay hs
                        JOIN Room r ON hs.RoomID = r.RoomID
                        WHERE r.RoomType = 'ICU'
                    );
                    """
                    mycursor.execute(query)
                    results = mycursor.fetchall()
                    df = pd.DataFrame(
                        results,
                        columns=["NurseID", "FirstName", "LastName"],
                    )
                    st.write(df)
                    st.code(query, language="sql")

                if (
                    selected_query
                    == "Find Doctors Who Specialize in Digestive and Renal Health"
                ):
                    query = """
                    SELECT DoctorID, FirstName, LastName
                    FROM Doctor
                    WHERE DepartmentID IN (
                        SELECT DepartmentID FROM Department
                        WHERE DepartmentName IN ('GASTROENTEROLOGY', 'NEPHROLOGY', 'UROLOGY')
                    );
                    """
                    mycursor.execute(query)
                    results = mycursor.fetchall()
                    df = pd.DataFrame(
                        results, columns=["DoctorID", "FirstName", "LastName"]
                    )
                    st.write(df)
                    st.code(query, language="sql")

                if (
                    selected_query
                    == "List Patients with Appointments in Multiple Departments"
                ):
                    query = """
                    SELECT DISTINCT
                        p.PatientID,
                        CONCAT(p.FirstName, ' ', p.LastName) AS PatientName
                    FROM Patient p
                    WHERE
                        EXISTS (
                            SELECT 1
                            FROM Appointment a1
                                INNER JOIN Doctor d1 USING (DoctorID)
                            WHERE
                                p.PatientID = a1.PatientID
                                AND d1.DepartmentID != (
                                    SELECT d2.DepartmentID
                                    FROM Appointment a2
                                        INNER JOIN Doctor d2 USING (DoctorID)
                                    WHERE
                                        p.PatientID = a2.PatientID
                                    LIMIT 1
                                )
                        );
                    """
                    mycursor.execute(query)
                    results = mycursor.fetchall()
                    df = pd.DataFrame(results, columns=["PatientID", "PatientName"])
                    st.write(df)
                    st.code(query, language="sql")

                if (
                    selected_query
                    == "List Doctors with No Appointments in a Specific Month"
                ):
                    query = """
                    SELECT doc.DoctorID, CONCAT(
                            doc.FirstName, ' ', doc.LastName
                        ) AS DoctorName
                    FROM Doctor doc
                    WHERE
                        NOT EXISTS (
                            SELECT 1
                            FROM Appointment a
                            WHERE
                                a.DoctorID = doc.DoctorID
                                AND a.AppointmentDate BETWEEN '2024-10-01' AND '2024-10-30'
                        );
                    """
                    mycursor.execute(query)
                    results = mycursor.fetchall()
                    df = pd.DataFrame(results, columns=["DoctorID", "DoctorName"])
                    st.write(df)
                    st.code(query, language="sql")

                # 3. set comparision --------------------------------------------------------
                if (
                    selected_query
                    == "Find Departments That Have More Appointments Than the Average"
                ):
                    query = """
                    SELECT d.DepartmentName, COUNT(a.AppointmentID) AS TotalAppointments
                    FROM
                        Appointment a
                        INNER JOIN Doctor doc ON a.DoctorID = doc.DoctorID
                        INNER JOIN Department d ON doc.DepartmentID = d.DepartmentID
                    GROUP BY
                        d.DepartmentName
                    HAVING
                        COUNT(a.AppointmentID) > (
                            SELECT AVG(TotalAppointments)
                            FROM (
                                    SELECT COUNT(a2.AppointmentID) AS TotalAppointments
                                    FROM
                                        Appointment a2
                                        INNER JOIN Doctor doc2 ON a2.DoctorID = doc2.DoctorID
                                        INNER JOIN Department d2 ON doc2.DepartmentID = d2.DepartmentID
                                    GROUP BY
                                        d2.DepartmentName
                                ) AS DeptAppointmentCounts
                        );
                    """
                    mycursor.execute(query)
                    results = mycursor.fetchall()
                    df = pd.DataFrame(
                        results,
                        columns=[
                            "DepartmentName",
                            "TotalAppointments",
                        ],
                    )
                    st.write(df)
                    st.code(query, language="sql")

                if selected_query == "Compare Availability of Rooms Across Branches":
                    query = """
                    SELECT RoomNumber
                    FROM Room
                    WHERE Branch_ID = 1 AND Availability = TRUE
                    EXCEPT
                    SELECT RoomNumber
                    FROM Room
                    WHERE Branch_ID = 2 AND Availability = TRUE;
                    """
                    mycursor.execute(query)
                    results = mycursor.fetchall()
                    df = pd.DataFrame(results, columns=["RoomNumber"])
                    st.write(df)
                    st.code(query, language="sql")

                if (
                    selected_query
                    == "Identify Patients Who Have Consulted Multiple Specialists"
                ):
                    query = """
                    SELECT a.PatientID, COUNT(DISTINCT d.DepartmentID) AS DepartmentCount
                    FROM Appointment a
                    JOIN Doctor doc ON a.DoctorID = doc.DoctorID
                    JOIN Department d ON doc.DepartmentID = d.DepartmentID
                    GROUP BY a.PatientID
                    HAVING COUNT(DISTINCT d.DepartmentID) > 1;
                    """
                    mycursor.execute(query)
                    results = mycursor.fetchall()
                    df = pd.DataFrame(results, columns=["PatientID", "DepartmentCount"])
                    st.write(df)
                    st.code(query, language="sql")

                if (
                    selected_query
                    == "Find Nurses Who Have Not Been Assigned Any Patients Recently"
                ):
                    query = """
                    SELECT NurseID, FirstName, LastName
                    FROM Nurse
                    WHERE NurseID NOT IN (
                        SELECT AssignedNurseID FROM HospitalStay
                        WHERE AdmitDate >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
                    );
                    """
                    mycursor.execute(query)
                    results = mycursor.fetchall()
                    df = pd.DataFrame(
                        results, columns=["NurseID", "FirstName", "LastName"]
                    )
                    st.write(df)
                    st.code(query, language="sql")

                if (
                    selected_query
                    == "Compare Appointment Schedules to Identify Overlaps"
                ):
                    query = """
                    SELECT a1.DoctorID, a1.AppointmentDate, a1.AppointmentTime
                    FROM Appointment a1
                    JOIN Appointment a2 ON a1.DoctorID = a2.DoctorID
                    WHERE a1.AppointmentID <> a2.AppointmentID
                    AND a1.AppointmentDate = a2.AppointmentDate
                    AND a1.AppointmentTime = a2.AppointmentTime;
                    """
                    mycursor.execute(query)
                    results = mycursor.fetchall()
                    df = pd.DataFrame(
                        results,
                        columns=["DoctorID", "AppointmentDate", "AppointmentTime"],
                    )
                    st.write(df)
                    st.code(query, language="sql")

                if (
                    selected_query
                    == "Identify High-Risk Patients Based on Multiple Admissions"
                ):
                    query = """
                    SELECT PatientID, COUNT(*) AS AdmissionCount
                    FROM HospitalStay
                    WHERE AdmitDate >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
                    GROUP BY PatientID
                    HAVING COUNT(*) > 3;
                    """
                    mycursor.execute(query)
                    results = mycursor.fetchall()
                    df = pd.DataFrame(results, columns=["PatientID", "AdmissionCount"])
                    st.write(df)
                    st.code(query, language="sql")

                if (
                    selected_query
                    == "Identify Patients Who Have Changed Their Phone Numbers"
                ):
                    query = """
                    SELECT p.PatientID, p.FirstName, p.LastName, p.Phone AS CurrentPhone, ph.Phone AS OldPhone
                    FROM Patient p
                    JOIN PatientHistory ph ON p.PatientID = ph.PatientID
                    WHERE p.Phone <> ph.Phone;
                    """
                    mycursor.execute(query)
                    results = mycursor.fetchall()
                    df = pd.DataFrame(
                        results,
                        columns=[
                            "PatientID",
                            "FirstName",
                            "LastName",
                            "CurrentPhone",
                            "OldPhone",
                        ],
                    )
                    st.write(df)
                    st.code(query, language="sql")

                # 4. subqueries using WITH clause
                if selected_query == "Total Revenue per Branch and Department":
                    query = """
                    WITH DepartmentBilling AS (
                        SELECT
                            doc.DepartmentID,
                            hb.Branch_ID,
                            SUM(b.TotalAmount) AS TotalRevenue
                        FROM
                            Billing b
                        INNER JOIN
                            Appointment a ON b.PatientID = a.PatientID
                        INNER JOIN
                            Doctor doc ON a.DoctorID = doc.DoctorID
                        INNER JOIN
                            Hospital_Branch hb ON doc.Branch_ID = hb.Branch_ID
                        GROUP BY
                            doc.DepartmentID, hb.Branch_ID
                    )
                    SELECT
                        hb.Branch_Name,
                        d.DepartmentName,
                        db.TotalRevenue
                    FROM
                        DepartmentBilling db
                    INNER JOIN
                        Department d ON db.DepartmentID = d.DepartmentID
                    INNER JOIN
                        Hospital_Branch hb ON db.Branch_ID = hb.Branch_ID
                    ORDER BY
                        hb.Branch_Name, d.DepartmentName;
                    """
                    mycursor.execute(query)
                    results = mycursor.fetchall()
                    df = pd.DataFrame(
                        results,
                        columns=["Branch_Name", "DepartmentName", "TotalRevenue"],
                    )
                    st.write(df)
                    st.code(query, language="sql")

                if (
                    selected_query
                    == "Doctors Who Treated More Patients Than the Average per Department"
                ):
                    query = """
                    WITH DepartmentAverage AS (
                        SELECT
                            DepartmentID,
                            AVG(PatientCount) AS AvgPatients
                        FROM (
                            SELECT
                                doc.DoctorID,
                                doc.DepartmentID,
                                COUNT(DISTINCT mr.PatientID) AS PatientCount
                            FROM
                                MedicalRecord mr
                            INNER JOIN
                                Doctor doc ON mr.DoctorID = doc.DoctorID
                            GROUP BY
                                doc.DoctorID, doc.DepartmentID
                        ) AS DoctorPatientCounts
                        GROUP BY
                            DepartmentID
                    )
                    SELECT
                        doc.DoctorID,
                        CONCAT(doc.FirstName, ' ', doc.LastName) AS DoctorName,
                        d.DepartmentName,
                        COUNT(DISTINCT mr.PatientID) AS PatientsTreated
                    FROM
                        MedicalRecord mr
                    INNER JOIN
                        Doctor doc ON mr.DoctorID = doc.DoctorID
                    INNER JOIN
                        Department d ON doc.DepartmentID = d.DepartmentID
                    INNER JOIN
                        DepartmentAverage da ON doc.DepartmentID = da.DepartmentID
                    GROUP BY
                        doc.DoctorID, doc.FirstName, doc.LastName, d.DepartmentName, da.AvgPatients
                    HAVING
                        COUNT(DISTINCT mr.PatientID) > da.AvgPatients
                    ORDER BY
                        PatientsTreated DESC;

                    """
                    mycursor.execute(query)
                    results = mycursor.fetchall()
                    df = pd.DataFrame(
                        results,
                        columns=[
                            "DoctorID",
                            "DoctorName",
                            "DepartmentName",
                            "PatientsTreated",
                        ],
                    )
                    st.write(df)
                    st.code(query, language="sql")

                if (
                    selected_query
                    == "List the Patients with the Longest Stay per Branch"
                ):
                    query = """
                    WITH PatientStayLength AS (
                        SELECT
                            hs.PatientID,
                            hs.Branch_ID,
                            DATEDIFF(hs.DischargeDate, hs.AdmitDate) AS StayLength
                        FROM
                            HospitalStay hs
                    )
                    SELECT
                        hb.Branch_Name,
                        p.PatientID,
                        CONCAT(p.FirstName, ' ', p.LastName) AS PatientFullName,
                        MAX(psl.StayLength) AS LongestStay
                    FROM
                        PatientStayLength psl
                    INNER JOIN
                        Patient p ON psl.PatientID = p.PatientID
                    INNER JOIN
                        Hospital_Branch hb ON psl.Branch_ID = hb.Branch_ID
                    GROUP BY
                        hb.Branch_Name, p.PatientID, p.FirstName, p.LastName
                    ORDER BY
                        hb.Branch_Name, LongestStay DESC;
                    """
                    mycursor.execute(query)
                    results = mycursor.fetchall()
                    df = pd.DataFrame(
                        results,
                        columns=[
                            "Branch_Name",
                            "PatientID",
                            "PatientFullName",
                            "LongestStay",
                        ],
                    )
                    st.write(df)
                    st.code(query, language="sql")

                if (
                    selected_query
                    == "Total Number of Appointments per Patient Over the Last 6 Months"
                ):
                    query = """
                    WITH RecentAppointments AS (
                        SELECT
                            a.PatientID,
                            a.AppointmentDate
                        FROM
                            Appointment a
                        WHERE
                            a.AppointmentDate BETWEEN DATE_SUB(CURDATE(), INTERVAL 6 MONTH) AND CURDATE()
                    )
                    SELECT
                        p.PatientID,
                        CONCAT(p.FirstName, ' ', p.LastName) AS PatientFullName,
                        COUNT(ra.AppointmentDate) AS TotalAppointments
                    FROM
                        RecentAppointments ra
                    INNER JOIN
                        Patient p ON ra.PatientID = p.PatientID
                    GROUP BY
                        p.PatientID, p.FirstName, p.LastName
                    ORDER BY
                        TotalAppointments DESC;
                    """
                    mycursor.execute(query)
                    results = mycursor.fetchall()
                    df = pd.DataFrame(
                        results,
                        columns=["PatientID", "PatientFullName", "TotalAppointments"],
                    )
                    st.write(df)
                    st.code(query, language="sql")

                if (
                    selected_query
                    == "List Nurses Who Have Assisted in More Stays Than the Average Nurse in Their Branch"
                ):
                    query = """
                    WITH NurseStayCounts AS (
                        SELECT
                            hs.AssignedNurseID,
                            hs.Branch_ID,
                            COUNT(hs.StayID) AS StayCount
                        FROM
                            HospitalStay hs
                        GROUP BY
                            hs.AssignedNurseID, hs.Branch_ID
                    ),
                    BranchAverage AS (
                        SELECT
                            Branch_ID,
                            AVG(StayCount) AS AvgStayCount
                        FROM
                            NurseStayCounts
                        GROUP BY
                            Branch_ID
                    )
                    SELECT
                        n.NurseID,
                        CONCAT(n.FirstName, ' ', n.LastName) AS NurseName,
                        hb.Branch_Name,
                        nsc.StayCount
                    FROM
                        NurseStayCounts nsc
                    INNER JOIN
                        Nurse n ON n.NurseID = nsc.AssignedNurseID
                    INNER JOIN
                        Hospital_Branch hb ON nsc.Branch_ID = hb.Branch_ID
                    INNER JOIN
                        BranchAverage ba ON nsc.Branch_ID = ba.Branch_ID
                    WHERE
                        nsc.StayCount > ba.AvgStayCount
                    ORDER BY
                        nsc.StayCount DESC;
                    """
                    mycursor.execute(query)
                    results = mycursor.fetchall()
                    df = pd.DataFrame(
                        results,
                        columns=["NurseID", "NurseName", "Branch_Name", "StayCount"],
                    )
                    st.write(df)
                    st.code(query, language="sql")

                # 5. advanced agg
                if (
                    selected_query
                    == "Calculate the total number of rooms available by branch"
                ):
                    query = """
                    SELECT hb.Branch_Name, COUNT(r.RoomID) AS AvailableRooms
                    FROM Room r
                    INNER JOIN Hospital_Branch hb USING(Branch_ID)
                    WHERE r.Availability = TRUE
                    GROUP BY hb.Branch_Name;
                    """
                    mycursor.execute(query)
                    results = mycursor.fetchall()
                    df = pd.DataFrame(
                        results, columns=["Branch_Name", "AvailableRooms"]
                    )
                    st.write(df)
                    st.code(query, language="sql")

                if (
                    selected_query
                    == "Find patients who have visited multiple departments"
                ):
                    query = """
                    SELECT  p.PatientID, p.FirstName, p.LastName, 
                            COUNT(DISTINCT doc.DepartmentID) AS DepartmentCount
                    FROM Patient p
                    INNER JOIN Appointment a USING(PatientID)
                    INNER JOIN Doctor doc USING(DoctorID)
                    GROUP BY p.PatientID, p.FirstName, p.LastName
                    HAVING COUNT(DISTINCT doc.DepartmentID) > 1;
                    """
                    mycursor.execute(query)
                    results = mycursor.fetchall()
                    df = pd.DataFrame(
                        results,
                        columns=[
                            "PatientID",
                            "FirstName",
                            "LastName",
                            "DepartmentCount",
                        ],
                    )
                    st.write(df)
                    st.code(query, language="sql")

                if (
                    selected_query
                    == "Generate a report showing total revenue per branch for the last month"
                ):
                    query = """
                    SELECT hb.Branch_Name, SUM(b.TotalAmount) AS TotalRevenue
                    FROM Billing b
                    INNER JOIN Hospital_Branch hb USING(Branch_ID)
                    WHERE b.PaymentDate BETWEEN DATE_SUB(CURDATE(), INTERVAL 1 MONTH) AND CURDATE()
                    GROUP BY hb.Branch_Name;
                    """
                    mycursor.execute(query)
                    results = mycursor.fetchall()
                    df = pd.DataFrame(results, columns=["Branch_Name", "TotalRevenue"])
                    st.write(df)
                    st.code(query, language="sql")

                if selected_query == "Total number of patients by branch and gender":
                    query = """
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

                    """
                    mycursor.execute(query)
                    results = mycursor.fetchall()
                    df = pd.DataFrame(
                        results, columns=["Branch_Name", "Gender", "TotalPatients"]
                    )
                    st.write(df)
                    st.code(query, language="sql")

                if (
                    selected_query
                    == "Calculate the total length of stay for each patient"
                ):
                    query = """
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
                    """
                    mycursor.execute(query)
                    results = mycursor.fetchall()
                    df = pd.DataFrame(
                        results,
                        columns=["PatientID", "PatientFullName", "TotalStayLength"],
                    )
                    st.write(df)
                    st.code(query, language="sql")

                if selected_query == "Room Availability Summary by Branch":
                    query = """
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
                    """
                    mycursor.execute(query)
                    results = mycursor.fetchall()
                    df = pd.DataFrame(
                        results,
                        columns=[
                            "Branch_ID",
                            "Branch_Name",
                            "TotalRooms",
                            "AvailableRooms",
                        ],
                    )
                    st.write(df)
                    st.code(query, language="sql")

                if selected_query == "Availability by Room Type and Branch":
                    query = """
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
                    """
                    mycursor.execute(query)
                    results = mycursor.fetchall()
                    df = pd.DataFrame(
                        results,
                        columns=[
                            "RoomType",
                            "Branch_Name",
                            "TotalRooms",
                            "AvailableRooms",
                        ],
                    )
                    st.write(df)
                    st.code(query, language="sql")

                if (
                    selected_query
                    == "Calculate the Number of Days Since Last Appointment"
                ):
                    query = """
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
                    """
                    mycursor.execute(query)
                    results = mycursor.fetchall()
                    df = pd.DataFrame(
                        results,
                        columns=[
                            "PatientID",
                            "PatientFullName",
                            "LastAppointmentDate",
                            "DaysSinceLastAppointment",
                        ],
                    )
                    st.write(df)
                    st.code(query, language="sql")

                # 6. OLAP
                if (
                    selected_query
                    == "Calculate the next payment amount for each patient"
                ):
                    query = """
                    SELECT p.PatientID, p.FirstName, p.LastName, b.PaymentDate, b.TotalAmount,
                        LEAD(b.TotalAmount, 1) OVER (PARTITION BY p.PatientID ORDER BY b.PaymentDate) 
                        AS NextPaymentAmount
                    FROM Billing b
                    INNER JOIN Patient p USING(PatientID)
                    ORDER BY p.PatientID, b.PaymentDate;
                    """
                    mycursor.execute(query)
                    results = mycursor.fetchall()
                    df = pd.DataFrame(
                        results,
                        columns=[
                            "PatientID",
                            "FirstName",
                            "LastName",
                            "PaymentDate",
                            "TotalAmount",
                            "NextPaymentAmount",
                        ],
                    )
                    st.write(df)
                    st.code(query, language="sql")

                if (
                    selected_query
                    == "Calculate the previous payment amount for each patient"
                ):
                    query = """
                    SELECT p.PatientID, p.FirstName, p.LastName, b.PaymentDate, b.TotalAmount,
                        LAG(b.TotalAmount, 1) OVER (PARTITION BY p.PatientID ORDER BY b.PaymentDate) 
                        AS PreviousPaymentAmount
                    FROM Billing b
                    INNER JOIN Patient p USING(PatientID)
                    ORDER BY p.PatientID, b.PaymentDate;
                    """
                    mycursor.execute(query)
                    results = mycursor.fetchall()
                    df = pd.DataFrame(
                        results,
                        columns=[
                            "PatientID",
                            "FirstName",
                            "LastName",
                            "PaymentDate",
                            "TotalAmount",
                            "NextPaymentAmount",
                        ],
                    )
                    st.write(df)
                    st.code(query, language="sql")

                if (
                    selected_query
                    == "Total number of appointments per department with a grand total"
                ):
                    query = """
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
                    """
                    mycursor.execute(query)
                    results = mycursor.fetchall()
                    df = pd.DataFrame(
                        results, columns=["DepartmentName", "TotalAppointments"]
                    )
                    st.write(df)
                    st.code(query, language="sql")

                if selected_query == "Total billing per branch with subtotals":
                    query = """
                    SELECT
                        hb.Branch_Name,
                        SUM(b.TotalAmount) AS TotalBilling
                    FROM
                        Billing b
                    INNER JOIN
                        Hospital_Branch hb USING(Branch_ID)
                    GROUP BY
                        hb.Branch_Name WITH ROLLUP;
                    """
                    mycursor.execute(query)
                    results = mycursor.fetchall()
                    df = pd.DataFrame(results, columns=["Branch_Name", "TotalBilling"])
                    st.write(df)
                    st.code(query, language="sql")

                if selected_query == "Total revenue per branch and payment method":
                    query = """
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
                    """
                    mycursor.execute(query)
                    results = mycursor.fetchall()
                    df = pd.DataFrame(
                        results,
                        columns=["Branch_Name", "PaymentMethod", "TotalRevenue"],
                    )
                    st.write(df)
                    st.code(query, language="sql")

                if selected_query == "Total billing per payment method with subtotals":
                    query = """
                    SELECT
                        PaymentMethod,
                        SUM(TotalAmount) AS TotalBilling
                    FROM
                        Billing
                    GROUP BY
                        PaymentMethod WITH ROLLUP;
                    """
                    mycursor.execute(query)
                    results = mycursor.fetchall()
                    df = pd.DataFrame(
                        results, columns=["PaymentMethod", "TotalBilling"]
                    )
                    st.write(df)
                    st.code(query, language="sql")

                if selected_query == "Total Billing for Each Patient (Cumulative Sum)":
                    query = """
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
                    """
                    mycursor.execute(query)
                    results = mycursor.fetchall()
                    df = pd.DataFrame(
                        results,
                        columns=[
                            "PatientID",
                            "PaymentDate",
                            "TotalAmount",
                            "CumulativeTotalBilling",
                        ],
                    )
                    st.write(df)
                    st.code(query, language="sql")

                if (
                    selected_query
                    == "Rank Patients Based on Total Billing Amount in Quartiles"
                ):
                    query = """
                    SELECT
                        p.PatientID,
                        CONCAT(p.FirstName, ' ', p.LastName) AS PatientFullName,
                        SUM(b.TotalAmount) AS TotalBilling,
                        NTILE(2) OVER (ORDER BY SUM(b.TotalAmount) DESC) AS BillingNTile2,
                        NTILE(3) OVER (ORDER BY SUM(b.TotalAmount) DESC) AS BillingNTile3,
                        NTILE(4) OVER (ORDER BY SUM(b.TotalAmount) DESC) AS BillingNTile4,
                        NTILE(5) OVER (ORDER BY SUM(b.TotalAmount) DESC) AS BillingNTile5
                    FROM
                        Billing b
                    INNER JOIN
                        Patient p USING(PatientID)
                    GROUP BY
                        p.PatientID, PatientFullName
                    ORDER BY
                        TotalBilling DESC;
                    """
                    mycursor.execute(query)
                    results = mycursor.fetchall()
                    df = pd.DataFrame(
                        results,
                        columns=[
                            "PatientID",
                            "PatientFullName",
                            "TotalBilling",
                            "BillingNTile2",
                            "BillingNTile3",
                            "BillingNTile4",
                            "BillingNTile5",
                        ],
                    )
                    st.write(df)
                    st.code(query, language="sql")

                if selected_query == "Running Total of Appointments by Doctor":
                    query = """
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
                    """
                    mycursor.execute(query)
                    results = mycursor.fetchall()
                    df = pd.DataFrame(
                        results,
                        columns=[
                            "DoctorID",
                            "DoctorName",
                            "AppointmentDate",
                            "RunningTotalAppointments",
                        ],
                    )
                    st.write(df)
                    st.code(query, language="sql")

                if selected_query == "Compare Ranking Methods for Billing":
                    query = """
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
                    """
                    mycursor.execute(query)
                    results = mycursor.fetchall()
                    df = pd.DataFrame(
                        results,
                        columns=[
                            "PatientID",
                            "PatientName",
                            "TotalBilling",
                            "RankBilling",
                            "DenseRankBilling",
                        ],
                    )
                    st.write(df)
                    st.code(query, language="sql")

                if selected_query == "Compare Ranking Methods for Appointment":
                    query = """
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
                    """
                    mycursor.execute(query)
                    results = mycursor.fetchall()
                    df = pd.DataFrame(
                        results,
                        columns=[
                            "DoctorID",
                            "DoctorFullName",
                            "TotalPatients",
                            "DoctorRank",
                            "DoctorDenseRank",
                        ],
                    )
                    st.write(df)
                    st.code(query, language="sql")

                if (
                    selected_query
                    == "Rank doctors by the number of patients they have attended"
                ):
                    query = """
                    SELECT  
                        doc.DoctorID, 
                        CONCAT(doc.FirstName, ' ', doc.LastName) AS DoctorName,
                        COUNT(mr.PatientID) AS TotalPatientsAttended,
                        COUNT(DISTINCT mr.PatientID) AS UniquePatientsTreated,
                        RANK() OVER (ORDER BY COUNT(mr.PatientID) DESC) AS DoctorRank,
                        DENSE_RANK() OVER (ORDER BY COUNT(DISTINCT mr.PatientID) DESC) AS DenseDoctorRank
                    FROM 
                        Doctor doc
                    INNER JOIN 
                        MedicalRecord mr USING(DoctorID)
                    GROUP BY 
                        doc.DoctorID, doc.FirstName, doc.LastName
                    ORDER BY 
                        DoctorRank;
                    """
                    mycursor.execute(query)
                    results = mycursor.fetchall()
                    df = pd.DataFrame(
                        results,
                        columns=[
                            "DoctorID",
                            "DoctorName",
                            "TotalPatientsAttended",
                            "UniquePatientsTreated",
                            "DoctorRank",
                            "DenseDoctorRank",
                        ],
                    )
                    st.write(df)
                    st.code(query, language="sql")

                # Add other queries based on selection
                elif selected_query == "Other Query Name":
                    query = "Your SQL Query"
                    mycursor.execute(query)
                    results = mycursor.fetchall()
                    df = pd.DataFrame(results, columns=["Column1", "Column2"])
                    st.write(df)

        except mysql.connector.Error as err:
            st.error(f"Error: {err}")
        finally:
            if mydb.is_connected():
                mycursor.close()
                mydb.close()
