#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
Created on Sun Nov 22 09:03 BRT 2020
Last modified on Mon Nov 23 08:13 BRT 2020
author: guilherme passos | github: @gpass0s

This module implements the json schema checkers which are functions to the corresponding field
"""

from desafios.exercicio1.jsonschema_validator.exceptions import JsonSchemaError, ValidationError

_EXCEPTED_SCHEMA_FORMAT = "http://json-schema.org/draft-07/schema"


def schema(schema):
    """
    This method verifies if the given schema format correspond to the json-schema.org draft07
    """

    if schema.get("$schema") != _EXCEPTED_SCHEMA_FORMAT:
        raise JsonSchemaError(
            f"Schema doesn't match the expected format. Expected format: {_EXCEPTED_SCHEMA_FORMAT}"
        )


def type(validator, types, document, schema):
    """
    This method verifies if document property values have the specified type
    """
    if isinstance(types, str):
        types = [types]

    if not any(validator.check_type(document, pytype) for pytype in types):
        raise ValidationError(
            f"Document or field does not match the expected type. Expected types: {repr(types)}"
        )


def required(validator, required, document, schema):
    """
    This method checks if document has all required fields in its properties
    """
    if not validator.check_type(document, "object"):
        return
    for field in required:
        if field not in document:
            raise ValidationError(f"'{field}' is a required field")


def properties(validator, properties, document, schema):
    """
    This method verifies all document properties
    """
    if not validator.check_type(document, "object"):
        return

    for field in document.keys():
        if field not in schema["properties"]:
            raise ValidationError(f"Field '{field}' is not allowed")

    for field, subschema in properties.items():
        if field in document:
            validator.check_nested_fields(document[field], subschema)
