FROM python:3.10.2-alpine3.15

# Install required packages
# For psycopg2 and curl
RUN apk update && \
    apk --no-cache add --virtual build-deps-alpine build-base && \
    apk --no-cache add --virtual postgresql-deps libpq-dev && \
    apk add --no-cache curl

# Install requirements
RUN pip install --upgrade pip
RUN pip install Django psycopg2==2.9.3

# Create directories  
RUN mkdir -p /root/workspace/src
COPY ./  /root/workspace/site

# Switch to project directory
WORKDIR /root/workspace/site
