# Use an official Python runtime as a parent image
FROM python:3.6-slim-stretch

ENV PYTHONUNBUFFERED 1

# Install any needed packages specified in requirements.txt
# Cached Layer of Docker, avooid reinstalling packages unless
# requirements.txt has changed since the last build
COPY requirements.txt /
RUN pip install -r requirements.txt

COPY . /app/
WORKDIR /app


# Define environment variable
ENV DJANGO_READ_DOT_ENV_FILE on

# Run django server when the container launches
CMD python manage.py collectstatic --no-input; python manage.py migrate; gunicorn -w 4 -b 0.0.0.0:8000 diomedes.wsgi