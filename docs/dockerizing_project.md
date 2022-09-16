# Dockerizing the Django Project

- In-order to dockerize the project we need to add a docker file and docker-compose file as we have discussed in our previous workshop.
- Follow the below step to achieve that.

1. Inside the root folder of the project create a folder called dockerfiles.

        mkdir dockerfiles
   
3. Get inside the folder and create a file called Dockerfile

        vi Dockerfile
4. Add the below content to that file
      
        FROM python:3.10.2-alpine3.15
        # Create directories  
        RUN mkdir -p /root/workspace/src
        COPY ./  /root/workspace/site
        # Switch to project directory
        WORKDIR /root/workspace/site
        # Install required packages
        RUN pip install --upgrade pip
        RUN pip install Django
5. Come out of the folder dockerfile and create a docker-compose file in the project root folder.
    
        vi docker-compose.yml
6. Add the following content to that file
    
        version: "3"
        services:
         web_service:
           build:
             context: ./
             dockerfile: ./dockerfiles/Dockerfile
           image: workshop1_web
           container_name: workshop_web_container
           stdin_open: true #  docker attach container_id
           tty: true
           ports:
            - "8000:8000"
           volumes:
            - .:/root/workspace/site

9. Go to the root folder of the project where the docker-compose file is present and bring the containers up
    
        docker-compose up -d
- This will create a container workshop_web_container
10. Need to exec into that container.
    
        docker exec -it workshop_web_container sh
11. This will get into that container. You will now be inside the container and the working directory will be /workspace/site.
12. Run the command to run the server 
    
        python manage.py runserver 0:8000
    
    - Here we are binding the localhost to the port 8000.
    - Explore here [https://docs.djangoproject.com/en/3.2/ref/django-admin/#examples-of-using-different-ports-and-addresses](https://docs.djangoproject.com/en/3.2/ref/django-admin/#examples-of-using-different-ports-and-addresses)
13. Run http://127.0.0.1:8000/admin/ in the browser and now it should load the webpage.

# Adding Postgres service to our project

- Till now we were using the SQLite database which was supported in Django by default. Now let us connect portsgres database to our Django project.
- We can run the postgres database as a separate service as we have done in our previous workshop.
- For that we need to update our current docker-compose file and add the new service to it. Add the following code to the docker-compose.yml file
    
         psql-db:
          image: 'postgres:14'
          container_name: psql-db
          environment:
            - PGPASSWORD=123456
            - POSTGRES_USER=postgres
            - POSTGRES_PASSWORD=123456
          ports:
            - '5432:5432'

- Also we should attach a volume to which our database need to be saved to. For that add the below lines at the bottom of the docker-compose.yml file.
  
        volumes:
          db:
            driver: local
- Now the whole content of the docker-compose.yml file should look like this

        version: "3"
        services:
         web_service:
           build:
             context: ./
             dockerfile: ./dockerfiles/Dockerfile
           image: workshop1_web
           container_name: workshop_web_container
           stdin_open: true #  docker attach container_id
           tty: true
           ports:
            - "8000:8000"
           volumes:
            - .:/app
         
         psql-db:
          image: 'postgres:14'
          container_name: psql-db
          environment:
            - PGPASSWORD=123456
            - POSTGRES_USER=postgres
            - POSTGRES_PASSWORD=123456
          ports:
            - '5446:5432'
          volumes:
            - db:/var/lib/postgresql/data
  
        volumes:
          db:
            driver: local

- Now bring the containers up. 

        docker-compose up -d
- Previously only one container was getting created. Now two containers will be created. 
    1. psql-db
    2. workshop_web_container
    
## Creating database

- Once the containers are up, exec into the database container ie., psql-db container.

        docker exec -it psql-db sh
- Now we need to login to postgres
    
        psql -U postrges
- Once we are logged into postgres we can run the sql command to create the database. Let us create a database called `memeber_db`

        CREATE DATABASE member_db;
- Adding the tables to this database can be done using the django models

## Adding tables using Django models

- As we have seen in the previous session, we can create tables using the Django models by running the migrate command.
- In order to do that we need to connect our exitsing Django app to the postgres database service.
- Following steps need to be followed for that.

1. We need to update the dockerfile to support postgres inside the workshop_web_container service. 
    
    - Update the dockerfile , Dockerfile, present in the folder `dockerfiles`, to the below content.
    
            FROM python:3.10.2-alpine3.15
            # Install required packages
            # For psycopg2
            RUN apk update && \
                apk --no-cache add --virtual build-deps-alpine build-base && \
                apk --no-cache add --virtual postgresql-deps libpq-dev
            # Install requirements
            RUN pip install --upgrade pip
            RUN pip install Django psycopg2==2.9.3
            # Create directories  
            RUN mkdir -p /root/workspace/src
            COPY ./  /root/workspace/site
            # Switch to project directory
            WORKDIR /root/workspace/site
    - Here we have added the commands to install the psycopg2 package to support postgres and also other dependency packages like build-base and libpq-dev that are required for the successful installation of psycopg2.
    
2. Now we need to update the settings.py file present inside the mysite folder inside the root folder of the project mysite (ie., mysite/mysite).
    
    - If you open the settings.py file inside that folder, you will find a section called DATABASES which will currently have the below content
    
            DATABASES = {
                'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
                }
            }
    - The above content support the SQLite database. In order to support the postgres database we need to make the below changes
    
            DATABASES = {
                'default': {
                    'ENGINE': 'django.db.backends.postgresql',
                    'NAME': 'member_db',
                    'USER': 'postgres',
                    'PASSWORD': '123456',
                    'HOST': 'psql-db',
                    'PORT': 5432,
                }
            }
    - 1. NAME should contain the name of the database you have created .
    - 2. USER, PASSWORD, and PORT should be the one which are mentioned in the postgres service of the docker-compose.yml file.
    - 3. HOST should be the name of the database container which is currently running.
    
3. Once the changes are made build the container again by running the below command

```buildoutcfg
docker-compose up --buld -d
```
4. This should build the images and bring both the containers up. Now exec into the workshop_web_container container and run the command to run migrations and create the tables from our model Members
```buildoutcfg
python manage.py makemigrations
python manage.py migrate
```
5. This should have created the table in the member_db database. To check that, open a new tab in your terminal and go inside the porject folder and exec into the database server

        docker exec -it psql-db sh
        psql -U postgres
        \c member_db
        \dt
    
    - The above commands should list down all the tables in the member_db and if the migration was success there should be a table called members_members added in the database along with other Django default tables.
    
6. In order to peform the CRUD operations, we will have to load the admin page. For that we will have to create a super user again since we have a new database now. Run the below command in the first tab where workshop_web_container container is running to create the user

        python manage.py createsuperuser
7. Once the user is created, we run our server. Run the below command
    
        python manage.py runserver 0:8000
8. Copy http://localhost:8000/admin in the web browser to load the web page and view the table and perform the CRUD operations.
