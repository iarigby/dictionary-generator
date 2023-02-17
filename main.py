import time

from deep_translator import LibreTranslator
import requests
from readability import Document
from html2text import html2text
import logging

article_full_page = requests.get('https://www.nachrichtenleicht.de/flughaefen-100.html')
document = Document(article_full_page.content)
logging.info('downloaded ' + document.title())
article_element = document.summary()
article_content = html2text(article_element)

translator = LibreTranslator(source='de', target='en', base_url='https://libretranslate.com/')

words_german = list(filter(lambda x: isinstance(x, str) and not x.isdigit(), set(article_content.split())))
logging.info(f'sending {len(words_german)} words for processing')

for word_german in words_german:
    time.sleep(3)
    print(word_german, translator.translate(word_german))
