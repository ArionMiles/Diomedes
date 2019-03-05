# Diomedes

Inspired by [django_moviealert](https://github.com/iAmMrinal0/django_moviealert)

Sends email alerts for movie tickets as soon as they become available.

I couldn't get the original project to run as well as it had some issues and limitations, such as the author forgetting to commit an important script for populating the regions into version control, and losing the script. It also used HTML scraping, and the markup of BookMyShow (BMS) has changed since the original project was last updated. This project uses a different technique to search the movies, and can do much more, including Sports, Plays, and other events (though the project is currently purposely limited to Movies).

# Components
- Django
- Gunicorn
- Nginx
- Redis
- Docker

# Setup

The project uses Mailgun for sending emails. You'll need a Mailgun API key.

You also need a Google OAuth2 app to use the Google Sign-in. Read how to get it setup from [django-allauth documentation](https://django-allauth.readthedocs.io/en/latest/providers.html#google).

Change `example.env` to `.env`, fill in the necessary environment variables.

## Running without Docker

To run locally, without docker you'll need to 

1. Install redis (`apt install redis-server`) and run it locally (`redis-server`)

Activate your virtual environment (if you use them), and run:

2. Run Migrations: `python3 manage.py migrate`

3. Create admin account: `python3 manage.py createsuperuser`

4. Populate the `Region` model:
    
    Run `python3 manage.py shell`
    ```
    >>> from moviealert.utils import save_region_data
    >>> save_region_data()
    ```

5. Star development server: `python3 manage.py runserver`

    or gunicorn: `gunicorn -b 0.0.0.0:8000 diomedes.wsgi`

## Running with Docker
The docker container runs using gunicorn by default and uses a Nginx server as a reverse-proxy to serve static files. 

If you wish to run with default Django developement server, make the necessary changes in the [Dockerfile](Dockerfile)

**NOTE: ** Change `REDISTOGO_URL` env var in `.env` to `redis://dioredis:6379`

Start the container by running:

`docker-compose up`

Run the container in detached mode using:

`docker-compose up -d`

# License
[MIT License](LICENSE)