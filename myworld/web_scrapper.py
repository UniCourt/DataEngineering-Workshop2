import os
import re
import html
import datetime
import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse

HTML_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saved_html")


def save_html_to_file(filename, content):
    os.makedirs(HTML_DIR, exist_ok=True)
    file_path = os.path.join(HTML_DIR, filename)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    return file_path


def start_extraction(start_date=None, end_date=None, no_of_articles=None, start_id=None):
    from members.models import Blog

    print("Extraction started")
    url = "https://blog.python.org/"

    try:
        response = requests.get(url, timeout=30)
        html_content = response.text
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        html_content = ""

    page_soup = BeautifulSoup(html_content, "html.parser")

    parsed_start_date = None
    parsed_end_date = None
    if start_date:
        try:
            parsed_start_date = parse(start_date).date()
        except Exception:
            pass
    if end_date:
        try:
            parsed_end_date = parse(end_date).date()
        except Exception:
            pass

    # Clear existing Blog entries
    Blog.objects.all().delete()

    articles = page_soup.select("article")
    if not articles:
        articles = page_soup.select("div.date-outer, div.post")

    extracted_blogs = []
    article_counter = 0
    saved_counter = 0

    for idx, art in enumerate(articles, start=1):
        article_counter += 1
        if start_id and article_counter < int(start_id):
            continue
        if no_of_articles and saved_counter >= int(no_of_articles):
            break

        # Title
        title_el = art.select_one("h3") or art.select_one(".post-title")
        title = title_el.get_text(strip=True) if title_el else f"Blog Post {idx}"

        # Author
        author_el = art.select_one("span.font-medium") or art.select_one(
            ".post-author span"
        )
        author = (
            author_el.get_text(strip=True)
            if author_el
            else "Python Software Foundation"
        )

        # Date & Time
        time_el = art.select_one("time")
        raw_datetime = (
            time_el.get("datetime") if time_el and time_el.get("datetime") else None
        )
        date_text = time_el.get_text(strip=True) if time_el else None

        rel_date = None
        b_time = "00:00:00"

        if raw_datetime:
            try:
                dt_obj = parse(raw_datetime)
                rel_date = dt_obj.date()
                b_time = dt_obj.strftime("%H:%M:%S")
            except Exception:
                pass

        if not rel_date and date_text:
            try:
                dt_obj = parse(date_text)
                rel_date = dt_obj.date()
            except Exception:
                rel_date = datetime.date.today()

        if not rel_date:
            rel_date = datetime.date.today()

        # Date range filtering
        if parsed_start_date and rel_date < parsed_start_date:
            continue
        if parsed_end_date and rel_date > parsed_end_date:
            continue

        # Content
        content_el = art.select_one("p") or art.select_one(".post-body")
        content = content_el.get_text(strip=True) if content_el else ""

        # Comments
        comments_el = art.select_one(".comment-link, a[href*='comment']")
        comments_count = 0
        if comments_el:
            digits = re.findall(r"\d+", comments_el.get_text())
            if digits:
                comments_count = int(digits[0])

        # Recommended / Reactions
        rec_el = art.select_one(".reaction-count, .g-plusone")
        recommended_count = 0
        if rec_el:
            digits = re.findall(r"\d+", rec_el.get_text())
            if digits:
                recommended_count = int(digits[0])

        # Save HTML file
        art_html = str(art)
        file_path = save_html_to_file(f"article_{idx}.html", art_html)

        blog_obj = Blog.objects.create(
            title=title,
            release_date=rel_date,
            blog_time=b_time,
            content=content,
            author=author,
            total_comments=comments_count,
            recommended_google=recommended_count,
            html_file_path=file_path,
        )
        extracted_blogs.append(blog_obj)
        saved_counter += 1

    print(f"Extracted {len(extracted_blogs)} blogs")
    return extracted_blogs


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myworld.settings")
    import django
    django.setup()
    start_extraction()

