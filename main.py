from dotenv import load_dotenv
from colored import fg, attr


def main():
    from api import fetch_questions, fetch_popular_tags, fetch_all_tag_synonyms
    
    blue = fg('blue')
    green = fg('green')
    reset = attr('reset')
    running = True   

    while running:
        print(f"{blue}Welcome to the Stackoverflow CLI!")
        print("Available commands:")
        print("1. Fetch popular tags")
        print("2. Fetch tag synonyms")
        print("3. Fetch questions")
        print(f"4. Exit{reset}")
        command = input(f"{blue}Enter a command number: {reset}").strip()

        if command == "1":
            print(f"{green}Fetching popular tags...{reset}")
            fetch_popular_tags()
            print(f"{green}Successfully fetched popular tags.{reset}")
        elif command == "2":
            print(f"{green}Fetching all tag synonyms...{reset}")
            fetch_all_tag_synonyms()
            print(f"{green}Successfully fetched all tag synonyms.{reset}")
        elif command == "3":
            tags_input = input(f"{blue}Enter some tags (separated by commas): {reset}").strip()
            tags = tags_input.split(',')
            # Trim whitespace from each tag
            tags = [tag.strip() for tag in tags]
            print(f"{green}Fetching all questions for tags: {tags}{reset}")
            fetch_questions(tags, 1, 0)
            print(f"{green}Successfully fetched all questions for the provided tags.{reset}")    
        elif command == "4":
            print(f"{green}Exiting the application. Goodbye!{reset}")
            running = False
        else:
            print(f"{green}Unknown command number. Please try again.{reset}")  

if __name__ == '__main__':
    # Load environment variables from .env file
    load_dotenv()
    
    # show the main menu
    main()
