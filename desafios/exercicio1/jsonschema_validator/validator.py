#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
Created on Sat Nov 21 17:21 BRT 2020
Last modified on Sat Nov 21 17:21 BRT 2020
author: guilherme passos | github: @gpass0s

This module validates a document schema under the given schema. It thorws an error whenever
the validation fails
"""

from jsonschema_validator import _checkers

_DEFAULT_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "$id": "http://example.com/example.json",
    "type": "object",
    "title": "The root schema",
    "description": "The root schema comprises the entire JSON document.",
    "required": ["eid", "documentNumber", "name", "age", "address"],
    "properties": {
        "eid": {
            "$id": "#/properties/eid",
            "type": "string",
            "title": "The eid schema",
            "description": "An explanation about the purpose of this instance.",
            "examples": ["3e628a05-7a4a-4bf3-8770-084c11601a12"],
        },
        "documentNumber": {
            "$id": "#/properties/documentNumber",
            "type": "string",
            "title": "The documentNumber schema",
            "description": "An explanation about the purpose of this instance.",
            "examples": ["42323235600"],
        },
        "name": {
            "$id": "#/properties/name",
            "type": "string",
            "title": "The name schema",
            "description": "An explanation about the purpose of this instance.",
            "examples": ["Joseph"],
        },
        "age": {
            "$id": "#/properties/age",
            "type": "integer",
            "title": "The age schema",
            "description": "An explanation about the purpose of this instance.",
            "examples": [32],
        },
        "address": {
            "$id": "#/properties/address",
            "type": "object",
            "title": "The address schema",
            "description": "An explanation about the purpose of this instance.",
            "required": ["street", "number", "mailAddress"],
            "properties": {
                "street": {
                    "$id": "#/properties/address/properties/street",
                    "type": "string",
                    "title": "The street schema",
                    "description": "An explanation about the purpose of this instance.",
                    "examples": ["St. Blue"],
                },
                "number": {
                    "$id": "#/properties/address/properties/number",
                    "type": "integer",
                    "title": "The number schema",
                    "description": "An explanation about the purpose of this instance.",
                    "examples": [3],
                },
                "mailAddress": {
                    "$id": "#/properties/address/properties/mailAddress",
                    "type": "boolean",
                    "title": "The mailAddress schema",
                    "description": "An explanation about the purpose of this instance.",
                    "examples": [True],
                },
            },
        },
    },
}

_EXCEPTED_SCHEMA_FORMAT = _DEFAULT_SCHEMA["$schema"]

_CHECKERS_MAPPING = {
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


def check_schema(schema):
    """
    This method verifies if the given schema format correspond to the json-schema.org draft07
    """
    if schema.get("$schema") != _EXCEPTED_SCHEMA_FORMAT:
        raise TypeError(
            f"""The given schema does not match the expected format. Check the expected format at
        {_EXCEPTED_SCHEMA_FORMAT}"""
        )


def validate(document, validator, schema=None):
    """
    This method validates an document under the given schema

    Arguments:

        document: The document that needs to be validated
        schema: The schema to validate

    Raises:
        ValueError or TypeError if the document or schema is not valid
    """

    if schema is None:
        schema = _DEFAULT_SCHEMA

    check_schema(schema)
    validator.check_document(document, schema)


validator = Validator()
