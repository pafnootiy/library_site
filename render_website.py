import json
import math
import os

from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked

COLUMN_ON_PAGE = 2
BOOKS_ON_PAGE = 20


def get_books_data_from_json():
    with open("./json/books.json", "r", encoding="utf8") as my_file:
        books = json.load(my_file)

    return books


def create_page():
    books = get_books_data_from_json()
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    chunked_books = list(chunked(books, COLUMN_ON_PAGE))
    chunked_pages = list(chunked(chunked_books, BOOKS_ON_PAGE))

    filepath_to_pages_directory = os.path.join("pages")
    os.makedirs(filepath_to_pages_directory, exist_ok=True)

    all_pages_number = math.ceil(len(chunked_books) / BOOKS_ON_PAGE)

    for index_number, chunked_pages in enumerate(chunked_pages, 1):
        html_filepath = os.path.join(filepath_to_pages_directory,
                                     f"index{index_number}.html")
        template = env.get_template('template.html')
        rendered_page = template.render(
            books=chunked_pages,
            page_number=index_number,
            all_pages_number=all_pages_number,
        )

        with open(html_filepath, 'w', encoding="utf8") as file:
            file.write(rendered_page)

    print('reload server')


def main():
    load_dotenv()
    create_page()
    server = Server()
    server.watch("template.html", create_page)
    server.serve(root='.')


if __name__ == '__main__':
    main()
