# HarvestingTablesInTheWild

## Requirements

- `pipenv`
- `docker-compose`

## Installation

```bash
pipenv install
```

## Lint and testing

Linting:

```bash
docker-compose up --build lint
# or
scripts/run_linter.sh
```

Tests:

```bash
docker-compose up --build test
```

## Run

```bash
docker-compose up --build spider
# or
URL_FILE=<your file containing urls> scrapy runspider table_parser.py
```
