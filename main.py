from dotenv import load_dotenv
from colored import fg, attr

def read_integer(prompt_message):
    red = fg('red')
    reset = attr('reset')
    while True:
        user_input = input(prompt_message)
        try:
            return int(user_input)
        except ValueError:
            print(f"{red}Please enter a valid integer.{reset}")

def read_yes_no(prompt_message):
    """
    Prompts the user with the given message and expects a 'Y' or 'N' input.
    Returns True for 'Y' and False for 'N'.
    """
    green = fg('green')
    red = fg('red')
    reset = attr('reset')    
    while True:
        user_input = input(prompt_message + f"{green} (Y/N): {reset}").strip().upper()
        if user_input == 'Y':
            return True
        elif user_input == 'N':
            return False
        else:
            print(f"{red}Invalid input. Please enter 'Y' for Yes or 'N' for No.{reset}")


def main():
    from api import fetch_questions, fetch_popular_tags, fetch_all_tag_synonyms
    
    blue = fg('blue')
    green = fg('green')
    reset = attr('reset')
    running = True   

    while running:
        print(f"{blue}Welcome to the Stackoverflow CLI!")
        print("Available commands:")
        print("0. Exit")
        print("1. Fetch popular tags")
        print("2. Fetch tag synonyms")
        print("3. Fetch questions")        
        command = input(f"Enter a command number: {reset}").strip()

        if command == "0":
            print(f"{green}Exiting the application. Goodbye!{reset}")
            running = False
        elif command == "1":            
            first_page = read_integer(f"{blue}Enter the first page number: {reset}")
            print(f"{green}Fetching popular tags...{reset}")          
            fetch_popular_tags(first_page)
            print(f"{green}Successfully fetched popular tags.{reset}")
        elif command == "2":
            print(f"{green}Fetching all tag synonyms...{reset}")
            fetch_all_tag_synonyms()
            print(f"{green}Successfully fetched all tag synonyms.{reset}")
        elif command == "3":
            
            tags_input = input(f"{blue}Enter some tags (separated by commas): {reset}").strip()
            tags = tags_input.split(',')
            just_new_questions = read_yes_no(f"{blue}Do you need only new questions? {reset}")
            first_page = read_integer(f"{blue}Enter the first page number: {reset}")
            # Trim whitespace from each tag
            tags = [tag.strip() for tag in tags]
            print(f"{green}Fetching all questions for tags: {tags}{reset}")
            fetch_questions(tags, first_page, 0, just_new_questions)
            print(f"{green}Successfully fetched all questions for the provided tags.{reset}")   
        
        else:
            print(f"{green}Unknown command number. Please try again.{reset}")  

if __name__ == '__main__':
    # Load environment variables from .env file
    load_dotenv()
    
    # show the main menu
    main()
