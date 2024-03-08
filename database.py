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
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tag_synonyms (
        from_tag TEXT NOT NULL,
        to_tag TEXT NOT NULL,
        creation_date INTEGER,
        last_applied_date INTEGER,
        applied_count INTEGER,
        PRIMARY KEY (from_tag, to_tag)
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

def insert_tag_synonym_data(conn, from_tag, to_tag, creation_date, last_applied_date, applied_count):
    """
    Inserts a tag synonym into the SQLite database.
    """
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO tag_synonyms (from_tag, to_tag, creation_date, last_applied_date, applied_count)
    VALUES (?, ?, ?, ?, ?)
    ON CONFLICT(from_tag, to_tag) DO UPDATE SET creation_date = excluded.creation_date, last_applied_date = excluded.last_applied_date, applied_count = excluded.applied_count
    ''', (from_tag, to_tag, creation_date, last_applied_date, applied_count))
    conn.commit()


