import ebooklib
from ebooklib import epub
book = epub.read_epub(file_name)
items = list(book.get_items_of_type(ebooklib.ITEM_DOCUMENT))