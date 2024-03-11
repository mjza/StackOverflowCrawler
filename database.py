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
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        account_id INTEGER PRIMARY KEY,
        reputation INTEGER,
        user_id INTEGER NOT NULL,
        user_type TEXT,
        accept_rate INTEGER,
        profile_image TEXT,
        display_name TEXT NOT NULL,
        link TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        question_id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        tags TEXT,
        owner_id INTEGER,
        is_answered BOOLEAN,
        view_count INTEGER,
        bounty_amount INTEGER,
        bounty_closes_date INTEGER,
        answer_count INTEGER,
        score INTEGER,
        last_activity_date INTEGER,
        creation_date INTEGER,
        last_edit_date INTEGER,
        content_license TEXT,
        link TEXT NOT NULL,
        body TEXT NULL,
        error BOOLEAN
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
    ON CONFLICT(name) DO UPDATE SET 
        count = excluded.count, 
        has_synonyms = excluded.has_synonyms
    ''', 
    (name, count, has_synonyms))
    conn.commit()

def insert_tag_synonym_data(conn, from_tag, to_tag, creation_date, last_applied_date, applied_count):
    """
    Inserts a tag synonym into the SQLite database.
    """
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO tag_synonyms (from_tag, to_tag, creation_date, last_applied_date, applied_count)
    VALUES (?, ?, ?, ?, ?)
    ON CONFLICT(from_tag, to_tag) DO UPDATE SET 
        creation_date = excluded.creation_date, 
        last_applied_date = excluded.last_applied_date, 
        applied_count = excluded.applied_count
    ''', 
    (from_tag, to_tag, creation_date, last_applied_date, applied_count))
    conn.commit()

def insert_user_data(conn, account_id, reputation, user_id, user_type, accept_rate, profile_image, display_name, link):
    """
    Inserts user data into the SQLite database.
    """
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO users (account_id, reputation, user_id, user_type, accept_rate, profile_image, display_name, link) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(account_id) DO UPDATE SET 
        reputation = excluded.reputation, 
        user_id = excluded.user_id, 
        user_type = excluded.user_type, 
        accept_rate = excluded.accept_rate, 
        profile_image = excluded.profile_image, 
        display_name = excluded.display_name, 
        link = excluded.link
    ''', 
    (account_id, reputation, user_id, user_type, accept_rate, profile_image, display_name, link))
    conn.commit()

def insert_question_data(conn, question_id, title, tags, owner_id, is_answered, view_count, bounty_amount, bounty_closes_date, answer_count, score, last_activity_date, creation_date, last_edit_date, content_license, link, body, error):
    """
    Inserts or updates question data into the SQLite database.
    """
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO questions (question_id, title, tags, owner_id, is_answered, view_count, bounty_amount, bounty_closes_date, answer_count, score, last_activity_date, creation_date, last_edit_date, content_license, link, body, error) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(question_id) DO UPDATE SET 
        title = excluded.title, 
        tags = excluded.tags, 
        owner_id = excluded.owner_id, 
        is_answered = excluded.is_answered, 
        view_count = excluded.view_count, 
        bounty_amount = excluded.bounty_amount, 
        bounty_closes_date = excluded.bounty_closes_date, 
        answer_count = excluded.answer_count, 
        score = excluded.score, 
        last_activity_date = excluded.last_activity_date, 
        creation_date = excluded.creation_date, 
        last_edit_date = excluded.last_edit_date, 
        content_license = excluded.content_license, 
        link = excluded.link,
        body = excluded.body,
        error = excluded.error
    ''', 
    (question_id, title, tags, owner_id, is_answered, view_count, bounty_amount, bounty_closes_date, answer_count, score, last_activity_date, creation_date, last_edit_date, content_license, link, body, error))
    conn.commit()