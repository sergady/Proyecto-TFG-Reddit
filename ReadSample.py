import json

from Constants import SAMPLE_FILE_NAME

def readSampleFile():
    with open(SAMPLE_FILE_NAME, "r+", encoding="utf-8") as sample_file:
        text = (sample_file.read())
    return text.split('\n')

def storeTextsInArray():
    posts_array = readSampleFile()
    texts = []
    for i in range(len(posts_array)-1):
        try: # Used to avoid exceptions for empty lines in the end
            text = json.loads(posts_array[i])
            texts.append(text['self_text'])
        except json.decoder.JSONDecodeError:
            continue

    return [texts, posts_array[0]]
