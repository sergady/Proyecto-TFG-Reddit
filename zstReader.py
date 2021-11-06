import zstandard
import json
import re 

# Open the file as fh
with open("RS_2019-09.zst", 'rb') as fh:
    dctx = zstandard.ZstdDecompressor()
    reader = dctx.stream_reader(fh)
    while True:
        chunk = reader.read(20000) # I need to be careful with this because it cuts jsons by half
        chunk = chunk.decode('UTF-8') # Changes byte-like to string
        data = chunk.split('\n') # Divides the text into posts
        data_dict = json.loads(data[3])
        print((data_dict))
    



class RedditComment:
    def __init__(self, self_text, subreddit):
        self.self_text = self_text
        self.subreddit = subreddit
        