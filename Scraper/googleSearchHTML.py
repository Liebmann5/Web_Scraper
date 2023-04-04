import requests
from bs4 import BeautifulSoup

# URL of the Google search results page
#url = "https://www.google.com/search?q=boobs"
url = "https://www.google.com/search?q=titans"

# Send a GET request to the URL and get the response
response = requests.get(url)

# Parse the HTML code of the response using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Find all the search result titles and extract their text
titles = [title.text for title in soup.select("div.g h3")]

# Write the titles to a file named "googleBoobs.txt"
with open("googleBoobs.txt", "w") as f:
    for title in titles:
        f.write(title + "\n")
        
        
        
#           O  /
#         ___\/
#         ____\         
#        /\    o
#       /  \   o



        
        