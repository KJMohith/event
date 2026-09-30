# Event Lifecycle & Certification System

A reproducible Django application for event registration, attendance, feedback, marks, QR verification, and conditional PDF certificate generation.

## Why this repository is structured this way

The project is intentionally self-contained and testable. A fresh checkout can install its dependencies, run migrations, execute the automated test suite, and start the development server without relying on local machine state.

## Features

- Event CRUD
- Participant registration with receipt/photo validation
- Unique transaction IDs
- Attendance toggle endpoint
- Feedback and rating workflow
- Marks validation from 0–100
- Eligibility rule for certificates
- QR codes linking to certificate verification/download routes
- PDF certificate generation with ReportLab
- AJAX dashboard updates
- Django admin integration
- Docker development environment
- GitHub Actions CI

## Project layout

```text
.
├── manage.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── .github/workflows/tests.yml
├── event_lifecycle/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── events/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   ├── utils.py
│   ├── validators.py
│   ├── admin.py
│   ├── migrations/
│   └── tests/
├── templates/
└── static/
```

## Requirements

- Python 3.12+
- pip
- Optional: Docker

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py check
python manage.py test
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Docker

```bash
docker compose up --build
```

## Testing

The test suite covers:

- certificate eligibility logic
- transaction uniqueness
- registration validation
- marks/rating validation
- dashboard rendering
- statistics endpoint
- attendance AJAX behavior
- marks updates
- certificate access control
- PDF certificate response

Run it with:

```bash
python manage.py test
```

CI runs Django system checks, migrations, and the complete test suite on every push and pull request.

## Certificate eligibility

A participant can download a certificate only when:

1. attendance is marked;
2. feedback has been submitted; and
3. marks have been entered.

The server enforces this rule, so the UI cannot bypass it.

## Configuration

Secrets and deployment settings are environment-driven. Do not commit `.env` or production secrets. See `.env.example` for the required variables.

## Security notes

The repository does not contain a production secret key. `DEBUG`, allowed hosts, and CSRF trusted origins are configurable through environment variables.
