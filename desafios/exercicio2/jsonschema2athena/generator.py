#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
Created on Mon Nov 23 01:09 BRT 2020
Last modified on Mon Nov 23 23:20 BRT 2020
author: guilherme passos | github: @gpass0s

This module generates an Athena CREATE TABLE query according to a given json schema
"""

import json

from pathlib import Path

_DEFAULT_DATABASE = "data-challange"

_DEFAULT_TABLE = "events"

_DEFAULT_LOCATION = "s3://iti-query-results/"

_DEFAULT_SERDE = "org.apache.hadoop.hive.serde2.RegexSerDe"

_DEFAULT_SERDEPROPERTIES = "'input.regex' = '^(?!#)([^ ]+)\\s+([^ ]+)\\s+([^ ]+)\\s+([^ ]+)\\s+([^ ]+)\\s+([^ ]+)\\s+([^ ]+)\\s+([^ ]+)\\s+([^ ]+)\\s+([^ ]+)\\s+[^\(]+[\(]([^\;]+).*\%20([^\/]+)[\/](.*)$'"


class TableFieldsGenerator:
    def __init__(self, tab="  ", keywords=["timestamp", "date", "datetime"]):

        self.tab = tab
        self.hive_keywords = keywords

    def generate_fields(self, schema, level=0):
        if level == 0:
            self.type_separator = " "
        else:
            self.type_separator = ":"

        _field_separator = "\n"

        table_fields = []
        self.level = level + 1
        self.indentation = self.level * self.tab

        for key, attributes in schema.items():

            field_name = key
            if field_name.lower() in self.hive_keywords:
                field_name = f"`{field_name}`"

            if attributes["type"] == "object":
                table_fields.append(
                    "{}{}{}STRUCT <\n{}\n{}>".format(
                        self.indentation,
                        field_name,
                        self.type_separator,
                        self.generate_fields(attributes["properties"], self.level),
                        self.indentation,
                    )
                )

            elif attributes["type"] == "array":

                extra_indentation = (self.level + 1) * self.tab

                if attributes["items"]["type"] == "object":
                    closing_bracket = "\n" + self.indentation + ">"
                    array_type = "STRUCT <\n{}\n{}>".format(
                        extra_indentation,
                        self.generate_fields(
                            attributes["items"]["properties"], self.level + 1
                        )
                    )
                else:
                    closing_bracket = ">"
                    array_type = attributes["items"]["type"].upper()

                table_fields.append(
                    "{}{}{}ARRAY<{}{}".format(
                        self.indetation,
                        field_name,
                        self.type_separator,
                        array_type,
                        closing_bracket,
                    )
                )

            else:
                table_fields.append(
                    "{}{}{}{},".format(
                        self.indentation,
                        field_name,
                        self.type_separator,
                        attributes["type"].upper(),
                    )
                )

        return _field_separator.join(table_fields)


def generate_query(
    database=None,
    table=None,
    schema=None,
    location=None,
    serde=None,
    serdeproperties=None,
):
    if database is None:
        database = _DEFAULT_DATABASE

    if table is None:
        table = _DEFAULT_TABLE

    if schema is None:
        with open(f"{Path(__file__).parent}/../schema.json") as file:
            schema = json.load(file)

    if location is None:
        location = _DEFAULT_LOCATION

    if serde is None:
        serde = _DEFAULT_SERDE

    if serdeproperties is None:
        serdeproperties = _DEFAULT_SERDEPROPERTIES

    generator = TableFieldsGenerator()

    table_fields = generator.generate_fields(schema["properties"])

    statement = f"""CREATE EXTERNAL TABLE IF NOT EXISTS {database}.{table} (
{table_fields}
)
ROW FORMAT SERDE '{serde}'
WITH SERDEPROPERTIES (
 {serdeproperties}
)
LOCATION '{location}';"""

    return statement
