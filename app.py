# app.py

import streamlit as st
from supabase import create_client, Client
import pandas as pd # Import pandas

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

# Use the provided table names directly
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

def get_all_tenistas_ranked():
    try:
        # Fetch all rows from Tenistas table, ordered by points descending
        # Corrected the order method arguments
        response = supabase.from_('Tenistas').select('*').order('points', 'desc').execute()
        return response.data
    except Exception as e:
        st.error(f"Error fetching Tenistas data: {e}")
        return []

# Simple mapping from country name to flag emoji
# You can expand this dictionary with more countries
country_flag_map = {
    "USA": "🇺🇸",
    "Spain": "🇪🇸",
    "France": "🇫🇷",
    "Germany": "🇩🇪",
    "UK": "🇬🇧",
    "Argentina": "🇦🇷",
    "Brazil": "🇧🇷",
    "Serbia": "🇷🇸",
    "Switzerland": "🇨🇭",
    # Add more countries as needed
}

def get_flag_emoji(country_name):
    return country_flag_map.get(country_name, "🏳️") # Default to white flag if country not in map


if tables:
    st.header("Tables Found:")
    for table in tables:
        st.subheader(f"Table: {table}")
        if table == "Tenistas":
            tenistas_data = get_all_tenistas_ranked()
            if tenistas_data:
                # Convert to pandas DataFrame for easier manipulation and display
                df = pd.DataFrame(tenistas_data)
                # Add a 'Flag' column
                if 'country' in df.columns:
                    df['Flag'] = df['country'].apply(get_flag_emoji)
                    # Optional: Reorder columns to put Flag at the beginning
                    cols = ['Flag'] + [col for col in df.columns if col != 'Flag']
                    df = df[cols]
                st.dataframe(df) # Display as a DataFrame
            else:
                st.info("No data found for Tenistas table or data could not be fetched.")
        else:
            # For other tables (like Partidos), display only the first row
            first_row = get_first_row(table)
            if first_row is not None:
                st.json(first_row) # Display the row as JSON
            else:
                st.info("Table is empty or data could not be fetched.")
else:
    st.info("No tables specified.")
