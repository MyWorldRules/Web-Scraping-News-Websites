# -*- coding: utf-8 -*-
"""
Created on Wed Dec  2 15:35:58 2020

@author: Tarun Ravi
"""

from bs4 import BeautifulSoup
import requests
from selenium import webdriver 

def fetchLinks(sourceURL, headURL):
    #url of the page we want to scrape 
      
    # initiating the webdriver. Parameter includes the path of the webdriver. 
    driver = webdriver.Edge('edgeDriver/edgedriver_win64/msedgedriver.exe')  
    
    #It is possible to change the options to .headless so a window doesnt physically open up. But this only works on the Chrome webdrivers not edge.
    #Opens and loads the website
    driver.get(sourceURL)  
      
    #This is just to ensure that the page is loaded 
    #time.sleep(5)  
        
    # this renders the JS code and stores all 
    # of the information in static HTML code. 
    html = driver.page_source 
    
    
    # Now, we could simply apply bs4 to html variable 
    soup = BeautifulSoup(html, "html.parser") 
    
    driver.close() # closing the webdriver 
    
    #Format the HTML
    rawCode = soup.prettify()
    
    #Grab only the cd__content stuff, this contains the links of articles
    linksRaw = soup.find_all('div', class_='cd__content')
    
    #list of links
    links = []
    
    #Only extracts the usable cnn article links
    for i in linksRaw:
        i = str(i)
        i = i[i.find('href')+6:]
        i = i[:i.find('">')]
        if (i[-4:] == "html" and i[:8]!="https://"):
            links.append(headURL+i)
    
    #Removes any duplicate links
    links = list(dict.fromkeys(links))
    
    return links

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
    return (title.strip(), bodyPar.strip(), URL)

#Just loops through the articles
def getAllArticles(links):
    data = []
    for link in links:
        data.append(list(cnnArticle(link)))

    return data

links = fetchLinks("https://www.cnn.com/us", "https://www.cnn.com")
data = getAllArticles(links)
