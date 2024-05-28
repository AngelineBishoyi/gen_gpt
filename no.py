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
st.title("Gemini APP To Retrieve Data From Database")

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
                    if record_type.lower() == "unique":
                        # Prepare the prompt
                        prompt = f'''Generate unique records based on the data in table '{selected_table}'.Do not add justification column in
                        the table. If there are multiple records with similar first names,
                        select the one with the longest first name and have different first name and last name address,state,city and zip-code
                        only give unique records not duplicates records.
                        The table data is as follows:
                         {table_data}
                        
                        Please generate the unique records in tabular form. Do not write any note for why the duplicates records
                        are being removed.only give the Justify why its unique after the table. Do not give justification for each record in
                        the table. one paragraph for every record is enough.Dont not include and notes like the details of all the records.
                        Do not add points of detail of all records.
                          '''
                        gemini_response = st.session_state.chat_session.send_message( record_type+prompt)
                        st.write("Gemini Pro Response:")
                        st.write(gemini_response.text)
                    elif record_type.lower() == "duplicate":
                        # Prepare the prompt for generating duplicate records
                        prompt = f'''Generate duplicate records present on the data in table '{selected_table}'based only on similar first name and
                        address,state,city and zip-code are same.Do not add Justification column in the table.

                        The table data is as follows:
                        {table_data}
                        
                        Please generate the duplicate records in tabular form.only give the Justify why its duplicate after the table.Dont mention the
                        whole details of the records.Do not give justification for each record in the table. one paragraph for every record 
                        is enough.
                        Do not add points of detail of all records. 
                          '''

                        # Send the prompt to the Gemini Pro model
                        gemini_response = st.session_state.chat_session.send_message(prompt)
                        st.write("Gemini Pro Response:")
                        st.write(gemini_response.text)
    # # Prepare the prompt
    #                         prompt = f'''Unique Records:
    #                         Generate a table showing unique records from the table '{selected_table}'. If there are multiple records with similar first names,
    #                         select the one with the longest first name and also provide the count of occurrences. If any records are completely dissimilar to others
    #                         based on the first name, last name, address, city, state, and zip code, include them in the unique records along with their count.
                            
    #                         Please generate the unique records based on the provided table data.
    #                         '''

    #                         # Send the prompt to the Gemini Pro model
    #                         gemini_response = st.session_state.chat_session.send_message(prompt)
    #                         st.write("Gemini Pro Response:")
    #                         st.write(gemini_response.text)  # Print Gemini Pro's response
