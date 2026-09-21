# AI Skill-Gap Analyzer

AI Skill-Gap Analyzer is a Django-based university project that will compare a user's skills with the skills expected for a target job role and recommend resources for closing meaningful gaps.

## Planned architecture

The project is organized as layered components: a framework-independent matcher, gap-scoring layer, recommender, Django REST Framework API, and templates with Chart.js for visualizations. The analysis engine remains independent of Django so it can be tested and reused outside the web application.

## Setup

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python webapp\manage.py migrate
python webapp\manage.py load_knowledge_base
pytest
python webapp\manage.py runserver
```

Set `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, and `DJANGO_ALLOWED_HOSTS` in the environment when running outside local development. Development defaults are intentionally provided for local setup.

## Phase 1 knowledge base

The domain model contains `Skill`, `JobRole`, `JobSkillRequirement`, `UserSkill`, and `LearningResource`. A role has many skills through requirements, each requirement storing a validated required level and importance. User skills can belong to an authenticated Django user or a free-text session, and resources are linked to skills with type, level, cost, URL, and notes.

Knowledge-base JSON is stored under `knowledge_base/`. `skills.json` contains canonical skills with `name`, `category`, and `description`. Each `knowledge_base/roles/<slug>.json` contains `title`, `slug`, `description`, and a `skills` array. Every array item names a skill exactly and contains `required_level`, `importance`, and one or more resources with `title`, `url`, `resource_type`, `level`, `is_free`, and `notes`.

After migrations, load or reload the fixtures with:

```powershell
python webapp/manage.py migrate
python webapp/manage.py load_knowledge_base
```

The loader is idempotent and can safely be run again. This knowledge base is a first draft and must be reviewed against real job postings and O*NET before it supports research conclusions or production recommendations.

## Project status

- Phase 0: repository and Django project setup complete.
- Phase 1: domain models, JSON knowledge base, loader, and tests complete.
- Phase 3+: matching, gap scoring, recommendations, API endpoints, and frontend are not implemented yet.
