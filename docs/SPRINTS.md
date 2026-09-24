# Sprint Plan

This file is the durable development roadmap. It should be updated as work is completed or priorities change.

## Completed foundation work

### Sprint 0 — Repository stabilization

Status: Complete

- Restore a supported Python/Django CI baseline.
- Run Django system checks and tests in CI.
- Add Pylint with Django awareness.
- Correct application defects uncovered by static analysis.
- Modernize incompatible dependency pins.

### Sprint 1 — Reproducible local development

Status: Complete

- Add a Dockerfile for the Django application.
- Add Docker Compose local-development and test services.
- Support configurable local host port.
- Validate the Compose configuration, image build, and test service in CI.
- Document local Docker commands.

### Sprint 2 — Dependency hygiene

Status: Complete / ongoing maintenance

- Remove duplicate and conflicted dependency PRs.
- Consolidate compatible dependency upgrades.
- Require the complete CI and Docker path for dependency changes.
- Keep automated dependency PRs actionable rather than accumulating stale duplicates.

## Current sprint

### Sprint 3 — Meaningful application test coverage

Status: Planned

Goals:

- establish behavioral tests for existing user-facing functionality;
- protect previously fixed regressions;
- make CI failures useful before larger feature development.

Initial scope:

- calculator valid-input behavior;
- calculator invalid-input behavior/regression coverage;
- forum response creation;
- authentication and core navigation smoke tests;
- blog list/detail behavior;
- model-level tests where business rules exist.

Exit criteria:

- important existing routes have meaningful behavioral coverage;
- known regression fixes have tests;
- all Python 3.12/3.13 and Docker Compose CI checks pass;
- test commands and any fixtures/factories are documented.

## Candidate future sprints

### Sprint 4 — Configuration and security hardening

Review environment-driven `DEBUG`, `ALLOWED_HOSTS`, secret handling, production-safe defaults, and deployment checks.

### Sprint 5 — Calculator quality and solar-domain features

Audit current calculators for validation, units, edge cases, presentation, and opportunities for practical residential/RV solar calculations.

### Sprint 6 — Forum and community UX

Review forum permissions, posting flows, moderation fundamentals, navigation, and regression coverage.

### Sprint 7 — Blog/content experience

Improve content presentation, authoring workflow, navigation, and tests.

## Sprint rules

- Sprint numbering is sequential and persistent.
- A sprint may be split into smaller PR-sized deliverables.
- Do not mark a sprint complete merely because code exists; its exit criteria and CI must pass.
- New defects discovered during a sprint should be fixed immediately when blocking or recorded as a follow-up item.
- Documentation and tests are deliverables, not cleanup tasks.
- After a sprint is completed, development proceeds to the next sprint without requiring a separate confirmation unless priorities have changed.
