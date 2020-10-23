# Crawlinator

Crawlinator crawls web pages and extracts tables. It's an initial prototype for knowledge extraction pipeline.

* Programming language: Python 3 (3.7)
* Data Storage: Apache Avro

## Installation

Clone the repository and `cd` into this directory.
Install the python dependencies:
```
python3 -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
```

When you add a new library, please add the *exact* version number to `requirements.txt`.

## Lint and testing

To lint the python code, run:
```
python3 -m pylint *.py
```

The Github Actions CI pipeline also automatically checks all code pushed to the repository.

## Run

(inside the activated virtual environment)
```
./crawlinator.py URL [URL...]
```

