import zstandard
import json
from json import JSONEncoder
import re 
import time

file_name = "RS_2019-09.zst"
subreddits_file_name = "subredditList.txt"


class Redditpost:
    def __init__(self, post_id, title, author, self_text, subreddit): # Añadir tambien el título, autor, id del post y timestamp (no hay)
        self.post_id = post_id
        self.title = title
        self.author = author
        self.self_text = self_text
        self.subreddit = subreddit

class RedditpostEncoder(JSONEncoder):
        def default(self, post):
            return post.__dict__

def checkSelfText(self_text):
    if ( self_text == '' or self_text == '[deleted]' or self_text == '[removed]'):
        return False
    return True


def readData(file_name, subreddit_dictionary):
    subreddits_array = [] # cambiar a reddit_posts_list
    # Open the file as fh
    with open(file_name, 'rb') as fh:
        dctx = zstandard.ZstdDecompressor()
        reader = dctx.stream_reader(fh)
        i = 0
        while True:
            # We read the data and save it into chunks
            chunk = reader.read(20000) # I need to be careful with this because it cuts jsons by half
            chunk = chunk.decode('UTF-8') # Changes byte-like to string
            data = chunk.split('\n') # Divides the text into posts
            for each in data:
                i += 1
                try:
                    data_dict = json.loads(each)
                    if(checkSelfText(data_dict['selftext'])):
                        if(subreddit_dictionary.get( data_dict['subreddit'], False)):
                            # We create the object
                            subreddits_array.append(Redditpost(data_dict['id'], data_dict['title'], data_dict['author'], data_dict['selftext'], data_dict['subreddit']))
                            

                    if(i%100000 == 0):
                        print('%d posts read' % i)
                        savePostsToJSON(subreddits_array, "posts.txt")
                        subreddits_array.clear()

                except json.decoder.JSONDecodeError:
                    continue # Seems like we do this to avoid errors but it is to eliminate divided posts
            if not chunk:
                break

    return subreddits_array

# Creates the dictionary of subreddits we are interested in
def createSubredditsDictionary(subreddits_file):
    with open(subreddits_file) as subreddits_text:
        subreddits_list = subreddits_text.read().split("\n")
        subreddits_dictionary = {}
        for subreddit in subreddits_list:
            subreddits_dictionary.update({subreddit[2:]:True})
    return subreddits_dictionary 

# Cleans the text from the posts 
def cleanPosts(subreddits_array):
    regexpUrls = re.compile("https?://(www\.)?(\w|-)+\.\w+") # URLs regexp
    regexpEmails = re.compile("[a-zA-Z1-9-]+@[a-zA-Z-]+\.[a-zA-Z]+") # Emails regexps
    regexpWeb = re.compile("(http)|(www)|(http www)|(html)|(htm)|.com") # Web keywords regexps
    regexpNumbers = re.compile("\d") # Numbers regexps
    for post in subreddits_array:
        post.subreddit = re.sub(regexpUrls,"",post.subreddit) # We clean the complete urls
        post.subreddit = re.sub(regexpEmails,"",post.subreddit) # We clean the emails
        post.subreddit = re.sub(regexpWeb,"",post.subreddit) # We clean url fragments
        post.subreddit = re.sub(regexpNumbers,"",post.subreddit) # We clean numbers
    
    return subreddits_array

def savePostsToJSON(subreddits_array, posts_file_JSON):
     with open(posts_file_JSON, "w") as posts_file:
        for post in subreddits_array:   
            posts_file.write(str(json.dumps(post, indent=2, cls=RedditpostEncoder)))
            posts_file.write("\n")

def main():
    start = time.time()
    subreddit_dictionary = createSubredditsDictionary(subreddits_file_name)
    subreddits_array = readData(file_name, subreddit_dictionary)
    subreddits_array = cleanPosts(subreddits_array)
    end = time.time()
    print('Time: ', end - start)

main()