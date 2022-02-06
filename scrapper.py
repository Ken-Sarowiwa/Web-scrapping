"""
importing the necessary ibraries for web scrapping, re will be used for regular expressions, requests module will be used 
for making HTTP requests, the urlsplit will be used to split the urls into five segments, the deque module will be used for deque elements that will be stored in the 
set and beautiful soup is used to extract contents from the html. the last and final pandas will be used to extract the data is good format 
"""

from ast import Continue
from distutils.filelist import findall
from operator import length_hint
from os import link
import re
import requests 
from urllib.parse import urlsplit
from collections import deque
from bs4 import BeautifulSoup
import pandas as pd
#from google.colab import files


original_url = input("please type in the url you want to scrap: ")

unscrapped_urls = deque([original_url])

scrapped_urls = set()

succesfully_scrapped_emaails = set()

while len(unscrapped_urls):
    new_url = unscrapped_urls.popleft()
    scrapped_urls.add(new_url)



parts = urlsplit(new_url)

base_url = "{0.scheme}://{0.netloc}".format(parts)
if '/' in parts.path:
    path = new_url[:new_url.rfind('/')+1]
else:
    path = new_url

    print("Crawling URL %s" % new_url)
try:
        response = requests.get(new_url)
except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
    Continue

new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.com",response.text, re.I))

succesfully_scrapped_emaails.update(new_emails)


# create a beutiful soup for the html document
soup = BeautifulSoup(response.text, 'lxml')

for nyama in soup.find_all("a"):
    if "href" in nyama.attrs:
        link = nyama.attrs["href"]
    else:
        link = ''

    if link.startswith('/'):
            link = base_url + link
    
    elif not link.startswith('http'):
            link = path + link

    if not link.endswith(".gz"):
     if not link in unscrapped_urls and not link in scrapped_urls:
              unscrapped_urls.append(link)


df = pd.DataFrame(new_emails, columns=["Email"]) # replace with column name you prefer
df.to_csv('email.csv', index=False)
#files.download("email.csv")
