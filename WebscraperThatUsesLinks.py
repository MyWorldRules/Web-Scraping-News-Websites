"""
Created on Thu Nov 26

@author: Tarun Ravi
"""

from bs4 import BeautifulSoup 
from selenium import webdriver 

#url of the page we want to scrape 
url = "https://www.cnn.com/us"
  
# initiating the webdriver. Parameter includes the path of the webdriver. 
driver = webdriver.Edge('edgeDriver/edgedriver_win64/msedgedriver.exe')  

#It is possible to change the options to .headless so a window doesnt physically open up. But this only works on the Chrome webdrivers not edge.
#Opens and loads the website
driver.get(url)  
  
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
        links.append("https://www.cnn.com"+i)

#Removes any duplicate links
links = list(dict.fromkeys(links))

