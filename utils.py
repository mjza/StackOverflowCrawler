import re
import html2text
import requests
from bs4 import BeautifulSoup

def extract_question_details(question_url, headers):
    """
    Fetches and extracts details from a given question URL. If the URL is None, returns an error message.
    
    Parameters:
    - question_url: The URL of the question to fetch details for.
    - headers: A dictionary of HTTP headers to use for the request.
    
    Returns:
    - A tuple of (title, body) if successful, with 'Error' as title if question_url is None or any issue arises.
    """
    # Check if the question_url is None
    if question_url is None:
        return ("Error", "The question URL was not provided.")

    try:       
        response = requests.get(question_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        title_tag = soup.find('h1')
        title = title_tag.text.strip() if title_tag else "Title not found"
        
        text_maker = html2text.HTML2Text()
        text_maker.ignore_links = False
        text_maker.ignore_images = True
        text_maker.ignore_emphasis = False
        text_maker.ignore_tables = False
        text_maker.mark_code = True
        text_maker.body_width = 0
        
        question_body = soup.find('div', class_='s-prose js-post-body')
        question_marke_down = text_maker.handle(str(question_body)) if question_body else "Question body not found"
        question_marke_down = re.sub(r'^\[code\]\s*$', '```', question_marke_down, flags=re.MULTILINE)
        question_marke_down = re.sub(r'^\[/code\]\s*$', '```', question_marke_down, flags=re.MULTILINE)
        
        return title, question_marke_down
    except Exception as e:
        print(f"An error occurred while fetching question details: {str(e)}")
        return "Error", str(e)
