from api import fetch_questions

def main():
    tags = ['ui5']
    pages = 1
    questions = fetch_questions(tags, pages)
    
    for question_url, title, question_md in questions:
        print(f"{question_url}\n----\n{title}\n----\n{question_md}\n")

if __name__ == '__main__':
    main()
