import streamlit as st
import mysql.connector
import pandas as pd
import requests
import home_page
import databasedesign_page
import crudoperations_page
import complexqueries_page

# --- Set the Streamlit page configuration (first Streamlit command) ---
st.set_page_config(page_title="Welcome to Hospital Management Application")

# --- Use st.secrets to get the database credentials ---
db_host = st.secrets["DB_HOST"]
db_user = st.secrets["DB_USER"]
db_password = st.secrets["DB_PASSWORD"]
db_name = st.secrets["DB_NAME"]

# Establish a connection to MySQL Server using credentials from st.secrets
mydb = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name
)
mycursor = mydb.cursor()

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({"title": title, "function": func})

    def run(self):
        st.sidebar.title("Welcome to Hospital Management Application")
        st.sidebar.markdown("## MAIN MENU")

        # Select the page to run
        app = st.sidebar.selectbox(
            "Select Page",
            self.apps,
            format_func=lambda app: app["title"]
        )
        st.sidebar.markdown("---")
        app["function"]()  # Call the selected function

# Instantiate MultiApp
app = MultiApp()

# Add apps with specific function references from the modules
app.add_app("Home Page", home_page.show_home)
app.add_app("Database Design", databasedesign_page.show_database_design)
app.add_app("CRUD Operations", crudoperations_page.show_crud_operations)
app.add_app("Complex Queries", complexqueries_page.show_complex_queries)

# Run the application
app.run()
