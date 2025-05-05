import functools
import json
import os
import urllib.parse

from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
from livereload import Server
from more_itertools import chunked


# Константы
TEMPLATE_PATH = "template.html"
METADATA_PATH = "media/meta_data.json"
DEFAULT_PAGE_SIZE = 20
SERVER_PORT = 5500
DEFAULT_BOOTSTRAP_PATH = "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"


def load_books():
    """Загружает и нормализует данные книг из media/meta_data.json."""
    with open(METADATA_PATH, "r", encoding="utf-8") as file:
        books = json.load(file)

    for book in books:
        if "img_src" in book:
            book["img_src"] = os.path.normpath(book["img_src"]).replace(os.sep, "/")
        if "book_path" in book:
            normalized_path = os.path.normpath(book["book_path"]).replace(os.sep, "/")
            path_parts = normalized_path.split("/")
            encoded_parts = [urllib.parse.quote(part) for part in path_parts]
            book["book_path"] = "/".join(encoded_parts)
    return books


def generate_pages(books, template, bootstrap_path, page_size=DEFAULT_PAGE_SIZE):
    """Генерирует HTML-страницы с книгами, разбитыми по страницам."""
    pages = list(chunked(books, page_size))
    total_pages = len(pages)
    os.makedirs("pages", exist_ok=True)
    
    for index, page_books in enumerate(pages, start=1):
        books_pairs = list(chunked(page_books, n=2))
        prev_page = f"index{index-1}.html" if index > 1 else None
        next_page = f"index{index+1}.html" if index < total_pages else None
        rendered_html = template.render(
            books_pairs=books_pairs,
            current_page=index,
            total_pages=total_pages,
            prev_page=prev_page,
            next_page=next_page,
            bootstrap_path=bootstrap_path
        )
        page_filename = f"pages/index{index}.html"
        with open(page_filename, "w", encoding="utf-8") as file:
            file.write(rendered_html)


def render_website(bootstrap_path):
    """Рендерит сайт, вызывая функции для загрузки данных и генерации страниц."""
    books = load_books()
    env = Environment(loader=FileSystemLoader("."), autoescape=True)
    template = env.get_template(TEMPLATE_PATH)
    generate_pages(books, template, bootstrap_path, page_size=DEFAULT_PAGE_SIZE)


def on_reload(bootstrap_path):
    """Перерендеривает сайт при изменении шаблона или данных."""
    render_website(bootstrap_path)


def main():
    """Запускает локальный сервер с livereload для удобной разработки."""
    load_dotenv()

    bootstrap_path = os.getenv("BOOTSTRAP_PATH", DEFAULT_BOOTSTRAP_PATH)
    
    render_website(bootstrap_path)
    
    server = Server()
    
    reload_handler = functools.partial(on_reload, bootstrap_path)
    
    server.watch(TEMPLATE_PATH, reload_handler)
    server.watch(METADATA_PATH, reload_handler)
    server.serve(root=".", port=SERVER_PORT)


if __name__ == "__main__":
    main()
