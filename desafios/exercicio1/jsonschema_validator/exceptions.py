#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
Created on Sun Nov 22 21:09 BRT 2020
Last modified on Sun Nov 22 23:06 BRT 2020
author: guilherme passos | github: @gpass0s

This module implements execpetions that are thrown when validation fails
"""


class JsonSchemaError(Exception):
    """
    Exception for an invalid json schema format
    """

    def __init__(self, msg=None):

        if msg is None:
            msg = "The given schema does not match the expected format"
        self.message = msg
        super(JsonSchemaError, self).__init__(msg)


class ValidationError(Exception):
    """
    Exception for an invalid type
    """

    def __init__(self, msg=None):
        if msg is None:
            msg = "Validation failed"
        self.message = msg
        super(ValidationError, self).__init__(msg)
