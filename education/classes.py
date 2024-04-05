import requests
from bs4 import BeautifulSoup


def get_words(level):

    url = f'https://lewisforemanschool.ru/words/{level}'

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    words = soup.find('p', class_='textable css102').prettify().split('\n')[1::2]

    word_dict = {}

    for word in words:
        try:
            if '-' in word:
                eng, rus = word.split(' - ')
            if '–' in word:
                eng, rus = word.split(' – ')
            word_dict[eng.split('.')[1].strip()] = rus.strip()
        except ValueError:
            continue

    return word_dict


class Words:
    def __init__(self, level):
        self.level = level
        self.words = get_words(level)

