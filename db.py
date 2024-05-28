# Insert sample data
#data = [
    #('Noa', 'Hernandez', '24 Maple Street', 'Detroit', 'MI', 48226),
    #('Noah', 'Hernande', '24 Maple Street', 'Detroit', 'MI', 48226),
    #('Noahh', 'Hernandez', '24 Maple Street', 'Detroit', 'MI', 48226),
#('N.', 'Hernandez', '24 Maple Street', 'Detroit', 'MI', 48226),
    #('Noah', 'Hern', '24 Maple Street', 'Detroit', 'MI', 48226),
    #('Noah Hernandez', '', '24 Maple Street', 'Detroit', 'MI', 48226),
    #('Liam', 'Johnson', '10 Elm Street', 'Chicago', 'IL', 60610),
    #('Noah Alex', 'Hernandez', '24 Maple Street', 'Detroit', 'MI', 48226),
    #('Noeh', 'Hernandez', '24 Maple Street', 'Detroit', 'MI', 48226),
    #('Noah', 'Mr. Hernandez', '24 Maple Street', 'Detroit', 'MI', 48226),
    #('Ethan', 'Miller', '5 Oak Lane', 'Austin', 'TX', 78704),
    #('Noah', 'Hernande', '24 Maple Street', 'Detroit', 'MI', 48226),
    #('David', 'Williams', '12 Main Street', 'Seattle', 'WA', 98104),
    #('Noahh', 'Hernandez', '24 Maple Street', 'Detroit', 'MI', 48226)
#]
#insert_query = "INSERT INTO test (first_name, last_name, address, city, state, zip_code) VALUES (%s, %s, %s, %s, %s, %s)"
#cursor.executemany(insert_query, data)

# Commit changes
#conn.commit()
#print("Inserted")
# Connect to MySQL
import streamlit as st
import mysql.connector
import pandas as pd

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="name"
)
cursor = conn.cursor()
# Sample data (replace with your actual data retrieval logic)
data = {
    "First Name": [
        "Amelia", "Ameliaa", "Ameila", "Am", "Amelian", "Amela", "Amel",
        "Amelia", "Amillia", "Amelya", "Amelie", "Amelia R", "Ameilaa Rose",
        "Amelia", "Am", "Ameliaa", "Amelie M", "Amelian", "Amela", "Amel",
        "Amelia Rose", "Am Ros", "Ameilaa R", "Amelie M", "Rosely R", "Amelia",
        "Ameliaa", "Ameila", "Am", "Amelian", "Amela", "Amel", "Amelia",  # Repeat for remaining entries
    ],
    "Last Name": [
        "Rose", "Rosee", "Rosse", "Ro", "Roser", "ose", "Roe", "Rose", "Rosez",
        "Rouse", "Amelie", "Rose M", "Rosse M", "Rose", "Ro", "Rosely", "Rose M",
        "Roser", "ose", "Roe", "Rose", "Roser", "Rosse M", "Rose M", "Rosely R", "Rose",
        "Rosee", "Rosse", "Ro", "Roser", "ose", "Roe", "Rose"  # Repeat for remaining entries
    ],
    "Address": ["Main St."] * 50,
    "City": ["Michigan"] * 50,
    "State": ["MS"] * 50,
    "Zip Code": ["12345"] * 50
}
# Set page configuration
st.set_page_config(
    page_title="Chat with Gemini Pro",
    page_icon=":brain:",
    layout="centered"
)

# Session
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Title
st.title("Gemini Pro chatbot")

# Display chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(message.role):
        st.markdown(message.parts[0].text)

# User input
user_prompt = st.chat_input("Ask me anything")
if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Display Gemini's response
    with st.chat_message("assistance"):
        st.markdown(gemini_response.text)

    # Check if user asked for unique data
    if "unique data" in user_prompt.lower():
        # Query for unique entries with count
        unique_query = '''SELECT first_name, last_name, address, city, state, zip_code, COUNT(*) as count
                         FROM test
                         GROUP BY first_name, last_name, address, city, state, zip_code'''
        cursor.execute(unique_query)
        unique_entries = cursor.fetchall()

        # Display unique entries with count in a spreadsheet format
        if unique_entries:
            st.subheader("Unique Entries with Count")
            unique_df = pd.DataFrame(unique_entries, columns=["First Name", "Last Name", "Address", "City", "State", "Zip Code", "Count"])
            st.dataframe(unique_df)
        else:
            st.write("No unique entries found.")

# Close connection
cursor.close()
conn.close()

