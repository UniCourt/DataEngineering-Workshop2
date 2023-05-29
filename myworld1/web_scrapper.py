import psycopg2
import requests
import re
from bs4 import BeautifulSoup, element
import os
        
# For the credentials mentioned below, you may refer the docker-compose.yml present in myworld .
db_name = 'member_db'
db_user = 'postgres'
db_pass = '123456'
db_host = 'psql-db'
db_port = '5432'
        
# This will create the connection the to postgres database.
conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_pass, host=db_host, port=db_port)
                   
                    
def add_row_to_blog(title, author, date, time,content,recommended,path):
    # This function will add the entry to database
    sql = """INSERT INTO members_blog (title, release_date, blog_time, created_date,content, author,recommended,path) VALUES (%s, %s::DATE, %s::TIME,  NOW(),%s,%s,%s,%s)"""
            
    with conn:
        with conn.cursor() as curs:
            time=time.replace('\u202f',"")
            curs.execute(sql, (title, date, time, content,author,recommended,path))
        
        
def truncate_table():
    # This function will delete the existing entries from the database.
    with conn:
        with conn.cursor() as curs:
            curs.execute("TRUNCATE members_blog CASCADE;")
        
        
def start_extraction():
    print("Extraction started")
    url = "https://blog.python.org/"
            
    # Each time when we add new entry we delete the existing entries.
    truncate_table()
    data = requests.get(url)
    page_soup = BeautifulSoup(data.text, 'html.parser')
            
    # Getting all the articles
    blogs = page_soup.select('div.date-outer')
    
    fp=open("scrapped_data.html","w")
    path=os.path.abspath("scrapped_data.html")
   
    for blog in blogs:
        # loop through each article
        date = blog.select('.date-header span')[0].get_text()
                
        post = blog.select('.post')[0]
        #print(post)
        fp.write(str(post))
        
        content=post.select('.post-body')[0].get_text()
        recommended =post.select('.post-share-buttons')[0].get_text()
         
             
        title = ""
        title_bar = post.select('.post-title')
        if len(title_bar) > 0:
            title = title_bar[0].text
        else:
            title = post.select('.post-body')[0].contents[0].text
        
        # getting the author and blog time
        post_footer = post.select('.post-footer')[0]
        
        author = post_footer.select('.post-author span')[0].text
        
        time = post_footer.select('abbr')[0].text
        
        
        # Inserting data into database
        add_row_to_blog(title, author, date, time,content,recommended,path)
        
        print("\nTitle:", title.strip('\n'))
        print("Date:", date, )
        print("Time:", time)
        print("Author:", author)
        print("Content:",content)
        print("recommended: ",recommended)
        
        # print("Number of blogs read:", count)
        print(
            "\n---------------------------------------------------------------------------------------------------------------\n")
    
    fp.close()
                
        
if __name__ == "__main__":
    start_extraction()
