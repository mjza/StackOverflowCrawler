from api import fetch_questions, fetch_popular_tags

def main():
    '''
    tags = ['ui5']
    pages = 1
    questions = fetch_questions(tags, pages)
    
    for question_url, title, question_md in questions:
        print(f"{question_url}\n----\n{title}\n----\n{question_md}\n")
    '''    
    # Call the function to start fetching and storing tag data
    fetch_popular_tags()

if __name__ == '__main__':
    main()
