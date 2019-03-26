# Diomedes

Inspired by [django_moviealert](https://github.com/iAmMrinal0/django_moviealert)

Sends email alerts for movie tickets as soon as they become available.

I had trouble getting the original project to run as it was missing an important script for populating the Regions database model, without which it's impossible to run the project. It also used HTML scraping, and the markup of BookMyShow (BMS) has changed since the original project was last updated. It also wasn't production ready (used Django development server).

This project uses a different technique to search the movies, and can do much more, including Sports, Plays, and other events (though the project is currently purposely limited to Movies). This project is easily deployable via Docker. The website is also mobile friendly.

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

2. Install dependencies: `pip3 install -r requirements.txt`

3. Run Migrations: `python3 manage.py migrate`

4. Create admin account: `python3 manage.py createsuperuser`

5. Populate the `Region` model:
    
    Run `python3 manage.py shell`
    ```
    >>> from moviealert.utils import save_region_data
    >>> save_region_data()
    ```

6. Star development server: `python3 manage.py runserver`

    or gunicorn: `gunicorn -b 0.0.0.0:8000 diomedes.wsgi`

## Running with Docker
The docker container runs using gunicorn by default and uses a Nginx server as a reverse-proxy to serve static files. 

If you wish to run with default Django developement server, make the necessary changes in the [Dockerfile](Dockerfile)

**NOTE: ** Change `REDISTOGO_URL` env var in `.env` to `redis://:defaultpass@dioredis:6379`

Also, change the `defaultpass` in the `REDISTOGO_URL` and `docker-compose.yml` file to something more secure.

Start the container in detached mode (recommended) using:

`docker-compose up -d`

Create admin account:

`docker exec -it diomedes_web python3 manage.py createsuperuser`

Finally, populate the `Region` model by running:

`docker exec -it diomedes_web python3 manage.py shell`

```
>>> from moviealert.utils import save_region_data
>>> save_region_data()
```

# License
[MIT License](LICENSE)