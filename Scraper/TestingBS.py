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
    
    print('WebsitesOK  ================ ' + ' | '.join(websites))
    return website

#OK OK GOOD LORD OK sssooooo I believe I do need to make another copy so I can make empty objects
def link_root(websites):
    dpWebsites = deepcopy(websites)
    
    print(type(dpWebsites))
    print('WebsitesBef ================ ' + ' | '.join(dpWebsites))
    bad_urls(dpWebsites)
    print('LinkRootAft ================ ' + ' | '.join(dpWebsites))
    print('$$$$$$$$$$$$$$$$$$$$$$\n')
    
    for website_root in dpWebsites:
        result = requests.get(website_root)
        content = result.text
        soup = BeautifulSoup(content, 'lxml')
        
        print(soup.prettify())
        print('\n$$$$$$$$$$$$$$$$$$$$$$\n')
        find_variables(soup, website_root)

#! HERE HERE HERE.... for what ever reason results are wrong -> I search for <div _class="row"> and it doesn't return just that code!!!!! (file_name && for loop)

#Maybe rename to like current_page   OR   keep this def for root and make a new def for all children!!
def find_variables(soup, website_root):
    global count
    
    list_object = soup.find('div', class_='row')
    
    #print('FileNameBef ================ ' + file_name)
    file_name = list_object.find('h1').get_text()
    print('FileNameAft ================ ' + file_name)
    print('listObject  ================ ')
    print(list_object.prettify())
    
    for list_index in list_object.find_all('div', class_='page'):   #Counteries doesn't have a class='page' INSTEAD it's id='page'
        a_tag = list_index.find('a')
        section_heading = a_tag.get_text(strip=True, separator=' ')
        a_href = a_tag['href']
        descriptions = list_index.find('p').get_text(strip=True, separator=' ')
        
        website_url = urljoin(website_root, a_href)
        
        #! A very simple debuging method is to just make a mathod that's arg is the value of the method that called it print statement that then just do a for loop that does print('.')
        print("*************************************************************************")
        print('            WebsitePage Info             ')
        print('FileName    ================ ' + file_name)
        print('SectionHead ================ ' + section_heading)
        print('Description ================ ' + descriptions)
        print('<a> href    ================ ' + a_href)
        print('Website URL ================ ' + website_url)
        print('Count       ================ ' + str(count))
        print("*************************************************************************")
        print('            BeautifulSoup Co             ')
        print('listIndex   ================ ')  #This is ONLY the <div class_="page"> tag with all the code inside it
        print(list_index.prettify())
        print('a_tag       ================ ')
        print(a_tag.prettify())
        
        
        
        if(count == 1):
            print('--------------------\n')
            find_links()
            count += 1
        else:
        #write_to_file(file_name, section_heading, a_href, descriptions)
            #return (file_name, a_href, descriptions)
            return 0

def find_links():
    link_root(['https://www.scrapethissite.com/pages/simple/'])



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
    
    # with open(f'{file_name}.txt', 'a', encoding='UTF-8') as converted:
    #     converted.write(section_heading)
    #     converted.write('\n')
    #     converted.write(a_href)
    #     converted.write('\n')
    #     converted.write('\t')
    #     converted.write(descriptions)
    #     converted.write('\n')    
    #     return 
        






#TODO: OK sssoooo find_variables/html_code needs to just organize what is sent to the next method!!!
#TODO: which is it sends everything below nav bar..........












link_root(['https://www.scrapethissite.com/pages/'])












print('\n')
print('\n')
print('\n')
print('Next code you dumb Mulsum! *spit*....... *stare*................... *deficate upon*')
print('\n')
print('\n')
print('\n')














def find_html_code(soup, website_root):
    global count
    
    list_object = soup.find('div', class_='row')
    
    #print('FileNameBef ================ ' + file_name)
    file_name = list_object.find('h1').get_text()
    print('FileNameAft ================ ' + file_name)

    
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









#link_root(['https://www.scrapethissite.com/pages/'])












