# lab3
Пономаренко Нікіта Євгенович КВ-21мп ЛР3 Організація виконання асинхронних задач Web-додатка Скорочення URL-посилань

https://docs.google.com/document/d/1g9JFNBCbH4q8Qniy8_yneX6dMoew_KY5/edit


# Docker

To run project in docker simply run:

```sh
docker-compose up -d --build
```

And then to apply migrations:

```sh
docker-compose exec main-api /bin/sh -c "python manage.py makemigrations && python manage.py migrate"
```

Optionaly create superuser:

```sh
docker-compose exec main-api /bin/sh
python manage.py createsuperuser
<Ctrl + D>
```

To see logs:

```sh
docker-compose logs -f
```

# Run localy

Install requirements:

```sh
pip install -r requirements.txt
```

Apply migrations:

```sh
cd cuttly
```

```sh
python manage.py makemigrations
python manage.py migrate
```

Run server:

```sh
python manage.py runserver
```

Optionaly create superuser:

```sh
python manage.py createsuperuser
```