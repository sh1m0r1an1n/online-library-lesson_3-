import json
import os
from jinja2 import Environment, FileSystemLoader
from livereload import Server
from more_itertools import chunked
import urllib.parse


def load_books():
    """Загружает и нормализует данные книг из media/meta_data.json."""
    with open("media/meta_data.json", "r", encoding="utf-8") as file:
        books = json.load(file)

    for book in books:
        if 'img_src' in book:
            book['img_src'] = os.path.normpath(book['img_src']).replace(os.sep, '/')
        if 'book_path' in book:
            normalized_path = os.path.normpath(book['book_path']).replace(os.sep, '/')
            path_parts = normalized_path.split('/')
            encoded_parts = [urllib.parse.quote(part) for part in path_parts]
            book['book_path'] = '/'.join(encoded_parts)
    return books


def generate_pages(books, template, page_size=20):
    """Генерирует HTML-страницы с книгами, разбитыми по страницам."""
    pages = list(chunked(books, page_size))
    total_pages = len(pages)
    os.makedirs("pages", exist_ok=True)
    
    for index, page_books in enumerate(pages, start=1):
        books_pairs = list(chunked(page_books, 2))
        prev_page = f"index{index-1}.html" if index > 1 else None
        next_page = f"index{index+1}.html" if index < total_pages else None
        rendered_html = template.render(
            books_pairs=books_pairs,
            current_page=index,
            total_pages=total_pages,
            prev_page=prev_page,
            next_page=next_page
        )
        page_filename = f"pages/index{index}.html"
        with open(page_filename, "w", encoding="utf-8") as file:
            file.write(rendered_html)
        print(f"Страница {index} с книгами успешно сгенерирована в {page_filename}")


def create_redirect_index():
    """Создает главный index.html для редиректа на первую страницу."""
    with open("index.html", "w", encoding="utf-8") as file:
        file.write('<meta http-equiv="refresh" content="0; URL=pages/index1.html">')
    print("Главная страница index.html успешно создана для редиректа на первую страницу.")


def render_website():
    """Рендерит сайт, вызывая функции для загрузки данных, генерации страниц и создания главной index.html."""
    books = load_books()
    env = Environment(loader=FileSystemLoader("."), autoescape=True)
    template = env.get_template("template.html")
    generate_pages(books, template, page_size=20)
    create_redirect_index()


def on_reload():
    """Перерендеривает сайт при изменении шаблона или данных."""
    render_website()
    return


def main():
    """Запускает локальный сервер с livereload для удобной разработки."""
    render_website()
    
    server = Server()
    server.watch('template.html', on_reload)
    server.watch('media/meta_data.json', on_reload)
    server.serve(root='.', port=5500)


if __name__ == "__main__":
    main()
