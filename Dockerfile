# pull official base image
FROM python:3.9.7-slim-bullseye

EXPOSE 8000

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV ACCEPT_EULA=Y
ENV DEBIAN_FRONTEND noninteractive

WORKDIR /usr/src/app

# install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc g++ musl-dev libpq-dev

COPY . .

RUN apt-get install -y git \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && python -m compileall . \
    && rm -rf /var/cache/apk/*

WORKDIR /usr/src/app/app

# development like environment
CMD ["python","app.py"]

# production like environment
#CMD ["sh", "-c", "gunicorn --worker-class eventlet -w 1 app:app --bind 0.0.0.0:8000"]

