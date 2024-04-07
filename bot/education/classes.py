import random
import requests
from bs4 import BeautifulSoup
from bot.database import WordsDb


class Words:
    def __init__(self, level, tg_id):
        self.tg_id = tg_id
        self.level = level
        self.words = self.get_words(level)

    def get_words(self, level):

        url = f'https://lewisforemanschool.ru/words/{level}'

        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        words = soup.find('p', class_='textable css102').prettify().split('\n')[1::2]

        word_dict = {}
        user_words = WordsDb(self.tg_id)
        for word in words:
            try:
                if '-' in word:
                    eng, rus = word.split(' - ')
                if '–' in word:
                    eng, rus = word.split(' – ')
                eng = eng.split('.')[1].strip()
                rus = rus.strip()
                if user_words.check_word(eng, rus):
                    continue
                word_dict[eng] = rus
            except (ValueError, IndexError):
                continue
        return word_dict

    def random_word(self):
        eng_res, rus_res = random.choice(list(self.words.items()))
        answers = self.random_answers(rus_res)
        return eng_res, rus_res, answers

    def random_answers(self, rus):
        answers = random.choices(list(self.words.values()), k=3)
        if rus not in answers:
            answers.append(rus)
            return answers
        self.random_answers(rus)


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

