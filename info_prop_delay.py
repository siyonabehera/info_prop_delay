#__author__ = "Siyona Behera"
#__copyright__ = "Copyright 2021, Information Propagation Delay Modeling Project"
#__license__ = "None"
#__version__ = "1.0.1"
#__maintainer__ = "Siyona Behera"
#__email__ = "beherasiyona@gmail.com"
#__status__ = "Beta Testing"


# importing python libraries
import re
import csv
from time import sleep
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# headers from html code in inspect element 
headers = {
    'accept': '*/*' ,
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'referer': 'https://www.google.com',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
 
}
 

# function that extracts information from the raw html 
def get_article(card):
    headline = card.find('h4', 's-title').text
    source = card.find("span", 's-source').text
    posted = card.find('span', 's-time').text.replace('.','').strip()
    article = (headline, source, posted)    
    return article


# converts the time(how long ago news was posted) to days 
def get_article_trim(card):
    headline = card.find('h4', 's-title').text
    source = card.find("span", 's-source').text
    posted = card.find('span', 's-time').text.replace('.','').strip()
    posted_number = card.find('span', 's-time').text.split()[1]
    posted_day    = card.find('span', 's-time').text.split()[2]
    if posted_day == "hour" or posted_day == "hours" or posted_day == "minute" or posted_day == "minutes":
        posted_days = -1
    if posted_day == "day" or posted_day == "days":
        posted_days = -1 * int(posted_number) 
    if posted_day == "week" or posted_day == "weeks":
            posted_days = -7 * int(posted_number)   
    if posted_day == "month" or posted_day == "months":
        posted_days = int(posted_number) * (-30)
    if posted_day == "year" or posted_day == "years":
        posted_days = int(posted_number) * (-365) 
    article_trim = (posted_days)
    return article_trim
 

# same as get_the_news except appends the articles(headline, source, posted)
def get_the_news_full(search):
    template = 'https://news.search.yahoo.com/search?p={}'
    url = template.format(search)  
    articles = []

 #scraping loop which appends the articles (headline, source, posted) and finds the next page's url
    while True:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            cards = soup.find_all('div','NewsArticle')
 
            for card in cards:
                article = get_article(card)
                articles.append(article)
 
            try:
                 url = soup.find('a','next').get('href')
                 sleep(1)
            except AttributeError:
                 break
 
    #writing article data to a csv file 
    with open('Full_report.csv','w',newline='',encoding='utf-8') as f:
         writer = csv.writer(f)
         writer.writerow(['Headline','Source','Posted' ])
         writer.writerows(articles)
 
    return articles


# function accepts a search argument and appends how long ago something was posted
def get_the_news(search):
    template = 'https://news.search.yahoo.com/search?p={}'
    url = template.format(search)  
    articles_trim = []
 
 #scraping loop which appends how long ago something was posted and finds the next page's url
    while True:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            cards = soup.find_all('div','NewsArticle')
 
            for card in cards:
                article_trim = get_article_trim(card)
                articles_trim.append(article_trim)        
                
 
            try:
                 url = soup.find('a','next').get('href')
                 sleep(1)
            except AttributeError:
                 break
 
    return articles_trim


# sorts articles by date 
def get_sorted_articles(list):
    articles_sort = []
    i=0
    for e in articles_trim:
       if i==articles_trim.index(e):
          # print(e,articles_trim.count(e))
            date = e
            if date > -30:
               frequency = articles_trim.count(e)
               article_sort = (date, frequency)
               articles_sort.append(article_sort)
            #print(articles_sort)
       i+=1

    #writing article data to a csv file 
    with open('Date_Freq.csv','w',newline='',encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Days ago','Frequency' ])
        writer.writerows(articles_sort)

    return articles_sort


# Main program 
search = 'Jack Ma missing'
articles = get_the_news_full(search) 
articles_trim = get_the_news(search)  
articles_trim.sort()
#print(articles_trim)
sorted_articles = get_sorted_articles(articles_trim)
#print(sorted_articles)
date_freq = pd.read_csv('Date_Freq.csv')
max_date = date_freq.set_index('Days ago').idxmax()
prop_delay = max_date[0] - sorted_articles[0][0]
print('')
print('Average propagation delay for the news article', '"',search,'"', 'is', prop_delay, 'days')
print('')

with open("Date_Freq.csv", "r") as i:
    rawdata = list(csv.reader(i,delimiter = ","))
 
exampledata = np.array(rawdata[1:],dtype=float)
xdata = exampledata[:,0]
ydata = exampledata[:,1]
 

#Plots the data
plt.figure(1,dpi=120)
plt.title("News articles VS Date Plot")
plt.xlabel(rawdata[0][0])
plt.ylabel(rawdata[0][1])
plt.plot(xdata,ydata,label=search)
#plt.boxplot(xdata,ydata)
plt.legend(loc="upper left")
plt.show()