#!/usr/bin/env python3

import json
import sys

import jsonschema


def load_json_file(filename):
    data = ""
    with open(filename, 'r') as file:
        data = json.load(file)

    return data

def validate_json(schema_file, data_file):
    execute_api_schema = load_json_file(schema_file)
    json_data = load_json_file(data_file)

    # if the file contains a list of JSON objects,
    # then we verify the structure of each object individually
    if not isinstance(json_data, list):
        json_data_list = [json_data]
    else:
        json_data_list = json_data

    for json_item in json_data_list:
        try:
            jsonschema.validate(instance=json_item, schema=execute_api_schema)
        except jsonschema.exceptions.ValidationError as err:
            return err

    return None


def main():
    if len(sys.argv) < 3:
        print("Usage: ./validate_schema.py SCHEMA.json DATA.json")
        sys.exit(1)

    schema_file = sys.argv[1]
    data_file = sys.argv[2]

    err = validate_json(schema_file, data_file)
    if err is not None:
        print(err)
        sys.exit(1)

    print("OK")
    sys.exit(0)

if __name__ == "__main__":
    main()
