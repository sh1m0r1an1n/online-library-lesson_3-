import json
import os
from jinja2 import Environment, FileSystemLoader
from livereload import Server
from more_itertools import chunked
import urllib.parse


def render_website():
    """Рендерит сайт с перечнем книг из media/meta_data.json."""
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

    books_pairs = list(chunked(books, 2))

    env = Environment(loader=FileSystemLoader("."), autoescape=True)
    template = env.get_template("template.html")
    rendered_html = template.render(books_pairs=books_pairs)
    with open("index.html", "w", encoding="utf-8") as file:
        file.write(rendered_html)
    print("Сайт с книгами успешно сгенерирован в index.html")
    
    return rendered_html


def on_reload():
    """Функция для перерендеринга при изменении шаблона."""
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
