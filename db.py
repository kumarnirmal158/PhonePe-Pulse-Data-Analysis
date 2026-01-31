import sqlite3
import streamlit as st

@st.cache_resource
def get_connection():
    return sqlite3.connect("Phonepe_project.db", check_same_thread=False)
