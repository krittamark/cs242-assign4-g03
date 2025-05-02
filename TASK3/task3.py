from bs4 import BeautifulSoup
import requests

url = 'https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)'
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

soup = BeautifulSoup(html_doc, 'html.parser')

allTablesCount = len(soup.find_all('table'))
print(f"The web page contains {allTablesCount} tables in total.")

targetTable = soup.find('table', class_='wikitable')
sourcesTableHead = targetTable.find('tr', class_='static-row-header').find_all('th')[1:]
sources = [th.find('a').text for th in sourcesTableHead]

print(f"We found {len(sources)} header rows indicating info sources as follows.")
print(sources)