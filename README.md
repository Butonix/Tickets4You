# Tickets4You

A **search interface** for traveling websites built with [Python](https://www.python.org/) using the [Django Web Framework](https://www.djangoproject.com/).

### Technology Stack

* [Python](https://www.python.org/) 3.6.x
* [Django Web Framework](https://www.djangoproject.com/) 2.1.x
* [Twitter Bootstrap 4](https://getbootstrap.com/docs/4.0/getting-started/introduction/)
* [jQuery 3](https://api.jquery.com/)

### Installation Guide

Clone this repository:

```shell
$ git clone https://github.com/thetruefuss/Tickets4You.git
```

Install requirements:

```shell
$ pip install -r requirements.txt
```

Copy `.env.example` file content to new `.env` file and update the credentials if any i.e Gmail account etc.

Run Django migrations to create database tables:

```shell
$ python manage.py migrate
```

Run the development server:

```shell
$ python manage.py runserver
```

Verify the deployment by navigating to [http://127.0.0.1:8000](http://127.0.0.1:8000) in your preferred browser.
