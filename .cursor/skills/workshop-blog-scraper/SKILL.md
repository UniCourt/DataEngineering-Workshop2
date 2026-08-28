---

name: blog-scraper
description: Create a single Python file to scrape blog content from a given website or blog URL and save the extracted data to a database.
-------------------------------------------------------------------------------------------------------------------------------------------

# Blog Scraper

When the user asks to scrape a blog or extract content from a blog website, create a single Python `.py` file.

The Python script should scrape the requested blog data and save the extracted information directly into the database.

## Requirements

* Create only one Python `.py` file.
* Do not create additional folders or files.
* Do not create JSON, CSV, Markdown, or other output files.
* Scrape the requested blog content.
* Save the scraped data directly into the database.
* Use the database configuration or connection details provided by the user or available in the project.
* Use `requests` and `BeautifulSoup` for static websites.

## Extracted Data

Extract relevant blog information when available:

* Title
* URL
* Author
* Published date
* Blog content

Save the extracted information into the appropriate database table.

## Database Requirements

* Use the existing database connection and configuration when available.
* Use environment variables or existing project configuration for database credentials.
* Handle database connection errors gracefully.
* Use parameterized queries when writing SQL.
* Avoid inserting duplicate blog records.
* Use transactions where appropriate.
* Ensure database connections and resources are properly closed.

## Scraping Requirements

* Handle missing information gracefully.
* Always use a request timeout.
* Use a descriptive User-Agent.
* Handle HTTP and network errors gracefully.
* Avoid unnecessary requests.
* Keep the implementation simple and focused.

## Dynamic Websites

If the blog content is rendered using JavaScript and cannot be extracted using `requests`, use Playwright in the same Python `.py` file.

## Code Quality

* Use descriptive variable and function names.
* Add type hints where appropriate.
* Keep functions small and focused.
* Separate webpage fetching, HTML parsing, and database operations.
* Handle missing HTML elements safely.
* Print meaningful error messages.
* Do not over-engineer the solution.

## Important

The output must be a single Python `.py` file only.
Create a new file with name `python_blog_scraper.py`

The script must:

1. Scrape the requested blog data.
2. Extract the required information.
3. Save the extracted data into the database.

Do not create additional files unless explicitly requested by the user.
