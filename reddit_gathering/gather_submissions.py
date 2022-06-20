import time
import RedditPost
import requests
import json

# Gathers the data from a subreddit between the first day and the last of 2019
def get_data_from_subreddit(subreddit):
    endpoint = "https://api.pushshift.io/reddit/submission/search/?subreddit="+subreddit+"&after=2019-01-01&before=2019-12-31&size=500" 
    result = requests.get(endpoint) 
    data = json.loads(result.text, strict=False) 
    return data['data']

# Gathers the data from a subreddit between the first day and the last of 2019
def get_data_from_subreddit(after, before):
    endpoint = "https://api.pushshift.io/reddit/submission/search/?after="+ after +"&before="+ before +"&size=100" 
    result = requests.get(endpoint) 
    data = json.loads(result.text, strict=False) 
    return data['data'] # dificil borrar resultados vacíos o incorrectos

def transform_data_into_objects(data):
    posts = list()
    errors =0 
    for submission in data:
        try:
            posts.append(RedditPost.RedditPost( submission['id'], submission['created_utc'], submission['title'], submission['author'], submission['selftext'], submission['subreddit']))
        except KeyError:
            errors += 1

    print("Errors: " + str(errors))
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

def gather_random_posts():
    posts = list()
    init_time = 1546297201
    increment = 11680
    end_time = init_time + 31536000
    
    for i in range(init_time, end_time, increment):
        posts.extend(transform_data_into_objects(get_data_from_subreddit(str(i), str(i+increment))))
        time.sleep(1)
    return posts

def write_random_posts(file_name, posts):
    with open(file_name, "a") as posts_file:
        errors = 0
        for post in posts:
            try:
                posts_file.write(str(json.dumps(post, indent=None, cls=RedditPost.RedditPostEncoder)))
                posts_file.write("\n")
            except json.decoder.JSONDecodeError:
                errors += 1

    print("Errors decoder: " + str(errors))

def main():
    print_subreddits_count(load_subredits())

write_random_posts("data/random_posts_control2.ndjson", gather_random_posts())

