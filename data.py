import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai
import os
import mysql.connector
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="Chat with Gemini Pro1",
    page_icon=":brain:",
    layout="centered"
)

# Function to establish MySQL connection
def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="name"
    )

# Function to execute SQL query and return result
def execute_query(query):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()

        return result, cursor  # Return both result and cursor
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return None, None

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel("gemini-pro")

# Session
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Title
st.title("Gemini Pro Chatbot")

# User input
user_prompt = st.text_input("Ask me anything")
if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Display Gemini's response
    # with st.empty():  
    #     st.markdown(gemini_response.text)

    # Check if user wants to connect to the database
    if "connect to database" in user_prompt.lower():
        st.write("Connected to database 'name'")
        tables, cursor = execute_query("SHOW TABLES")  # Get both result and cursor
        if tables:
            table_names = [table[0] for table in tables]
            selected_table = st.selectbox("Select a table:", table_names)
            if selected_table:
                st.markdown(f"You selected '{selected_table}'.")
                table_data, cursor = execute_query(f"SELECT * FROM {selected_table}")  # Get both result and cursor
                if table_data:
                    st.subheader(f"Data from table '{selected_table}'")
                    df = pd.DataFrame(table_data, columns=[i[0] for i in cursor.description])
                    st.table(df)

                    

                    # Add selectbox for choosing unique or duplicate records
                    record_type = st.selectbox("Select record type:", ["Unique", "Duplicate"])
                    if record_type == "Unique":
                        unique_records_query = f"SELECT first_name, last_name, address, city, state, zip_code, COUNT(*) as Count FROM {selected_table} GROUP BY first_name, last_name, address, city, state, zip_code HAVING COUNT(*) = 1"
                        unique_records, cursor = execute_query(unique_records_query)
                        if unique_records:
                            st.subheader("Unique Records")
                            unique_df = pd.DataFrame(unique_records, columns=["First Name", "Last Name", "Address", "City", "State", "Zip Code", "Count"])
                            st.table(unique_df)
                        else:
                            st.write("No unique records found.")
                    elif record_type == "Duplicate":
                        duplicate_records_query = f"SELECT first_name, last_name, address, city, state, zip_code, COUNT(*) as Count FROM {selected_table} GROUP BY first_name, last_name, address, city, state, zip_code HAVING COUNT(*) > 1"
                        duplicate_records, cursor = execute_query(duplicate_records_query)
                        if duplicate_records:
                            st.subheader("Duplicate Records")
                            duplicate_df = pd.DataFrame(duplicate_records, columns=["First Name", "Last Name", "Address", "City", "State", "Zip Code", "Count"])
                            st.table(duplicate_df)
                        else:
                            st.write("No duplicate records found.")
                else:
                    st.write(f"No data found in table '{selected_table}'.")
