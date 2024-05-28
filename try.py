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
# for message in st.session_state.chat_session.history:
#     with st.chat_message(translate_Streamlit(message.role)):
#         st.markdown(message.parts[0].text)

# User input
user_prompt = st.text_area("Enter the records")
if user_prompt:
    

    # Send user input to Gemini Pro with a promptduplicate
    prompt = """From the provided records, I want you to generate three tables:

1. Unique Records:
   Generate a table showing unique records based on the larger length of the first name. If there are multiple records with similar first names,
   select the one with the longest first name. Include the count of occurrences for each unique record. Only include records entered by the user
   in this table.if the first name of that record is not similar to other first name record then display in unique records.Only user input data not the recor in given in example

2. Duplicate Records:
    Generate a table showing duplicate records based on the smaller length of the first name compared to unique records.
    If a duplicate record has the same first name as a unique record, increase the count of the unique record instead of listing it separately.
    Please only consider records from the user provided data, not any examples.Do not display the example record.Only take out duplicates from the 
    user input records not from the example i given in the prompt.
        
3. Similar Records:
   Generate a table combining records with similar first names to those in the unique records table. Records with similar first names are those where the first name matches the unique record's first name partially or entirely. Include the count of occurrences for each similar record.
    it should have only one record which is the combination of othere similar records.There should be only one record in this table. And take
    similar record only from the user input record not from the example.
For example:

Input:
First Name  Last Name  Address       City    State  Code
Noah        Hernandez  Maple Street  Detroit  MI     48226
Noa         Hernandez  Maple Street  Detroit  MI     48226
Noah        Hernande   Maple Street  Detroit  MI     48226
Noahh       Hernandez  Maple Street  Detroit  MI     48226
N.          Hernandez  Maple Street  Detroit  MI     48226
Noah        Hern       Maple Street  Detroit  MI     48226  


Unique Records:
First Name  Last Name  Address       City    State  Code   Count
Noah        Hernandez  Maple Street  Detroit  MI     48226  1
Amelia      Gracia     Mansion Street Chicago US     23678  1

Duplicate Records:
First Name  Last Name  Address       City    State  Code   Count
Noa         Hernandez  Maple Street  Detroit  MI     48226  1
Noahh       Hernandez  Maple Street  Detroit  MI     48226  1
N.          Hernandez  Maple Street  Detroit  MI     48226  1
Noah        Hern       Maple Street  Detroit  MI     48226  1

Similar Records:
First Name  Last Name  Address       City    State  Code   Count
Noah        Hernandez   Maple Street  Detroit  MI     48226  5

Additionally, at the end provide a justification for the unique, duplicate, and similar records in one paragraph. For unique records, explain why certain records were chosen as unique. For duplicate records, explain why they were identified as duplicates. For similar records, explain the rationale behind combining them. Justifications should be concise, with a maximum of 300 words for unique records and 200 words for duplicates and similar records.
Justification should be displayed after displaying all three tables in a paragraph; I don't need separate justifications.
"""
    
    gemini_response = st.session_state.chat_session.send_message(user_prompt + prompt)

    # Display Gemini's response
    with st.chat_message("assistance"):
        st.markdown(gemini_response.text)
        print(gemini_response.text)
