# Онлайн-библиотека

Веб-приложение для просмотра и чтения книг. Сайт автоматически генерируется из JSON-файла с метаданными книг.

## Возможности

- 📚 Отображение книг в виде карточек с обложками
- 🔍 Разбивка книг по страницам для удобной навигации
- 📖 Прямые ссылки на тексты книг
- 🎨 Адаптивный дизайн на Bootstrap
- 🔄 Автоматическое обновление при изменении данных
- 💻 Работа в оффлайн-режиме

## Требования

- Python 3.7+
- Зависимости из `requirements.txt`
- Bootstrap CSS и JS (включены локально или доступны через CDN)

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/your-username/online-library.git
cd online-library
```

2. Создайте виртуальное окружение и активируйте его:
```bash
python -m venv venv
source venv/bin/activate  # для Linux/macOS
venv\Scripts\activate     # для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Скопируйте пример конфигурации и настройте под себя:
```bash
cp .env.example .env
```

## Использование

### Запуск сервера разработки

```bash
python render_website.py
```

Сайт будет доступен по адресу: http://localhost:5500

### Настройка

Все настройки можно задать через:
- Переменные окружения в файле `.env`
- Аргументы командной строки

#### Переменные окружения

Создайте файл `.env` со следующими параметрами:
```env
# Пути к файлам
TEMPLATE_PATH=template.html
METADATA_PATH=media/meta_data.json

# Bootstrap файлы (для оффлайн-режима)
BOOTSTRAP_PATH=../static/bootstrap.min.css
BOOTSTRAP_JS_PATH=../static/bootstrap.bundle.min.js

# Bootstrap файлы (для онлайн-режима)
# BOOTSTRAP_PATH=https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css
# BOOTSTRAP_JS_PATH=https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js

# Настройки сайта
PAGE_SIZE=20
SERVER_PORT=5500
```

#### Аргументы командной строки

```bash
python render_website.py --help
```

Доступные параметры:
- `--template-path` - путь к HTML шаблону
- `--metadata-path` - путь к файлу с метаданными книг
- `--bootstrap-path` - путь к CSS файлам Bootstrap
- `--bootstrap-js-path` - путь к JS файлам Bootstrap
- `--page-size` - количество книг на странице
- `--server-port` - порт для локального сервера

### Структура проекта

```
online-library/
├── media/              # Медиафайлы (обложки, тексты книг)
│   └── meta_data.json  # Метаданные книг
├── pages/             # Сгенерированные HTML-страницы
├── static/            # Статические файлы (Bootstrap, favicon)
│   ├── bootstrap.min.css
│   ├── bootstrap.bundle.min.js
│   └── favicon.ico
├── template.html      # Шаблон сайта
├── render_website.py  # Скрипт генерации сайта
├── requirements.txt   # Зависимости проекта
└── .env              # Настройки (не включен в репозиторий)
```

### Формат метаданных

Файл `meta_data.json` должен содержать список книг в формате:
```json
[
  {
    "title": "Название книги",
    "author": "Автор",
    "img_src": "путь/к/обложке.jpg",
    "book_path": "путь/к/тексту.txt",
    "genres": ["жанр1", "жанр2"]
  }
]
```

## Разработка

При изменении шаблона или метаданных сайт автоматически перегенерируется благодаря livereload.

## Лицензия

MIT
