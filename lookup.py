import requests
from chatgpt_wrapper import ChatGPT
# import nest_asyncio
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}

def getAnswers(phrase):
    words = phrase.split(' ')
    query = "https://www.google.com/search?q="
    for word in words:
        if word == '+':
            query += ("%2B")
            continue

        if '+' in word:
            word = word.replace('+', '%2B')

        query += (word+'+')

    r = requests.get(query, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')

    # For headers results:
    result = soup.find('div', attrs={"class": lambda value: value and (value.startswith("Z0LcW XcVN5d"))})
    if result is None:
        # Purposes
        result = soup.find('span', attrs={"class": lambda value: value and (value.startswith("hgKElc"))})

    if result is None:
        # Calculations
        result = soup.find('div', attrs={"class": lambda value: value and (value.startswith("z7BZJb"))})
        
    if result is None:
        #Definitions (wikipedia)
        result = soup.find('div', attrs={"class": lambda value: value and (value.startswith("kno-rdesc"))})
        if result is not None:
            result = result.findChild("span", recursive=True)

    if result is None:
        #Definitions (wikipedia)
        result = soup.find('div', attrs={"class": lambda value: value and (value.startswith("gsrt vk_bk"))})

    if result is None:
        #Definitions (wikipedia)
        result = soup.find('div', attrs={"class": lambda value: value and (value.startswith("vk_bk"))})

#Working on lyrics currently
#    if result is None:
#        #Song lyrics
#        result = soup.find('div', attrs={"class": lambda value: value and (value.startswith("Oh5wg"))})

    if result is None: 
        return "I don't really understand what you trying to tell me tbh."
    else:
        return result.text