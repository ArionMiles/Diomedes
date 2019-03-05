# Use an official Python runtime as a parent image
FROM python:3.6-alpine

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /app/

# Set the working directory to /app
WORKDIR /app

# Install any needed packages specified in requirements.txt
# Cached Layer of Docker, avooid reinstalling packages unless
# requirements.txt has changed since the last build
RUN pip install -r requirements.txt

# Define environment variable
ENV DJANGO_READ_DOT_ENV_FILE on

# Run django server when the container launches
CMD python manage.py collectstatic --no-input && python manage.py makemigrations && python manage.py migrate && gunicorn -w 4 -b 0.0.0.0:8000 diomedes.wsgi
