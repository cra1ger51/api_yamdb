# YaMDb(API)
API для сервиса YaMDb. Групповой проект.
_________________________________________________
## Описание
База произведений с обзорами, оценками и комментариями.

### YaMDB - возможности:

- Просмотреть список доступных произведений
- Оставлять обзоры, ставить оценки.
- Обсуждать обзоры в комментариях
- Посмотреть рейтинг произведения, либо поделиться своим опытом.
- Обладает удобным API-интерфейсом
 
_____________________________________________________

## Техническое описание

### Примененные технологии
 > Python 3.7.9
 > Django 3.2.16
 > djangorestframework 3.12.4
 > djangorestframework-simplejwt 4.7.2
 > PyJWT 2.1.0

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/cra1ger51/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```
Наполнение базы из CSV:

```
python manage.py basefill
```

Документация к APi доступна по адресу: 
```
http://127.0.0.1:8000/redoc/
```
## Примеры запросов
### Регистрация пользователя
>Тип запроса 
```POST```
>Endpoint 
```api/v1/auth/signup/```

Запрос:
```
{
  "email": "user@example.com",
  "username": "string"
}
```
Ответ:
```
{
  "email": "string",
  "username": "string"
}
```
______________________________________
### Авторы
- Даниил Алексеенко(https://github.com/cra1ger51)
- Андрей Иванишин(https://github.com/AIvanishin)
- Виталий Симоненко(https://github.com/SimoneVita)

### Лицензия
BSD 3-Clause License
