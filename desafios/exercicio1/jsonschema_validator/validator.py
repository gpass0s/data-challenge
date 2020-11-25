#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
Created on Sat Nov 21 17:21 BRT 2020
Last modified on Mon Nov 23 11:02 BRT 2020
author: guilherme passos | github: @gpass0s

Validates a document under the given schema. It raises an exeception whenever validation fails
"""
import json

from pathlib import Path
from jsonschema_validator import _checkers

_CHECKERS_MAPPING = {
    "schema": _checkers.schema,
    "required": _checkers.required,
    "type": _checkers.type,
    "properties": _checkers.properties,
}

_TYPES_MAPPING = {
    "array": list,
    "boolean": bool,
    "integer": int,
    "null": type(None),
    "object": dict,
    "string": str,
}


class Validator:
    """
    Implements a validator object to perform validation
    """

    def check_schema(self, schema):
        schema_checker = _CHECKERS_MAPPING["schema"]
        schema_checker(schema)

    def check_document(self, document, schema):
        for key, value in schema.items():
            checker = _CHECKERS_MAPPING.get(key)
            if checker is None:
                continue
            checker(self, value, document, schema)

    def check_type(self, value, expected_type):
        pytype = _TYPES_MAPPING.get(expected_type)
        return isinstance(value, pytype)

    def check_nested_fields(self, document, schema):
        self.check_document(document, schema)


def validate(document, validator, schema=None):
    """
    This method validates an document under the given schema

    Arguments:

        document: The document that needs to be validated
        schema: The schema to validate

    Raises:
        JsonSchemaError or ValidationError when validation fails
    """
    if schema is None:
        with open(f"{Path(__file__).parent}/../schema.json") as file:
            schema = json.load(file)

    validator.check_schema(schema)
    validator.check_document(document, schema)


validator = Validator()
