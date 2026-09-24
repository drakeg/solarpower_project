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

Then open `http://localhost:8000`. The host port and the port Django listens on inside the container can be configured independently:

```bash
APP_PORT=8080 docker compose up --build
```

The command above maps host port `8080` to the default container port `8000`. To change the container's listening port as well, set `CONTAINER_PORT`:

```bash
APP_PORT=8080 CONTAINER_PORT=9000 docker compose up --build
```

This maps host port `8080` to container port `9000`, with Django listening on `0.0.0.0:9000`. You can also put these values in `.env`:

```text
APP_PORT=8080
CONTAINER_PORT=9000
```

Run the Django test suite in an isolated one-off container:

```bash
docker compose run --rm test
```

Run Django's system checks:

```bash
docker compose run --rm web python manage.py check
```

The Compose configuration supplies development-only fallback settings. To test with your own values, set them in the shell or a local `.env` file. Do not use the Compose fallback secret keys in production.

Core Django configuration is environment-driven:

- `SECRET_KEY` is required outside the Compose development/test fallbacks.
- `DEBUG` defaults to `False`; accepted true values are `1`, `true`, `yes`, and `on` (case-insensitive).
- `ALLOWED_HOSTS` is a comma-separated list. Its non-Compose default is `drakeg.pythonanywhere.com,127.0.0.1`; Compose explicitly adds `localhost` for local browser access.

Example `.env` for direct local development:

```text
SECRET_KEY=replace-with-a-generated-secret
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

For an HTTPS production deployment, explicitly enable the security settings only after HTTPS is correctly terminated for the application:

```text
DEBUG=False
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
```

HSTS is disabled by default because enabling it before HTTPS is correctly configured can make a deployment inaccessible. When `SECURE_HSTS_SECONDS` is greater than zero, subdomain coverage and preload are enabled as well.

Stop the local stack with:

```bash
docker compose down
```

## Development documentation

Project development conventions and roadmap are maintained in:

- `docs/DEVELOPMENT.md` — workflow, Definition of Done, PR and documentation expectations.
- `docs/CODING_STANDARDS.md` — Python/Django, testing, dependency, front-end, and commit standards.
- `docs/SPRINTS.md` — completed, current, and planned sprint work.

These documents are intended to remain current as part of normal feature and maintenance PRs.
