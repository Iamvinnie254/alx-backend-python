#!/usr/bin/python3
import mysql.connector

def stream_users_in_batches(batch_size):
    """
    Generator that fetches users from the database in batches.
    Yields a list (batch) of user dicts.
    """
    # connect to your database
    connection = mysql.connector.connect(
        host="localhost",
        user="root",         
        password="root",        
        database="ALX_prodev" 
    )

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT user_id, name, email, age FROM user_data")

    batch = []
    for row in cursor:
        batch.append(row)
        if len(batch) == batch_size:
            yield batch
            batch = []
    # yield remaining users (if less than batch_size)
    if batch:
        yield batch

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    """
    Processes each batch to filter users over age 25.
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)
