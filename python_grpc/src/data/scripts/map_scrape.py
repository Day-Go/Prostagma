import requests
from bs4 import BeautifulSoup

# Specify the URL of the page to scrape
url = "https://ageofempires.fandom.com/wiki/Category:Maps"

# Send HTTP request to the specified URL and save the response from server in a response object called r
r = requests.get(url)

# Create a BeautifulSoup object and specify the parser
soup = BeautifulSoup(r.text, 'html.parser')

# Find all the map descriptions
map_descriptions = soup.find_all('a', class_='category-page__member-link')


# Find all the map descriptions
a_tag = soup.find_all('div', class_='category-page__member-left').find('a')

# Get the href attribute of the a tag
link = a_tag['href']
# To navigate to the link
# base_url = "https://ageofempires.fandom.com"
# full_url = base_url + link
# response = requests.get(full_url)
print(a_tag)

# Iterate over the descriptions and print them out
for description in map_descriptions:
    print(description.text)
