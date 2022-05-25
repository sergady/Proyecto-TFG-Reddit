from psaw import PushshiftAPI
import requests
import json

#api = PushshiftAPI()
#results = list(api.search_submissions(subreddit=100))
subreddit = "NarcissisticAbuse"
endpoint = "https://api.pushshift.io/reddit/submission/search/?subreddit="+subreddit+"&after=2019-01-01&before=2019-12-31"
result = requests.get(endpoint) 
data = json.loads(result.text, strict=False) 
#print(data['data'])

for submission in data['data']:
    print(submission)