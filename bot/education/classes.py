import random
import requests
from bs4 import BeautifulSoup


class Words:
    def __init__(self, level):
        self.level = level
        self.words = self.get_words(level)

    @staticmethod
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

    def random_word(self):
        eng_res, rus_res = random.choice(list(self.words.items()))
        answers = random.choices(list(self.words.values()), k=3)
        if rus_res not in answers:
            answers.append(rus_res)
            return eng_res, rus_res, answers
        self.random_word()


if __name__ == '__main__':
    word = Words('a1')
    eng, rus, incorrect = word.random_word()
    incorrect.append(rus)
    random.shuffle(incorrect)
    print(eng + ':')
    for i, r in enumerate(incorrect):
        right = ''
        if r == rus:
            right = 'right'
        print(f'{i + 1}. {r}', right)

