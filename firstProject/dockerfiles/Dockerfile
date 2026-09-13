 FROM python:3.10.2-alpine3.15
 RUN apk update && \
     apk --no-cache add --virtual build-deps-alpine build-base && \
     apk --no-cache add --virtual postgresql-deps libpq-dev
 RUN pip install --upgrade pip
 COPY requirements.txt /tmp/requirements.txt
 RUN pip install --no-cache-dir -r /tmp/requirements.txt
 RUN mkdir -p /root/workspace/src
 COPY ./  /root/workspace/site
 WORKDIR /root/workspace/site
 CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
