# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30

@author: Tarun Ravi
"""

import requests
from bs4 import BeautifulSoup

def cnnArticle(URL):    
    page = requests.get(URL)
    
    soup = BeautifulSoup(page.content, 'lxml') 
    #lxml best for dynamic pages, try html.parser if that doesnt work
    
    rawCode = soup.prettify()
    
    #Looks in the HTML for divs with the zn-body__paragraph name, then adds that to bodyPar var
    bodyParRaw = soup.find_all('div', class_='zn-body__paragraph')
    bodyPar = ""
    for i in bodyParRaw:
        bodyPar += i.text
    
    #Grabs the headline and adds it to the bodyPar var
    headlineRaw = soup.find_all('p', class_='zn-body__paragraph speakable')
    headline = ""
    for i in headlineRaw:
        headline += i.text
    
    bodyPar = headline + bodyPar

    #Graphs the title and adds that to the title var    
    titleRaw = soup.find_all('h1', class_='pg-headline')
    title = ""
    for i in titleRaw:
        title += i.text
    
    #returns the title and body paragraph
    return (title.strip(), bodyPar.strip())

URL = "https://www.cnn.com/2020/12/02/politics/georgia-recount-results-brad-raffensperger/index.html"

title, bodyPar = cnnArticle(URL)
