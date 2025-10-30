import mysql.connector
from mysql.connector import Error

def stream_users():
    """Generator that streams rows one by one from user_data table"""
    try:
        # Connect to ALX_prodev database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',             
            password='root',
            database='ALX_prodev'
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user_data;")

            # Fetch and yield rows one by one
            for row in cursor:
                yield row

            cursor.close()
            connection.close()

    except Error as e:
        print(f"Error while streaming users: {e}")
