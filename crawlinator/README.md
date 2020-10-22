# Crawlinator

Crawlinator crawls web pages and extracts tables. It's an initial prototype for knowledge extraction pipeline.

* Programming language: Python 3
* Data Storage: Apache Arrow

## Installation

Clone the repository and `cd` into this directory.
Install the python dependencies:
```
python3 -m venv venv
. ./venv/bin/activate
pip install -r requirements.txt
```

## Run

```
./crawlinator.py URL [URL...]
```

