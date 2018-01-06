import requests
import json
from pprint import pprint
from bs4 import BeautifulSoup

url = "https://www.rottentomatoes.com"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def search_rt(query):
    query = "/search/?search=" + query
    search_query = url + query
    response = requests.get(search_query, headers=headers)
    htmldoc = response.text
    movies_json =  json.loads("{" + htmldoc[htmldoc.index("\"movies\":[") : htmldoc.index("\"tvCount\"")-1] + "}")
    return movies_json

def get_scores(movie_url):
    response = requests.get(movie_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    aud_score = soup.findAll("div", {"class": "meter-value"})[0].contents[1].contents[0]
    aud_rating = soup.findAll("div", {"class": "audience-info hidden-xs superPageFontColor"})[0].contents[1].contents[2].strip(' \t\n\r')
    all_crit_score = soup.findAll("span", {"class": "meter-value"})[0].contents[0].contents[0] + "%"
    top_crit_score = soup.findAll("span", {"class": "meter-value"})[1].contents[0].contents[0] + "%"
    all_crit_rating = soup.findAll("div", {"class": "superPageFontColor"})[0].contents[2].strip(' \t\n\r')
    top_crit_rating = soup.findAll("div", {"class": "superPageFontColor"})[4].contents[2].strip(' \t\n\r')
    return aud_rating, aud_score, all_crit_rating, all_crit_score, top_crit_rating, top_crit_score

def main():
    query = input("Give me a movie name: ")
    movies_json = search_rt(query)
    i = 1
    for movie in movies_json["movies"]:
        print(str(i) + "). \t" + movie["name"])
        i = i + 1
    print("")
    element = int(input("Which element? " )) - 1
    movie = url + movies_json["movies"][element]["url"]
    print(get_scores(movie))

if __name__ == "__main__":
    main()
