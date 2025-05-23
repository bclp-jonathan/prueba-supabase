# app.py

import streamlit as st
from supabase import create_client, Client

# Replace with your Supabase Project URL and anon key
SUPABASE_URL = "https://oebhpvjeewmidbhcxuqn.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9lYmhwdmplZXdtaWRiaGN4dXFuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDc5NjY3NzMsImV4cCI6MjA2MzU0Mjc3M30.LEPP0DLrmb0iYhyP6Nc-hWh1FHAGjvn0KG7mF1GJvnI"

@st.cache_resource
def init_supabase_client():
    url: str = SUPABASE_URL
    key: str = SUPABASE_KEY
    return create_client(url, key)


supabase: Client = init_supabase_client()

st.title("Supabase Table Data")

# Use the provided table names directly instead of querying information_schema
tables = ["Partidos", "Tenistas"]

def get_first_row(table_name):
    try:
        # Fetch the first row from the table
        response = supabase.from_(table_name).select('*').limit(1).execute()
        if response.data:
            return response.data[0]
        else:
            return None # Handle empty table
    except Exception as e:
        st.warning(f"Could not fetch data for table '{table_name}': {e}")
        return None

if tables:
    st.header("Tables Found:")
    for table in tables:
        st.subheader(f"Table: {table}")
        first_row = get_first_row(table)
        if first_row is not None:
            st.json(first_row) # Display the row as JSON
        else:
            st.info("Table is empty or data could not be fetched.")
else:
    # This case should not be reached with hardcoded table names unless the list is empty
    st.info("No tables specified.")
