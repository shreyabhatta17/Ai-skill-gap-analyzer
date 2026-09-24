# AI Skill-Gap Analyzer Progress Summary

This document records the current implementation milestone for the university project.

## Completed work

### Phase 0: Repository and project setup

- Created the layered repository structure and framework-independent placeholders in `analyzer/`:
  - `matching.py`
  - `gap_scoring.py`
  - `recommender.py`
  - `engine.py`
- Created the Django project under `webapp/` with `manage.py`, settings, URLs, WSGI, and ASGI configuration.
- Added Django apps for `webapp/api/` and `webapp/core/`.
- Configured SQLite, environment-based settings, pytest, requirements, `.gitignore`, and the README.
- Added the Phase 0 smoke test.

### Phase 1: Domain model and knowledge base

- Replaced the starter schema with the five required models:
  - `Skill`
  - `JobRole`
  - `JobSkillRequirement`
  - `UserSkill`
  - `LearningResource`
- Added validated skill levels and requirement importance values, model ordering, string representations, relationships, and admin registration.
- Replaced the old migration with a clean `0001_initial` migration.
- Expanded `knowledge_base/skills.json` to 67 canonical skills.
- Added role fixtures for:
  - Data Analyst
  - Data Scientist
  - Machine Learning Engineer
  - Backend Developer
  - DevOps Engineer
- Added 15–16 requirements per role, with 76 total requirements and 47 learning resources.
- Added the idempotent `load_knowledge_base` management command with unknown-skill error handling and count summaries.
- Added pure JSON tests and pytest-django model/loader tests.
- Updated README with the model description, fixture schema, commands, and first-draft review note.

### Phase 2: Gap-scoring module

- Added pure-Python dataclasses for requirements, individual gaps, and reports.
- Added slug/path role loading from `knowledge_base/roles/`.
- Added weighted gap calculation, case-insensitive skill matching, status buckets, deterministic ordering, and validation.
- Added focused unit and integration-style tests for hand-calculated scores and the real Data Analyst fixture.
- Documented the formulas and usage in the README.

### Phase 3: Embedding-based skill matcher

- Added `analyzer/matching.py` with a cached `all-MiniLM-L6-v2` model, canonical
  vocabulary loading, normalized cosine similarity, thresholded `MatchResult`
  values, top-three near-miss candidates, and efficient batch matching.
- Added the pinned `sentence-transformers` dependency.
- Added 60 hand-labelled free-text examples and the reusable
  `analyzer.eval_matching` harness.
- Added slow-marked matcher tests, including exact names, paraphrases, nonsense,
  the SQL/NoSQL trap, batch ordering, and the measured accuracy threshold.
- Measured 89.7% top-1 accuracy (52/58) on the first-pass evaluation fixture.

## Validation status

- `python webapp/manage.py migrate` succeeds.
- `python webapp/manage.py load_knowledge_base` succeeds on repeated runs without duplicates.
- `python webapp/manage.py makemigrations --check --dry-run` reports no changes.
- `pytest` passed with 23 tests after Phase 3 implementation.
- Loaded database counts: 67 skills, 5 roles, 76 requirements, 47 resources.

## Not implemented yet

These items remain intentionally deferred to later phases:

- Recommendation ranking/engine integration
- Django REST API endpoints
- Templates, frontend, and Chart.js visualizations
- Docker, CI, and deployment configuration

## Current project status

Phase 0 through Phase 3 are complete. The project is ready for recommendation work. The knowledge base and hand-labelled matcher evaluation set are first drafts and must be reviewed against real job postings and O*NET data before being treated as authoritative.

Phase 2 changes are committed locally; nothing has been pushed.
