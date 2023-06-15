# Developer Guide

Welcome to Feminnovate Backend. This guide will guide you through setting up PostgreSQL database and ensuring that the backend is available for local development

## Setting up: Ubuntu and Windows

This guide is built with **Ubuntu environment on Windows (or WSL)** in mind. If you are a windows user, you can follow through the following commands by first opening your Ubuntu terminal or using your WSL.

### Download Ubuntu

1. Download **Ubuntu 22.04.2 LTS** in Microsoft Store
2. Open Windows PowerShell as an administrator
3. Start the Ubuntu WSL shell

### Update Packages

1. Update your package repository, upgrade existing packages, and reboot

```
$ sudo apt update
$ sudo apt upgrade
$ reboot
```

2. (If you haven't done so) Install PIP, the Python package manager and Virtual Environment module. Install Git as well

```
$ sudo apt install python3-pip python3-venv
$ sudo apt install git
```

### Install PostgreSQL and PostGIS

1. Import the PostgreSQL repository key, and add the repository

```
$ sudo apt install curl ca-certificates gnupg
$ curl https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/apt.postgresql.org.gpg >/dev/null
$ echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" | sudo tee /etc/apt/sources.list.d/pgdg.list
$ sudo apt update
```

2. Install **PostgreSQL 14**.
(Why 14?) because currently my internship uses 14 and I'm too lazy to have to store 2 postgres versions in my ubuntu terminal :(

```
$ sudo apt install postgresql-14 postgresql-client-14
```

3. Start the PostgreSQL service on your computer

```
$ sudo service postgresql start
```

Note: this command is unique for Windows WSL users. If you are using "pure" Ubuntu (Linux OS), please use `sudo systemctl start postgresql` instead.

4. Log in as the Postgres superuser

```
$ sudo su - postgres
```

5. Start the Postgres interactive terminal

```
psql postgres
```

6. Create a database called `feminnovate` on Postgres, then create a user and grant it privileges to modify and write to the database

```
# CREATE DATABASE feminnovate;
# CREATE USER feminnovateuser WITH PASSWORD 'feminnovate';
# GRANT ALL PRIVILEGES ON DATABASE feminnovate TO feminnovateuser;
```

7. `CTRL-D` to exit the Postgres shell, and `CTRL-D` to logout of the Postgres superuser

### Create a Virtual Environment and Install Requirements

1. Navigate to the directory of the cloned repository

2. Create a Python Virtual Environment

```
$ python3 -m venv env
```

3. Activate the Virtual Environment

```
$ source env/bin/activate
```

4. Install the required packages.

```
$ pip install -r requirements.txt
```

### Create Admin User

1. Run in terminal

```
$ python3 manage.py createsuperuser
```

2. Enter username and password

### Setup and Run the Django Backend

1. Get a copy of the `.env` file from another team member. Place the `.env` file in the `feminnovate_backend` folder

Ideally, the folder should have the following structure. 

```
feminnovate_backend
├── Developer Guide.md
├── feminnovate_backend
│   ├── __init__.py
│   ├── __pycache__
|   ├── .env
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
└── requirements.txt
```

Note that this structure is taken at the time this README is created. However, I believe that the inner `feminnovate_backend` folder should remain untouched, as it won't be the main development app for Django.

2. Update your Postgres username and password in this file so Django can connect to your database

If you use the default user `feminnovateuser` and password `feminnovate`, then you don't have to modify the username anymore. However, you might be needing to update your PostgreSQL port. Check this accordingly with your system.

3. Run the database migrations needed for this project

```
$ python3 manage.py migrate
```

4. Run the local Django development server

```
$ python3 manage.py runserver
```

5. Using your browser or Postman, navigate to `localhost:8000/api/public` and see if it works

## Setting up: MacOS

Cos of our frens who use MacOS (more superior than windows tho T_T)

### Create Virtual Environment and Install Requirements

1. Navigate to the repository after cloning

2. Create a Python Virtual Environment

```
$ python3 -m venv env
```

3. Activate the Virtual Environment

```
$ source env/bin/activate
```

4. Install the required packages

```
$ pip install -r requirements.txt
```

### Install and Setup PostgreSQL

1. If you are on MacOS, make sure you have the [Homebrew](https://brew.sh/) package manager installed.<br>
This is a legit gamechanger :O

2. Using Homebrew, install and start Postgres:

```
$ brew install postgresql
$ brew services start postgresql
```

3. Start the Postgres interactive terminal

```
$ psql postgres
```

4. Create a database called `feminnovate` on Postgres, then create a user and grant it privileges to modify and write to the database

```
# CREATE DATABASE feminnovate;
# CREATE USER feminnovateuser WITH PASSWORD 'feminnovate';
# GRANT ALL PRIVILEGES ON DATABASE feminnovate TO feminnovateuser;
```

5. `CTRL-D` to exit the Postgres shell.


### Setup and Run the Django Backend

1. Get a copy of the `.env` file from another team member. Place the `.env` file in the `feminnovate_backend` folder

Ideally, the folder should have the following structure. 

```
feminnovate_backend
├── Developer Guide.md
├── feminnovate_backend
│   ├── __init__.py
│   ├── __pycache__
|   ├── .env
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
└── requirements.txt
```

Note that this structure is taken at the time this README is created. However, I believe that the inner `feminnovate_backend` folder should remain untouched, as it won't be the main development app for Django.

2. Update your Postgres username and password in this file so Django can connect to your database.

If you use the default user `feminnovateuser` and password `feminnovate`, then you don't have to modify the username anymore. However, you might be needing to update your PostgreSQL port. Check this accordingly with your system.

3. Run the database migrations needed for this project

```
$ python3 manage.py migrate
```

4. Run the local Django development server

```
$ python3 manage.py runserver
```

5. Using your browser or Postman, navigate to `localhost:8000/api/public` and see if it works
