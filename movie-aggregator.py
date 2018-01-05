import requests
import json
from pprint import pprint
from bs4 import BeautifulSoup

url = "https://www.rottentomatoes.com"
temp = input("Give me a movie name: ")
query = "/search/?search=" + temp
search_query = url + query

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

response = requests.get(search_query, headers=headers)

htmldoc = response.text
movies_json =  json.loads("{" + htmldoc[htmldoc.index("\"movies\":[") : htmldoc.index("\"}]});")+3] + "}")

element = int(input("Which element? " ))
movie_url = url + movies_json["movies"][element]["url"]
print(movie_url)

response = requests.get(movie_url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')

aud_score = soup.findAll("div", {"class": "meter-value"})[0].contents[1].contents[0]
all_crit_score = soup.findAll("span", {"class": "meter-value"})[0].contents[0].contents[0] + "%"
top_crit_score = soup.findAll("span", {"class": "meter-value"})[1].contents[0].contents[0] + "%"
all_crit_rating = soup.findAll("div", {"class": "superPageFontColor"})[0].contents[2].strip(' \t\n\r')
top_crit_rating = soup.findAll("div", {"class": "superPageFontColor"})[4].contents[2].strip(' \t\n\r')
aud_rating = soup.findAll("div", {"class": "audience-info hidden-xs superPageFontColor"})[0].contents[1].contents[2].strip(' \t\n\r')


print(aud_score + " of the audience gave a positive rating. The average score was a " + aud_rating + ".")
print(all_crit_score + " of all critics gave a positive rating. The average score was a " + all_crit_rating + ".")
print(top_crit_score + " of all top critics gave a positive rating. The average score was a " + top_crit_rating + ".") 

