import requests
from database import open_connection, close_connection, create_tables, insert_tag_data
from config import BASE_URL, PARAMS_BASE, HEADERS
from utils import extract_question_details
import time

def fetch_questions(tags, pages=10):
    """
    Fetches questions for given tags and handles pagination.
    """
    base_url = BASE_URL + 'questions'

    results = []
    for page in range(1, pages + 1):
        params = PARAMS_BASE.copy()
        params['sort'] = 'activity'
        params['tagged'] = ';'.join(tags)
        params['page'] = page

        response = requests.get(base_url, params=params)
        questions = response.json()

        for question in questions.get('items', []):
            question_url = question['link']
            url, title, body = extract_question_details(question_url, HEADERS)
            results.append((url, title, body))
    return results

def fetch_popular_tags():
    base_url = BASE_URL + 'tags'

    params = PARAMS_BASE.copy()
    params['sort'] = 'popular'    

    has_more = True

    conn = open_connection()

    create_tables(conn)
    sleep = 10
    while has_more:
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            for item in data['items']:
                # Extract relevant data
                name = item['name']
                count = item['count']
                has_synonyms = item['has_synonyms']
                
                # Insert data into the database
                insert_tag_data(conn, name, count, has_synonyms)
            
            has_more = data['has_more']
            print(f"The page {params['page']} has been done.")
            params['page'] += 1
            if sleep > 10:
                sleep /= 2
            time.sleep(sleep)
        else:
            print(response.status_code, response.text)
            sleep *= 2
            time.sleep(sleep)
            
    close_connection(conn)