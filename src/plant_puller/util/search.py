import os
from googleapiclient.discovery import build
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

def google_search(search_term, **kwargs):
    # Load API key from environment variable
    api_key = os.getenv('SEARCH_KEY')
    cse_id = os.getenv('CSE_ID')

    if not api_key:
        raise EnvironmentError("SEARCH_KEY environment variable not set.")

    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']

if __name__=="__main__":
    results = google_search("What are the best plants for the home?")
    print(results)