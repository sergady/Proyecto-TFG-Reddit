import random
import re

DATA_FILE_NAME = "RS_2019-09.ndjson"
SAMPLE_FILE = "sample_file.txt"
SAMPLE_SIZE = 5000

# Reads the json file and returns an array of json in string
def readFromJSON(json_file_name):
    with open(json_file_name, "r") as json_file:
        posts = json_file.read().split('\n')
    return posts

# Cleans the text from the posts
def cleanPosts(posts_array):
    regexpUrls = re.compile("https?://(www\.)?(\w|-)+\.\w+")  # URLs regexp
    regexpEmails = re.compile("[a-zA-Z1-9-]+@[a-zA-Z-]+\.[a-zA-Z]+")  # Emails regexps
    regexpWeb = re.compile("(http)|(www)|(http www)|(html)|(htm)|.com|(and)|(to)|(the)|(but)|(for)")# Web keywords regexps
    regexpNumbers = re.compile("\d")  # Numbers regexps
    for post in posts_array:
        # We clean the complete urls
        post = re.sub(regexpUrls, "", post)
        # We clean the emails
        post = re.sub(regexpEmails, "", post)
        # We clean url fragments
        post = re.sub(regexpWeb, "", post)
        post = re.sub(regexpNumbers, "", post)  # We clean numbers

    return posts_array

def createWorkingFile(new_file_name, number_of_posts):
    posts = readFromJSON(DATA_FILE_NAME)
    posts = cleanPosts(posts)
    k = len(posts) / number_of_posts
    init = random.randrange(round(k))

    with open(new_file_name, "w") as sample_file:
        i = init
        while(round(i)<len(posts)):
            sample_file.write(str(posts[round(i)]))
            sample_file.write("\n")
            i += k
    print("File created!")

createWorkingFile(SAMPLE_FILE, SAMPLE_SIZE)