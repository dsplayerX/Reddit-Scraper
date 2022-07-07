# REDDIT SCRAPER by dsplayerX

import praw
import requests
import os
import base64
from RedDownloader import RedDownloader

def initReddit():

    global reddit

    if os.path.exists(os.getcwd() + "/creds.txt"):
        encoded_msg = open("creds.txt", "r").read()
        bs64_bytes = encoded_msg.encode('ascii')
        msg_bytes = base64.b64decode(bs64_bytes)
        decoded_msg = msg_bytes.decode('ascii')
        access_secret = decoded_msg.splitlines()
        userID = access_secret[0]
        userSecret = access_secret[1]
    else:
        userID = input("Enter your Client ID: ")
        userSecret = input("Enter your Client Secret: ")
        access_secret = userID + "\n" + userSecret
        msg_bytes = access_secret.encode('ascii')
        bs64_bytes = base64.b64encode(msg_bytes)
        encoded_msg = bs64_bytes.decode('ascii')
        file = open("creds.txt", "w")
        file.write(encoded_msg)
        file.close()

    reddit = praw.Reddit(
        client_id=userID,
        client_secret=userSecret,
        user_agent="bot v1",
        username="",
        password="",
        )


def scrapePosts(sub_name, sub_sort, scrape_limit):
    try:
        subreddit = reddit.subreddit(sub_name)
    
        postCount = 0

        if os.path.exists(os.getcwd() + "/savedscrapes"):
            pass
        else:
            os.mkdir(os.getcwd() + "/savedscrapes")

        print(f" > Scraping {scrape_limit} posts from r/{sub_name}...")

        with open("savedscrapes/" + sub_name + "-" + str(sub_sort) + "-" + str(scrape_limit) + ".txt", "a", encoding="utf-8") as file:
            for submission in getSortedSubreddit(subreddit, sub_sort)(limit = scrape_limit):
                postCount += 1
                permaURL = "https://www.reddit.com/"+submission.permalink
                print("\n > " + str(postCount) + ". " + submission.title)
                print("   - " + permaURL)

                file.write("\n\n" + str(postCount) + ". " + submission.title)
                file.write(" - " + permaURL)

                # print(submission.url)
        file.close()

        print(f"\n > Found {postCount} post(s).")

        userSave = input("\nSave scraped posts? (y/n) : ")
        if userSave.lower() == "y" or userSave.lower() == "yes":               
            print(" > Saved data to a text file successfully!")
        else:
            if os.path.exists(os.getcwd() + "/savedscrapes/" + sub_name + "-" + str(sub_sort) + "-" + str(scrape_limit) + ".txt"):
                os.remove(os.getcwd() + "/savedscrapes/" + sub_name + "-" + str(sub_sort) + "-" + str(scrape_limit) + ".txt")
            else:
                pass
            print(" > Removed saved cache...")

    except:
        print("ERROR!")


def scrapeImages(sub_name, sub_sort, scrape_limit):

    if os.path.exists(os.getcwd() + "/images"):
        pass
    else:
        os.mkdir(os.getcwd() + "/images")

    subreddit = reddit.subreddit(sub_name)
  
    imageCount = 0
    galleryCount = 0

    print(f" > Scraping {scrape_limit} posts from r/{sub_name} for images...")

    for submission in getSortedSubreddit(subreddit, sub_sort)(limit = scrape_limit):
        subURL = submission.url
        if "i.redd.it" in subURL.lower():  
            if "jpg" in subURL.lower() or "jpeg" in subURL.lower():
                image = requests.get(subURL)
                with open("images/" + sub_name + "-" + submission.id + ".jpg", "wb") as file:
                    file.write(image.content)
                file.close()
                imageCount += 1
            elif "png" in subURL.lower():
                image = requests.get(subURL)
                with open("images/" + sub_name + "-" + submission.id + ".png", "wb") as file:
                    file.write(image.content)
                file.close()
                imageCount += 1
        elif "www.reddit.com/gallery" in subURL.lower():
            print()
            RedDownloader.Download(url = subURL , output=sub_name + "-" + submission.id , destination="images/")
            galleryCount += 1

    print(f"\n > Found {imageCount} image(s).")
    if imageCount > 0:
        print(f" > Saved {imageCount} image(s).")
    if galleryCount > 0:
        print(f"\n > Found {galleryCount} gallery(s).")


def scrapeVideos(sub_name, sub_sort, scrape_limit, quality):

    if os.path.exists(os.getcwd() + "/videos"):
        pass
    else:
        os.mkdir(os.getcwd() + "/videos")

    subreddit = reddit.subreddit(sub_name)

    videoCount = 0

    print(f" > Scraping {scrape_limit} posts from r/{sub_name} for videos...")
    
    for submission in getSortedSubreddit(subreddit, sub_sort)(limit = scrape_limit):
        if "v.redd.it" in submission.url.lower():
            permaURL = "https://www.reddit.com/"+submission.permalink
            RedDownloader.Download(url = permaURL , output=sub_name + "-" + submission.id , destination="videos/" , quality = quality)
            # print(permaURL)
            videoCount += 1
    print(f" > Found {videoCount} video(s).")

        
def menu():
    print("\n----------------")
    print(" Reddit Scraper ")
    print("----------------")
    print("1. Post URLs")
    print("2. Images")
    print("3. Videos")
    print("q. Quit")
    userChoice = input("\nWhat do you want to scrape? ")
    return userChoice


def printSortMethods():
    print(" 1.hot")
    print(" 2.new")
    print(" 3.rising")
    print(" 4.gilded")
    print(" 5.controversial")    
    print(" 6.top of all time")

    
def getSortedSubreddit(subreddit, sort):
    sub_sort_dict = {
        1 : subreddit.hot,
        2 : subreddit.new,
        3 : subreddit.rising,
        4 : subreddit.gilded,
        5 : subreddit.controversial,
        6 : subreddit.top
    }
    return sub_sort_dict[sort]


def main():
    
    initReddit()

    isRunning = True

    while isRunning:
        userChoice = menu()
        if userChoice == "1":
            userSub = input("Enter subreddit name: ")
            printSortMethods()
            userSort = int(input("Enter sort method: "))
            userLimit = int(input("How many posts to scrape: "))
            scrapePosts(userSub, userSort, userLimit)

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

            print("Avaliable options to choose from are 360, 480, 720, 1080")
            print("If a video file in specified resolution is not found it will try for a lower resolution")

            userQuality = int(input("Enter video quality: "))
            scrapeVideos(userSub, userSort, userLimit, userQuality)

        elif userChoice.lower() == "q":
            isRunning = False

        else:
            print("Wrong input! Try again!")


if __name__ == "__main__":
    main()
