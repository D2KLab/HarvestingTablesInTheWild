FROM python:3.8

WORKDIR /srv/app

RUN set -ex; \
    apt update && apt install -y --no-install-recommends \
    libsqlite3-dev \
    sqlite3 \
    nano \
    kafkacat \
    \
    && apt-get -y autoclean; apt-get -y autoremove; \
    rm -rf /var/lib/apt/lists/*

COPY Pipfile Pipfile.lock ./

RUN python -m pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --system --ignore-pipfile --dev
RUN python -m spacy download en

COPY . .
