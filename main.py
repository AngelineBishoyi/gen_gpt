import genai
import streamlit as st
import mysql.connector
import os

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
st.title("SQL Database Explorer with Gemini Pro")

# Initial state variables
connected = False
selected_table = None

# Connect to database button
if st.button("Connect to Database"):
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
        )
        connected = True
        st.success("Connection established successfully!")
    except Exception as e:
        st.error(f"Connection failed: {e}")

if connected:
    # List tables if connected
    tables = get_tables()
    if tables:
        selected_table = st.selectbox("Select a table:", tables)

    # Display table data if a table is selected
    if selected_table:
        try:
            table_data = get_table_data(selected_table)
            st.dataframe(table_data)
        except Exception as e:
            st.error(f"Error retrieving data: {e}")

    # Natural language query input
    user_query = st.text_input("Enter your natural language query (optional)")

    if user_query:
        # Example prompt (customize based on desired behavior)
        prompt = "Write an SQL query to "

        try:
            gemini_query = get_gemini_response(prompt, user_query)
            st.write("Generated SQL query:", gemini_query)

            # Execute the generated query (optional)
            if st.button("Execute Gemini Pro Query"):
                try:
                    results = execute_query(gemini_query)
                    if results:
                        st.dataframe(results)
                    else:
                        st.info("No results found.")
                except Exception as e:
                    st.error(f"Error executing query: {e}")
        except Exception as e:
            st.error(f"Error generating query: {e}")

