"""
Workshop scraper for https://blog.python.org/

What this script does (beginner summary):
1) Connects to the workshop Postgres database
2) Clears old rows in members_blog (TRUNCATE ... CASCADE)
3) Downloads the Python Insider homepage
4) Finds each blog card (article.post-card)
5) Reads title, author, and date/time
6) Inserts each row into members_blog
"""

import psycopg2
import requests
from bs4 import BeautifulSoup

# For the credentials mentioned below, you may refer the docker-compose.yml present in myworld .
db_name = 'member_db'
db_user = 'postgres'
db_pass = '123456'
db_host = 'psql-db2'
db_port = '5432'

conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_pass, host=db_host, port=db_port)


def add_row_to_blog(title, author, date, time):
    sql = """INSERT INTO members_blog (title, release_date, blog_time, author, created_date) VALUES (%s, %s::DATE, %s::TIME, %s, NOW())"""
    with conn:
        with conn.cursor() as curs:
            curs.execute(sql, (title, date, time, author))


def truncate_table():
    with conn:
        with conn.cursor() as curs:
            curs.execute("TRUNCATE members_blog CASCADE;")


def start_extraction():
    print("Extraction started")
    url = "https://blog.python.org/"
    truncate_table()
    data = requests.get(url, timeout=30)
    page_soup = BeautifulSoup(data.text, 'html.parser')
    blogs = page_soup.select('article.post-card')

    for blog in blogs:
        title_node = blog.select_one('h3')
        title = title_node.get_text(strip=True) if title_node else ""

        author_node = blog.select_one('span.font-medium')
        author = author_node.get_text(strip=True) if author_node else "Unknown"

        time_node = blog.select_one('time')
        if time_node and time_node.get('datetime'):
            iso_value = time_node['datetime']
            date = iso_value[:10]
            time = iso_value[11:19] if len(iso_value) >= 19 else "00:00:00"
        else:
            date = time_node.get_text(strip=True) if time_node else "1970-01-01"
            time = "00:00:00"

        add_row_to_blog(title, author, date, time)

        print("\nTitle:", title)
        print("Date:", date)
        print("Time:", time)
        print("Author:", author)
        print(
            "\n---------------------------------------------------------------------------------------------------------------\n"
        )


if __name__ == "__main__":
    start_extraction()