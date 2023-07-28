from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup
import requests

class Anime:
    def __init__(self, siteLink, title, img, release, seriesID):
        self.siteLink = siteLink
        self.title = title
        self.img = img
        self.release = release
        self.seriesID = seriesID

    def display(self):
        print(self.title)
        print(f"Poster Image: {self.img}")
        print(f"Watch Link: {self.siteLink}")
        print(f"Series ID: {self.seriesID}")
        print(f"Release Year: {self.release}")
        print()

def displayAll(choices):
    for i in choices:
        i.display()

load_dotenv('.env')
wantedAnime: str = os.getenv('WANTED_ANIME')
targetSite: str = os.getenv('TARGET_SITE')
print(wantedAnime, targetSite)

html_content = requests.get(targetSite+"/search.html?keyword="+wantedAnime).text
soup = BeautifulSoup(html_content, "lxml")
searchResults = soup.find("ul", class_="items")
rawSources = searchResults.find_all("a")
rawDates = searchResults.find_all("p",class_="released")
dates=[]
sources = []
choices = []
for i in rawDates:
    dates.append(i.text.split('Released: ')[1].split(' ')[0])
for i in range(len(rawSources)):
    if (i%2==0):
        sources.append(rawSources[i])
for i in range(len(sources)):
    title = sources[i].get("title")
    linkStem = sources[i].get("href")
    seriesLink = targetSite+linkStem
    seriesID = linkStem.split('category/')[1]
    img = sources[i].find("img").get('src')
    releaseDate = dates[i]
    animeSeries = Anime(seriesLink,title,img,releaseDate,seriesID)
    choices.append(animeSeries)

    

