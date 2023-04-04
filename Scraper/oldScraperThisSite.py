from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from copy import deepcopy

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#      ADD/BUILD A PROXY
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

visited_urls = []
visited_urls.append('https://www.scrapethissite.com/lessons/')
visited_urls.append('https://www.scrapethissite.com/faq/')
visited_urls.append('https://www.scrapethissite.com/login/')
count = 1












def bad_urls(websites: list):
    print('VisitedURLs ================ ' + ' | '.join(visited_urls))
    for website in websites[:]:
        #print('\n')
        print('HERE')
        print(website in visited_urls)
        print(website)
        print(visited_urls)
        #print('\n')
        
        #maybe make multiple lists and have many if statements that read them!!! This might be very big or organized?!?!?
        if website in visited_urls:
            websites.remove(website)
            print('WebsitesRem ================ ' + ' | '.join(websites))
    
    print('Websites    ================ ' + ' | '.join(websites))
    return website















#OK OK GOOD LORD OK sssooooo I believe I do need to make another copy so I can make empty objects
def link_root(websites):
    dpWebsites = deepcopy(websites)
    
    print(type(dpWebsites))
    print('WebsitesBef ================ ' + ' | '.join(dpWebsites))
    bad_urls(dpWebsites)
    print('WebsitesAft ================ ' + ' | '.join(dpWebsites))
    print('\n-------------------------')
    
    for website_root in dpWebsites:
        result = requests.get(website_root)
        content = result.text
        soup = BeautifulSoup(content, 'lxml')

        find_html_code(soup, website_root)












    

# #! HERE HERE HERE.... for what ever reason results are wrong -> I search for <div _class="row"> and it doesn't return just that code!!!!! (file_name && for loop)

# #Maybe rename to like current_page   OR   keep this def for root and make a new def for all children!!
def find_html_code(soup, website_root):
    global count
    
    list_object = soup.find('div', class_='row')
    
    #print('FileNameBef ================ ' + file_name)
    file_name = list_object.find('h1').get_text()
    print('FileNameAft ================ ' + file_name)
    truncate_file(file_name)
    
    for list_index in list_object.find_all('div', class_='page'):
        a_tag = list_index.find('a')
        section_heading = a_tag.get_text(strip=True, separator=' ')
        a_href = a_tag['href']
        descriptions = list_index.find('p').get_text(strip=True, separator=' ')
        
        website_url = urljoin(website_root, a_href)
        
        #! A very simple debuging method is to just make a mathod that's arg is the value of the method that called it print statement that then just do a for loop that does print('.')
        print('FileName    ================ ' + file_name)
        print('SectionHead ================ ' + section_heading)
        print('Description ================ ' + descriptions)
        print('<a> href    ================ ' + a_href)
        print('Website URL ================ ' + website_url)
        print('Count       ================ ' + str(count))
  
        find_links(website_url)
        write_to_file(file_name, section_heading, a_href, descriptions)
    
    return (file_name, a_href, descriptions)
















def truncate_file(file_name):
    with open(f'{file_name}.txt', 'w', encoding='UTF-8') as dueces:
        dueces.write('')
        













    #! I dont think it was ever my code I believe this code just sucks!!!!!!
#ALSO!!! I'm pretty sure /pages is basically set as the root which is great!! BUT... make sure!     //////#Just having this be for root is better I believe BECAUSE find_links() gets all the <a> links!!!... of the next page actually so maybe actually of sending it a child URL just send the current that way all the chinamen are happy PLUS+++ I think this will fix my output to .txt file problemo!?!?
#! Links are just being added to External and not Internal !!!!!
#TODO: Hockey webpage repeats page 1
#TODO: Oscars AJAX is a good practice example!!! You have to figure out how to get things that render later!!
def find_links(user_input_url):
    global count
    
    if count == 1:
        print('------------' + user_input_url + '----------------')
    elif count == 2:
        print('-------------/2nd/---------------')
    else:
        count = 2
        return        
    

    # if user_input_url in visited_urls:
    #     return
    # elif not user_input_url or len(user_input_url) < 1:
    #     raise Exception("INFO: Invalid Input")
    # visited_urls.append(user_input_url)

    _start = user_input_url.find('//')
    _end   = user_input_url.find('.com')

    readable_website_name = user_input_url[_start+2:_end].strip()   #!In their code they took only 1 user URL that's why singular is ok!!!

    # try:
    #     website_content = requests.get(user_input_url.strip()).text
    # except:
    #     check_internet = requests.get('https://google.com').status_code
        
    #     if check_internet != requests.codes.ok:
    #         raise ConnectionError("ERROR: Check internet connection.")
    
    _soup = BeautifulSoup(website_content, features='lxml')
    
    internal_url_links = []
    external_url_links = []
    
    for link in _soup.find_all('a', href=True):
        if readable_website_name in link.get('href'):
            internal_url_links.append(urljoin(user_input_url, link['href']))
        
        if readable_website_name not in link.get('href') and len(link.get('href')) > 3:
            external_url_links.append(urljoin(user_input_url, link['href']))
            # external_link = urljoin(user_input_url, link['href'])
            # external_url_links.append(external_link)
            # visited_urls.add(external_link)
    
    print('Internal links ...............')
    print(internal_url_links, '\n')
    print('External links ...............')
    print(external_url_links, '\n')
    
    
    print('vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv')
    print('\n')
    print('\n')
    print('\n')
    print('\n')
    print('\n')
    print('\n')
    count += 1
    
    link_root(internal_url_links + external_url_links)















def write_to_file(file_name, section_heading, a_href, descriptions):
    print('\n')
    print('\n')
    print("*************************************************************************")
    print('            Writing to Excel             ')
    print('Title.txt   ================ ' + file_name)
    print('SectionHead ================ ' + section_heading)
    print('<a href     ================ ' + a_href)
    print("*************************************************************************")
    print('\n')
    print('\n')
    
    #file_name = 'DataOutput/' + file_name
    
    with open(f'{file_name}.txt', 'a', encoding='UTF-8') as converted:
        converted.write(section_heading)
        converted.write('\n')
        converted.write(a_href)
        converted.write('\n')
        converted.write('\t')
        converted.write(descriptions)
        converted.write('\n')    
        return 
        


















link_root(['https://www.scrapethissite.com/pages/'])






