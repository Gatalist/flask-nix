FROM python:3.10.7-slim-buster

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY . .
RUN python -m pip install --upgrade pip && pip install -r req.txt
