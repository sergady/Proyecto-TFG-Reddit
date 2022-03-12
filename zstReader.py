import zstandard
import json
import time
import RedditPost

RAW_FILE_NAME = "data/RS_2019-09.zst"
SUBREDDITS_LIST = "static_data/subredditList.txt"
RESULT_FILE = "data/RS_2019-09.ndjson"
UTF = 'UTF-8'
ENTER = '\n'
CHUNK_SIZE = 200000

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
            # We read the data and save it into chunks
            # I need to be careful with this because it cuts jsons by half
            chunk = reader.read(CHUNK_SIZE)
            chunk = chunk.decode(UTF)  # Changes byte-like to string
            data = chunk.split(ENTER)  # Divides the text into posts
            for each in data:
                i += 1
                try:
                    data_dict = json.loads(each)
                    if(checkSelfTextAndSubreddit(data_dict, subreddit_dictionary)):
                        # We create the object
                        subreddits_array.append(createRedditPost(data_dict))
                        correctPosts +=1

                    if(i % 100000 == 0):
                        postsCounter(i, printSwitch)
                        postsSaver(subreddits_array)
                        savedPosts += len(subreddits_array)
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
    # Creates the dictionary of subreddits that we use
    subreddit_dictionary = createSubredditsDictionary(SUBREDDITS_LIST)

    # Reads data from the file and saves the data
    readData(subreddit_dictionary, False)

    end = time.time()
    print('Time: ', end - start)

main()