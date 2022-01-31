from json import JSONEncoder

# Class that represents the posts, containing important
# fields for our data
class RedditPost:
    def __init__(self, post_id, created_utc, title, author, self_text, subreddit): 
        self.post_id = post_id
        self.created_utc = created_utc
        self.title = title
        self.author = author
        self.self_text = self_text
        self.subreddit = subreddit

# Encodes the reddit posts to JSON encode it
class RedditPostEncoder(JSONEncoder):
        def default(self, post):
            return post.__dict__