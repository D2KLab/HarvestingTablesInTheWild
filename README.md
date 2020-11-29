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

## Monitoring/Logging

### Setup

```bash
# Kibana will take a while to initialize...
docker-compose -f docker-compose.elk.yml up --build kibana
# logspout is a container for redirecting docker logs to elasticsearch
# run it after kibana is ready
docker-compose -f docker-compose.elk.yml up --build logspout
```

### Usage

Navigate to [http://localhost:5601/](http://localhost:5601/).
These are container logs, so if you want only logs from specific containers, you could eg. query:

Logs for web spider

```kql
docker.image : harvestingtablesinthewild_spider
```

Logs for common crawl spider

```kql
docker.image : harvestingtablesinthewild_cc
```
