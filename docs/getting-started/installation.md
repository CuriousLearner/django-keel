# Installation

Django Keel is a [Copier](https://copier.readthedocs.io/) template. You install
the tooling once, then generate projects from it.

## Prerequisites

- [Python 3.12+](https://www.python.org/downloads/)
- [Copier](https://copier.readthedocs.io/) — `pipx install copier` (or `uv tool install copier`)
- [Docker & Docker Compose](https://docs.docker.com/get-docker/) — to run the generated stack

Optional, depending on the options you pick:

- [uv](https://docs.astral.sh/uv/) or [Poetry](https://python-poetry.org/) for the generated project's dependencies
- Node.js 20 LTS + npm/pnpm/yarn if you choose the Next.js frontend

## Generate a project

```bash
copier copy gh:CuriousLearner/django-keel your-project-name
```

Answer the prompts and Copier writes your project. See
[Creating Your First Project](first-project.md) for a walk-through of the
prompts and what gets generated.

## Update an existing project

Regenerate against a newer template version from inside your project:

```bash
copier update
```
