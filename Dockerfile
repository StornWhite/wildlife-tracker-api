# Use official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code
ENV PATH="${PATH}:/"

# Install dependencies
COPY requirements.txt /code/
COPY manage.py /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . /code/