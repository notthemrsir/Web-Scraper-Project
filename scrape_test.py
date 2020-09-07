import sys
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

#Lucas Beal 2/11/2020 CS 3150

def fetchFromURL(url):
    """
    fetch content from URL via HTTP GET request.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                print("Error retrieving information") 
    except RequestException as e:
        log_error('Error during request to {0}:{1}' . format(url, str(e)))

def is_good_response(resp):
    """
    Returns true if response looks like HTML
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None 
            and content_type.find('html') > -1)

def log_error(e):
    """
    log the errors or you'll regret it later...
    """
    print(e)        

def grab_each_book_act(link):
    #MUST have a '/' at the end of the baseurl
    baseURL = 'http://shakespeare.mit.edu/'
    fullURL = baseURL + link
    print(fullURL)
    rawHTML = fetchFromURL(fullURL)   
    soup = BeautifulSoup(rawHTML, 'html.parser') 
    alllinks = []
    #Grab All Links
    for link in soup.find_all('a'):
        alllinks.append(link.get('href'))           
    relevantlinks = []
    #in order to correctly navigate to each webpage, must know name of work
    relevantlinksNamesOnly = []
    #Now Grab just the relevant links
    for link in alllinks:
        if "html" in link:
            if "full" not in link:
                relevantlinks.append(link)
                templist = link.split(".")
                relevantlinksNamesOnly.append(templist[0])
    for link2 in relevantlinks:
        #Counter set at zero, as all works passed in this method are all of the same singular composition
        #A new composition wouldn't occur until the method is called again, etc. 
        counter = 0
        fullURL2 = 'http://shakespeare.mit.edu/' + relevantlinksNamesOnly[counter] + '/' + link2
        print(fullURL2)
        rawHTML2 = fetchFromURL(fullURL2)      
        soup2 = BeautifulSoup(rawHTML2, 'html.parser')
        #This is necessary, as Python throws errors if trying to "Write in Bytes"
        linkandhtml = link2 + '.html'
        with open(linkandhtml, "w", encoding='utf-8') as file:
            file.write(str(soup2))

def grab_each_sonnet_act(link):
    #MUST have a '/' at the end of the baseurl
    baseURL = 'http://shakespeare.mit.edu/'
    fullURL = baseURL + link
    print(fullURL)
    rawHTML = fetchFromURL(fullURL)   
    soup = BeautifulSoup(rawHTML, 'html.parser') 
    alllinks = []
    #Grab All Links
    for link in soup.find_all('a'):
        alllinks.append(link.get('href'))           
    relevantlinks = []
    #Now Grab just the relevant links
    for link in alllinks:
        if "html" in link:
                relevantlinks.append(link)
    for link in relevantlinks:
        fullURL2 = 'http://shakespeare.mit.edu/Poetry/' + link
        rawHTML2 = fetchFromURL(fullURL2)      
        soup2 = BeautifulSoup(rawHTML2, 'html.parser')
        print(fullURL2)
        with open(link, "w", encoding='utf-8') as file:
            file.write(str(soup2))
        

def grab_each_poetry(link):
    #MUST have a '/' at the end of the baseurl
    baseURL = 'http://shakespeare.mit.edu/'
    fullURL = baseURL + link
    print(fullURL)
    rawHTML = fetchFromURL(fullURL)   
    soup = BeautifulSoup(rawHTML, 'html.parser') 
    documentname = link.split('/')
    #Because "elegy" is such a long work, it actually exceeds python's normal recursion limit,
    #therefore i have to manually increase the recursion limit when it comes to decoding from html and writing
    #to a file
    #i found this out from here: https://stackoverflow.com/questions/31528600/beautifulsoup-runtimeerror-maximum-recursion-depth-exceeded
    #trust me, I was highly confused when everything saved just fine except this. although i understand why now
    sys.setrecursionlimit(1000000)
    with open(documentname[1], "w", encoding='utf-8') as file:
            file.write(str(soup))

def main():
    rawHTML = fetchFromURL('http://shakespeare.mit.edu/')
    #Save HTML Main Page
    soup = BeautifulSoup(rawHTML, 'html.parser')
    #This is necessary, as Python throws errors if trying to "Write in Bytes"
    #with open("main_html.html", "w", encoding='utf-8') as file:
    #    file.write(str(soup))
    
    #Store all html links in a list
    alllinks = []

    #Grab the links that have an 'a' tag and put into list whatever comes after href
    for link in soup.find_all('a'):
        alllinks.append(link.get('href'))
        #print(link.get('href'))

    #As Books, Sonnets, and Poetry are organized differently on the website, will need to work with them differently
    onlybookworks = []
    onlysonnets   = []
    onlypoetry    = []
    for link in alllinks:
        if "index" in link:
            onlybookworks.append(link)
        if "Poetry" in link:
            if "sonnets" not in link:
                onlypoetry.append(link)
            if "sonnets" in link:
                onlysonnets.append(link)

    for link in onlybookworks:
        grab_each_book_act(link)
    for link in onlysonnets:
        grab_each_sonnet_act(link)
    for link in onlypoetry:
        grab_each_poetry(link)
        
    #FROM HERE, run the tokenizer.py file to have all the html files saved as txt files, then tokenized, normalized, and saved as JSON
main()    