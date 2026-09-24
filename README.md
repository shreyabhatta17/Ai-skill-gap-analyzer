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

## Gap scoring

The framework-independent scorer in `analyzer/gap_scoring.py` compares each role requirement with a user's skill level from 0 to 5. For each skill, `raw_gap = max(0, required_level - user_level)` and `weighted_gap = raw_gap * importance`. The overall gap score is `sum(weighted_gap) / sum(required_level * importance)`; the match percentage is `round((1 - overall_gap_score) * 100, 1)`. Missing skills count as level 0, and over-qualified skills receive no bonus.

```python
from analyzer.gap_scoring import calculate_gap, load_role

title, requirements = load_role("data-analyst")
report = calculate_gap(requirements, {"SQL": 4, "Python": 2}, title)
print(report.overall_match_percent)
print([gap.skill for gap in report.missing])
```

## Skill matching

Phase 3 adds a framework-independent embedding matcher in `analyzer/matching.py`.
It embeds each of the 67 canonical skills once and compares free-text phrases with
cosine similarity using `all-MiniLM-L6-v2`. A result is accepted when its best
similarity is at least the default threshold of `0.55`; otherwise the result is
rejected and includes the top three near-miss candidates for debugging. Use one
`SkillMatcher` instance for the lifetime of a Django process rather than creating
one per request.

The first matcher run downloads the approximately 90 MB model and therefore needs
internet access once. The reusable hand-labelled evaluation set is in
`tests/fixtures/matching_examples.json`. Run it with:

```powershell
python -m analyzer.eval_matching
```

The current measured top-1 accuracy is 89.7% (52/58) on this first-pass fixture.
It may change if the model, vocabulary, or fixture changes.

## Project status

- Phase 0: repository and Django project setup complete.
- Phase 1: domain models, JSON knowledge base, loader, and tests complete.
- Phase 2: framework-independent gap scoring, validation, role loading, tests, and documentation complete.
- Phase 3: embedding-based skill matching, reusable labelled evaluation data,
  evaluation harness, and tests complete.
- Phase 4+: recommendations, API endpoints, and frontend are not implemented yet.
