import zstandard
import json
import re 
import time

file_name = "RS_2019-09.zst"


class RedditComment:
    def __init__(self, self_text, subreddit):
        self.self_text = self_text
        self.subreddit = subreddit

def checkSelfText(self_text):
    if ( self_text == '' or self_text == '[deleted]' or self_text == '[removed]'):
        return False
    return True

start = time.time()

def readData(file_name):
    reddit_comment_list = []
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
                        reddit_comment_list.append(RedditComment(data_dict['selftext'], data_dict['subreddit']))
                    if(i%100000 == 0):
                        print('%d posts read' % i)
                except json.decoder.JSONDecodeError:
                    continue # Seems like we do this to avoid errors but it is to eliminate divided posts
            if not chunk:
                break

    return reddit_comment_list
 

def cleanComments(reddit_comment_list):
    

end = time.time()
print('Time: ', end - start)

