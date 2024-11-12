import praw
import validators
import datetime
import re
import json
from database import engine
from sqlalchemy import text
import pandas as pd
import prawcore
reddit = praw.Reddit(client_id ='SjxzNO1UScdmzWv0XpuXOA',
					client_secret ='DFf97wok54p5NSByXWJmxZyCMF-eyw',
					user_agent ='Testing_API',
					username="Group_17", password = "reddit_cr@wler") ## can be made more secure if it needs to be, just for testing (i.e put into a JSON file and write a function to extract)


def validate_link(input_link): ## only works for https atm, http is deprecated so not sure whether to worry about http // to be implemented at a later date
	valid_link = False

	if (validators.url(("https://" + input_link))):
		valid_link = True
		
	if (validators.url(input_link)):
		valid_link = True
  
	return valid_link

def search(link, reddit, apiidx):
	posts_dict = {
        "Title": [],
        "Url": [],
        "Subreddits": [],
        "Post Text": [],
        "Score": [],
        "Total Comments": [],
        "Upvotes": [],
        "Downvotes": [],
        "Unix-Time": [],
        "Time": [],
    }	#Updated to improve readability.
	if apiidx == 1:
		SEARCH_QUERY_API = reddit.subreddit("all").search(f'url:"{link}"', syntax="lucene", limit=None)
	else:
		SEARCH_QUERY_API = reddit.subreddit("all").search(link, syntax="lucene", limit=None)
		
	for post in SEARCH_QUERY_API:
		posts_dict["Title"].append(post.title)
		posts_dict["Url"].append(post.url)
		posts_dict["Subreddits"].append(str(post.subreddit))  # convert subreddit object to string
		posts_dict["Post Text"].append(post.selftext)
		posts_dict["Score"].append(post.score)
		posts_dict["Total Comments"].append(post.num_comments)
		posts_dict["Upvotes"].append(post.ups)
		downvotes = round((post.upvote_ratio * post.score)/2*post.upvote_ratio - 1) if post.upvote_ratio != 0.5 else round(post.score / 2) 
		if downvotes == -1: downvotes = 0 # Gotta give props to an old 2015 post for this fix :D
		posts_dict["Downvotes"].append(downvotes)
		posts_dict["Unix-Time"].append(post.created_utc)  # Unix time to be used at a later date.
		posts_dict["Time"].append(datetime.datetime.fromtimestamp(post.created_utc).strftime("%Y-%m-%d %H:%M:%S"))  # Since its Unix time, it converts it to a readable time.
	return posts_dict

# Takes reddit link and returns a list of all links present in the text. Returns False if no links in text. (Note that this doesn't fetch links attached to post.) // to be implemented at a later date
def get_links_in_reddit_post(link): 
	post = reddit.submission(url=link)
	links = []
	links.append(post.url)
	return links[0]