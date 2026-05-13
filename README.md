# Student Notes App - Security Audit and Hardening

This Django application was created for Lesson 12 - Assignment 2: Audit and Harden a Django Application. It is a small notes application where users can create, search, view, edit, and delete notes. The project demonstrates security fixes for SQL injection risk, XSS prevention, CSRF protection, secret management, production settings, caching, and scalability planning.

## Features

- Create, view, edit, and delete notes
- Search notes by title
- Safe database queries using Django ORM
- CSRF protection on every POST form
- Auto-escaped template variables for user-supplied data
- Environment-variable based configuration
- Production-focused security settings
- Cached notes list view

## How to Run Locally

1. Create a virtual environment:

```bash
python -m venv .venv
```

2. Activate the virtual environment:

```bash
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a local `.env` file from `.env.example` and set the variables:

```bash
cp .env.example .env
```

5. Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

6. Start the development server:

```bash
python manage.py runserver
```

7. Open the app in a browser:

```text
http://127.0.0.1:8000/
```

## Security Fix Summary

The application was audited and hardened in several places. The Django secret key was moved out of `settings.py` and into an environment variable. Production settings were added for `DEBUG`, `ALLOWED_HOSTS`, HTTPS redirection, and secure cookies. All POST forms include `{% csrf_token %}`. Templates render user-supplied data with normal Django template variables such as `{{ note.title }}` and `{{ note.content }}`, which are auto-escaped by default. The code avoids raw SQL string concatenation and uses the Django ORM for user search input.

## Caching

The notes list view in `notes/views.py` uses Django's `@cache_page(60 * 5)` decorator. This caches the page for 5 minutes. The list page is a good caching candidate because users may visit it repeatedly and it performs a database query. The stale-data risk is that users may see an older notes list for up to 5 minutes after a note is created, edited, or deleted. For this small application, that risk is acceptable because notes do not require real-time updates.

## Scalability Plan

If this Django application needed to support 10x more users, I would first use vertical scaling for a quick short-term improvement by increasing CPU and memory on the server. After that, I would move to horizontal scaling by running multiple Django application servers behind a load balancer. The load balancer would distribute incoming requests across the servers so no single server becomes overloaded. Because users may be sent to different servers on different requests, sessions should be stored in a shared location such as database-backed sessions or Redis instead of local server memory. For the database, I would start with read replication if many users are reading notes at the same time. Partitioning would only be needed later if the database tables became very large.

## Files to Review

- `student_notes/settings.py` - environment variables, DEBUG, ALLOWED_HOSTS, HTTPS, cookies, cache configuration
- `notes/views.py` - safe ORM query and cached view
- `notes/templates/notes/note_form.html` - CSRF token in POST form
- `notes/templates/notes/note_confirm_delete.html` - CSRF token in POST form
- `notes/templates/notes/note_list.html` - auto-escaped user data and no unsafe filter on trusted output
- `SECURITY.md` - full audit findings, risk, fix, and location
