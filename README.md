# Diomedes

Sends email alerts for movie tickets as soon as they become available.

# Components
- Django
- Celery
- Gunicorn
- Nginx
- Redis
- Docker

# Setup

The project uses Mailgun for sending emails. You'll need a Mailgun API key.

You also need a Google OAuth2 app to use the Google Sign-in. Read how to get it setup from [django-allauth documentation](https://django-allauth.readthedocs.io/en/latest/providers.html#google).

Change `example.env` to `.env`, fill in the necessary environment variables.

## Running with Docker
The docker container runs using gunicorn by default and uses a Nginx server as a reverse-proxy to serve static files. 

If you wish to run with default Django developement server, make the necessary changes in the [Dockerfile](Dockerfile)

For development, there's a separate compose file you can run with:
`docker-compose -f docker-compose.dev.yml up`

**NOTE:** Change the `defaultpass` in `docker-compose.yml` (Redis command and POSTGRES_PASSWORD) to something more secure and set the same in the `.env` file for `POSTGRES_PASSWORD`.

Change `defaultpass` in `REDISTOGO_URL` to what you wrote in `docker-compose.yml` for Redis command

Start the container in detached mode (recommended) using:

`docker-compose up -d`

Create admin account:

`docker exec -it diomedes_web python3 manage.py createsuperuser`

Finally, populate the `Region` model by running:

`docker exec -it diomedes_web python3 manage.py shell`

```python
>>> from moviealert.utils import *
>>> save_region_data()
>>> save_subregion_data()
>>> save_theater_data()
```
The last function will take some time, and may timeout sometimes, run it multiple times to make sure you have all the theater data.

To stop and remove all containers:
`docker-compose down --remove-orphans`

**NOTE:** Change the Google Analytics tracking code in [base.html](./moviealert/templates/base.html) with your own if you are hosting the project publically somewhere else so that your traffic doesn't get logged with mine.

Inspired by [django_moviealert](https://github.com/iAmMrinal0/django_moviealert)

# License
[MIT License](LICENSE)