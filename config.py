import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration settings for the application
BASE_URL = 'https://api.stackexchange.com/2.3/'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
}
PARAMS_BASE = {
    'order': 'desc',
    'sort': 'activity',
    'site': 'stackoverflow',
    'page': 1,
    'pagesize': 100,
    'key': os.getenv('APP_KEY')
}