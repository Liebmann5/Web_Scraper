from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from copy import deepcopy
import sys

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#      ADD/BUILD A PROXY
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

visited_urls = []
visited_urls.append('https://www.scrapethissite.com/lessons/')
visited_urls.append('https://www.scrapethissite.com/faq/')
visited_urls.append('https://www.scrapethissite.com/login/')
count = 0

#This acts as tree!
    #1st call is the link root
    #2nd call are all the <a> from root so the 2nd layer
    #....
def link_root(websites):
    global count
    dpWebsites = deepcopy(websites)

    check_URL(dpWebsites)
    check_depth()
    
    for website_root in dpWebsites:
        try:
            result = requests.get(website_root)
            content = result.text
            soup = BeautifulSoup(content, 'lxml')

            use_BS(soup, website_root) #website_root => The name of the .txt file we make & write to!!
        except:
            check_internet = requests.get('https://google.com').status_code
        
            if check_internet != requests.codes.ok:
                raise ConnectionError("ERROR: Check internet connection.")

#! COUNT ----> is in charge of the tree!! Don't go beyond the 2nd level you piece of worthless maget crap!

def check_URL(websites: list):
    for website in websites[:]:
        website.strip()
        
        if not website or len(website) < 1:
            raise Exception("INFO: Invalid Input")
        elif(has_visited(website)):
            websites.remove(website)
        #An example just for now till I remember
        elif(count == 1000):
            return
    return websites

def has_visited(website):
    if website in visited_urls:
        website.remove(website)
    return website


def check_depth():
    global count
    
    if count == 1:
        print("Thats hot") #1 == only read page 1 | 2 == only read the <a> URLs from pg. 1
    else:
        sys.exit()
    
    count += 1

def use_BS(soup, website_root):
    list_object = soup.find('div', class_='row')
    file_name = list_object.find('h1').get_text()
    #truncate_file(file_name)
    
    for list_index in list_object.find_all('div', class_='page'):
        a_tag = list_index.find('a')
        section_heading = a_tag.get_text(strip=True, separator=' ')
        a_href = a_tag['href']
        descriptions = list_index.find('p').get_text(strip=True, separator=' ')
        
        website_url = urljoin(website_root, a_href)

        #Out of order: 1
        find_links(website_url)
        write_to_file(file_name, section_heading, a_href, descriptions)
    
    return (file_name, a_href, descriptions)


def use_Selin():
    return













