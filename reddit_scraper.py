import praw
import requests
import os
from RedDownloader import RedDownloader


def initReddit():

    global reddit

    myid = open("pass.txt", "r").read()
    mysecret = open("shh.txt", "r").read()


    reddit = praw.Reddit(
        client_id=myid,
        client_secret=mysecret,
        user_agent="bot v1",
        username="",
        password="",
        )

def scrapeImages(sub_name, sub_sort, scrape_limit):

    subreddit = reddit.subreddit(sub_name)

    for submission in subreddit.hot(limit = scrape_limit):
        print(submission.title)
        print(submission.url)
        print()
        if "jpg" in submission.url.lower() or "png" in submission.url.lower():
            print("Image found")
            image = requests.get(submission.url)
            file = open("images/" + sub_name + "-" + submission.id + ".png", "wb")
            file.write(image.content)
            file.close()


def scrapeVideos(reddit):
    permaurl = "https://www.reddit.com/"+submission.permalink
    file = RedDownloader.Download(url = permaurl , output=subreddit_name + "-" + submission.id , destination="videos/" , quality = 360)
    print(permaurl)

        
def scrapePosts(reddit):
    pass        

def menu():
    print("Reddit Scraper")
    print("1. Post URLs")
    print("2. Images")
    print("3. Videos")
    print("q. Quit")
    userChoice = input("What do you want to scrape? ")
    return userChoice

def main():
    
    initReddit()

    isRunning = True

    while isRunning:
        userChoice = menu()
        if userChoice == "1":
            pass
        elif userChoice == "2":
            scrapeImages("aww", "top", 2)
        elif userChoice == "3":
            pass
        elif userChoice.lower() == "q":
            isRunning = False
        else:
            print("Wrong input! Try again!")


if __name__ == "__main__":
    main()
