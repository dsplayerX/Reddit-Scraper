import praw
import prawcore
import requests
import os
from RedDownloader import RedDownloader
from data.config_cred import *

# REDDIT SCRAPER by dsplayerX

def initReddit():

    global reddit

    if os.path.exists(os.getcwd() + "/data/creds.txt"):
        creds = decodeCreds()
        userID = creds[0]
        userSecret = creds[1]
    else:
        print("> Credits token not found! Enter your details below to create one.")
        userID = input("Enter your Client ID: ")
        userSecret = input("Enter your Client Secret: ")
        encodeCreds(userID, userSecret)
        print("> Credentials saved!")

    reddit = praw.Reddit(
        client_id=userID,
        client_secret=userSecret,
        user_agent="reddit-scraper",
        username="",
        password="",
        )


def scrapePosts(sub_name, sub_sort, scrape_limit):

    subreddit = reddit.subreddit(sub_name)

    postCount = 0

    if os.path.exists(os.getcwd() + "/savedscrapes"):
        pass
    else:
        os.mkdir(os.getcwd() + "/savedscrapes")

    print(f" > Scraping {scrape_limit} posts from r/{sub_name}...")

    try:
        with open("savedscrapes/" + sub_name + "-" + str(sub_sort) + "-" + str(scrape_limit) + ".txt", "a", encoding="utf-8") as file:
            for submission in getSortedSubreddit(subreddit, sub_sort)(limit = scrape_limit):
                postCount += 1
                permaURL = "https://www.reddit.com/"+submission.permalink
                print("\n > " + str(postCount) + ". " + submission.title)
                print("   - " + permaURL)
                # print(submission.url)
                file.write("\n\n" + str(postCount) + ". " + submission.title)
                file.write(" - " + permaURL)
        file.close()
        print(f"\n > Found {postCount} post(s).")
    except (prawcore.exceptions.NotFound, prawcore.exceptions.Redirect):
        print(">> ERROR: Invalid Subreddit!")
    except (praw.exceptions.PRAWException, prawcore.exceptions.PrawcoreException) as e:
        print(">> ERROR: Reddit API Error - " + e)

    userSave = input("\nSave scraped posts? (y/n) : ")
    if userSave.lower() == "y" or userSave.lower() == "yes":               
        print(" > Saved data to a text file successfully!")
    else:
        if os.path.exists(os.getcwd() + "/savedscrapes/" + sub_name + "-" + str(sub_sort) + "-" + str(scrape_limit) + ".txt"):
            os.remove(os.getcwd() + "/savedscrapes/" + sub_name + "-" + str(sub_sort) + "-" + str(scrape_limit) + ".txt")
        else:
            pass
        print(" > Removed saved cache...")


def scrapeImages(sub_name, sub_sort, scrape_limit):

    if os.path.exists(os.getcwd() + "/images"):
        pass
    else:
        os.mkdir(os.getcwd() + "/images")

    subreddit = reddit.subreddit(sub_name)
  
    imageCount = 0
    galleryCount = 0

    print(f" > Scraping {scrape_limit} posts from r/{sub_name} for images...")
    try:
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
    except (prawcore.exceptions.NotFound, prawcore.exceptions.Redirect):
        print(">> ERROR: Invalid Subreddit!")
    except (praw.exceptions.PRAWException, prawcore.exceptions.PrawcoreException) as e:
        print(">> ERROR: Reddit API Error - " + e)

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
    try:
        for submission in getSortedSubreddit(subreddit, sub_sort)(limit = scrape_limit):
            try:
                if "v.redd.it" in submission.url.lower():
                    permaURL = "https://www.reddit.com/"+submission.permalink
                    RedDownloader.Download(url = permaURL , output=sub_name + "-" + submission.id , destination="videos/" , quality = quality)
                    # print(permaURL)
                    videoCount += 1
            except:
                print(">> ERROR: Video Downloading Failed!")
    except (prawcore.exceptions.NotFound, prawcore.exceptions.Redirect):
        print(">> ERROR: Invalid Subreddit!")
    except (praw.exceptions.PRAWException, prawcore.exceptions.PrawcoreException) as e:
        print(">> ERROR: Reddit API Error - " + e)

    print(f" > Found {videoCount} video(s).")

        
def menuChoice():
    print("\n------------------")
    print("| Reddit Scraper |")
    print("------------------")
    print("\nSelect what you want to do.")
    print("\n 1. Scrape Post URLs")
    print(" 2. Scrape Images")
    print(" 3. Scrape Videos")
    print("\n q. Quit\n")

    userChoices = ["1", "2", "3", "q"]
    while True:
        try:
            userChoice = input("Enter your choice: ")
        except:
            print("Try again!")
            continue
        else:
            if userChoice.lower() in userChoices:
                break
            else:
                print("> Select number from the given options!")
                continue
    return userChoice


def printSortMethods():
    print("\nSorting Methods for Subreddits")
    print(" 1. Hot")
    print(" 2. New")
    print(" 3. Rising")
    print(" 4. Gilded")
    print(" 5. Controversial")    
    print(" 6. Top of all time")

    
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


def getUserInputs():
    userSub = input("\nEnter subreddit name: ")
    printSortMethods()

    while True:
        try:
            userSort = int(input("Enter sort method: "))
        except ValueError:
            print("> You have to enter an integer!")
            continue
        else:
            if userSort >= 1 and userSort <=6:
                break
            else:
                print("> Select from the options above!")
                continue

    while True:
        try:
            userLimit = int(input("How many posts to scrape: "))
        except ValueError:
            print("> You have to enter an integer!")
            continue
        else:
            break

    return userSub, userSort, userLimit


def main():
    
    initReddit()

    isRunning = True

    while isRunning:

        userChoice = menuChoice()

        if userChoice == "1":
            scrapePosts(*getUserInputs())

        elif userChoice == "2":
            scrapeImages(*getUserInputs())

        elif userChoice == "3":
            userInputs = getUserInputs()
            
            # Getting video quality input from user
            videoQualities = [360, 480, 720, 1080]
            print("\nSelect Video Quality")
            print("  > Avaliable options to choose from are 360, 480, 720, 1080")
            print("  > If a video file in specified resolution is not found, will try for a lower resolution")
            while True:
                try:
                    userQuality = int(input("Enter video quality: "))
                except ValueError:
                    print("> Enter video quality in integers!")
                    continue
                else:
                    if userQuality in videoQualities:
                        break
                    else:
                        print("> Enter a video quality from the given options!")

            scrapeVideos(*userInputs, userQuality)

        elif userChoice.lower() == "q":
            isRunning = False

        else:
            print("Wrong input! Try again!")


if __name__ == "__main__":
    main()
