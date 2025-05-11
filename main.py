from __future__ import annotations

import pickle
import time

from deep_translator import GoogleTranslator
import requests
from readability import Document
from html2text import html2text
import logging

dictionary_file_name = 'dictionary.pkl'


def main():
    article_full_page = requests.get('https://www.nachrichtenleicht.de/flughaefen-100.html')
    document = Document(article_full_page.content)
    logging.info('downloaded ' + document.title())
    article_element = document.summary()
    article_content = html2text(article_element)

    translator = GoogleTranslator(source='de', target='en')

    words_german = list(filter(lambda x: isinstance(x, str) and not x.isdigit(), set(article_content.split())))
    logging.info(f'sending {len(words_german)} words for processing')

    dictionary = Dictionary()

    for word_german in words_german:
        time.sleep(1)
        if word_german not in dictionary:
            print(word_german)
            word_english = translator.translate(word_german)
            print(word_english)
            dictionary.save(word_german, word_english)


class Dictionary(dict):
    @staticmethod
    def read() -> Dictionary:
        try:
            with open(dictionary_file_name, 'rb') as file:
                return pickle.load(file)
        except FileNotFoundError:
            return Dictionary()

    def save(self, word, translation):
        self[word] = translation
        self._save_file()

    def _save_file(self):
        with open(dictionary_file_name, 'wb') as file:
            pickle.dump(self, file)

    def __str__(self):
        return '\n'.join(f'{w}, {self[w]}' for w in self)


if __name__ == '__main__':
    # main()
    print(Dictionary.read())
