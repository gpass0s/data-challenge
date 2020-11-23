#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
Created on Sun Nov 22 23:42 BRT 2020
Last modified on Sun Nov 22 23:42 BRT 2020
author: guilherme passos | github: @gpass0s

This module implements a custom log
"""

import logging
from pythonjsonlogger.jsonlogger import JsonFormatter


def _get_logger():
    """Generate a logger."""
    logger = logging.getLogger("data-challenge")
    logger.propagate = False  # reset handler to avoid duplicates
    logger.handlers = [_get_json_handler()]
    logger.setLevel(logging.INFO)
    return logger


def _get_json_handler():
    formatter = JsonFormatter("(asctime) (levelname) (module) (funcName) (message)")
    log_handler = logging.StreamHandler()
    log_handler.setFormatter(formatter)
    return log_handler


logger = _get_logger()
