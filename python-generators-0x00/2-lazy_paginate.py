#!/usr/bin/python3
import seed


def paginate_users(page_size, offset):
    """
    Fetch a single page of users from the database.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Generator function to lazily fetch paginated user data.
    Fetches the next page only when needed.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:  # stop when no more records are found
            break
        yield page
        offset += page_size
