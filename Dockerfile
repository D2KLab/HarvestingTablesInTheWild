FROM python:3.8

WORKDIR /srv/app

COPY Pipfile Pipfile.lock ./

RUN python -m pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install --system --ignore-pipfile --dev

COPY . .

CMD ["scrapy", "crawl", "table_parser"]
