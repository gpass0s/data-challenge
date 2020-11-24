#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 01:15 BRT 2020
Last modified Tue Nov 24 02:26 BRT 2020
author: guilherme passos | twitter: @gpass0s

This module tests exercicio1.jsonchchema_validator._checkers module
"""
import pytest
from unittest.mock import call, MagicMock, patch

from desafios.exercicio1.jsonschema_validator import _checkers


@patch.object(_checkers, "_EXCEPTED_SCHEMA_FORMAT")
def test_schema(mocked_excepted_schema_format):
    # arange
    mocked_excepted_schema_format.return_value = (
        "http://json-schema.org/draft-07/schema"
    )
    schema = {"$schema": "Not expected schema"}
    # act
    with pytest.raises(Exception) as execinfo:
        _checkers.schema(schema)
    # assert
    assert str(execinfo.value) == (
      f"Schema doesn't match the expected format. Expected format: {mocked_excepted_schema_format}"
    )


def test_type():
    # arrange
    mocked_validator = MagicMock()
    types = "integer"
    event = {"eid": "3e628a05-7a4a-4bf3-8770-084c11601a12"}
    schema = None
    # act
    _checkers.type(mocked_validator, types, event, schema)
    # assert
    mocked_validator.check_type.assert_called_once_with(event, types)


def test_required():
    # arrange
    mocked_validator = MagicMock()
    required = ["eid", "documentNumber"]
    event = {"eid": "3e628a05-7a4a-4bf3-8770-084c11601a12"}
    schema = None
    # act
    with pytest.raises(Exception) as execinfo:
        _checkers.required(mocked_validator, required, event, schema)
    # assert
    assert str(execinfo.value) == "'documentNumber' is a required field"


def test_properties_fail():
    # arrange
    mocked_validator = MagicMock()
    properties = {"eid": {"type": "string"}, "age": {"type": "integer"}}
    event = {
        "eid": "3e628a05-7a4a-4bf3-8770-084c11601a12",
        "documentNumber": "42323235600",
        "age": 32,
    }
    schema = {"properties": {"eid": {"type": "string"}, "age": {"type": "integer"}}}
    # act
    with pytest.raises(Exception) as execinfo:
        _checkers.properties(mocked_validator, properties, event, schema)
    # assert
    assert str(execinfo.value) == "Field 'documentNumber' is not allowed"


def test_properties_pass():
    # arrange
    mocked_validator = MagicMock()
    properties = {"eid": {"type": "string"}, "age": {"type": "integer"}}
    event = {
        "eid": "3e628a05-7a4a-4bf3-8770-084c11601a12",
        "age": 32,
    }
    schema = {"properties": {"eid": {"type": "string"}, "age": {"type": "integer"}}}
    calls = [
        call(event["eid"], {"type": "string"}),
        call(event["age"], {"type": "integer"}),
    ]
    # act
    _checkers.properties(mocked_validator, properties, event, schema)
    # assert
    mocked_validator.check_nested_fields.assert_has_calls(calls)


def test_event_type():
    # arrange
    mocked_validator = MagicMock()
    properties = {"eid": {"type": "string"}, "age": {"type": "integer"}}
    event = {
        "eid": "3e628a05-7a4a-4bf3-8770-084c11601a12",
        "age": 32,
    }
    schema = {"properties": {"eid": {"type": "string"}, "age": {"type": "integer"}}}
    # act
    _checkers.properties(mocked_validator, properties, event, schema)
    # assert
    mocked_validator.check_type.assert_called_once_with(event, "object")
