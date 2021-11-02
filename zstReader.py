import zstandard
import json
import re 

# Comprueba que cogemos lo que nos interesa de los datos
def correct(data):
    if(data.find(b'selftext') > 0): # va hasta send replies
        if(not (data.find(b'[removed]') > 0 or data.find(b'[deleted]') > 0)):
            if(not (data.find(b'[removed]') > 0)):
                if(len(data)>13):
                    return True
    else:
        return False



with open("RS_2019-09.zst", 'rb') as fh:
    dctx = zstandard.ZstdDecompressor()
    reader = dctx.stream_reader(fh)
    #while True:
    chunk = reader.read(16384) # I need to be careful with this because it cuts jsons by half
    chunk = chunk.decode('UTF-8') # Changes byte-like to string
    data = chunk.split('\n')
    data_dict = json.loads(data[4])
    print((data_dict['selftext']))
    for j in range(len(data)):
        #if(correct(data[j])):
        #print(data[j].decode('UTF-8'))
        continue
    # if not chunk:
    #     break



# Debería comprobar: "subreddit":"[...]"
# Luego la información se suele encontrar en "selftext":"[...]"

class RedditComment:
    def __init__(self, self_text, subreddit):
        self.self_text = self_text
        self.subreddit = subreddit
        