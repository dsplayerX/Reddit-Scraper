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


def scrapePosts(reddit):
    pass        


def scrapeImages(sub_name, sub_sort, scrape_limit):

    subreddit = reddit.subreddit(sub_name)
  
    saveCount = 0

    print(f" > Scraping {scrape_limit} posts from r/{sub_name} for images...")

    for submission in getSortedSubreddit(subreddit, sub_sort)(limit = scrape_limit):
        if "jpg" in submission.url.lower() or "png" in submission.url.lower():
            image = requests.get(submission.url)
            file = open("images/" + sub_name + "-" + submission.title[:15] + "-" + submission.id + ".png", "wb")
            file.write(image.content)
            file.close()
            saveCount += 1
    print(f" > Saved {saveCount} image(s).")


def scrapeVideos(sub_name, sub_sort, scrape_limit, quality):

    subreddit = reddit.subreddit(sub_name)

    saveCount = 0

    print(f" > Scraping {scrape_limit} posts from r/{sub_name} for videos...")

    for submission in getSortedSubreddit(subreddit, sub_sort)(limit = scrape_limit):
        permaURL = "https://www.reddit.com/"+submission.permalink
        file = RedDownloader.Download(url = permaURL , output=sub_name + "-" + submission.id , destination="videos/" , quality = quality)
        print(permaURL)
    print(f" > Saved {saveCount} video(s).")
        
def menu():
    print("Reddit Scraper")
    print("1. Post URLs")
    print("2. Images")
    print("3. Videos")
    print("q. Quit")
    userChoice = input("What do you want to scrape? ")
    return userChoice


def printSortMethods():
    print(" 1.controversial")
    print(" 2.gilded")
    print(" 3.hot")
    print(" 4.new")
    print(" 5.rising")
    print(" 6.top of all time")

    
def getSortedSubreddit(subreddit, sort):
    sub_sort_dict = {
        1 : subreddit.controversial,
        2 : subreddit.gilded,
        3 : subreddit.hot,
        4 : subreddit.new,
        5 : subreddit.rising,
        6 : subreddit.top
    }
    return sub_sort_dict[sort]


def main():
    
    initReddit()

    isRunning = True

    while isRunning:
        userChoice = menu()
        if userChoice == "1":
            pass

        elif userChoice == "2":
            userSub = input("Enter subreddit name: ")
            printSortMethods()
            userSort = int(input("Enter sort method: "))
            userLimit = int(input("How many posts to scrape: "))
            scrapeImages(userSub, userSort, userLimit)

        elif userChoice == "3":
            userSub = input("Enter subreddit name: ")
            printSortMethods()
            userSort = int(input("Enter sort method: "))
            userLimit = int(input("How many posts to scrape: "))

            print("Avaliable options to choose from are 144, 240, 360, 480, 720, 1080")
            print("If a video file in specified resolution is not found it will try for a lower resolution")

            userQuality = int(input("Enter video quality: "))
            scrapeVideos(userSub, userSort, userLimit, userQuality)

        elif userChoice.lower() == "q":
            isRunning = False

        else:
            print("Wrong input! Try again!")


if __name__ == "__main__":
    main()
