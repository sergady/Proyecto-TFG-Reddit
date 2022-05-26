from psaw import PushshiftAPI
import requests
import json


def get_data_from_subreddit(subreddit):
    endpoint = "https://api.pushshift.io/reddit/submission/search/?subreddit="+subreddit+"&after=2019-01-01&before=2019-12-31"
    result = requests.get(endpoint) 
    data = json.loads(result.text, strict=False) 
    return data['data']


for submission in get_data_from_subreddit('abuse'):
    print(submission)