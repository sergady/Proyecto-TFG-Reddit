import json

from SamplingScript import SAMPLE_FILE

def readSampleFile():
    with open(SAMPLE_FILE, "r+") as sample_file:
        text = (sample_file.read())
    return text.split('\n')

def storeTextsInArray():
    posts_array = readSampleFile()
    texts = []
    for i in range(len(posts_array)-1):
        text = json.loads(posts_array[i])
        texts.append(text['self_text'])

    return texts

print(storeTextsInArray())