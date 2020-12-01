# HarvestingTablesInTheWild

## Requirements

- Python 3.8
- `pipenv`
- `docker-compose`

## Installation

For installing runtime dependencies:
```bash
pipenv install
```

For also installing development dependencies (linting & testing):
```
pipenv install --dev
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
scrapy crawl web
# output items as JSON
scrapy crawl web -O output.json
```

URLs can either be specified as a string in environment variable `URL_STRING` (e.g. `URL_STRING=http://a.example.com,http://b.example.com`) or loaded from a file specified by `URL_FILE` with one URL per line.

By default, only the specified URLs will be crawled.
To enable deep crawls, i.e. follow links within those pages, set `FOLLOW_LINKS=true`.
The crawling strategy can be found in `core/crawling/strategy`.
