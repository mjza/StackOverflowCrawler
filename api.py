import requests
from config import BASE_URL, PARAMS_BASE, HEADERS
from utils import extract_question_details

def fetch_questions(tags, pages=10):
    """
    Fetches questions for given tags and handles pagination.
    """
    results = []
    for page in range(1, pages + 1):
        params = PARAMS_BASE.copy()
        params['tagged'] = ';'.join(tags)
        params['page'] = page

        response = requests.get(BASE_URL, params=params)
        questions = response.json()

        for question in questions.get('items', []):
            question_url = question['link']
            url, title, body = extract_question_details(question_url, HEADERS)
            results.append((url, title, body))
    return results
