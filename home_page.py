import streamlit as st
from streamlit_lottie import st_lottie
import json


def load_lottie_file(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


def show_home():
    # Create two columns for layout
    left_col, right_col = st.columns(2)

    # Right column: Display header and description
    with right_col:
        right_col.markdown(" ## Welcome to LifeCare!")
        right_col.markdown(" ")
        right_col.markdown(
             " ##### LifeCare's database application efficiently manages patient records, appointments, staff, and medical resources."
        )
        right_col.markdown(" ")
        right_col.markdown("***Created by Truc Thi Thanh Vo***")

    # Left column: Display Lottie animation
    with left_col:
        lottie_filepath = r"img/globe.json"
        lottie_animation = load_lottie_file(lottie_filepath)

        if lottie_animation:
            st_lottie(lottie_animation, height=350, key="hospital_animation")

    # Create Database-Related Links in the sidebar
    st.sidebar.markdown("## Database-Related Links")
    st.sidebar.link_button(
        "LifeCare Hospital Site",
        "https://lifecarediagnostic.com/",
    )
    st.sidebar.link_button(
        "Github Page",
        "https://github.com/vtruc",
    )
    st.sidebar.markdown("---")
    st.sidebar.markdown("## Software-Related Links")
    st.sidebar.link_button(
        "Python",
        "https://www.python.org/",
    )
    st.sidebar.link_button(
        "Pandas",
        "https://pandas.pydata.org/",
    )
    st.sidebar.link_button(
        "MySQL",
        "https://www.mysql.com/",
    )
    st.sidebar.link_button(
        "Streamlit",
        "https://streamlit.io/",
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
