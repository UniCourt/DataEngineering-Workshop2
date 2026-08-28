  FROM python:3.10.2-alpine3.15

  RUN apk update && \
      apk --no-cache add --virtual build-deps-alpine build-base && \
      apk --no-cache add --virtual postgresql-deps libpq-dev

  RUN pip install --upgrade pip
  RUN pip install Django psycopg2==2.9.3
  
  RUN mkdir -p /root/workspace/src
  COPY ./  /root/workspace/site

  WORKDIR /root/workspace/site
