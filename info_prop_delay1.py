# ======================================================================================== 
#__Author__ = "Siyona Behera"
#__Copyright__ = "Copyright Oct, 2021, Information Propagation Delay Modeling Project"
#__License__ = "None"
#__Version__ = "1.0.1"
#__Maintainer__ = "Siyona Behera"
#__Email__ = "beherasiyona@gmail.com"
#__Status__ = "Beta Testing"
# ========================================================================================
 
#import what we need
from requests_html import HTMLSession
import csv
import operator
from bs4 import BeautifulSoup
from time import sleep
import requests
import re
from datetime import date
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from fuzzywuzzy import fuzz, process
 
#Definitions of all Functions used in the main program
 
#Get the 'header' and 'date posted' info from a news article using "h3" and "div" tag, then process the data to standard "list" format 
 
def get_source_name(list):
    if (list[len(list)-1] == "ago"):
        if (len(list) == 7):
            source = (list[0]+" "+list[1]+" "+list[2]+" "+list[3])
        if (len(list) == 6):
            source = (list[0]+" "+list[1]+" "+list[2])  
        if (len(list) == 5):
            source = (list[0]+" "+list[1])
        if (len(list) == 4):
            source = (list[0])
    if (list[len(list)-2] == "Jan") or (list[len(list)-2] == "Feb") or (list[len(list)-2] == "Mar") or (list[len(list)-2] == "Apr") or (list[len(list)-2] == "May") or (list[len(list)-2] == "Jun") or (list[len(list)-2] == "Jul") or (list[len(list)-2] == "Aug") or (list[len(list)-2] == "Sep") or (list[len(list)-2] == "Oct") or (list[len(list)-2] == "Nov") or (list[len(list)-2] == "Dec"):
        if (len(list) == 7):
            source = (list[0]+" "+list[1]+" "+list[2]+" "+list[3]+" "+list[4])
        if (len(list) == 6):
            source = (list[0]+" "+list[1]+" "+list[2]+" "+list[3])  
        if (len(list) == 5):
            source = (list[0]+" "+list[1]+" "+list[2])
        if (len(list) == 4):
            source = (list[0]+" "+list[1])    
        if (len(list) == 3):
            source = (list[0])  
    if (list[len(list)-1] == "Yesterday"):      
        if (len(list) == 5):
            source = (list[0]+" "+list[1]+" "+list[2]+" "+list[3])
        if (len(list) == 4):
            source = (list[0]+" "+list[1]+" "+list[2])    
        if (len(list) == 3):
            source = (list[0]+" "+list[1])             
    return source
 
def get_article_full(card):
    headline = card.find('h3', first=True).text
    posted = (card.find('div', first=True).text).split("\nbookmark_border\nshare\nmore_vert")[0]
    pdate = re.sub("[A-Za-z]+", lambda ele: " " + ele[0] + " ", posted)
    #print(pdate)
  
    date1 = pdate.replace("Jan", " Jan")
    date2 = date1.replace("Feb", " Feb")
    date3 = date2.replace("Mar", " Mar")
    date4 = date3.replace("Apr", " Apr")
    date5 = date4.replace("May", " May")
    date6 = date5.replace("Jun", " Jun")
    date7 = date6.replace("Jul", " Jul")
    date8 = date7.replace("Aug", " Aug")
    date9 = date8.replace("Sep", " Sep")
    date10 = date9.replace("Oct", " Oct")
    date11 = date10.replace("Nov", " Nov")
    date12 = date11.replace("Dec", " Dec")
    date13 = date12.replace("Yesterday", " Yesterday")
    final_date = date12.replace(",","").split()
    #print(final_date)
 
    if (final_date[len(final_date)-2] == "days") or (final_date[len(final_date)-2] == "day"):
        time = (final_date[(len(final_date)-3)]+" "+final_date[(len(final_date)-2)]+" "+final_date[(len(final_date)-1)])
        source = get_source_name(final_date)
        days = max(-30, -1 * int(final_date[len(final_date)-3]))
    
    if (final_date[len(final_date)-2] == "hours") or (final_date[len(final_date)-2] == "hour") or (final_date[len(final_date)-2] == "minutes") or (final_date[len(final_date)-2] == "minute") or (final_date[len(final_date)-1] == "yesterday"):
        time = (final_date[(len(final_date)-3)]+" "+final_date[(len(final_date)-2)]+" "+final_date[(len(final_date)-1)])
        source = get_source_name(final_date)
        days = -1
 
    if (final_date[len(final_date)-1] == "Yesterday"):
        time = ("1 day ago")
        source = get_source_name(final_date)
        days = -1
 
    if (final_date[len(final_date)-2] == "May"):
        time = (final_date[(len(final_date)-2)]+" "+final_date[(len(final_date)-1)])
        source = get_source_name(final_date)
        days = -1 * (int(date.today().month) - 5) * 30 - int(date.today().day) + int(final_date[len(final_date)-1])
    if (final_date[len(final_date)-2] == "Jun"):
        time = (final_date[(len(final_date)-2)]+" "+final_date[(len(final_date)-1)])
        source = get_source_name(final_date)
        days = -1 * (int(date.today().month) - 6) * 30 - int(date.today().day) + int(final_date[len(final_date)-1])
    if (final_date[len(final_date)-2] == "Jul"):
        time = (final_date[(len(final_date)-2)]+" "+final_date[(len(final_date)-1)])
        source = get_source_name(final_date)
        days = -1 * (int(date.today().month) - 7) * 30 - int(date.today().day) + int(final_date[len(final_date)-1])
    if (final_date[len(final_date)-2] == "Aug"):
        time = (final_date[(len(final_date)-2)]+" "+final_date[(len(final_date)-1)])
        source = get_source_name(final_date)
        days = -1 * (int(date.today().month) - 8) * 30 - int(date.today().day) + int(final_date[len(final_date)-1])
    if (final_date[len(final_date)-2] == "Sep"):
        time = (final_date[(len(final_date)-2)]+" "+final_date[(len(final_date)-1)])
        source = get_source_name(final_date)
        days = -1 * (int(date.today().month) - 9) * 30 - int(date.today().day) + int(final_date[len(final_date)-1])
    if (final_date[len(final_date)-2] == "Oct"):
        time = (final_date[(len(final_date)-2)]+" "+final_date[(len(final_date)-1)])
        source = get_source_name(final_date)
        days = -1 * (int(date.today().month) - 10) * 30 - int(date.today().day) + int(final_date[len(final_date)-1])
    if (final_date[len(final_date)-2] == "Nov"):
        time = (final_date[(len(final_date)-2)]+" "+final_date[(len(final_date)-1)])
        source = get_source_name(final_date)
        days = -1 * (int(date.today().month) - 11) * 30 - int(date.today().day) + int(final_date[len(final_date)-1])
    if (final_date[len(final_date)-2] == "Dec"):
        time = (final_date[(len(final_date)-2)]+" "+final_date[(len(final_date)-1)])
        source = get_source_name(final_date)
        days = -1 * (int(date.today().month) - 12) * 30 - int(date.today().day) + int(final_date[len(final_date)-1])
 
    article = (headline, source, time, days)
    return article
 
def get_sorted_articles(list):
    articles_sort = []
    i=0
    for e in list:
       if i==list.index(e):
            date = e
            frequency = list.count(e)
            article_sort = (date, frequency)
            articles_sort.append(article_sort)
       i+=1
    return articles_sort
 

#Start main program
session = HTMLSession()
search = "Chip shortage"
template = 'https://news.google.com/search?q={}&hl=en-US&gl=US&ceid=US%3Aen'
url = template.format(search)
r = session.get(url)
 
#render the html, sleep=1 to give it a second or two to finish before moving on. scrolldown= how many times to page down on the browser, to get more results. 10 was a good number here
r.html.render(sleep=1, scrolldown=10)
 
#find all the articles by using inspect element and create blank list
articles = r.html.find('article')
fullnewslist = []
fullnewslist_sorted = []
daysfield = []
 
#loop through each article and print each article's header, source, time posted and days in [] format and then sort based on days field 
for item in articles:
    try:
        fullnews = get_article_full(item)
        fullnewslist.append(fullnews)
    except:
       pass
 
fullnewslist_sorted = sorted(fullnewslist, key=operator.itemgetter(3))
print(fullnewslist_sorted)
 
#Write filtered news title, source, date and days into a csv file
with open(search + '.csv','w', newline='',encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Headline', 'Source', 'Date', 'Days'])
    writer.writerows(fullnewslist_sorted)
 
#Print days filed in sorted order 
for item in fullnewslist_sorted:
    try:
        field = int(item[3])
        daysfield.append(field)
    except:
       pass
articles_days = daysfield
articles_days.sort()
sorted_articles_days = get_sorted_articles(articles_days)
 
#Write Days ago and Frequency into a csv file
with open(search + '_Date_Freq.csv','w',newline='',encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Days ago','Frequency' ])
    writer.writerows(sorted_articles_days)
 

#Using Pandas dataframe to calculate Propagation Delay of a perticular news item
date_freq = pd.read_csv(search + '_Date_Freq.csv')
max_date = date_freq.set_index('Days ago').idxmax()
prop_delay = max_date[0] - sorted_articles_days[0][0]
print('')
print('Average propagation delay for the news article', '"',search,'"', 'is', prop_delay, 'days')
print('')
 
#Setting up X and Y variable from the Date_Freq csv file for plot
with open(search + "_Date_Freq.csv", "r") as i:
    rawdata = list(csv.reader(i,delimiter = ",")) 
exampledata = np.array(rawdata[1:],dtype=float)
xdata = exampledata[:,0]
ydata = exampledata[:,1]
plt.figure(1,dpi=120)
plt.title("News articles VS Date Plot")
plt.xlabel(rawdata[0][0])
plt.ylabel(rawdata[0][1])
plt.plot(xdata,ydata,label=search)
plt.legend(loc="upper left")
plt.show()