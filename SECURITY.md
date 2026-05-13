# Security Audit - Student Notes App

## Finding 1: Secret key exposed in settings.py

* Risk: Anyone who reads the source code could access the Django secret key. This could help an attacker forge session cookies or abuse cryptographic signing.
* Fix: Moved `SECRET_KEY` to an environment variable using `python-decouple` and `config('DJANGO_SECRET_KEY')`.
* Location: `student_notes/settings.py`

## Finding 2: Production DEBUG setting could expose sensitive details

* Risk: If `DEBUG=True` is used in production, Django error pages may expose stack traces, file paths, settings, and other sensitive information.
* Fix: Changed `DEBUG` so it is controlled by the `DJANGO_DEBUG` environment variable. Production should use `DJANGO_DEBUG=False`.
* Location: `student_notes/settings.py`

## Finding 3: ALLOWED_HOSTS needed production verification

* Risk: If `ALLOWED_HOSTS` is too broad or not configured, the application may be more exposed to Host header attacks.
* Fix: Added `DJANGO_ALLOWED_HOSTS` environment variable support and provided safe local defaults for development.
* Location: `student_notes/settings.py`

## Finding 4: HTTPS and secure cookie settings needed production logic

* Risk: Without HTTPS redirect and secure cookies in production, session and CSRF cookies could be sent over unencrypted HTTP.
* Fix: Added `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, and HSTS settings that become active when `DEBUG=False`.
* Location: `student_notes/settings.py`

## Finding 5: SQL injection risk from unsafe raw SQL

* Risk: Concatenating user input into a raw SQL query could allow an attacker to change the query and access or modify data.
* Fix: Used the Django ORM with `Note.objects.filter(title__icontains=search)`. Django ORM parameterizes the query instead of treating user input as executable SQL. The unsafe and safe versions are shown side by side in comments.
* Location: `notes/views.py`

## Finding 6: User note content could be rendered unsafely

* Risk: If user-created note content were rendered with `|safe` or inside `{% autoescape off %}`, a user could store a `<script>` tag and cause cross-site scripting in another user's browser.
* Fix: Verified templates use Django auto-escaping with `{{ note.title }}`, `{{ note.content }}`, and `{{ search }}`. The project does not use `|safe` for untrusted user content.
* Location: `notes/templates/notes/note_list.html`, `notes/templates/notes/note_detail.html`, `notes/templates/notes/note_confirm_delete.html`

## Finding 7: POST forms require CSRF protection

* Risk: Without CSRF tokens, an attacker could trick a logged-in user into submitting a form from another website.
* Fix: Added `{% csrf_token %}` inside every POST form.
* Location: `notes/templates/notes/note_form.html`, `notes/templates/notes/note_confirm_delete.html`

## Finding 8: Notes list view needed caching

* Risk: Without caching, repeated visits to the notes list can cause unnecessary database queries and reduce performance as traffic increases.
* Fix: Added `@cache_page(60 * 5)` to cache the notes list view for 5 minutes. The timeout is documented in the code comment.
* Location: `notes/views.py`

## Finding 9: Cache stale-data risk documented

* Risk: Cached pages can show outdated content. In this app, a user may see an older notes list for up to 5 minutes after a note is changed.
* Fix: Documented the stale-data risk in the code comments and README. The short 5-minute timeout balances performance and freshness for this small app.
* Location: `notes/views.py`, `README.md`
