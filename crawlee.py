import imdb  
import requests 
import time
from datetime import datetime
from bs4 import BeautifulSoup
import csv 

  
# creating instance of IMDb  
movie_obj = imdb.IMDb()  


notionNames = []
notionDates = []
failedNames = []
fields = ["Date", "Name", "Year", "Letterboxd URI"]
letterboxdDict = []

watchlist_names = []
watched_names = []


def convert_to_yyyy_mm_dd(date_str):
  try:
    # Try with time (February 10, 2022 10:19 PM)
    date_obj = datetime.strptime(date_str, "%B %d, %Y %I:%M %p")
  except ValueError:
    try:
      # Try without time (September 10, 2022)
      date_obj = datetime.strptime(date_str, "%B %d, %Y")
    except ValueError:
      # Invalid format
      return None
  return date_obj.strftime("%Y-%m-%d")


with open("../letterboxd-itssatix-2024-06-18-02-35-utc/watchlist.csv", "r", encoding="utf-8") as f:
  data = csv.DictReader(f)

  for row in data:
    watchlist_names.append(row["Name"])


with open("../letterboxd-itssatix-2024-06-18-02-35-utc/watched.csv", "r", encoding="utf-8") as f:
  data = csv.DictReader(f)

  for row in data:
    watched_names.append(row["Name"])


with open('towatch.csv', encoding="utf-8", mode='r') as csvfile:
 data = csv.DictReader(csvfile)
 for row in data:
    n = str(row["Name"])
    date = convert_to_yyyy_mm_dd(str(row["Last edited time"]))
    if not n in watchlist_names and not n in watched_names:  
      notionNames.append(n)
      notionDates.append(date)

def convert_to_letterboxd(text):
  replaced = text.replace(": ", "-").replace(" : ", "-").replace(" - ", "-").replace(" & ", "-").replace(" ", "-").replace(", ", "-").replace(", ", "-").replace(",", "-").replace("...", "-").replace("!", "").replace("'", "").replace("&", "").replace("?", "").lower()
  return replaced

# searching the movie 
for index, name in enumerate(notionNames): 
  print(name)
  search = movie_obj.search_movie(name)  
  try:
    # printing the result 
    print(notionDates[index])
    print(search[0]) 
    letterboxd_name = convert_to_letterboxd(str(search[0]))
    print(letterboxd_name)
    URL = f"https://letterboxd.com/film/{letterboxd_name}/" 
    r = requests.get(URL) 
      
    soup = BeautifulSoup(r.content, 'html5lib') 
      

    movieName = soup.find('span', attrs = {'class':'name js-widont prettify'}).text
    movieReleaseYear = soup.find('div', attrs = {'class':'releaseyear'}).a.text
    letterboxdURI = soup.find('div', attrs = {'class':'urlgroup'}).input["value"]
    if movieName and movieReleaseYear and letterboxdURI:
      # print(movieName)
      # print(movieReleaseYear)
      print(letterboxdURI)
      movie = {fields[0]: notionDates[index],fields[1]: movieName, fields[2]: movieReleaseYear, fields[3]: letterboxdURI}
      letterboxdDict.append(movie)
      print("✅✅✅✅")
      # print(letterboxdDict)
    else:
      failedNames.append(name)
      print("❌❌❌❌")
  except:
      failedNames.append(name)
      print("❌❌❌❌")
  
  print("-------------------------------------")
  time.sleep(5)

with open("test.csv", "w", encoding='UTF8', newline='') as f:
  # creating a csv dict writer object
  writer = csv.DictWriter(f, fieldnames=fields)

  # writing headers (field names)
  writer.writeheader()

  # writing data rows
  writer.writerows(letterboxdDict)

print(failedNames)


