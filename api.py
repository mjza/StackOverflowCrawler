import requests
import json
from database import open_connection, close_connection, create_tables, insert_tag_data, insert_tag_synonym_data, insert_user_data, insert_question_data, insert_answer_data, get_nonexistent_question_ids, get_nonexistent_answer_ids
from config import BASE_URL, PARAMS_BASE, HEADERS
from utils import extract_question_details
import time

def fetch_questions(tags, first_page=1, last_page=0, just_new_questions = False):
    """
    Fetches questions for given tags, handles pagination, and inserts data into the database.
    """
    base_url = f"{BASE_URL}/questions"
    params = PARAMS_BASE.copy()
    params.update({
        'sort': 'activity',
        'tagged': ';'.join(tags),
        'page': first_page
    })
    
    conn = open_connection()
    create_tables(conn)

    has_more = True
    sleep = 1
    
    while has_more:
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            items = data.get('items', [])
            question_ids = [item['question_id'] for item in items if 'question_id' in item]
            new_ids = get_nonexistent_question_ids(conn, question_ids) if just_new_questions else question_ids
            for item in items:
                question_id = item.get('question_id', 0)
                answer_count = item.get('answer_count',0)
                if question_id in new_ids:
                    owner = item.get('owner', {})
                    # Fallback to 0 if 'account_id' or 'user_id' is not present
                    user_type = owner.get('user_type', '')
                    if user_type == 'registered' :
                        # Extracting remaining owner data, with default values where applicable
                        user_data = (
                            owner.get('account_id', 0), owner.get('reputation', 0),
                            owner.get('user_id', 0), owner.get('user_type', ''),
                            owner.get('accept_rate', 0), owner.get('profile_image', ''),
                            owner.get('display_name', ''), owner.get('link', '')
                        )
                        insert_user_data(conn, *user_data)                
                    
                    
                    link = item.get('link', None)    
                    
                    title, body, answers = extract_question_details(link, HEADERS, answer_count)
                    
                    error = False
                    if title != item.get('title', '') and title == "Error":
                        error = True               
                    
                    if question_id != 0:
                        # Insert question data into the questions table
                        question_data = (
                            question_id, item.get('title', title), ",".join(item.get('tags', '')), owner.get('account_id', 0), item.get('is_answered', False), 
                            item.get('view_count', 0), item.get('bounty_amount', 0), item.get('bounty_closes_date', None), answer_count, item.get('score', 0),
                            item.get('last_activity_date', 0), item.get('creation_date', 0), item.get('last_edit_date', None), item.get('content_license', None), link, body, error
                        )
                        insert_question_data(conn, *question_data)
                    # we check for any new answers        
                    if(answer_count > 0):
                        fetch_answers(question_id, answers)
            
            print(f"Page {params['page']} of questions for the tags {tags} has been processed.")
            
            has_more = data['has_more']            
            params['page'] += 1
            if(last_page != 0 and params['page'] > last_page):
                break            
            sleep = max(sleep / 2, 1)
            time.sleep(sleep)
        elif response.status_code == 400:
            error_details = json.loads(response.text)
            if error_details.get('error_name') == 'throttle_violation':
                sleep = min(sleep * 2, 60)
                print(f"Failed to fetch data due to throttle violation, retrying in {sleep} seconds...")
                time.sleep(sleep)
        else:
            print(f"Failed to fetch data: HTTP {response.status_code}, Error: {response.text}")    
            break  
            
            
def fetch_answers(question_id, answers, first_page=1, last_page=0, just_new_answers = False):
    """
    Fetches answers for a given question, handles pagination, and inserts data into the database.
    """    
    if not answers or "0" in answers:
        return
    
    base_url = f"{BASE_URL}/questions/{question_id}/answers"
    params = PARAMS_BASE.copy()
    params.update({
        'page': first_page
    })

    conn = open_connection()
    create_tables(conn)

    has_more = True
    sleep = 1

    while has_more:
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            items = data['items']
            answer_ids = [item['answer_id'] for item in items if 'answer_id' in item]
            new_ids = get_nonexistent_answer_ids(conn, answer_ids) if just_new_answers else answer_ids
            for item in items:
                answer_id = item.get('answer_id', 0)
                if answer_id in new_ids:
                    owner = item.get('owner', {})
                    user_data = (
                        owner.get('account_id', 0), owner.get('reputation', 0),
                        owner.get('user_id', 0), owner.get('user_type', ''),
                        owner.get('accept_rate', 0), owner.get('profile_image', ''),
                        owner.get('display_name', ''), owner.get('link', '')
                    )
                    insert_user_data(conn, *user_data)

                    # Fetch the answer body from somewhere, this part needs to be implemented                
                    answer_body = answers[str(answer_id)]
                    answer_error = False if answer_body else True

                    answer_data = (
                        answer_id, item.get('question_id', 0), owner.get('account_id', 0),
                        item.get('is_accepted', False), item.get('score', 0),
                        item.get('last_activity_date', 0), item.get('last_edit_date', 0),
                        item['creation_date'], item.get('content_license', ''), answer_body, answer_error
                    )
                    insert_answer_data(conn, *answer_data)            

            has_more = data.get('has_more', False)
            params['page'] += 1
            if last_page != 0 and params['page'] > last_page:
                break
            sleep = max(sleep / 2, 1)
            time.sleep(sleep)
        elif response.status_code == 400:
            error_details = json.loads(response.text)
            if error_details.get('error_name') == 'throttle_violation':
                sleep = min(sleep * 2, 60)
                print(f"Failed to fetch data due to throttle violation, retrying in {sleep} seconds...")
                time.sleep(sleep)
        else:
            print(f"Failed to fetch data: HTTP {response.status_code}, Error: {response.text}")    
            break
    # print(f"Answers of question {question_id} processed.")
    close_connection(conn)                     
    
def fetch_popular_tags(first_page=1):
    base_url = f"{BASE_URL}/tags"

    params = PARAMS_BASE.copy()
    params.update({
        'sort': 'popular',
        'page': first_page
    })     

    conn = open_connection()
    create_tables(conn)
    
    has_more = True
    sleep = 10
    while has_more:
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            for item in data['items']:
                # Extract relevant data
                name = item['name']
                count = item.get('count', 0)
                has_synonyms = item.get('has_synonyms', False)
                
                # Insert data into the database
                insert_tag_data(conn, name, count, has_synonyms)
            
            has_more = data['has_more']
            print(f"The page {params['page']} has been done.")
            params['page'] += 1
            sleep = max(sleep / 2, 10)
            time.sleep(sleep)
        elif response.status_code == 400:
            error_details = json.loads(response.text)
            if error_details.get('error_name') == 'throttle_violation':
                sleep = min(sleep * 2, 60)
                print(f"Failed to fetch data due to throttle violation, retrying in {sleep} seconds...")
                time.sleep(sleep)
        else:
            print(f"Failed to fetch data: HTTP {response.status_code}, Error: {response.text}")    
            break 
        
    close_connection(conn)    
    
def fetch_all_tag_synonyms():
    base_url = f"{BASE_URL}/tags/synonyms"
    params = PARAMS_BASE.copy()
    params['sort'] = 'applied'

    has_more = True

    conn = open_connection() 
    create_tables(conn)

    sleep = 1
    while has_more:
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            for item in data['items']:
                # Extract relevant data
                from_tag = item['from_tag']
                to_tag = item['to_tag']
                creation_date = item.get('creation_date', None)
                last_applied_date = item.get('last_applied_date', None)
                applied_count = item.get('applied_count', 0)
                
                # Insert synonym data into the database
                insert_tag_synonym_data(conn, from_tag, to_tag, creation_date, last_applied_date, applied_count)
            
            has_more = data['has_more']
            print(f"The page {params['page']} has been done.")
            params['page'] += 1
            sleep = max(sleep / 2, 1)
            time.sleep(sleep)
        elif response.status_code == 400:
            error_details = json.loads(response.text)
            if error_details.get('error_name') == 'throttle_violation':
                sleep = min(sleep * 2, 60)
                print(f"Failed to fetch data due to throttle violation, retrying in {sleep} seconds...")
                time.sleep(sleep)
        else:
            print(f"Failed to fetch data: HTTP {response.status_code}, Error: {response.text}")    
            break     
            
    close_connection(conn)  # Ensure this function is defined to properly close the DB connection
    