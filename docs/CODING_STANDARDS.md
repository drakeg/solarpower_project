# Coding Standards

## Python and Django

- Target the Python versions exercised by CI.
- Follow PEP 8 unless the repository has an explicit local exception.
- Prefer clear, descriptive names over abbreviations.
- Keep views and functions focused; move reusable domain logic into appropriate modules/services.
- Avoid wildcard imports.
- Remove unused imports and dead code.
- Use `settings.AUTH_USER_MODEL` for relationships to the configured Django user model.
- Keep secrets and environment-specific values out of source control.
- Treat Django system-check warnings and migration problems as defects to resolve, not suppress.
- Do not silence lint rules merely to make CI green unless the exception is intentional and documented.

## Django patterns

- Validate user input with forms or serializers rather than trusting request data.
- Use ORM APIs instead of hand-built SQL unless there is a documented need.
- Protect state-changing requests with Django's normal CSRF/authentication mechanisms.
- Keep authorization checks server-side.
- Prefer named URLs and `reverse()`/`redirect()` patterns over hard-coded internal URLs.
- Create migrations whenever model state changes and test those migrations as part of CI.

## Tests

Every bug fix should include a regression test when practical. New behavior should cover its important success path plus meaningful validation/error paths.

Tests should be deterministic and independent. Do not depend on external network services, production credentials, or execution order.

At minimum, changes should preserve:

```bash
python manage.py check
python manage.py test
```

The Docker equivalent is the preferred reproducibility check:

```bash
docker compose run --rm test
```

## Dependencies

Keep dependencies pinned according to the repository's existing policy. Dependency updates must pass the complete CI matrix and Docker build/test path. Security updates receive priority, but still require verification.

Avoid maintaining multiple automated dependency PRs for the same package/version. Close or supersede stale duplicates.

## Front end

- Keep shared styling in static assets rather than duplicating large inline styles.
- Preserve responsive behavior and accessibility.
- Use semantic HTML and labels for interactive controls.
- Avoid introducing JavaScript dependencies for behavior that can be implemented simply with existing project tooling.

## Commits

Use concise imperative commit messages, for example:

- `test: cover invalid savings calculator input`
- `fix: preserve forum response category behavior`
- `docs: document Docker Compose workflow`

Keep generated files, local databases, secrets, editor metadata, and environment files out of commits.
