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
user_prompt = st.text_area("Enter the records")
if user_prompt:
    

    # Send user input to Gemini Pro with a promptduplicate
    prompt = """From the above records give me the unique record based on the larger length of the name and there  count  in a table and 
    justification and also return the duplicate records which has smaller length to the unique name and there count based on the first 
    name if already exists increase count in a nice table . The unique records and duplictes records should always be in table only
    
    Example:
    I am expecting response like below
    Input:
    First Name	Last Name	Mail	Role	   Address     Zip-code
    Amelia		Rose	      amelia@23 Manager	   Main St.    12345	
    Amelia.D	Rose	      amelia@23 Manager	   Main St.    12345	
    Amelia asjfjsdafsjdf		Rose	      amelia@23 Manager	   Main St.    12345

    Unique Records
    First Name	Last Name	Mail	Role	   Address     Zip-code
    Amelia asjfjsdafsjdf		Rose	      amelia@23 Manager	   Main St.    12345

    Duplicate Records
    First Name	Last Name	Mail	Role	   Address     Zip-code
    Amelia		Rose	  amelia@23 Manager	   Main St.    12345  
    Amelia.D	Rose	  amelia@23 Manager	   Main St.    12345	
    
    I want another  table with only one record that combine the  records if the first name is similar to the first name of the unique records and their 
    ocuurence.The first name should be compared to other first name unique records if it similar that the first name record is to be shown in
    the table. it should give only one record not all similar records.
    I am expecting rsponse like below:
    Example 
    input:
    First Name	Last Name	Mail	Role	   Address     Zip-code
    Amelia		Rose	      amelia@23 Manager	   Main St.    12345	
    Amelia.D	Rose	      amelia@23 Manager	   Main St.    12345
    Amelia asjfjsdafsjdf		Rose	      amelia@23 Manager	   Main St.    12345
     
    Reason:
    The provided address are valid.After analyzing the adress,its found that the name Amelia Rose,Amelia.D rose and Amelia asjfsdafsjdf likely
    refer to the same person with same adress.Thus ,they will combine under  Amelia asjfjsdafsjdf		Rose	      amelia@23 Manager	   Main St.    12345
    No overlaps with other adress in the list were noted.
    Example
    output:
    First Name	Last Name	Mail	Role	   Address     Zip-code                    count
    Amelia asjfjsdafsjdf		Rose	      amelia@23 Manager	   Main St.    12345    2
     The above is just an example.
    dont show the above name it is just an example. take the user input name which match the condition i gave above for similar records
    I also want justication for unique and duplicates records but not in the table and  the unique record justification answer it with 
    maximumm 300 words of justification and the duplicates justification should be in also 200 maximum words but not for each duplicate 
    record but not in the  table and similar records justification which being combine to one record. 
    once you generate the tables then you should display the justification.
    Justification for unique records ,duplicates records and similar records should be in one paragraph not after each of the tables of 
    unique records and duplicates records and similar records.
    The justification should always be in line not in the table
    """
    gemini_response = st.session_state.chat_session.send_message(user_prompt + prompt)

    # Display Gemini's response
    with st.chat_message("assistance"):
        st.markdown(gemini_response.text)
