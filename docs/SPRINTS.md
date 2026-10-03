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

## Completed application-quality work

### Sprint 3 — Meaningful application test coverage

Status: Complete

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

## Completed configuration/security work

### Sprint 4 — Configuration and security hardening

Status: Complete

Review environment-driven `DEBUG`, `ALLOWED_HOSTS`, secret handling, production-safe defaults, and deployment checks.

Exit criteria:

- `DEBUG`, `SECRET_KEY`, and `ALLOWED_HOSTS` have explicit environment-driven behavior;
- local Docker development works with `localhost` without weakening production defaults;
- deployment/security-oriented Django checks are incorporated where appropriate;
- configuration behavior has automated tests;
- README/development documentation describes required environment variables;
- the complete Python and Docker CI matrix passes.

## Completed solar-domain work

### Sprint 5 — Calculator quality and solar-domain features

Status: Complete

Delivered:

- corrected the lifetime-savings formula and added input validation;
- replaced the opaque savings result with an auditable cost/savings breakdown and explicit assumptions;
- added solar-array and battery-bank sizing from daily load, peak sun hours, efficiency, autonomy, voltage, and usable battery capacity;
- added single-load and multi-load daily energy estimators;
- connected the load worksheet directly to system sizing;
- added inverter continuous and surge sizing with configurable headroom;
- added regression coverage for valid, invalid, edge-case, and calculator-handoff behavior.

Exit criteria:

- calculator inputs use explicit units and reject mathematically invalid values;
- user-facing results explain assumptions and important limitations;
- practical residential/RV planning covers daily load, solar array, battery bank, and inverter sizing;
- calculator workflows have behavioral and utility-level regression tests;
- the complete CI pipeline passes on the merged Sprint 5 implementation.

## Completed community work

### Sprint 6 — Forum and community UX

Status: Complete

Review forum permissions, posting flows, moderation fundamentals, navigation, and regression coverage.

Delivered so far:

- require authentication for reply creation while keeping thread reading public;
- escape user-authored forum content to prevent stored markup execution;
- let authors manage their own threads and responses while staff can moderate all forum content;
- use explicit 403 responses for authenticated users attempting unauthorized management actions;
- consolidate reply submission onto a single POST-only endpoint with auth-aware UI;
- add real forum pagination, efficient reply counts, and authenticated/anonymous empty states;
- enforce explicit HTTP method boundaries for forum read and mutation views;
- standardize thread/response form styling and visible validation feedback.

Exit criteria met:

- thread and response permissions and authentication behavior are covered by regression tests;
- posting and validation UX is explicit and consistent;
- author ownership and staff moderation boundaries are enforced;
- forum navigation, pagination, and empty states are functional;
- the complete CI pipeline passes on the merged Sprint 6 implementation.

## Completed content work

### Sprint 7 — Blog/content experience

Status: Complete

Improve content presentation, authoring workflow, navigation, and tests.

Delivered so far:

- make blog listing pagination and empty states deterministic;
- remove NLTK download/tokenizer runtime dependencies from blog summaries;
- add author/staff edit and delete controls with permission regression tests;
- render stored keywords and authored content consistently;
- enforce explicit HTTP method boundaries on blog read and authoring views.

Exit criteria met:

- blog rendering and startup no longer depend on runtime network downloads or external tokenizer data;
- pagination and empty states are functional and covered by regression tests;
- authoring forms, content presentation, and keyword rendering are consistent;
- author ownership and staff moderation rules protect edit/delete actions;
- blog read and mutation endpoints have explicit HTTP method boundaries;
- the complete CI pipeline passes on the merged Sprint 7 implementation.

## Current sprint

### Sprint 8 — Site navigation and application polish

Status: In progress

Improve shared navigation, remove placeholder/dead controls, modernize shared layout details, and add regression coverage for cross-application navigation.

Delivered so far:

- remove dead Contact, About, Messages, and nonfunctional Search controls rather than presenting placeholder actions;
- give shared navigation dropdowns unique HTML identifiers;
- remove Bootstrap example canonical/docsearch metadata from the application shell;
- render the footer year dynamically;
- add shared-layout regression coverage.

## Sprint rules

- Sprint numbering is sequential and persistent.
- A sprint may be split into smaller PR-sized deliverables.
- Do not mark a sprint complete merely because code exists; its exit criteria and CI must pass.
- New defects discovered during a sprint should be fixed immediately when blocking or recorded as a follow-up item.
- Documentation and tests are deliverables, not cleanup tasks.
- After a sprint is completed, development proceeds to the next sprint without requiring a separate confirmation unless priorities have changed.
