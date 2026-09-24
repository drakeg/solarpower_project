# Development Guide

This document defines the working agreement for development of SolarPower Project.

## Development workflow

Work is organized into small, reviewable increments. Each change should have a clear purpose, automated verification, and documentation updates when behavior or developer workflow changes.

1. Start from the latest `main`.
2. Create a focused branch for one coherent change.
3. Implement the change and its tests together.
4. Run Django checks, tests, and linting.
5. For changes that affect runtime or dependencies, verify the Docker Compose path.
6. Open a pull request with a concise summary and verification notes.
7. Merge only after required CI checks pass.
8. Continue with the next planned sprint item; completed work should be reflected in the sprint documentation.

## Definition of Done

A work item is complete when:

- requested behavior is implemented;
- relevant automated tests exist and pass;
- `python manage.py check` passes;
- Pylint passes under the repository CI configuration;
- Docker Compose remains usable for local development and testing;
- documentation is updated when interfaces, setup, architecture, or behavior changes;
- no unrelated changes or known merge conflicts are included;
- CI is green.

A green pipeline with zero meaningful tests is not considered sufficient coverage. Tests should exercise behavior and regressions, not merely imports.

## Local verification

Preferred reproducible commands:

```bash
docker compose run --rm web python manage.py check
docker compose run --rm test
```

The application itself can be exercised with:

```bash
docker compose up --build
```

See the README for port configuration and setup details.

## Pull requests

Keep PRs small enough to review and diagnose. Avoid mixing feature work, broad refactors, dependency updates, and formatting-only changes unless they are inseparable.

PR descriptions should state:

- what changed;
- why it changed;
- how it was tested;
- any migration, configuration, security, or compatibility impact.

Dependency-bot PRs that overlap or conflict may be consolidated into one tested update. Superseded duplicate PRs should be closed to keep the queue actionable.

## Documentation discipline

Documentation is part of the change. Update it in the same PR when a change affects setup, commands, architecture, user-visible behavior, configuration, or development conventions.
