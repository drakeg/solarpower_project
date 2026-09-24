Solar Web Site

This is my attempt to pull in several resources regarding Solar power in homes, tiny homes, RVs, campers, etc.  It will include resources such as calculators, product links, reviews, a forum for help, and a blog (mostly detailing my current testing of a small solar setup).

Instructions:
Clone this repository.
Change directory into the new folder.
pip install -r requirements.txt
python manage.py shell -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
Copy/paste the output of this command into a .env file.
(i.e. SECRET_KEY=kdkfjknvkldsjf234jkl)

## Local development with Docker Compose

Docker Compose provides a reproducible local environment without installing the project's Python dependencies on the host.

Start the application:

```bash
docker compose up --build
```

Then open `http://localhost:8000`. To use a different host port, set `APP_PORT`, for example:

```bash
APP_PORT=8080 docker compose up --build
```

Run the Django test suite in an isolated one-off container:

```bash
docker compose run --rm test
```

Run Django's system checks:

```bash
docker compose run --rm web python manage.py check
```

The Compose configuration supplies development-only fallback secret keys. To test with your own value, set `SECRET_KEY` in the shell or a local `.env` file. Do not use the fallback values in production.

Stop the local stack with:

```bash
docker compose down
```
