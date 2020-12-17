# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 20:21:33 2020

@author: Tarun Ravi
"""

import requests
from bs4 import BeautifulSoup

def fetchLinks(sourceURL, headURL):
    page = requests.get(sourceURL)
    
    soup = BeautifulSoup(page.content, 'lxml') 
    #lxml best for dynamic pages, try html.parser if that doesnt work
    
    rawCode = soup.prettify()
    
    #Looks in the HTML for divs with the zn-body__paragraph name, then adds that to bodyPar var
    linkRaw = soup.find_all('div','c-compact-river__entry')
    links = []
    for i in linkRaw:
        i = str(i)
        i = i[i.find('href')+6:]
        i = i[:i.find('>')-1]
        links.append(i)
    
    return links

def voxArticle(URL):   
    page = requests.get(URL)
    
    soup = BeautifulSoup(page.content, 'lxml') 
    #lxml best for dynamic pages, try html.parser if that doesnt work
    
    rawCode = soup.prettify()
    
    #Looks in the HTML for divs with the zn-body__paragraph name, then adds that to bodyPar var
    bodyParRaw = soup.find_all('div', class_='c-entry-content')
    bodyPar = ""
    for i in bodyParRaw:
        bodyPar += i.text
    
    #Grabs the headline and adds it to the bodyPar var
    headlineRaw = soup.find_all('p', class_='c-entry-summary p-dek')
    headline = ""
    for i in headlineRaw:
        headline += i.text
    
    bodyPar = headline + bodyPar
    
    #Graphs the title and adds that to the title var    
    titleRaw = soup.find_all('h1', class_='c-page-title')
    title = ""
    for i in titleRaw:
        title += i.text
    
    #returns the title and body paragraph
    return (title.strip(), bodyPar.strip(), URL)

def getAllArticles(links):
    data = []
    for link in links:
        data.append(list(voxArticle(link)))

    return data

links = fetchLinks("https://www.vox.com/policy-and-politics", "https://www.vox.com/")
data = getAllArticles(links)

import pandas as pd

my_df = pd.DataFrame(data)

my_df.to_csv('vox.csv', index=False, header=False)
