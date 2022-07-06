import praw
import requests
import os
from RedDownloader import RedDownloader

myid = open("pass.txt", "r").read()
mysecret = open("shh.txt", "r").read()


reddit = praw.Reddit(
    client_id=myid,
    client_secret=mysecret,
    user_agent="bot v1",
    username="",
    password="",
    )

subreddit_name = "aww"

subreddit = reddit.subreddit(subreddit_name)

for submission in subreddit.hot(limit = 10):
    print(submission.title)
    print(submission.url)
    print()
    if "jpg" in submission.url.lower() or "png" in submission.url.lower():
        print("Image found")
        image = requests.get(submission.url)
        file = open("images/" + subreddit_name + " " + submission.id + ".png", "wb")
        file.write(image.content)
        file.close()
    else:
        permaurl = "https://www.reddit.com/"+submission.permalink
        file = RedDownloader.Download(url = permaurl , output=submission.id , destination="videos/" , quality = 360)
        print(permaurl)