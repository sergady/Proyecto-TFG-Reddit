from zstReader import readData
from pydoc_data.topics import topics
import time

def load_subreddits():
    with open("static_data\datasetSubreddits.txt", "r", encoding="utf-8") as sample_file:
        text = sample_file.readlines()
        for i in range(len(text)):
            text[i] = text[i].replace("\t", "").replace('\n', '').replace(' ','')
    return text

def create_dictionaries():
    topics_and_subreddits = load_subreddits()
    list_dictionaries = list()
    for topic_and_subreddits in topics_and_subreddits:
        dictonary_topic = topic_and_subreddits.split(',')[0]
        dictonary = dict()
        for subreddit in topic_and_subreddits.split(',')[1:]:
            dictonary.update({subreddit: True})
        list_dictionaries.append([dictonary_topic, dictonary])
    return list_dictionaries

def read_specific_subreddits(list_dictionaries):
    start = time.time()

    print("Topic: " + list_dictionaries[0][0])
    # Reads data from the file and saves the data
    readData(list_dictionaries[0][1], False)

    end = time.time()
    print('Time: ', end - start)


read_specific_subreddits(create_dictionaries())