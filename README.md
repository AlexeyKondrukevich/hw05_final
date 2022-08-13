# Веб-приложение социальной сети

![https://github.com/AlexeyKondrukevich](https://img.shields.io/badge/Developed%20by-Kondr-blue)


Стек технологий:

- Python
- Django
- SQLite
- GIT

В приложении реализованы следующие возможности: публикация поста с возможностью прикрепить к нему картинку; комментирование поста; подписки на любимых авторов; отнести пост к какой-либо группе. Используется пагинация и кеширование. В админ-зоне можно добавлять/удалять посты, комментарии, группы. К приложению написаны unit-тесты. Проект реализован и запущен с помощью nginx и gunicorn, задеплоен на Яндекс.Облако.

### Настройка и запуск на ПК

Клонируем проект:

```bash
git clone git@github.com:AlexeyKondrukevich/hw05_final.git
```


Переходим в папку с проектом:

```bash
cd hw05_final
```

Устанавливаем виртуальное окружение:

```bash
python -m venv venv
```

Активируем виртуальное окружение:

```bash
source venv/bin/activate
```

> Для деактивации виртуального окружения выполним (после работы):
> ```bash
> deactivate
> ```

Устанавливаем зависимости:

```bash
python -m pip install --upgrade pip
```
```bash
pip install -r requirements.txt
```

Применяем миграции:

```bash
python yatube/manage.py makemigrations
python yatube/manage.py migrate
```

Создаем супер пользователя:

```bash
python yatube/manage.py createsuperuser
```

При желании делаем коллекцию статики:

```bash
python yatube/manage.py collectstatic
```

Предварительно сняв комментарий с:
```bash
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
```

И закомментировав: 
```bash
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
```

Иначе получим ошибку: You're using the staticfiles app without having set the STATIC_ROOT setting to a filesystem path.



Для запуска тестов выполним:

```bash
pytest
```

Запускаем проект:

```bash
python yatube/manage.py runserver
```