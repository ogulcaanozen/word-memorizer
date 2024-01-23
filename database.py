import mysql.connector
from mysql.connector import Error
from datetime import datetime
import tkinter.messagebox as messagebox
from mysql.connector import connect, Error
import random

def close_connection(cursor, connection):
    if cursor:
        cursor.close()

    if connection and connection.is_connected():
        connection.close()

# MySQL database configuration
db_config = {
    'host': 'localhost',  # Update this with the correct host address
    'user': 'root',
    'password': 'Darkman106',
    'database': 'translating_and_practicing_app',  # Use underscore instead of hyphen
    'port': 3306  # Update this with the correct port
}


cursor = None
connection = None  # Declare connection variable outside the try block

# Establish a connection to MySQL server
try:
    connection = mysql.connector.connect(**db_config)

    # Create a cursor to execute SQL queries
    cursor = connection.cursor()

    # Create the database if it doesn't exist
    create_db_query = "CREATE DATABASE IF NOT EXISTS {}".format(db_config['database'])
    cursor.execute(create_db_query)

    # Switch to the specified database
    cursor.execute("USE {}".format(db_config['database']))

    # Create the table if it doesn't exist
    create_table_query = """
    CREATE TABLE IF NOT EXISTS words (
        id INT AUTO_INCREMENT PRIMARY KEY,
        word VARCHAR(255) NOT NULL,
        translation TEXT NOT NULL,
        entry_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_practice_date DATE,
        days_until_practice INT
    )
"""

    cursor.execute(create_table_query)

    # Commit the changes
    connection.commit()

except Error as e:
    print("Error:", e)

finally:
    close_connection(cursor, connection)

def check_if_word_exists(cursor, word):
    # Check if the word already exists in the database
    check_query = "SELECT COUNT(*) FROM words WHERE word = %s"
    cursor.execute(check_query, (word,))
    count = cursor.fetchone()[0]
    return count > 0

def save_to_database(word, translation):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Check if the word already exists
        if check_if_word_exists(cursor, word):
            messagebox.showerror(title="Word Already in Learnings", message="Warning! The word '{word}' already exists in the database.")
            return  # Exit the function if the word already exists

        # Get the current timestamp
        current_timestamp = datetime.now()

        # Insert the word, translation, entry_date, and last_practice_date into the database
        insert_query = """
        INSERT INTO words (word, translation, entry_date, last_practice_date, days_until_practice)
        VALUES (%s, %s, %s, %s, %s)
        """

        data = (word, translation, current_timestamp, current_timestamp, 1)
        cursor.execute(insert_query, data)

        # Commit the changes
        connection.commit()

    except Error as e:
        print("Error:", e)

    finally:
        close_connection(cursor, connection)


def practice_word(word_id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Get the current timestamp
        current_timestamp = datetime.now()

        # Update the last_practice_date for the specified word_id
        update_query = "UPDATE words SET last_practice_date = %s WHERE id = %s"
        data = (current_timestamp, word_id)
        cursor.execute(update_query, data)

        # Commit the changes
        connection.commit()

    except Error as e:
        print("Error:", e)

    finally:
        close_connection(cursor, connection)

def fetch_words():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Fetch all words and their meanings from the database
        fetch_query = "SELECT word, translation FROM words"
        cursor.execute(fetch_query)
        words_and_meanings = cursor.fetchall()

        return words_and_meanings

    except Error as e:
        print("Error:", e)

    finally:
        close_connection(cursor, connection)

def delete_word(word):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Delete the given word from the database
        delete_query = f"DELETE FROM words WHERE word = '{word}'"
        cursor.execute(delete_query)

        # Commit the changes
        connection.commit()

    except Error as e:
        print("Error:", e)

    finally:
        close_connection(cursor, connection)


def get_meaning_by_word(word):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Retrieve the meaning of the given word from the database
        select_query = "SELECT translation FROM words WHERE word = %s"
        cursor.execute(select_query, (word,))
        result = cursor.fetchone()

        if result:
            return result[0]  # Return the meaning
        else:
            return None  # Return None if the word is not found in the database

    except Error as e:
        print("Error:", e)

    finally:
        close_connection(cursor, connection)

def fetch_all_meanings_from_database():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Fetch all meanings from the database
        cursor.execute("SELECT translation FROM words")
        all_meanings = [result[0] for result in cursor.fetchall()]

        return all_meanings

    except Error as e:
        print("Error:", e)
        return []

    finally:
        close_connection(cursor, connection)

def fetch_expired_words():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Fetch all expired words
        cursor.execute("SELECT word FROM words WHERE CURDATE() > last_practice_date + INTERVAL days_until_practice DAY;")        
        pending_words_tuples = cursor.fetchall()

        # Process the result to extract words from tuples
        pending_words = [word_tuple[0] for word_tuple in pending_words_tuples]

        return pending_words

    except Error as e:
        print("Error:", e)
        return []

    finally:
        close_connection(cursor, connection)
    
        