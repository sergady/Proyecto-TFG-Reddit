import pandas as pd 
import requests 
import json 
import datetime 
import csv

# Incomplete file from https://www.youtube.com/watch?v=tjM78abmHY8

def get_pushshift_data(after, before, sub) :
    url = "https://api.pushshift.io/reddit/search/submission/?&after="+str(after)+"&before=" + str(after) + "&sub=" + str(sub)
    print(url) 
    r = requests.get(url) 
    data = json. loads(r. text, strict=False) 
    return data['data']

def collect_subData(subm):
    subData = list() #list to store data points 
    title = subm['title'] 
    url = subm['url'] 
    try:
        flair = subm["link_flair_text"]
    except KeyError:
        flair = "NaN" 
    
    try:
    # returns the body of the posts
        body = subm['selftext'] 
    except KeyError:
        body = ''
        
    author = subm['author'] 
    subId = subm['id'] 
    score = subm['score'] 
    created = datetime.datetime.fromtimestamp( subm['created_utc']) #1520561700.0 
    numComms = subm['num_comments'] 
    permalink = subm['permalink']
    subData.append((subId, title, body, url, author, score, created, numComms, permalink, flair)) 
    subStats[subId] = subData

def update_subFile():
    upload_count = 0 
    location = "subreddit_data_uncleaned/"
    print("input filename of submission file, please add .csv")
    filename = input() 
    file = location + filename
