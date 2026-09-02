import psycopg2
import requests
from bs4 import BeautifulSoup

# Workshop 2 Postgres (same database and table as web_scrapper.py)
db_name = "member_db"
db_user = "postgres"
db_pass = "123456"
db_host = "psql-db"
db_port = "5432"

# Step 1: Open a connection to PostgreSQL so we can insert rows later.
conn = psycopg2.connect(
    dbname=db_name,
    user=db_user,
    password=db_pass,
    host=db_host,
    port=db_port,
)


def add_row_to_blog(title, author, date, time):
    """Insert one blog post into members_blog."""
    # %s placeholders keep the SQL safe (values are sent separately, not glued into the query).
    sql = """
        INSERT INTO members_blog
        (title, release_date, blog_time, author, created_date)
        VALUES (%s, %s::DATE, %s::TIME, %s, NOW())
    """

    with conn:
        with conn.cursor() as curs:
            curs.execute(sql, (title, date, time, author))


def truncate_table():
    """Clear old rows so a re-run does not duplicate posts."""
    with conn:
        with conn.cursor() as curs:
            curs.execute("TRUNCATE members_blog CASCADE;")


def start_extraction():
    print("Extraction started")
    url = "https://blog.python.org/"

    # Step 2: Empty the table before loading a fresh scrape.
    truncate_table()

    # Step 3: Download the HTML of the blog homepage.
    data = requests.get(url, timeout=30)

    # Step 4: Turn the HTML text into a tree we can search with CSS selectors.
    page_soup = BeautifulSoup(data.text, "html.parser")

    # Step 5: Each post on Python Insider is wrapped in <article class="post-card">.
    blogs = page_soup.select("article.post-card")

    for blog in blogs:
        # Title is usually in an <h3> inside the card.
        title_node = blog.select_one("h3")
        title = title_node.get_text(strip=True) if title_node else ""

        # Author is in a <span class="font-medium">.
        author_node = blog.select_one("span.font-medium")
        author = author_node.get_text(strip=True) if author_node else "Unknown"

        # Date and time come from the datetime="..." attribute on <time>.
        # Example: 2026-09-01T12:00:00+00:00 -> date 2026-09-01, time 12:00:00
        time_node = blog.select_one("time")
        if time_node and time_node.get("datetime"):
            iso_value = time_node["datetime"]
            date = iso_value[:10]
            time = iso_value[11:19] if len(iso_value) >= 19 else "00:00:00"
        else:
            date = time_node.get_text(strip=True) if time_node else "1970-01-01"
            time = "00:00:00"

        # Step 6: Save this post in members_blog.
        add_row_to_blog(title, author, date, time)

        print("\nTitle:", title)
        print("Date:", date)
        print("Time:", time)
        print("Author:", author)
        print("\n----------------------------------------\n")


if __name__ == "__main__":
    start_extraction()
