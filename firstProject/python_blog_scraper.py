"""
Workshop scraper for https://blog.python.org/

What this script does (beginner summary):
1) Connects to the workshop Postgres database (member_db)
2) Clears old rows in members_blog (TRUNCATE ... CASCADE)
3) Downloads the Python Insider homepage
4) Finds each blog card (article.post-card)
5) Reads title, author, release date, and blog time
6) Inserts each row into members_blog

Run it the same way as web_scrapper.py, inside the web container:
    python3 python_blog_scraper.py
"""

from typing import List, Optional, Tuple

import psycopg2
import requests
from bs4 import BeautifulSoup, Tag

# Same credentials as docker-compose.yml / web_scrapper.py
# HOST is the Postgres container name so this works from workshop2_web_container.
db_name = "member_db"
db_user = "postgres"
db_pass = "123456"
db_host = "psql-db2"
db_port = "5432"

BLOG_URL = "https://blog.python.org/"
USER_AGENT = "Mozilla/5.0 (compatible; WorkshopBlogScraper/1.0; +https://blog.python.org/)"
REQUEST_TIMEOUT_SECONDS = 30


def connect_to_database():
    """Step 1: open a connection to Postgres. Returns None if it fails."""
    try:
        return psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_pass,
            host=db_host,
            port=db_port,
        )
    except psycopg2.Error as error:
        print("Could not connect to Postgres:", error)
        print("Tip: run this script inside workshop2_web_container so host psql-db2 works.")
        return None


def add_row_to_blog(conn, title: str, author: str, date: str, time: str) -> None:
    """Step 6: insert one blog row. %s placeholders stop SQL injection."""
    sql = """
        INSERT INTO members_blog (title, release_date, blog_time, author, created_date)
        VALUES (%s, %s::DATE, %s::TIME, %s, NOW())
    """
    with conn:
        with conn.cursor() as curs:
            curs.execute(sql, (title, date, time, author))


def truncate_table(conn) -> None:
    """Step 2: wipe old scrapes so we do not keep duplicate rows."""
    with conn:
        with conn.cursor() as curs:
            curs.execute("TRUNCATE members_blog CASCADE;")


def fetch_homepage_html(url: str) -> Optional[str]:
    """Step 3: download the page HTML (timeout + User-Agent required)."""
    try:
        response = requests.get(
            url,
            timeout=REQUEST_TIMEOUT_SECONDS,
            headers={"User-Agent": USER_AGENT},
        )
        response.raise_for_status()
        return response.text
    except requests.RequestException as error:
        print("Could not download the blog page:", error)
        return None


def parse_datetime(time_node: Optional[Tag]) -> Tuple[str, str]:
    """Turn a <time datetime='...'> tag into (YYYY-MM-DD, HH:MM:SS)."""
    if time_node is None:
        return "1970-01-01", "00:00:00"

    iso_value = time_node.get("datetime")
    if iso_value:
        date = iso_value[:10]
        time = iso_value[11:19] if len(iso_value) >= 19 else "00:00:00"
        return date, time

    text = time_node.get_text(strip=True) or "1970-01-01"
    return text, "00:00:00"


def parse_blog_cards(page_soup: BeautifulSoup) -> List[Tuple[str, str, str, str]]:
    """
    Step 4–5: find cards and read title / author / date / time.

    Current Python Insider homepage uses article.post-card.
    Older Blogger layout used div.date-outer — we try that if no cards are found.
    """
    rows: List[Tuple[str, str, str, str]] = []
    blogs = page_soup.select("article.post-card")
    if not blogs:
        blogs = page_soup.select("div.date-outer")

    for blog in blogs:
        title_node = blog.select_one("h3") or blog.select_one(".post-title")
        title = title_node.get_text(strip=True) if title_node else ""
        if not title:
            continue

        author_node = (
            blog.select_one("span.font-medium")
            or blog.select_one(".post-author")
            or blog.select_one("span.fn")
        )
        author = author_node.get_text(strip=True) if author_node else "Unknown"

        time_node = blog.select_one("time") or blog.select_one("abbr.published")
        date, time = parse_datetime(time_node)

        rows.append((title, author, date, time))

    return rows


def start_extraction() -> None:
    print("Extraction started")

    conn = connect_to_database()
    if conn is None:
        return

    try:
        html = fetch_homepage_html(BLOG_URL)
        if html is None:
            return

        page_soup = BeautifulSoup(html, "html.parser")
        blogs = parse_blog_cards(page_soup)
        if not blogs:
            print("No blog posts found. The site HTML may have changed.")
            return

        truncate_table(conn)

        for title, author, date, time in blogs:
            add_row_to_blog(conn, title, author, date, time)
            print("\nTitle:", title)
            print("Date:", date)
            print("Time:", time)
            print("Author:", author)
            print(
                "\n---------------------------------------------------------------------------------------------------------------\n"
            )

        print(f"Saved {len(blogs)} row(s) into members_blog.")
    except psycopg2.Error as error:
        print("Database error while saving blogs:", error)
    finally:
        conn.close()


if __name__ == "__main__":
    start_extraction()
