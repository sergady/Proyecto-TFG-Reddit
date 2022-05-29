import time
from isort import file
from RedditPost import RedditPost
import requests
import json

# Gathers the data from a subreddit between the first day and the last of 2019
def get_data_from_subreddit(subreddit):
    endpoint = "https://api.pushshift.io/reddit/submission/search/?subreddit="+subreddit+"&after=2019-01-01&before=2019-12-31&size=500" 
    result = requests.get(endpoint) 
    data = json.loads(result.text, strict=False) 
    return data['data']

def transform_data_into_objects(data):
    posts = list()
    for submission in data:
        posts.append(RedditPost( submission['id'], submission['created_utc'], submission['title'], submission['author'], submission['selftext'], submission['subreddit']))
        #print(submission)

    return posts

def load_subredits():
    with open("static_data\datasetSubreddits.txt", "r", encoding="utf-8") as sample_file:
        text = sample_file.readlines()
        for i in range(len(text)):
            text[i] = text[i].replace("\t", "").replace('\n', '').replace(' ','')
    return text

def print_subreddits_count(subreddits):
    for line in subreddits:
        subredditNames = line.split(',')
        print(subredditNames)
        for subreddit in subredditNames[1:]:
            try:
                posts = transform_data_into_objects(get_data_from_subreddit(subreddit))
                time.sleep(1) 
            except json.decoder.JSONDecodeError:
                print(subreddit + " error")
                break
            print(subreddit+": "+str(len(posts)))

def main():
    print_subreddits_count(load_subredits())

main()