# import streamlit as st
# from dotenv import load_dotenv
# import google.generativeai as gen_ai
# import os
# import mysql.connector
# import pandas as pd
# # Set page configuration
# st.set_page_config(
#     page_title="Chat with Gemini Pro",
#     page_icon=":brain:",
#     layout="centered"
# )

# # Connect to MySQL
# conn = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="root",
#     database="name"
# )
# cursor = conn.cursor()

# load_dotenv()

# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# gen_ai.configure(api_key=GOOGLE_API_KEY)
# model = gen_ai.GenerativeModel("gemini-pro")

# def translate_Streamlit(user_role):
#     if user_role == "model":
#         return "assistance"
#     else:
#         return user_role

# # Session
# if "chat_session" not in st.session_state:
#     st.session_state.chat_session = model.start_chat(history=[])

# # Title
# st.title("Gemini Pro chatbot")

# # Display chat history
# for message in st.session_state.chat_session.history:
#     with st.chat_message(translate_Streamlit(message.role)):
#         st.markdown(message.parts[0].text)

# # User input
# user_prompt = st.chat_input("Ask me anything")
# if user_prompt:
#     st.chat_message("user").markdown(user_prompt)
#     gemini_response = st.session_state.chat_session.send_message(user_prompt)

#     # Display Gemini's response
#     with st.chat_message("assistance"):
#         st.markdown(gemini_response.text)

#     # Check if user asked for unique data
#     if "unique data" in user_prompt.lower():
#         # Query for unique entries with count
#         unique_query = '''SELECT first_name, last_name, address, city, state, zip_code, COUNT(*) as count
#                          FROM test
#                          GROUP BY first_name, last_name, address, city, state, zip_code'''
#         cursor.execute(unique_query)
#         unique_entries = cursor.fetchall()

#         # Display unique entries with count in a spreadsheet format
#         if unique_entries:
#             st.subheader("Unique Entries with Count")
#             unique_df = pd.DataFrame(unique_entries, columns=["First Name", "Last Name", "Address", "City", "State", "Zip Code", "Count"])
#             st.dataframe(unique_df)
#         else:
#             st.write("No unique entries found.")

#Close connection
#.close()
 .close()
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai
import os
import pandas as pd

# Set page configuration
st.set_page_config(
    page_title="Chat with Gemini Pro",
    page_icon=":brain:",
    layout="centered"
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

# Display chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_Streamlit(message.role)):
        st.markdown(message.parts[0].text)

# User input
user_prompt = st.chat_input("Ask me anything")
if user_prompt:
    st.chat_message("user").markdown(user_prompt)

    prompt = "Generate unique records from the above set of records"
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Display Gemini's response
    with st.chat_message("assistance"):
        st.markdown(gemini_response.text)

  