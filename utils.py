import re
import html2text
from bs4 import BeautifulSoup

def extract_question_details(question_url, headers):
    """
    Extracts and prints the question title and Markdown-formatted body from a given URL.
    """
    try:
        import requests  # Import here to keep utility functions focused
        
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
        question_md = text_maker.handle(str(question_body)) if question_body else "Question body not found"
        question_md = re.sub(r'^\[code\]\s*$', '```', question_md, flags=re.MULTILINE)
        question_md = re.sub(r'^\[/code\]\s*$', '```', question_md, flags=re.MULTILINE)
        
        return question_url, title, question_md
    except Exception as e:
        print(f"An error occurred while fetching question details: {str(e)}")
        return question_url, "Error", str(e)
