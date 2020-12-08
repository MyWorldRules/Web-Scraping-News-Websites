# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 15:35:58 2020

@author: Tarun Ravi
"""

from bs4 import BeautifulSoup
import requests
from selenium import webdriver 

def fetchLinks(sourceURL, headURL):
    page = requests.get(sourceURL)
    
    soup = BeautifulSoup(page.content, 'lxml') 
    #lxml best for dynamic pages, try html.parser if that doesnt work
    
    rawCode = soup.prettify()
    
    #Looks in the HTML for divs with the zn-body__paragraph name, then adds that to bodyPar var
    linkRaw = soup.find_all('article','article')
    links = []
    for i in linkRaw:
        i = str(i)
        i = i[i.find('href')+6:]
        i = i[:i.find('>')-1]
        links.append(headURL+i)

    return links

def foxArticle(URL):    
    page = requests.get(URL)
    
    soup = BeautifulSoup(page.content, 'lxml') 
    #lxml best for dynamic pages, try html.parser if that doesnt work
    
    rawCode = soup.prettify()
    
    #Looks in the HTML for divs with the zn-body__paragraph name, then adds that to bodyPar var
    bodyParRaw = soup.find_all('div', class_='article-body')
    bodyPar = ""
    for i in bodyParRaw:
        bodyPar += i.text
    
    
    #Graphs the title and adds that to the title var    
    titleRaw = soup.find_all('h1', class_='headline')
    title = ""
    for i in titleRaw:
        title += i.text
    return (title.strip(), bodyPar.strip(), URL)

#Just loops through the articles
def getAllArticles(links):
    data = []
    for link in links:
        data.append(list(foxArticle(link)))

    return data

links = fetchLinks("https://www.foxnews.com/politics", "https://www.foxnews.com")
data = getAllArticles(links)

import pandas as pd

my_df = pd.DataFrame(data)

my_df.to_csv('fox.csv', index=False, header=False)
