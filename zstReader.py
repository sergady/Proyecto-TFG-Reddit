import zstandard
import json
import re 
import time

file_name = "RS_2019-09.zst"
subreddits_file_name = "subredditList.txt"


class RedditComment:
    def __init__(self, post_id, title, author, self_text, subreddit): # Añadir tambien el título, autor, id del post y timestamp (no hay)
        self.post_id = post_id;
        self.title = title;
        self.author = author;
        self.self_text = self_text
        self.subreddit = subreddit

def checkSelfText(self_text):
    if ( self_text == '' or self_text == '[deleted]' or self_text == '[removed]'):
        return False
    return True


def readData(file_name, subreddit_dictionary):
    reddit_comment_list = [] # cambiar a reddit_posts_list
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
                            reddit_comment_list.append(RedditComment(data_dict['id'], data_dict['title'], data_dict['author'], data_dict['selftext'], data_dict['subreddit']))
                        # Volcar a un archivo cuando acabo el chunk
                        # Guardarlo en ndjson/ldjson/jsonlines
                        # Comprobar que no haya saltos de línea
                        # Si acaso guardar la línea para luego volver a leer la línea exacta
                    if(i%100000 == 0):
                        print('%d posts read' % i)
                except json.decoder.JSONDecodeError:
                    continue # Seems like we do this to avoid errors but it is to eliminate divided posts
            if not chunk:
                break

    return reddit_comment_list
 
def cleanSubreddits(reddit_comment_list, subreddits_list): # Hacer un diccionario
    return reddit_comment_list

def createSubredditsDictionary(subreddits_file):
    with open(subreddits_file) as subreddits_text:
        subreddits_list = subreddits_text.read().split("\n")
        subreddits_dictionary = {}
        for subreddit in subreddits_list:
            subreddits_dictionary.update({subreddit[2:]:True})
    return subreddits_dictionary 

def cleanComments(reddit_comment_list):
    regexpUrls = re.compile("https?://(www\.)?(\w|-)+\.\w+") # URLs regexp
    regexpEmails = re.compile("[a-zA-Z1-9-]+@[a-zA-Z-]+\.[a-zA-Z]+") # Emails regexps
    regexpWeb = re.compile("(http)|(www)|(http www)|(html)|(htm)|.com") # Web keywords regexps
    regexpNumbers = re.compile("\d") # Numbers regexps
    for comment in reddit_comment_list:
        comment.subreddit = re.sub(regexpUrls,"",comment.subreddit) # We clean the complete urls
        comment.subreddit = re.sub(regexpEmails,"",comment.subreddit) # We clean the emails
        comment.subreddit = re.sub(regexpWeb,"",comment.subreddit) # We clean url fragments
        comment.subreddit = re.sub(regexpNumbers,"",comment.subreddit) # We clean numbers
    
    return reddit_comment_list


start = time.time()
subreddit_dictionary = createSubredditsDictionary(subreddits_file_name)
readData(file_name, subreddit_dictionary)
end = time.time()
print('Time: ', end - start)