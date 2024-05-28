import mysql.connector

# Database credentials (replace with your actual details)


# Sample data (replace with your actual data)
people_data = [
    ("Amelia", "Rose", "Main St.", "Michigan", "MS", "12345"),
    ("John", "Doe", "1st Avenue", "California", "CA", "90210"),
    ("David", "Lee", "Elm Street", "Texas", "TX", "78759"),
]

# Connect to the database
connection = mysql.connector.connect(
     host="localhost",
        user="root",
        password="root",
        database="name"
)

# Prepare the INSERT statement
sql = """INSERT INTO examine (fname, lname, address, city, state, zip_code)
           VALUES (%s, %s, %s, %s, %s, %s)"""

# Create a cursor object
cursor = connection.cursor()

for data in people_data:
    try:
        # Execute the statement with data
        cursor.execute(sql, data)
        connection.commit()
        print(f"Data inserted successfully: {data}")
    except Exception as e:
        print(f"Error inserting data: {e}")

# Close the connection
connection.close()
