from psaw import PushshiftAPI

api = PushshiftAPI()
endpoint = "https://api.pushshift.io/reddit/search/submission"
results = list(api.search_submissions(subreddit=100))
print(results)