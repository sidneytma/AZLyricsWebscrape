# Imports

import pandas as pd
import requests
import re

# Functions

def get_search_url(artist_title, query_code):
    artist_title_no_spaces = artist_title.replace(" ", "+")
    return f"https://search.azlyrics.com/search.php?q={artist_title_no_spaces}&x={query_code}"

def get_lyrics_url(artist_title, query_code):
    search_url = get_search_url(artist_title, query_code)
    response = requests.get(search_url)
    if response.status_code != 200:
        return None
    
    text = response.text
    pattern = r'<a href="(https?://[^"]+)">'
    match = re.search(pattern, text)
    if not match:
        return None
    
    return match.group(1)

def get_lyrics(artist_title, query_code):
    lyrics_url = get_lyrics_url(artist_title, query_code)
    
    if not lyrics_url:
        return None
    
    response = requests.get(lyrics_url)
    if response.status_code != 200:
        return None
    
    text = response.text
    pattern = r"Sorry about that. -->(.*?)<\/div>"
    match = re.search(pattern, response.text, re.DOTALL)
    if not match:
        return None
    
    lyrics = match.group(1)
    return lyrics.replace("<br>", "").replace("&quot;", "\"")

