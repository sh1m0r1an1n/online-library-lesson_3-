import json
import os
from jinja2 import Environment, FileSystemLoader


def render_website():
    """Рендерит сайт с перечнем книг из media/meta_data.json."""
    with open("media/meta_data.json", "r", encoding="utf-8") as file:
        books = json.load(file)

    for book in books:
        if 'img_src' in book:
            book['img_src'] = os.path.normpath(book['img_src']).replace(os.sep, '/')

    env = Environment(loader=FileSystemLoader("."), autoescape=True)
    template = env.get_template("template.html")
    rendered_html = template.render(books=books)
    with open("index.html", "w", encoding="utf-8") as file:
        file.write(rendered_html)
    print("Сайт с книгами успешно сгенерирован в index.html")


def main():
    render_website()


if __name__ == "__main__":
    main()
