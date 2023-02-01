from enchant import Dict
import string
from natasha import (
    Segmenter,
    NewsEmbedding,
    NewsNERTagger,
    Doc, PER
)


class TypoFinder:
    def __init__(self, xlsx_file):
        self.file_name = xlsx_file
        self.dictionary = Dict('ru_RU')
        self.dont_replace_words = []
        self.right_replaced_words = []

    def find_names_in_str(self, text):
        doc = Doc(text)
        doc.segment(Segmenter())
        doc.tag_ner(NewsNERTagger(NewsEmbedding()))
        names = [span.text for span in doc.spans if span.type == PER]

        return names if names else False

    def find_typos_in_all_rows(self, rows):
        for row in rows:
            print('Строка', rows.index(row))
            for cell in row:
                text = cell.value
                if type(text) is str:
                    names = self.find_names_in_str(text)
                    names = " ".join(names) if names else names
                    cell.value = self.find_typos_in_text(text, cell.coordinate, names)

    def find_typos_in_text(self, text, cell_coord, names):
        for word in text.split():
            temp_word = word.translate(str.maketrans('', '', string.punctuation))
            if temp_word not in self.dont_replace_words and temp_word and (not names or (
                    temp_word.lower() not in names.lower() and word.lower() not in names.lower())) \
                    and not self.dictionary.check(temp_word):
                suggest = self.dictionary.suggest(temp_word)
                if temp_word in self.right_replaced_words:
                    text.replace(temp_word, suggest[0])
                else:
                    print('Предположительная опечатка в слове', f"'{word}' (Ячейка {cell_coord})")
                    if suggest:
                        print('Предположительно подходящее слово:', f"'{suggest[0]}'")
                        suggest = self.input_answer_and_replace(temp_word, suggest[0])
                    else:
                        print('Предположительно подходящее слово: None')
                        suggest = self.input_answer_and_replace(temp_word, None)
                    if suggest:
                        text.replace(temp_word, suggest)

        return text

    def input_answer_and_replace(self, word, suggest):
        print('Верно ли предположение?(y/n/dr): ')
        yn = input().lower()
        if yn == 'y':
            self.right_replaced_words.append(word)
            return suggest
        elif yn == 'n':
            print('Введите верное слово: ')
            suggest = input()
            return suggest
        elif yn == 'dr':
            self.dont_replace_words.append(word)
            return False
        else:
            print('Неправильный ответ, попробуйте еще раз')
            return self.input_answer_and_replace(word, suggest)
