# ✨ Clean Python / Django Guidelines

> «Правила — это чек-лист для разработчика и готовый промпт для ИИ-ассистента. Следуйте им, если не указано иное.»

---

## 1. 🐍  Clean Python (для человека)

### 1.1 Именование
* `snake_case` для переменных/функций, `PascalCase` для классов.
* Главное слово в конце: `get_user_profile()`, а не `profile_get()`.
* **Никаких безымянных литералов.**  Число/строка должны **объяснять себя**:  
  **Плохо:** `user_id = 42` / `func(10, 20)`  
  **Хорошо:** `moscow_timezone_offset = 3` / `resize(img, width=1920, height=1080)`.
* Избегаем «data/info/object/item/result».  
  **Плохо:** `def process_data(data):`  
  **Хорошо:** `def filter_expired_coupons(coupons):`.

### 1.2 Функции
* Одна функция — одно действие, ≤ 20 строк.
* Не изменяет глобальное состояние → возвращает новое значение.
* Всегда имеет doctstring-однострочник:  
  `"""Фильтрует истёкшие купоны."""`

### 1.3 Структура файла
1. Импорты (`stdlib`, `third-party`, `local`).
2. Константы.
3. Логика (функции/классы).
4. `main()`.
5. `if __name__ == "__main__": main()`.

### 1.4 Ошибки
* `try/except` только там, где можно обработать.
* Ловим конкретные исключения → логируем → сообщаем пользователю.

### 1.5 Ввод / Вывод
* Чтение файлов/сети — в отдельных функциях-обёртках.
* Логика обработки отделена и тестируема.

### 1.6 Форматирование коллекций
```python
nums = [
    1, 2, 3,
    4, 5, 6,
]
url = build_url(base="/search", q="python", page=2)
```

### 1.7 Пакет
* `requirements.txt`, `.gitignore`, `.env.example`, `README.md`.

### 1.8 Тестирование и качество
* **pytest** + `pytest-cov` — пишем модульные тесты.
* Линтеры: `ruff`/`flake8`, форматирование — `black` или `ruff format`.
* CI (GitHub Actions): `python -m pip install -r requirements.txt && pytest`.

### 1.9 Стиль кода (Zen / PEP)
* **Flat is better than nested** — избегаем лишних `if/else/for`-вложенностей, выносим логику в функции.
* **Be Pythonic, but explicit** — `any(x > 0 for x in nums)` вместо ручного цикла.
* **Type hints** обязательны для публичных функций/методов, опциональны для простых локальных.
* Следуем `PEP 8` (стиль), `PEP 257` (docstrings). Форматирование — `black`/`ruff`.
* Все позиционные литералы — только именованными аргументами:  
  `send_mail(subject="Hi", message="...", to=["user@example.com"])`.
* **Нет комментариев** — понятный код > комментариев. Допускаются docstring и TODO.
* GET-запросы ➜ параметры передаём словарём: `requests.get(url, params={"q": "python"})`.

### 1.10 main()
* Все «скриптовые» вызовы функций — через `main()`, а зависимости передаём аргументами; никакой «магии» при импорте.

---

## 2. 🕸️  Django Best Practices

### 2.1 Модели
* `related_name`, `verbose_name`, `help_text`, `db_index`.
* `__str__` — человекочитаемое.
* Сигналы только при невозможности сделать через `Model.save()`.

### 2.2 Views
* Логика — во вьюхах или сервис-слое, а не в шаблонах.
* CBV/FBV — выберите один стиль на проект.

### 2.3 Admin Cheat-Sheet

```python
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "published_at", "likes_count")
    list_display_links = ("title",)
    list_filter = ("author", "tags", "published_at")
    list_select_related = ("author",)  # уменьшает N+1
    search_fields = ("title", "text", "author__username")
    autocomplete_fields = ("tags",)
    filter_horizontal = ("tags",)      # для M2M
    readonly_fields = ("created", "updated")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("-published_at",)
    date_hierarchy = "published_at"
    list_per_page = 50
```

| Параметр | Что делает |
|----------|------------|
| `list_display` / `list_display_links` | Колонки и кликабельные ссылки |
| `list_filter` | Панель фильтров справа |
| `list_select_related` | Авто-`select_related()` в списке |
| `search_fields` | Поля полнотекстового поиска |
| `filter_horizontal` | Удобный виджет для M2M |
| `autocomplete_fields` / `raw_id_fields` | Поиск по FK/M2M |
| `readonly_fields` | Отображение без редактирования |
| `prepopulated_fields` | Авто-заполнение `slug` из `title` |
| `date_hierarchy` | Быстрая навигация по датам |
| `list_per_page` | Пагинация |
| `fieldsets` / `inlines` | Кастомизация формы + связанные модели |

### 2.4 Производительность
* Django-Debug-Toolbar для анализа SQL.
* Кэш fragment / per-view / low-level.

### 2.5 QuerySets и кастомные менеджеры

```python
class PostQuerySet(models.QuerySet):
    def published(self):
        """Фильтрует опубликованные посты."""
        return self.filter(is_draft=False)

    def popular(self):
        return self.annotate(likes=models.Count("likes")).order_by("-likes")


class Post(models.Model):
    # … поля …

    # «objects» → базовый менеджер, «public» → кастомный
    objects = models.Manager()
    public = PostQuerySet.as_manager()

```

**Плюсы кастомных QuerySet-ов**
* `Post.public.published().popular()` — читаемо, можно комбинировать.

**Часто используемые методы QuerySet**

### 2.6 Production-tips
* `DEBUG = False`, `ALLOWED_HOSTS`, `SECURE_*` headers.
* WSGI-сервер — Gunicorn/Uvicorn, `--workers = 2×CPU`.
* Статика: `collectstatic` + nginx.
* БД: отдельный контейнер/PostgreSQL, регулярные бэкапы.

### 2.7 Django > Python (что использовать)
| Python | Django QuerySet | Почему лучше |
|--------|-----------------|-------------|
| `sorted(qs, key=...)` | `qs.order_by()` | сортировка на уровне БД, не грузим всё в память |
| `len(qs)` | `qs.count()` | `COUNT(*)` без выборки данных |
| `obj in qs` | `qs.filter(pk=obj.pk).exists()` | проверка существования 1 запросом |
| `list(set(ids))` | `qs.values_list("id", flat=True).distinct()` | `DISTINCT` в БД |

### 2.8 Короткие шорткаты
* `get_object_or_404(Model, **lookup)`  — вместо `try/except DoesNotExist`.
* `redirect("view-name", pk=obj.pk)`  — вместо ручного `HttpResponseRedirect`.
* `render(request, "template.html", ctx)`  — шорткат для `TemplateResponse`.

### 2.9 Оптимизация SQL запросов

При работе с Django ORM важно оптимизировать SQL-запросы для повышения производительности приложения. Рекомендуемые подходы:

- Избегайте проблемы N+1 запросов. Используйте:
  - `select_related()` для полей ForeignKey и OneToOne;
  - `prefetch_related()` для ManyToMany и обратных связей.
  Пример:
  ```python
  # Не оптимизированный вариант
  posts = Post.objects.all()
  for post in posts:
      print(post.author.username)

  # Оптимизированный вариант
  posts = Post.objects.select_related('author').all()
  for post in posts:
      print(post.author.username)
  ```

- Не выполняйте запросы в циклах – объединяйте фильтрации через ORM, чтобы избежать множества SQL-запросов.
- Используйте агрегатные функции и аннотации (`annotate()`, `aggregate()`) для вычислений на стороне базы данных.
- Применяйте `values()`/`values_list()` с аннотациями для группировки и выборки данных напрямую из БД.
- Для обновлений используйте `F()` выражения, чтобы проводить вычисления непосредственно в SQL.
- При необходимости сложных запросов рассмотрите использование подзапросов (`Subquery()`, `OuterRef()`) вместо ручного объединения множества запросов.
- Избегайте избыточного использования `.all()` – фильтруйте данные через `filter()`, а также используйте `only()` или `defer()` для ограничения выбираемых полей.
- Сырой SQL через `raw()` используйте только в крайних случаях, когда стандартные возможности ORM не удовлетворяют требованиям по оптимизации.
- Используйте `Prefetch()` для более гибкого управления выборкой связанных объектов, позволяя задавать кастомные фильтры и сортировку.
- Применяйте `Coalesce()` для обработки NULL-значений, чтобы задать значения по умолчанию в аннотированных полях.

Следуя этим рекомендациям, вы сможете существенно снизить нагрузку на базу данных и улучшить производительность вашего приложения.

---

## 3. 🤖  Guidelines for AI (если задача поручена LLM)

1. **Не выдумывай контекст.**  Используй только факты из задания/репозитория.
2. **Генерируй минимальный diff.**  При редактировании файла повторяй только изменённые строки + `// ... existing code ...`.
3. **Без «волшебных» зависимостей.**  Любая новая библиотека → добавь в `requirements.txt`.
4. **Соблюдай правила из разд. 1 и 2.**  Именование, аннотации, `select_related()` и т.д.
5. **Тестируй ментально.**  Перед ответом проверь, что код запускается без ошибок линтера.
6. **Комментарий-объяснение вынеси в чат, не в код.**

---

## 4. 🚀 Пример
```python
from datetime import datetime
from typing import Iterable

TODAY = datetime.now().date()

def filter_expired_coupons(coupons: Iterable["Coupon"]) -> list["Coupon"]:
    """Возвращает купоны, срок которых не истёк."""
    return [coupon for coupon in coupons if coupon.expired_at >= TODAY]
```

## 5. 📑 Django Model Fields Cheat-Sheet

> Часто используемые поля + самые популярные аргументы. Значения по умолчанию опущены, если они очевидны.
>
> **Общие аргументы:** `verbose_name`, `help_text`, `null`, `blank`, `default`, `choices`, `db_index`, `unique`, `editable`, `validators`.

### 5.1 Авто- и числовые
| Поле | Ключевые аргументы | Пример |
|------|-------------------|--------|
| `AutoField` / `BigAutoField` | primary_key<br>`BigAutoField` = `BIGINT` | `id = models.BigAutoField(primary_key=True)` |
| `IntegerField` / `SmallIntegerField` / `PositiveIntegerField` | `null`, `blank` | `rating = models.PositiveIntegerField()` |
| `DecimalField` | `max_digits`, `decimal_places` | `price = models.DecimalField(max_digits=10, decimal_places=2)` |
| `FloatField` | — | `weight = models.FloatField()` |
| `DurationField` | — | `ttl = models.DurationField()` |

### 5.2 Строковые
| Поле | Ключевые аргументы | Пример |
|------|-------------------|--------|
| `CharField` | `max_length` | `name = models.CharField(max_length=120)` |
| `TextField` | — | `description = models.TextField(blank=True)` |
| `SlugField` | `max_length`, `allow_unicode` | `slug = models.SlugField(max_length=200, unique=True)` |
| `EmailField` / `URLField` | `max_length` | `email = models.EmailField()` |
| `UUIDField` | `default=uuid4`, `editable=False` | `uuid = models.UUIDField(default=uuid.uuid4, editable=False)` |
| `JSONField` | `encoder`, `decoder` | `meta = models.JSONField(blank=True, default=dict)` |

### 5.3 Дата и время
| Поле | Аргументы | Пример |
|------|-----------|--------|
| `DateField` / `TimeField` | `auto_now`, `auto_now_add` | `created = models.DateField(auto_now_add=True)` |
| `DateTimeField` | те же | `updated = models.DateTimeField(auto_now=True)` |

### 5.4 Файлы и медиа
| Поле | Аргументы | Пример |
|------|-----------|--------|
| `FileField` / `ImageField` | `upload_to`, `storage`, `max_length` | `avatar = models.ImageField(upload_to="avatars/")` |
| `BinaryField` | `editable=False` | `raw = models.BinaryField()` |

### 5.5 Сетевые
| Поле | Аргументы | Пример |
|------|-----------|--------|
| `GenericIPAddressField` | `protocol="IPv4/IPv6/both"`, `unpack_ipv4` | `ip = models.GenericIPAddressField(protocol="IPv4")` |

### 5.6 Связи
| Поле | Ключевые аргументы | Пример |
|------|-------------------|--------|
| `ForeignKey` | `to`, `on_delete`, `related_name`, `limit_choices_to`, `db_constraint` | `author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")` |
| `OneToOneField` | всё как у `ForeignKey` + `parent_link` | `profile = models.OneToOneField(User, on_delete=models.CASCADE)` |
| `ManyToManyField` | `to`, `related_name`, `through`, `through_fields`, `db_table` | `tags = models.ManyToManyField(Tag, related_name="posts")` |

### 5.7 Ограничения/индексы (Meta)
```python
class Meta:
    indexes = [models.Index(fields=["slug", "published_at"])]
    constraints = [models.UniqueConstraint(fields=["slug"], name="uniq_slug")] 
```

### 5.8 Дополнительные специальные поля
| Поле | Хранит | Ключевые моменты | Пример |
|------|--------|-----------------|--------|
| `BooleanField` | `True/False` | `default=False` | `is_active = models.BooleanField(default=True)` |
| `BigIntegerField` | 64-bit int | Когда нужно > 2^31 | `views = models.BigIntegerField()` |
| `PositiveSmallIntegerField` | 0…32767 | маленький UNSIGNED | `age = models.PositiveSmallIntegerField()` |
| `FilePathField` | путь к файлу | `path`, `match`, `recursive` | `log_file = models.FilePathField(path="/var/log", match=".*\.log")` |
| `ArrayField`* | массив любого типа | only PostgreSQL | `tags = ArrayField(models.CharField(max_length=20))` |
| `HStoreField`* | key/value (строки) | only PostgreSQL | `meta = HStoreField()` |
| `CITextField`* | case-insensitive text | only PG/`django.contrib.postgres` | `email = CITextField(unique=True)` |
| `GeometryField` / `PointField` | гео-данные | GeoDjango | `location = PointField()` |
| `MoneyField`** | деньги + валюта | из `django-money` | `price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')` |

\* — из `django.contrib.postgres`.  
\** — сторонняя библиотека, добавить в `requirements.txt`.

### 5.9 Часто используемые аргументы (расшифровка)
| Аргумент | Что делает | Пример |
|----------|-----------|--------|
| `verbose_name` | Человекочитаемое имя поля в админке | `title = models.CharField(max_length=200, verbose_name="Заголовок")` |
| `help_text` | Подсказка под полем | `slug = models.SlugField(help_text="url-имя, латиница")` |
| `null` / `blank` | `null` — в БД, `blank` — в формах | `middle_name = models.CharField(max_length=60, null=True, blank=True)` |
| `default` | Значение по умолчанию | `is_active = models.BooleanField(default=False)` |
| `choices` | Ограничение списка значений | `status = models.CharField(max_length=20, choices=Status.choices)` |
| `unique` | Уникальное значение в колонке | `slug = models.SlugField(unique=True)` |
| `db_index` | Создать индекс | `created = models.DateTimeField(db_index=True)` |
| `on_delete` | Поведение FK при удалении | `models.CASCADE / PROTECT / SET_NULL` |
| `related_name` | Имя обратной связи | `author = models.ForeignKey(User, related_name="posts", ...)` |
| `upload_to` | Путь загрузки файлов | `image = models.ImageField(upload_to="blog/%Y/%m/%d")` |
| `auto_now` / `auto_now_add` | Авто-обновление даты/времени | `updated = models.DateTimeField(auto_now=True)` |
| `max_digits`, `decimal_places` | Для `DecimalField` | `price = models.DecimalField(max_digits=8, decimal_places=2)` |

---

## 6. ⚙️  Полезные команды CLI (Python & Django)

### 6.1 Python / venv
```bash
# создать и активировать окружение
python -m venv venv
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate          # Windows

# установка зависимостей
pip install -r requirements.txt

# посмотреть установленные пакеты
pip freeze > requirements.txt   # вывести версии

# запуск скрипта
python main.py --help

# дополнительные команды:
deactivate                           # выйти из виртуального окружения
pip list                             # показать установленные пакеты
python -m pip install --upgrade pip  # обновить pip до последней версии
cd <путь>                       # перейти в указанный каталог
pip install <пакет>             # установить пакет
pip uninstall <пакет>           # удалить пакет
python --version                # показать версию Python
```

### 6.2 Django основные
```bash
# запуск сервера
python manage.py runserver

# миграции
python manage.py makemigrations           # создать
python manage.py makemigrations app --empty comment  # пустая
python manage.py migrate                  # применить
python manage.py showmigrations           # список
python manage.py migrate app 0003         # откат до 0003

# superuser и интерактивная консоль
python manage.py createsuperuser
python manage.py shell_plus --ipython     # django-extensions

# создать проект/приложение
django-admin startproject myproject
python manage.py startapp blog

# дополнительные команды:
python manage.py check                  # проверить конфигурацию проекта
python manage.py collectstatic          # собрать статические файлы
python manage.py dbshell                # открыть оболочку БД проекта
python manage.py dumpdata > data.json   # экспортировать данные
python manage.py loaddata data.json     # импортировать данные
python manage.py shell                # зайти в Django shell
exit()                                  # выйти из Django shell
```

### 6.3 Тесты / качество
```bash
pytest -q                # быстрый запуск тестов
pytest --cov=app tests/  # + покрытие
ruff check .             # анализ стиля
ruff format .            # авто-форматирование
```

### 6.4 Основные Linux команды
```bash
pwd                             # показать текущую директорию
ls -la                          # перечислить файлы и каталоги
cd <путь>                       # перейти в указанный каталог
nano <файл>                     # открыть файл в nano
vim <файл>                      # открыть файл в vim
./<скрипт>                      # запустить исполняемый файл
bash <скрипт.sh>                # запустить bash-скрипт
<команда> &                     # запустить процесс в фоне
nohup <команда> &               # запустить без прерывания после выхода
chmod +x <файл>                 # сделать файл исполняемым
chmod 755 <файл>                # задать права rwxr-xr-x
export VAR=value                # установить переменную окружения
printenv VAR                    # показать значение переменной
env                             # вывести все переменные окружения
# Права доступа:
# r (read=4), w (write=2), x (execute=1)
chmod 644 <файл>               # rw-r--r--
chmod 600 <файл>               # rw-------
chown <пользователь>:<группа> <файл>  # сменить владельца и группу
# Пайпы и перенаправления:
<команда1> | <команда2>        # передать вывод первой команды второй
<команда1> && <команда2>       # выполнить вторую команду, если первая удалась
<команда1>; <команда2>         # выполнить команды последовательно
# Работа с файлами:
echo "текст" > файл.txt        # записать текст в файл (перезапись)
echo "текст" >> файл.txt       # добавить текст в конец файла
cat файл.txt                   # вывести содержимое файла
# Скрытые файлы:
ls -a                          # показать все файлы, включая скрытые
# Изменение прав через символы:
chmod u+rw,go-w <файл>        # добавить rw владельцу, убрать w группе и прочим
# Выход из редакторов:
# vim: :q (выйти), :wq (сохранить и выйти)
# nano: Ctrl+X, затем Y/Enter — сохранить и выйти
# Файлы с символом '~' или '$' в конце — резервные копии файлов, создаваемые редакторами (например, file.txt~)
# Переменные окружения обозначаются через $VAR
# Разница между редакторами:
# vim — modal editor: нажмите i для вставки, Esc для команд, :wq для сохранения и выхода
# nano — простой редактор: Ctrl+O для сохранения, Ctrl+X для выхода
# Справка и документация:
<команда> --help / <команда> -h    # краткая/подробная справка
man <команда>                      # ман-страница
info <команда>                     # info-страница
whatis <команда>                   # однострочное описание
type <команда>                     # тип команды и путь до неё
tree -d -a                         # дерево директорий и файлов, включая скрытые
which <команда>                    # путь к исполняемому файлу
whereis <команда>                  # расположение бинарников и документации
touch <файл>                       # создать пустой файл или обновить время модификации
mkdir -p <директория>              # создать каталог, включая вложенные
cp -r <источник> <назначение>      # рекурсивное копирование
mv <источник> <назначение>         # перемещение или переименование
rm -r <файл/директория>            # рекурсивное удаление
# Pipes и перенаправления:
<команда1> | <команда2>            # передать вывод первой команды второй
<команда1> && <команда2>           # выполнить вторую, если первая успешна
<команда1>; <команда2>             # последовательное выполнение
# Работа с файлами:
echo "текст" > файл.txt            # перезаписать файл
echo "текст" >> файл.txt           # дописать в конец файла
cat файл.txt                        # вывести содержимое файла
# Просмотр:
less <файл>                        # постраничный просмотр
# Привилегированное выполнение:
sudo -u <пользователь> <команда>   # запустить от имени другого пользователя
su [<пользователь>]                # переключиться на другого пользователя
# Поиск:
grep '<паттерн>' <файл>            # поиск по шаблону
```

---

## 7. 📂 Django project structure (что за что отвечает)

| Путь | Содержит | Комментарий |
|------|----------|-------------|
| `manage.py` | CLI-обёртка | Запуск сервера, миграции |
| `project/settings.py` | Настройки | DEBUG, DATABASES, INSTALLED_APPS |
| `project/urls.py` | Глобальные маршруты | `include(app.urls)` |
| `app/models.py` | Модели | ORM-слой |
| `app/views.py` | Контроллеры | FBV/CBV |
| `app/urls.py` | URL-ы приложения | Чётко отражают REST |
| `templates/` | HTML-шаблоны | Поддержка вложенных каталогов |
| `static/` | CSS/JS/img | Собирается `collectstatic` |
| `media/` | Загружаемые пользователем файлы | Сервится nginx |
| `requirements.txt` | Зависимости | Версионируем |
| `.env` | Секреты | НЕ коммитим |

---

## 8 Информация по PostgreSQL
- [YouTube плейлист](https://www.youtube.com/playlist?list=PLPPIc-4tm3YQsdhSV1qzAgDKTuMUNnPmp)
- Установлена версия PostgreSQL 17.4 (предыдущая версия удалена)
- Пароль: ``
- Порт: 5432 (стандартный)
- Доступ через меню «Пуск»: `PostgreSQL 17`
- `pgAdmin 4` — панель для управления серверами и базами данных
- `SQL Shell (psql)` — для выполнения SQL-запросов вручную
- Основные команды в psql:
  - `\?` — список всех команд
  - `q` — выход
  - `\l` — список баз данных
  - `CREATE DATABASE название;` — создать базу данных
  - `\c название` — подключиться к базе данных
  - `\conninfo` — информация о подключении (БД, пользователь, сервер, адрес, порт)
  - `DROP DATABASE название;` — удалить базу данных
  - `CREATE TABLE название(параметры);` — создать таблицу
  - `\d` — список таблиц
  - `\d название` — показать структуру таблицы
  - `DROP TABLE название;` — удалить таблицу
  - `\dt` — альтернативный список таблиц
  - `\h` — справка по SQL-командам
  - `\copy <таблица> TO 'file.csv' CSV HEADER` — экспорт таблицы в CSV
  - `\copy <таблица> FROM 'file.csv' CSV HEADER` — импорт таблицы из CSV
- Проблема с кодировкой в shell (Windows):
  - Одноразовое решение: `psql \! chcp 1251`
  - Постоянное решение:
    - Открыть реестр: Win+R → regedit →
      `Компьютер\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Command Processor`
    - Создать строковый параметр `Autorun` со значением `chcp 1251`
    - [Видео решение](https://youtu.be/nxGhGQFk34Y?si=dgzUUrlzaGbMrn1s)