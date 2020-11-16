#!/bin/bash

if [[ -z "${REQUIRED_QUALITY}" ]]; then
    echo "Using default linting failure limit..."
    REQUIRED_QUALITY=9
fi

module_directories=$(find . -name __init__.py -print0 | xargs -0 -n1 dirname | sort --unique)
pylint --rcfile=.pylintrc --fail-under=$REQUIRED_QUALITY $module_directories
