import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai
import os
import pandas as pd
import mysql.connector
# Set page configuration
st.set_page_config(
    page_title="Chat with Gemini Pro",
    page_icon=":brain:",
    layout="centered"
)
def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="name"
    )
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel("gemini-pro")

def translate_Streamlit(user_role):
    if user_role == "model":
        return "assistance"
    else:
        return user_role

# Session
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Title
st.title("Gemini Pro chatbot")
user_prompt = st.text_input("Enter here.....")
if user_prompt:
    

    # Send user input to Gemini Pro with a promptduplicate
    prompt ='''If the user enters "Connect to database", display a message "Connected to the database successfully!". 
            Then, provide a list of all tables existing in that database.Once the user selects a table from the list,
            display the data from that table.

Example:
User: Connect to database
Gemini Pro: Connected to the database successfully! Here are the tables in the database:
1. Customers
2. Orders
3. Products
Please select a table to view its data.
'''

    gemini_response = st.session_state.chat_session.send_message(user_prompt + prompt)

    # Display Gemini's response
    with st.chat_message("assistance"):
        st.markdown(gemini_response.text)
        print(gemini_response.text)