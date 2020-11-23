#!/bin/bash

docker-compose up -d arangodb-test
sleep 10 # Wait for arangodb to initialize
docker-compose build test
docker-compose run --rm test
exitcode=$?
docker-compose down
if [ $exitcode -ne 0 ]; then
    exit $exitcode
fi
