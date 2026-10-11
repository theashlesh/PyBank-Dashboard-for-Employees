# PyBank - Django learning project

## Requirements
- Python 3.10+
- pip

## Setup (Windows)
Open a terminal in this folder:

```powershell
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
py manage.py makemigrations bank
py manage.py migrate
py manage.py createsuperuser
py manage.py runserver
```

Open http://127.0.0.1:8000/ and log in with the superuser credentials.
Create staff users in Django Admin at http://127.0.0.1:8000/admin/ if needed.
Only authenticated staff users can use the employee banking pages.

## Notes
This is an educational demo, not production banking software. It has no real payment rails,
regulatory/KYC controls, audit infrastructure, multi-factor authentication, or production-grade
deployment configuration. Use fictional customer data only. SQLite is intended for local learning.
