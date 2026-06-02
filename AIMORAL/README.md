# MoralMachine

This repository contains a Django app named `AIMORAL` and the supporting project scaffolding to deploy on Render.

## Local development

1. Create a Python virtual environment and activate it.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run migrations:
   ```bash
   python manage.py migrate
   ```
4. Start the app:
   ```bash
   python manage.py runserver
   ```

## Render deployment

The project includes `render.yaml` and `Procfile` for Render.

- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn project.wsgi:application`
- Release command: `python manage.py migrate`

### Recommended environment variables on Render

- `DJANGO_DEBUG = False`
- `DJANGO_ALLOWED_HOSTS = your-app.onrender.com,moralmachine-3.onrender.com`
- `DJANGO_CSRF_TRUSTED_ORIGINS = https://your-app.onrender.com,https://moralmachine-3.onrender.com`
- `DJANGO_SECURE_SSL_REDIRECT = True`
- `DJANGO_SECRET_KEY = <your secret key>`
- `DATABASE_URL = <your database URL>` (optional; falls back to SQLite)
