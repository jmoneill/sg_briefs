import requests
from bs4 import BeautifulSoup
import re
import time
import pickle

## As set up right now, this script will search for briefs from specified October Terms. The Supreme Court divides up its
## years into October Terms, which is simply the term that starts with the Court's first October sitting (where they're
## coming back from a lengthy summer vacation). So searching for briefs from "2005" will return briefs that were filed during
## the year starting in October 2005. (OT 2005 was a particular exciting term, as it was the first term of Chief Justice
## Roberts and Justice Alito!)

pdf_links = []

# Pick your starting and ending years.

year_start = 2000  
year_stop = 2017   

# Loops through every year you picked, printing which year you're on as you go. This searches the SG's website for all
# the briefs from a particular term, downloads the HTML of the search results, and collects a list of links to PDF files
# contained on those pages. It stops when it reaches a page with no PDF links.

for i in list(range(year_start,year_stop)):
    pdf_count = 1  ## hacky way to make sure the loop below actually starts
    counter = 0
    print(i) 
    while pdf_count > 0: ## stops the scraper when it reaches a page with no PDF links - reached end of search results
        url = "https://www.justice.gov/osg/supreme-court-briefs?text=&sc_term=" + str(i) + "&type=All&subject=All&filing_date%5Bvalue%5D%5Bmonth%5D=&filing_date%5Bvalue%5D%5Byear%5D=&page=" + str(counter)
        r = requests.get(url)
        soup = BeautifulSoup(r.text,'html5lib')
        loop_links = soup.find_all("a", string=re.compile("pdf"))
        loop_urls = [u['href'] for u in loop_links]
        pdf_count = len(loop_urls)
        pdf_links = pdf_links + loop_urls
        counter += 1
        
# Find out how many links you got

print len(pdf_links)

# Save list of links to a file

file_name = "urls.txt"
with open(file_name, "wb") as fp:
    pickle.dump(pdf_links, fp)
