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
        self.status = None
        self.genre = None
        self.category = None
        self.summary = None

    def optionDisplay(self):
        print(self.title)
        print(f"Poster Image: {self.img}")
        print(f"Watch Link: {self.siteLink}")
        print(f"Release Year: {self.release}")
        print()

    def detailedDisplay(self):
        print(self.title)
        print("--------------")
        print(f"Release Year: {self.release}")
        print(f"Status: {self.status}")
        print()
        print(f"Poster Image: {self.img}")
        print()
        print(f"Type: {self.category}")
        print()
        print(f"Plot Summary: {self.summary}")
        print()
        print(f"Genre(s): {self.genre}")
        print()
        print(f"Watch Link: {self.siteLink}")
        
    

def displayAll(choices):
    for i in choices:
        i.optionDisplay()

load_dotenv('.env')
searchRequest: str = os.getenv('WANTED_ANIME')
targetSite: str = os.getenv('TARGET_SITE')
selectedOption: int = os.getenv('CHOICE')

def generateOptions(requestedAnime):
    html_content = requests.get(targetSite+"/search.html?keyword="+requestedAnime).text
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
    return choices

choices = generateOptions(searchRequest)

def obtainMoreInfo(selectionNumber):
    html_content = requests.get(targetSite+"/category/"+choices[selectionNumber-1].seriesID).text
    soup = BeautifulSoup(html_content,"lxml")
    rawDetails = soup.find_all("p",class_="type")
    choices[selectionNumber-1].category = rawDetails[0].find("a").text
    choices[selectionNumber-1].summary = rawDetails[1].text[14:]
    choices[selectionNumber-1].genre = rawDetails[2].text[8:]
    choices[selectionNumber-1].status = rawDetails[4].text[9:-1]





    

