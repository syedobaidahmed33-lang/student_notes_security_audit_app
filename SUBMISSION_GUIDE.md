# Submission Guide - Lesson 12 Assignment 2

## What to Upload

Upload one PDF to Populi/Blackboard that contains:

1. Public GitHub repository link
2. Screenshot of app running in browser
3. Screenshot of `student_notes/settings.py` showing environment variables, DEBUG, ALLOWED_HOSTS, and secure cookie settings
4. Screenshot of `notes/views.py` showing SQL injection safe ORM comment and cached view
5. Screenshot of `note_form.html` showing `{% csrf_token %}`
6. Screenshot of `note_confirm_delete.html` showing `{% csrf_token %}`
7. Screenshot of template auto-escaping in `note_list.html` or `note_detail.html`
8. Screenshot of `SECURITY.md`
9. Screenshot of README scalability section

## GitHub Steps

```bash
git init
git add .
git commit -m "Add hardened Django student notes app"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

Make sure `.env` and `db.sqlite3` are not uploaded. The `.gitignore` file already blocks them.

## Local Run Steps

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Then open:

```text
http://127.0.0.1:8000/
```
