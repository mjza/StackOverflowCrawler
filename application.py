import requests
from bs4 import BeautifulSoup
import html2text

# Constants
BASE_URL = 'https://api.stackexchange.com/2.3/questions'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
}
PARAMS_BASE = {
    'order': 'desc',
    'sort': 'activity',
    'site': 'stackoverflow',
    'pagesize': 1
}

def print_line():
    print('\n----------------------')

def fetch_questions(tags, pages=1):
    """
    Fetches questions for given tags and handles pagination.
    """
    for page in range(1, pages + 1):
        params = PARAMS_BASE.copy()
        params['tagged'] = ';'.join(tags)  # Support multiple tags
        params['page'] = page

        response = requests.get(BASE_URL, params=params)
        questions = response.json()

        for question in questions.get('items', []):
            question_url = question['link']
            extract_question_details(question_url)

def extract_question_details(question_url):
    """
    Extracts and prints the question title and Markdown-formatted body from a given URL.
    """
    try:
        response = requests.get(question_url, headers=HEADERS)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract title
        title_tag = soup.find('h1')
        title = title_tag.text.strip() if title_tag else "Title not found"
        
        # Initialize html2text converter
        text_maker = html2text.HTML2Text()
        text_maker.ignore_links = False
        text_maker.ignore_images = True
        text_maker.ignore_emphasis = False
        text_maker.body_width = 0
        
        # Convert HTML question body to Markdown
        question_body = soup.find('div', class_='s-prose js-post-body')
        if question_body:
            question_md = text_maker.handle(str(question_body))
        else:
            question_md = "Question body not found"
        
        print(f"{question_url}\n----\n{title}\n----\n{question_md}\n")
    except Exception as e:
        print(f"An error occurred while fetching question details: {str(e)}")

def main():
    """
    Main function to orchestrate the fetching of questions and processing.
    """
    tags = ['ui5']  # Add or change tags as needed
    pages = 1  # Number of pages to fetch
    fetch_questions(tags, pages)

if __name__ == '__main__':
    main()
