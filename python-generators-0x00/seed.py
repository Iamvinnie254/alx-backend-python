import mysql.connector
from mysql.connector import Error
import csv

# Step 1: Connect to MySQL server (no specific DB yet)
def connect_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root'  # <-- change this
        )
        if connection.is_connected():
            print("Connected to MySQL server")
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")

# Step 2: Create the ALX_prodev database
def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        print("Database ALX_prodev created successfully")
    except Error as e:
        print(f"Error creating database: {e}")

# Step 3: Connect directly to ALX_prodev
def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',  # <-- change this
            database='ALX_prodev'
        )
        if connection.is_connected():
            print("Connected to ALX_prodev database")
            return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev: {e}")

# Step 4: Create user_data table
def create_table(connection):
    try:
        cursor = connection.cursor()
        query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(10, 2) NOT NULL,
            INDEX(user_id)
        );
        """
        cursor.execute(query)
        connection.commit()
        print("Table user_data created successfully")
    except Error as e:
        print(f"Error creating table: {e}")

# Step 5: Insert data from CSV
def insert_data(connection, csv_file):
    try:
        cursor = connection.cursor()
        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                cursor.execute("SELECT * FROM user_data WHERE user_id = %s", (row['user_id'],))
                result = cursor.fetchone()
                if not result:
                    insert_query = """
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute(insert_query, (row['user_id'], row['name'], row['email'], row['age']))
        connection.commit()
        print("Data inserted successfully")
    except Error as e:
        print(f"Error inserting data: {e}")

# Step 6: Generator to stream data one row at a time
def stream_user_data(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user_data;")
    while True:
        row = cursor.fetchone()
        if row is None:
            break
        yield row
    cursor.close()
