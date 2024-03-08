import requests
import sqlite3

def open_connection():
    # Defines and returns the database connection
    conn = sqlite3.connect('./db/stackoverflow_tags.db')
    return conn

def close_connection(conn):
    conn.commit()
    # Close the database connection
    conn.close()

def create_tables(conn):
    cursor = conn.cursor()
    # Create the tags table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tags (
        name TEXT NOT NULL PRIMARY KEY,
        count INTEGER NOT NULL,
        has_synonyms BOOLEAN NOT NULL
    )
    ''')
    conn.commit()

def insert_tag_data(conn, name, count, has_synonyms):
    """
    Inserts tag data into the SQLite database.
    """
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO tags (name, count, has_synonyms) VALUES (?, ?, ?)
    ON CONFLICT(name) DO UPDATE SET count = excluded.count, has_synonyms = excluded.has_synonyms
    ''', (name, count, has_synonyms))
    conn.commit()




