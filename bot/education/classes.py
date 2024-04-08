import random
from bot.database import WordsDb


class Words:
    def __init__(self, level, tg_id):
        self.tg_id = tg_id
        self.level = level
        self.words = self.get_words()

    def get_words(self):
        word_list = {}
        users_db = WordsDb(self.tg_id)
        with open(rf'.\education\word_dir\{self.level}.txt', 'r', encoding='utf-8') as file:
            words = file.readlines()
        for word in words:
            try:
                eng, rus = word.split('-')
                if not users_db.check_word(eng, rus):
                    word_list[eng.strip()] = rus.strip()
            except ValueError:
                print(word)
        return word_list


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
    level = input('Введите уровень: ')
    word_list = {}
    with open(rf'.\word_dir\{level}.txt', 'r', encoding='utf-8') as file:
        words = file.readlines()
    count = 0
    for word in words:
        eng, rus = word.split('-')
        word_list[eng] = rus
        count += 1
    print(count)
