import functools
import json
import os
import urllib.parse
import argparse

from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader
from livereload import Server
from more_itertools import chunked


DEFAULT_TEMPLATE_PATH = "template.html"
DEFAULT_METADATA_PATH = "media/meta_data.json"
DEFAULT_PAGE_SIZE = 20
DEFAULT_SERVER_PORT = 5500
DEFAULT_BOOTSTRAP_PATH = "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"


def parse_arguments():
    """Парсит аргументы командной строки и переменные окружения."""
    parser = argparse.ArgumentParser(description="Генератор сайта библиотеки")
    
    parser.add_argument(
        "--template-path",
        default=os.getenv("TEMPLATE_PATH", DEFAULT_TEMPLATE_PATH),
        help="Путь к HTML шаблону"
    )
    parser.add_argument(
        "--metadata-path",
        default=os.getenv("METADATA_PATH", DEFAULT_METADATA_PATH),
        help="Путь к файлу с метаданными книг"
    )
    parser.add_argument(
        "--bootstrap-path",
        default=os.getenv("BOOTSTRAP_PATH", DEFAULT_BOOTSTRAP_PATH),
        help="Путь к CSS файлам Bootstrap"
    )
    parser.add_argument(
        "--page-size",
        type=int,
        default=int(os.getenv("PAGE_SIZE", DEFAULT_PAGE_SIZE)),
        help="Количество книг на странице"
    )
    parser.add_argument(
        "--server-port",
        type=int,
        default=int(os.getenv("SERVER_PORT", DEFAULT_SERVER_PORT)),
        help="Порт для локального сервера"
    )
    
    return parser.parse_args()


def load_books(metadata_path):
    """Загружает и нормализует данные книг из media/meta_data.json."""
    with open(metadata_path, "r", encoding="utf-8") as file:
        books = json.load(file)

    for book in books:
        if "img_src" in book:
            book["img_src"] = os.path.normpath(book["img_src"]).replace(os.sep, "/")
            book["img_src"] = f"../media/{book['img_src']}"
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


def render_website(args):
    """Рендерит сайт, вызывая функции для загрузки данных и генерации страниц."""
    books = load_books(args.metadata_path)
    env = Environment(loader=FileSystemLoader("."), autoescape=True)
    template = env.get_template(args.template_path)
    generate_pages(books, template, args.bootstrap_path, args.page_size)


def on_reload(args):
    """Перерендеривает сайт при изменении шаблона или данных."""
    render_website(args)


def main():
    """Запускает локальный сервер с livereload для удобной разработки."""
    load_dotenv()
    args = parse_arguments()
    
    render_website(args)
    
    server = Server()
    reload_handler = functools.partial(on_reload, args)
    
    server.watch(args.template_path, reload_handler)
    server.watch(args.metadata_path, reload_handler)
    server.serve(root=".", port=args.server_port)


if __name__ == "__main__":
    main()
