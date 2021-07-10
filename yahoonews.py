# importing python libraries
import re
import csv
from time import sleep
from bs4 import BeautifulSoup
import requests

# headers from html code in inspect element 
headers = {
    'accept': '*/*' ,
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'referer': 'https://www.google.com',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
 
}
 
 # function that extracts information from the raw html 
def get_article(card):
    headline = card.find('h4', 's-title').text
    source = card.find("span", 's-source').text
    posted = card.find('span', 's-time').text.replace('.','').strip()
    article = (headline, source, posted)
    return article

 # function that accepts a single arguement(search term/phrase)
def get_the_news(search):

    template = 'https://news.search.yahoo.com/search?p={}'
    url = template.format(search)
    articles = []

 #scraping loop and finds the next page's url
    while True:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        cards = soup.find_all('div','NewsArticle')

        for card in cards:
            article = get_article(card)
            articles.append(article)

        try:
            url = soup.find('a', 'next').get('href')
            sleep(1)
        except AttributeError:
             break

    print(articles[:5])

    #saving article data to a csv file 
    with open('results.csv','w', newline='',encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Headline', 'Source', 'Posted'])
        writer.writerows(articles)

    return articles

# shows the headline, source, and date posted after entering a news topic 
articles = get_the_news('Federal Bank Interest Rate')

