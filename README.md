# InfoLib 2.0
Redesigned version of InfoLib – a book checkout, reviewing and browsing application for the guild of Information Networks. Originally created as a school group project for course: CS-E4400 - Design of WWW Services (Aalto University).

The previous, original version can be found here: https://github.com/JoelLappalainen/infoLib

---

## Main technologies:

* Django
* Tailwind CSS framework in the frontend

## Getting started (from scratch)

Install Python 3.11.0 and Postgres 15.1

Clone the repository
```bash
$ git clone git@github.com:alexialeimu/infoLib-2.0.git
$ cd infolib-2.0
```

Setup virtual environment
```bash
$ python3 -m venv .venv
$ source .venv/bin/activate
```

Install dependencies
```bash
$ cd infolib/theme/static_src
$ npm install
```

Install requirements
```bash
$ cd infolibdemo/
$ pip3 install -r requirements.txt
```

Install Postgres.app cmd line tools
```bash
# close & reopen the window after the installation
$ sudo mkdir -p /etc/paths.d && echo /Applications/Postgres.app/Contents/Versions/latest/bin | sudo tee /etc/paths.d/postgresapp 
```

Create database
```bash
$ psql
> create database <dbname>;
> create user <username> superuser;
> alter user <username> password <password>;
```

Replace sqlite3 information with the new ones. Store the database name, username and password in a .env file in the root of the project.

## Running the app

Make migrations
```bash
$ python3 manage.py makemigrations
$ python3 manage.py migrate
```

Backend:
```bash
$ python3 manage.py runserver
```

Frontend (Tailwind development mode):
```bash
$ python3 manage.py tailwind start
```

Navigate to to http://127.0.0.1:8000