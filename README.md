# HarvestingTablesInTheWild

To get a brief overview of the project, please refer to the [project presentation (PDF)](./report/final-presentation.pdf).

For all details, check out the [full report (PDF)](./report/report.pdf).

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

## Pipeline

Scrapy Spider -> Kafka Message Queue -> ArangoDB document store

### Scrapy

Run with:
```bash
docker-compose up --build spider # or "cc-spider"
# or
scrapy crawl web # or "common_crawl_table_parser"
# output items as JSON
scrapy crawl web -O output.json
```

URLs can either be specified as a string in environment variable `URL_STRING` (e.g. `URL_STRING=http://a.example.com,http://b.example.com`) or loaded from a file specified by `URL_FILE` with one URL per line.

By default, only the specified URLs will be crawled.
To enable deep crawls, i.e. follow links within those pages, set `FOLLOW_LINKS=true`.
The crawling strategy can be found in `core/crawling/strategy`.

To avoid visiting the same URL multiple times, set the environment variable `CRAWL_ONCE=true` (this is the default inside the container).
The database with the visited URLs is kept in `.scrapy/crawl_once/web.sqlite`.

#### Stopping and resuming crawls

To support stopping and later resuming crawls, Scrapy is storing some state in the JOBDIR (.scrapy/crawls).
For the state to be persisted properly, Scrapy needs to be shut down "gracefully" (i.e. `SIGTERM` instead of `SIGKILL`).
However, after receiving `SIGTERM` Scrapy will still finish all running requests before storing the state to disk.
Thus, it needs to have enough time to do this (and not receive `SIGTERM`, which will immediately abort but not persist state).
*This process can take SEVERAL minutes*, because we are crawling with very high concurrency.

To reset the state of the spider, run the following commands:
```
# with docker-compose
docker-compose stop spider
docker-compose rm # deletes stopped containers
docker volume rm harvestingtablesinthewild_spider_data
# or locally:
rm -r .scrapy/crawls .scrapy/crawl_once
```

### Kafka

The export of scraped items to Kafka can be enabled by setting the environment variable `KAFKA_EXPORT=true`.
The topic is called `tablecollector`.

Some commands for debugging with Kafka:
```
# open shell inside running spider container
docker exec -it htw_kafka_1

# install kafkacat
apt update && apt install -y kafkacat

# print queue metadata
kafkacat -b kafka:9092 -t tablecollector -L
> Metadata for tablecollector (from broker 1001: kafka:9092/1001):
>  1 brokers:
>   broker 1001 at kafka:9092
>  1 topics:
>   topic "tablecollector" with 2 partitions:
>     partition 0, leader 1001, replicas: 1001, isrs: 1001
>     partition 1, leader 1001, replicas: 1001, isrs: 1001


# act as a listener (consumer)
kafkacat -b kafka:9092 -t tablecollector -C
> % Reached end of topic tablecollector [1] at offset XXX

# act as a sender (producer)
kafkacat -b kafka:9092 -t tablecollector -P
(type and hit enter)
```

### ArangoDB

Bring up the database:
```
docker-compose up -d arangodb
```

The `ARANGO_ROOT_PASSWORD` is stored in the `.env` file.

Connect with a shell:
```
docker exec -it htw_arangodb_1 arangosh
(enter password)
```

Run a basic AQL query:
```
db._query({"query": "FOR table IN parsed_tables RETURN [table.url, table.tableNum]"}).toArray()
```

Arango Shell Cheatsheet: https://gist.github.com/jperocho/893a52748a27349a99452e78a6565da6

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
