import praw
import requests
import os

myid = open("pass.txt", "r").read()
mysecret = open("shh.txt", "r").read()


reddit = praw.Reddit(
    client_id=myid,
    client_secret=mysecret,
    user_agent="bot v1",
    username="",
    password="",
    )

subreddit_title = "cyberpunkgame"

subreddit = reddit.subreddit(subreddit_title)

for submission in subreddit.hot(limit = 10):
    print(submission.title)
    print(submission.url)
    print()
    if "jpg" in submission.url.lower() or "png" in submission.url.lower():
        print(True)
        image = requests.get(submission.url)
        file = open("images/" + subreddit_title + " " + submission.id + ".png", "wb")
        file.write(image.content)
        file.close()