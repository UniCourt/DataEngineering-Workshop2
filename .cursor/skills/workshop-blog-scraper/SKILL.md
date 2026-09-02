---
name: workshop-blog-scraper
description: >-
  Guides Django, Docker, Postgres, and Python Insider scraping for the myworld
  workshop project. Use when scraping https://blog.python.org/, writing or
  updating web_scrapper.py, inserting into member_db/members_blog, running
  manage.py inside workshop_web_container, or when the user asks to use the
  workshop-blog-scraper skill.
---

# Workshop blog scraper (Django / Docker / Postgres)

You are assisting a **Data Engineering Workshop 2** student on the dockerized Django project `myworld`. Follow this file as the source of truth for paths, credentials, scrape selectors, and how commands are run.

When you write or change a scraper, **explain each step briefly for a beginner** (connect, truncate, download, find cards, parse fields, insert).

## Project Overview

The Django app is named `myworld` with an app called `members`. It is fully dockerized and uses PostgreSQL. A secondary function is scraping blog posts from `https://blog.python.org/` (Python Insider) and saving them to Postgres.

Typical layout (workshop copy may live under `workshop/myworld/`):

- `myworld/` — root project directory (Django project + scraper)
- `myworld/myworld/settings.py` — Django settings (`ALLOWED_HOSTS=['*']`, Postgres config)
- `myworld/members/models.py` — `Members` and `Blog` models
- `myworld/web_scrapper.py` — scrapes Python Insider and inserts into the DB
- `myworld/dockerfiles/Dockerfile` — Alpine-based Python image
- `myworld/docker-compose.yml` — `web_service` and `psql-db`
- `myworld/requirements.txt` — Django, psycopg2-binary, beautifulsoup4, requests

Do **not** invent a different database name, table, or column layout. Do **not** change Workshop 1 or unrelated folders unless the user asks.

## Tech Stack

- Python 3.10 (inside Docker) / Python 3.14 (local host — **do not** run workshop Python commands there)
- Django 4.2.16
- PostgreSQL 14
- Docker and Docker Compose
- Web scraping: `requests` and `re` (regular expressions) and/or `beautifulsoup4`
- Database driver: `psycopg2-binary`

## How to Run

Start services from the `myworld/` directory that contains `docker-compose.yml`:

```bash
docker compose up -d
```

Rebuild **only** if `requirements.txt` or the `Dockerfile` changed:

```bash
docker compose up --build -d
```

**Local sync:** compose maps `.` to `/root/workspace/site`. Edits on the host appear in the container immediately. Do not rebuild for ordinary `.py` changes.

**Port mapping:**

- Web: `8000:8000` (Django at http://127.0.0.1:8000/)
- Postgres published on the host: `5446:5432` (avoids local port 5432 conflicts)
- Django and `web_scrapper.py` connect **inside the Docker network** with `HOST: psql-db` and `PORT: 5432` — never `5446` from inside a container

**Docker exec:** to run commands, use:

```bash
docker exec -it workshop_web_container sh
```

Then inside the container:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
python3 web_scrapper.py
```

Non-interactive equivalent (from the host):

```bash
docker exec workshop_web_container python3 web_scrapper.py
docker exec workshop_web_container python manage.py migrate
```

## How to Scrape

Target URL: `https://blog.python.org/`

Store **title**, **release date**, **blog time**, and **author** in workshop Postgres (`member_db` / `members_blog`) the same way `web_scrapper.py` does.

### Selectors (Python Insider cards)

The live layout uses `article.post-card` (not the old Blogger `div.date-outer`).

Regex approach (find each card, then fields):

- Cards: `<article class="post-card...">...</article>`
- Title: `<h3>...</h3>` (strip nested tags)
- Author: `<span class="font-medium...">...</span>` (fallback `"Unknown"`)
- Date/time: `<time datetime="...">` — first 10 characters are the date (`YYYY-MM-DD`), characters 11–19 are the time (`HH:MM:SS`). If missing, use `1970-01-01` / `00:00:00`

BeautifulSoup equivalent (also valid in this workshop):

- `page_soup.select('article.post-card')`
- title: `blog.select_one('h3')`
- author: `blog.select_one('span.font-medium')`
- datetime: `blog.select_one('time')` and the `datetime` attribute

### Database steps in the scraper

1. Connect with `psycopg2` using the credentials below.
2. `TRUNCATE members_blog CASCADE;` — **do not** add `RESTART IDENTITY`.
3. Download the homepage (`requests.get(url, timeout=30)`).
4. Find cards, parse fields, insert each row.
5. Print title, date, time, and author for the student.

Insert contract:

```sql
INSERT INTO members_blog (title, release_date, blog_time, author, created_date)
VALUES (%s, %s::DATE, %s::TIME, %s, NOW())
```

Prefer writing or updating `myworld/web_scrapper.py` rather than adding a second unrelated scraper.

## Database Details

| Item | Value |
|------|--------|
| Database | `member_db` |
| Table | `members_blog` (Django model `members.Blog`) |
| User | `postgres` |
| Password | `123456` |
| Host (from containers) | `psql-db` |
| Port (from containers) | `5432` |
| Host port (from laptop / `psql` on host) | `5446` |

`Blog` fields: `title` (CharField), `release_date` (DateField), `blog_time` (TimeField), `author` (CharField), `created_date` (DateTimeField, `auto_now_add`).

If `member_db` does not exist yet:

```bash
docker exec -it psql-db sh
psql -U postgres
CREATE DATABASE member_db;
```

Verify after a scrape:

```sql
SELECT title, author, release_date, blog_time FROM members_blog LIMIT 5;
```

Create the table with migrations **inside** `workshop_web_container` (`makemigrations` / `migrate`), not with ad-hoc DDL unless the student is stuck.

## Strict Agent Rules

1. **Docker-first execution:** All `python manage.py` commands (migrations, runserver, createsuperuser) **and** script executions (`python3 web_scrapper.py`) **MUST** be run **inside** the `workshop_web_container` Docker container, **never** on the local host machine.
2. **Docker exec command:** To run commands, use: `docker exec -it workshop_web_container sh`.
3. **Port mapping:** The web service maps `8000:8000`. Postgres maps `5446:5432` (to avoid local port conflicts). Django connects to Postgres internally using `HOST: psql-db` and `PORT: 5432`.
4. **Local sync:** Because of volume mapping (`.` to `/root/workspace/site`), file edits on the local machine instantly sync to the container. Rebuilding is only required if `requirements.txt` or the `Dockerfile` changes (`docker compose up --build -d`).
5. **Web scraping logic:** The scraper uses regex to find `<article class="post-card">` tags. It extracts the title (`<h3>`), author (`<span class="font-medium">`), and date/time (`<time datetime="...">`). It truncates the `members_blog` table before inserting new records.
6. **Gotchas:** YAML files require spaces (no tabs). Watch out for local processes blocking port 8000. Do not use host port `5446` as Django/`psycopg2` `PORT` inside a container. Keep parameterized SQL (`%s`); do not concatenate user or HTML strings into queries.
7. **Scope:** Change only what the task needs (usually `myworld/`). Explain selectors and the insert in beginner language when you deliver a scraper.
