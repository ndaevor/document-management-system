# document-management-system
A website created using python with django where user can upload and download documents



## Features

- **User Account Management**: Registration, login, and account settings.
- **Document Upload**: Users can upload, download, and delete documents.

## Setup Instructions

# Prerequisites

- Python 3.x
- Django 3.x or later
- SQLite (default database for Django)

# Installation

python -m venv venv
venv\Scripts\activate
This command sets up a new directory (venv) that contains a clean Python installation and allows you to install packages in isolation from your global Python environment.


pip install -r requirements.txt
installing the requirements


python manage.py migrate
applying migrations


python manage.py createsuperuser
creating superuser


python manage.py runserver
start the server

