---

name: workshop-blog-scraper

description: Scrape a blog URL and store title, release date, blog time, and author in the Workshop 2 PostgreSQL database.

---

# Workshop Blog Scraper

Use this skill when asked to scrape a blog website and store the results in the Workshop 2 PostgreSQL database.

## Project conventions

- Work inside the existing `DataEngineering-Workshop2` project.

- Python scripts for scraping should be placed under `myworld/`.

- Use Python `requests` to download the webpage.

- Use BeautifulSoup to parse the HTML.

- Extract:

  - title

  - release date

  - blog time

  - author

- For the Python Insider website, blog cards use the selector:

  `article.post-card`

## Database

Use the existing Workshop 2 PostgreSQL database:

- Database: `member_db`

- User: `postgres`

- Password: `123456`

- Host: `psql-db`

- Port: `5432`

- Table: `members_blog`

Do not create a different database or table.

## Database columns

Store the scraped values in:

- `title`

- `release_date`

- `blog_time`

- `author`

- `created_date`

## Scraping workflow

1. Download the requested URL with `requests`.

2. Parse the response using BeautifulSoup.

3. Find the blog cards.

4. Extract the title, author, and date/time.

5. Connect to PostgreSQL using `psycopg2`.

6. Insert the extracted rows into `members_blog`.

7. Print a short message showing what was inserted.

8. Explain the important selectors and database insert briefly for a beginner.

## Important

- Follow the existing Workshop 2 database structure.

- Do not invent a new database, table, or schema.

- Do not run Django project creation commands.

- Do not unnecessarily modify the existing working `myworld/web_scrapper.py`.

- If a new scraper is requested, create a separate runnable Python script under `myworld/`.

- Keep the solution simple and beginner-friendly.