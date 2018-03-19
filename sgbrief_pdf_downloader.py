import pickle
import requests
import os
import os.path
from pathlib import Path

# import file saved from URL links scraper

file_name = "new_urls.txt"

with open(file_name, "rb") as fp:
    url_links = pickle.load(fp)
    
x = 0

## Pick a path to save your PDF's too, and an alternate path. PDF's with duplicate names are saved to the alternate path.
## These duplicates generally exist because they were uploaded twice by the SG, but putting them in a separate directory
## lets you check to make sure. Obviously change these paths to something on your system.

save_path = "/Users/literroy/sg_brief_pdfs"
alt_save_path = "/Users/literroy/sg_brief_pdfs/duplicates"

## Loop through all the urls in your url list and download them, saving them to your save path.
## There's also a crude progress counter here that lets you know after every 100 downloads how far you've gone and
## much you have left to go.

for url in url_links:
    x = x + 1
    file_name = url.split('/')[-1] 
    full_path = os.path.join(save_path, file_name)
    if Path(full_path).is_file():
        full_path = os.path.join(alt_save_path, file_name)
    r = requests.get(url, stream = True)
    with open(full_path,'wb') as pdf:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                pdf.write(chunk)
    if x % 100 == 0:
        print(str(x) + "/" + str(len(url_links)) + " files downloaded.")
