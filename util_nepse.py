"""utili for npse api"""
import re
import csv
import requests

from bs4 import BeautifulSoup
import pandas as pd

def get_soup(url: str) -> 'Beautiful soup':
    headers = {'User-Agent': 
                 ('Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                  'AppleWebKit/537.36 (KHTML, like Gecko)'
                  'Chrome/61.0.3163.100 Safari/537.36')}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content, 'xml')
    print(r.url)
    return soup

def get_text(x: 'soup list or soup str') -> 'list or str':
    if isinstance(x, list):
        return [i.get_text(strip=True) for i in x]
    else:
        return x.get_text(strip=True)
    
def chunks(l: list, n: int) -> 'generator':
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def get_date_range(start: str='2017-10-15', 
                   end: str='2017-10-25') -> list:
    """get list of days in str --'YYYY-MM-DD' and day of week"""
    range = pd.date_range(start, end, freq = 'D')
    return [(str(i)[:10], i.dayofweek) for i in range]

def write_csv(l: list, filename: str, 
              mode: str='w') -> 'write file':
    with open(filename, mode, newline='') as f:
        writer = csv.writer(f)
        for row in l:
            writer.writerow(row)
            
def clean_names(words: list) -> list:
    """replace space with _ and remove any non letter"""
    for i, word in enumerate(words):
        word = re.sub(' ', '_', word)
        word = re.sub('[^a-zA-Z_]', '', word.lower())
        words[i] = word
    return words
