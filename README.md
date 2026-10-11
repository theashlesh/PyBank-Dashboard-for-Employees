# PyBank - Banking Management System

PyBank is a web-based Banking Management System developed using Python and Django. It is designed to help bank employees manage customer information, bank accounts, transactions, and banking reports through a centralized dashboard.

## Features

- **Employee Dashboard** — View an overview of banking operations.
- **Customer Management** — Add, view, update, and manage customer details.
- **Account Management** — Create and manage bank accounts.
- **Transaction Management** — Manage deposits, withdrawals, and transfers.
- **Reports** — View account details and transaction history.
- **Employee Authentication** — Provide authorized access to the system.

*Note: Features will be implemented progressively as development continues.*

## Technologies Used

- **Backend:** Python, Django
- **Frontend:** HTML, CSS
- **Database:** SQLite
- **Version Control:** Git and GitHub

## Project Structure

```text
PyBank/
├── manage.py
├── pybank/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── your_app/
│   ├── views.py
│   ├── models.py
│   ├── urls.py
│   └── admin.py
├── templates/
│   └── dashboard.html
├── static/
│   └── dashboard.css
├── db.sqlite3
├── requirements.txt
└── README.md
```

*Note: Replace `your_app` with your actual Django app name. The structure may vary depending on your project configuration.*

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/PyBank.git
cd PyBank
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install django
```

If a `requirements.txt` file is available, use:

```bash
pip install -r requirements.txt
```

### 4. Apply Database Migrations

```bash
python manage.py migrate
```

### 5. Create an Admin Account

```bash
python manage.py createsuperuser
```

Follow the instructions to set up your administrator account.

### 6. Run the Development Server

```bash
python manage.py runserver
```

Open the following URL in your browser:

http://127.0.0.1:8000/

## Learning Objectives

This project helps demonstrate practical knowledge of:

- Python and Django web development.
- Django models, views, URLs, and templates.
- HTML and CSS integration.
- Database operations using SQLite.
- Git and GitHub version control.
- Building a structured web application.

## Future Improvements

- Role-based employee access.
- Customer search and filtering.
- Account balance management.
- Transaction validation and audit logs.
- Dashboard analytics and reports.
- Responsive user interface.
- Deployment to a hosting platform.

## Security Notice

PyBank is an educational project and is not intended for handling real customer funds or sensitive banking operations. Production use would require appropriate security controls, access management, transaction integrity, audit logging, and regulatory compliance.

## Author

**Ashlesh**

## License

This project is available for learning and educational purposes. Add a `LICENSE` file if you want to specify formal reuse and distribution terms.
