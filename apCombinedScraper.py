# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 20:21:33 2020

@author: Tarun Ravi
"""

import requests
from bs4 import BeautifulSoup

URL = "https://apnews.com/article/joe-biden-environment-north-carolina-3067fc22ce4e1e0cbc3279c8af9bf67c"

def apArticle(URL):
    page = requests.get(URL)
    
    soup = BeautifulSoup(page.content, 'lxml') 
    #lxml best for dynamic pages, try html.parser if that doesnt work
    
    rawCode = soup.prettify()
    
    #Looks in the HTML for divs with the zn-body__paragraph name, then adds that to bodyPar var
    bodyParRaw = soup.find_all('div', class_='Article')
    bodyPar = ""
    for i in bodyParRaw:
        bodyPar += i.text
    
    #Graphs the title and adds that to the title var    
    titleRaw = soup.find_all('div', class_='CardHeadline')
    title = ""
    for i in titleRaw:
        i = str(i)
        i = i[i.index("h1"): i.index("</h1")]
        i = i[i.index(">")+1:]
        title += i

    return (title.strip(), bodyPar.strip(), URL)


def fetchLinks(sourceURL, headURL):
    page = requests.get(sourceURL)
    
    soup = BeautifulSoup(page.content, 'html.parser') 
    #lxml best for dynamic pages, try html.parser if that doesnt work
    
    rawCode = soup.prettify()
    
    #Needed for regex stuff
    import re 
    #Looks in the HTML for divs with the zn-body__paragraph name, then adds that to bodyPar var
    linkRaw = soup.find_all('a', class_=re.compile('Component-headline'))
    links = []
    for i in linkRaw:
        i = str(i)
        i = i[i.find('href')+6:]
        i = i[:i.find('>')-1]
        links.append(headURL+i)
    
    return links
    
def getAllArticles(links):
    data = []
    for link in links:
        data.append(list(apArticle(link)))

    return data

links = fetchLinks("https://apnews.com/hub/politics", "https://apnews.com/")
data = getAllArticles(links)

import pandas as pd

my_df = pd.DataFrame(data)

my_df.to_csv('ap.csv', index=False, header=False)
