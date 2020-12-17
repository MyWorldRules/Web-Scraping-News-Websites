import requests
from bs4 import BeautifulSoup
from time import sleep

def dailyCallerArticle(URL):    
    try:
        page = requests.get(URL)
    except requests.exceptions.ConnectionError:
        return []
        
    soup = BeautifulSoup(page.content, 'lxml') 
    #lxml best for dynamic pages, try html.parser if that doesnt work
    
    rawCode = soup.prettify()
    
    #Looks in the HTML for divs with the zn-body__paragraph name, then adds that to bodyPar var
    bodyParRaw = soup.find_all('div', id='ob-read-more-selector')
    bodyPar = ""
    for i in bodyParRaw:
        bodyPar += i.text
    
    
    #Graphs the title and adds that to the title var    
    titleRaw = soup.find_all('h1', class_='mb-6 xl:mb-10 leading-tight font-oswald font-medium')
    title = ""
    for i in titleRaw:
        title += i.text
    
    #returns the title and body paragraph
    
    return (title.strip(), bodyPar.strip(), URL)

def fetchLinks(sourceURL, headURL): 
    page = requests.get(sourceURL)
    
    soup = BeautifulSoup(page.content, 'lxml') 
    #lxml best for dynamic pages, try html.parser if that doesnt work
    
    rawCode = soup.prettify()
    
    #Looks in the HTML for divs with the zn-body__paragraph name, then adds that to bodyPar var
    linkRaw = soup.find_all('li', class_="md:w-1/2 px-4 mb-6 landing")
    links = []
    for i in linkRaw:
        i = str(i)
        i = i[i.find('href')+6:]
        i = i[:i.find('>')-1]
        i = i[:i.find('"')-1]
        if i[:4]=="http":
            pass
        links.append(headURL+i)
        
    return links

def getAllArticles(links):
    data = []
    for link in links:
        data.append(list(dailyCallerArticle(link)))
        print("done")

    return data


links = fetchLinks("https://dailycaller.com/section/politics/", "https://dailycaller.com")
data = getAllArticles(links)

import pandas as pd

my_df = pd.DataFrame(data)

my_df.to_csv('dailyclub.csv', index=False, header=False)
