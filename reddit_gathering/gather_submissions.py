from RedditPost import RedditPost
import requests
import json

# Gathers the data from a subreddit between the first day and the last of 2019
def get_data_from_subreddit(subreddit):
    endpoint = "https://api.pushshift.io/reddit/submission/search/?subreddit="+subreddit+"&after=2019-01-01&before=2019-12-31"
    result = requests.get(endpoint) 
    data = json.loads(result.text, strict=False) 
    return data['data']

def transform_data_into_objects(data):
    posts = list()
    for submission in data:
        posts.append(RedditPost.RedditPost( submission['id'], submission['created_utc'], submission['title'], submission['author'], submission['selftext'], submission['subreddit']))
        #print(submission)

    return posts

def main():
    posts = transform_data_into_objects(get_data_from_subreddit('abuse'))
    print(len(posts))

main()