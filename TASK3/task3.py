from bs4 import BeautifulSoup
import requests

url = 'https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(cnominal)'
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    print(f"Request to {url} successful !!")
    print(f"Status code: {response.status_code} -- {response.reason}")
    html_doc = response.text
    
else:
    print(f"Request to {url} failed !!")
    print(f"Status code: {response.status_code} -- {response.reason}")
    exit()