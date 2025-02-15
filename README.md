<h2 align="center"> Implementation of Clean Architecture (Uncle Bob) on FastAPI </h2>

---

<p align="center">
  <a href="https://github.com/Maclovi/pure-architecture-fastapi/actions/workflows/pr_tests.yaml" target="_blank">
    <img src="https://github.com/Maclovi/pure-architecture-fastapi/actions/workflows/pr_tests.yaml/badge.svg?branch=main" alt="Test Passing"/>
  </a>

  <a href="https://github.com/Maclovi/pure-architecture-fastapi/blob/main/LICENSE" target="_blank">
    <img src="https://img.shields.io/github/license/Maclovi/pure-architecture-fastapi.png" alt="License"/>
  </a>
</p>

---

<!--toc:start-->

- [Requirements](#requirements)
- [Cloning the Repository](#cloning-the-repository)
- [How to run](#how-to-run)
- [How to use](#how-to-use)
- [Author](#author)
<!--toc:end-->

### Requirements

- Git
- Docker & Docker-compose latest

### Cloning the Repository and Setup

```bash
git clone https://github.com/Maclovi/pure-architecture-fastapi
cd pure-architecture-fastapi
cp .env.dist .env

python -m venv .venv
source .venv/bin/activate
source ./scripts/set_variables.sh

pip install uv && uv pip install -e ".[dev]"
pre-commit install
```

## How to run

Just:

```bash
docker-compose up
```

## How to use

Follow this [swagger](http://localhost:8000/docs) link and test the API

## Author

**Sergey** - [GitHub Profile](https://github.com/Maclovi)
