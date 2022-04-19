import json
import re

from Constants import SAMPLE_FILE_NAME


# Reads the files and puts them in a matrix
def readSampleFile():
    with open(SAMPLE_FILE_NAME, "r", encoding="utf-8") as sample_file:
        text = sample_file.readlines()
    return text


# Removes symbols and urls
def removeSymbolsAndUrlsDani(text):
    # We have several regular expressions to clean the texts from unuseful data
    regexpUrls = re.compile("https?://(www\.)?(\w|-)+\.\w+")
    regexpEmails = re.compile("[a-zA-Z1-9-]+@[a-zA-Z-]+\.[a-zA-Z]+")
    regexpWeb = re.compile("(http)|(www)|(http www)|(html)|(htm)|.com")
    regexpNumbers = re.compile("\d")

    text = re.sub(regexpUrls, "", text)  # We clean the complete urls
    text = re.sub(regexpEmails, "", text)  # We clean the emails
    text = re.sub(regexpWeb, "", text)  # We clean url fragments
    text = re.sub(regexpNumbers, "", text)  # quitamos los números

    return text


def storeTextsInArray():
    posts_array = readSampleFile()
    texts = []
    for i in range(len(posts_array)-1):
        try:  # Used to avoid exceptions for empty lines in the end
            text = json.loads(posts_array[i])
            texts.append(text)
        except json.decoder.JSONDecodeError:
            continue

    return [texts, posts_array[0]]
