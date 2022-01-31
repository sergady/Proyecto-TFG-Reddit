import zstandard
import json
<<<<<<< HEAD
from json import JSONEncoder
import re 
import time

<<<<<<< HEAD
file_name = "RS_2019-09.zst"
subreddits_file_name = "subredditList.txt"

# Class that represents the posts, containing important
# fields for our data
class Redditpost:
    def __init__(self, post_id, created_utc, title, author, self_text, subreddit): 
        self.post_id = post_id
        self.created_utc = created_utc
        self.title = title
        self.author = author
        self.self_text = self_text
        self.subreddit = subreddit

# Encodes the reddit posts to JSON encode it
class RedditpostEncoder(JSONEncoder):
        def default(self, post):
            return post.__dict__
import re
import time
import RedditPost

>>>>>>> e638f65 (Removed NDJSON)
RAW_FILE_NAME = "RS_2019-09.zst"
SUBREDDITS_LIST = "subredditList.txt"
RESULT_FILE = "RS_2019-09.ndjson"
UTF = 'UTF-8'
ENTER = '\n'
CHUNK_SIZE = 2000000

def checkSelfText(self_text):
    if ( self_text == '' or self_text == '[deleted]' or self_text == '[removed]'):

def checkSelfText(self_text):
    if (self_text == '' or self_text == '[deleted]' or self_text == '[removed]'):
        return False
    return True

# Reads data and works with it
def readData(subreddit_dictionary, printSwitch):
    subreddits_array = []  # cambiar a reddit_posts_list
    # Open the file as fh
    with open(RAW_FILE_NAME, 'rb') as fh:
        dctx = zstandard.ZstdDecompressor()
        reader = dctx.stream_reader(fh)
        i = 0
        errorCounter = 0
        correctPosts = 0
        savedPosts = 0
        while True:
            # I need to be careful with this because it cuts jsons by half
            chunk = reader.read(CHUNK_SIZE)
            chunk = chunk.decode(UTF)  # Changes byte-like to string
            data = chunk.split(ENTER)  # Divides the text into posts
            for each in data:
                i += 1
                try:
                    data_dict = json.loads(each)
                    if(checkSelfText(data_dict['selftext'])):
                        if(subreddit_dictionary.get( data_dict['subreddit'], False)):
                            # We create the object
                            subreddits_array.append(Redditpost(data_dict['id'], data_dict['created_utc'], data_dict['title'], data_dict['author'], data_dict['selftext'], data_dict['subreddit']))

                    if(i%100000 == 0):
                        print('%d posts read' % i)
                        savePostsToJSON(subreddits_array, "posts.txt") #TODO: guardamos en chunks pero no limpiamos los textos
                        subreddits_array.clear()

                except json.decoder.JSONDecodeError:
                    errorCounter += 1
                    continue  # Seems like we do this to avoid errors but it is to eliminate divided posts
            if not chunk:
                break

    print('%d Posts read' % i)
    print('%d Errors detected' % errorCounter)
    print('%d Correct posts' % correctPosts)
    print('%d Saved posts' % savedPosts)
    return subreddits_array

def checkSelfTextAndSubreddit(data_dict, subreddit_dictionary):
    if(checkSelfText(data_dict['selftext'])):
        if(subreddit_dictionary.get(data_dict['subreddit'], False)):
            return True
    return False

def createRedditPost(data_dict):
    return RedditPost.RedditPost( data_dict['id'], data_dict['created_utc'], data_dict['title'], data_dict['author'], data_dict['selftext'], data_dict['subreddit'])

def postsCounter(i, printSwitch):
    if (printSwitch):
        print('%d posts read' % i)

def postsSaver(subreddits_array):
    savePostsToJSON(subreddits_array, RESULT_FILE)

# Creates the dictionary of subreddits we are interested in
def createSubredditsDictionary(subreddits_file):
    with open(subreddits_file) as subreddits_text:
        subreddits_list = subreddits_text.read().split("\n")
        subreddits_dictionary = {}
        for subreddit in subreddits_list:
            subreddits_dictionary.update({subreddit[2:]:True}) # We remove the 'r/' from the subreddits with [2:]
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

# Saves an array of subreddits posts into a file in JSON format
def savePostsToJSON(subreddits_array, posts_file_JSON):
     with open(posts_file_JSON, "w") as posts_file:
        for post in subreddits_array:   
            posts_file.write(str(json.dumps(post, indent=None, cls=RedditpostEncoder)))
            # We remove the 'r/' from the subreddits with [2:]
            subreddits_dictionary.update({subreddit[2:]: True})
    return subreddits_dictionary

# Saves an array of subreddits posts into a file in JSON format
def savePostsToJSON(subreddits_array, posts_file_JSON):
    with open(posts_file_JSON, "a") as posts_file:
        for post in subreddits_array:
            posts_file.write(str(json.dumps(post, indent=None, cls=RedditPost.RedditPostEncoder)))
            posts_file.write("\n")

def main():
    start = time.time()
    subreddit_dictionary = createSubredditsDictionary(subreddits_file_name)
    subreddits_array = readData(file_name, subreddit_dictionary)
    subreddits_array = cleanPosts(subreddits_array) # TODO: no se utiliza para nada si se guardan los textos en readData
    end = time.time()
    print('Time: ', end - start)

main()
    # Creates the dictionary of subreddits that we use
    subreddit_dictionary = createSubredditsDictionary(SUBREDDITS_LIST)

    # Reads data from the file and saves the data
    readData(subreddit_dictionary, False)

    end = time.time()
    print('Time: ', end - start)

main()
