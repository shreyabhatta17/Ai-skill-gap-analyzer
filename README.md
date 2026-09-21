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
pytest
python webapp\manage.py runserver
```

Set `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, and `DJANGO_ALLOWED_HOSTS` in the environment when running outside local development. Development defaults are intentionally provided for local setup.

## Knowledge base review

The starter skills taxonomy is illustrative project scaffolding, not authoritative labor-market data. It must be reviewed and expanded against real job postings and O*NET before it is used for research conclusions or production recommendations. Role files can be added under `knowledge_base/roles/` as the taxonomy is validated.

## Project status

- Phase 0: repository and Django project setup complete.
- Phase 1: initial domain models and starter knowledge-base structure complete.
- Phase 3+: matching, gap scoring, recommendations, API endpoints, and frontend are not implemented yet.
