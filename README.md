# О проекте
Учебный проект для группы Python26_Ev

## Настройка проекта

### Создайте виртуальное окружение

```bash
python3 -m venv venv
```

### Активируйте виртуальное окружение

```bash
source venv/bin/activate
```

### Используйте pip для установки библиотек

```bash
pip install -r requirements-dev.txt
```

### Создайте базу данных в PostgreSQL

```bash
createdb <db_name>
```

### Создайте файл .env и заполните данные как в .env.template

```bash
cat .env.template > .env
```

### Проведите [миграции](https://docs.djangoproject.com/en/4.1/topics/migrations/)

```bash
python3 manage.py migrate
```

### Создайте супер-пользователя

```bash
python3 manage.py createsuperuser
```

### Запустите сервер

```bash
python3 manage.py runserver
```


## Полезные ссылки

[Django](https://docs.djangoproject.com/en/4.1/)

[DRF](https://www.django-rest-framework.org/)

[PostgreSQL](https://www.postgresql.org/)

[Swagger](https://drf-yasg.readthedocs.io/en/stable/)
