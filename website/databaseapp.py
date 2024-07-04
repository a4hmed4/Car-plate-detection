import streamlit as st
import pandas as pd
import mysql.connector

# Function to create a connection to the MySQL database
def connect_to_database():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="shahoda",
        database="car_plates"
    )

# Function to add data to the database
def add_data(conn, plate_number, plate_letters, car_type, car_owner, governorate, chasset_number):
    try:
        query = "INSERT INTO car_data (plate_number, plate_letters, car_type, car_owner, governorate, chasset_number) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (plate_number, plate_letters, car_type, car_owner, governorate, chasset_number)
        with conn.cursor() as cursor:
            cursor.execute(query, values)
        conn.commit()
        st.success("Data added successfully!")
    except Exception as e:
        st.error(f"Error: {e}")
        conn.rollback()

# Function to search for data in the database
def search_data(conn, search_query):
    with conn.cursor() as cursor:
        query = "SELECT * FROM car_data WHERE plate_number LIKE %s OR plate_letters LIKE %s"
        values = ('%' + search_query + '%', '%' + search_query + '%')
        cursor.execute(query, values)
        result = cursor.fetchall()
    return result

# Function to retrieve data from the database
def get_data(conn):
    with conn.cursor() as cursor:
        query = "SELECT * FROM car_data"
        cursor.execute(query)
        result = cursor.fetchall()
    return result

# Streamlit App
st.title("Car Plates Database Management")

# Connect to the database
conn = connect_to_database()

# Streamlit form to add data
st.header("Add Data to the Database")

plate_number = st.text_input("Plate Number:")
plate_letters = st.text_input("Plate Letters:")
car_type = st.text_input("Car Type:")
car_owner = st.text_input("Car Owner:")
governorate = st.text_input("Governorate:")
chasset_number = st.text_input("Chasset Number:")

if st.button("Add Data"):
    add_data(conn, plate_number, plate_letters, car_type, car_owner, governorate, chasset_number)

# Streamlit search form
st.header("Search Data in the Database")
search_query = st.text_input("Search by Plate Number or Letters:")
if st.button("Search"):
    search_result = search_data(conn, search_query)
    st.header("Search Results:")
    if not search_result:
        st.info("No matching records found.")
    else:
        for record in search_result:
            st.text(f"ID: {record[0]}, Plate Number: {record[1]}, Plate Letters: {record[2]}, Car Type: {record[3]}, Car Owner: {record[4]}, Governorate: {record[5]}, Chasset Number: {record[6]}")

# Display current data in the database
st.header("Current Data in the Database")
result = get_data(conn)
df = pd.DataFrame(result, columns=["ID", "Plate Number", "Plate Letters", "Car Type", "Car Owner", "Governorate", "Chasset Number"])
st.dataframe(df)

# Close the database connection
conn.close()

