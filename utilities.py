#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Project utilities.
Utility functions for the project.
Load from disk: json, yaml, txt, csv optionally validate with JSON Schema.
Save to disk: Text as bjson, yaml or just dump, or binary.
Text as UTF-8 only.
"""

__author__ = "Lars Mårelius <morre@tentixo.com>"

import settings

import json
import yaml
import csv
import os
import fnmatch
import jsonschema
import logging
from logging.config import dictConfig
from dotenv import load_dotenv

load_dotenv()
ENV = os.getenv("ENV")

# Set up logging
LOGGING_CONFIG_PATH = os.path.join(settings.CONFIG_DIR, f"{ENV}-logging-config.json")
with open(LOGGING_CONFIG_PATH, 'r') as log_json:
    log_cfg = json.load(log_json)
logging.config.dictConfig(log_cfg)
logger = logging.getLogger(__name__)


def load_data_from_disk(file_path, schema=None):
    """Reads JSON, Yaml, txt, csv from disk and optionally validates against a JSON Schema.
    :param file_path:
    :param schema: Optional JSON Schema for validation.
    :return: Loaded data or None if validation fails.
    """
    try:
        with open(file_path, 'r') as fr:
            if fnmatch.fnmatch(file_path, '*.json'):
                loaded_data = json.load(fr)
            elif fnmatch.fnmatch(file_path, '*.yaml') or fnmatch.fnmatch(file_path, '*.yml'):
                loaded_data = yaml.safe_load(fr)
            elif fnmatch.fnmatch(file_path, '*.txt') or fnmatch.fnmatch(file_path, '*.html'):
                loaded_data = fr.read()
            elif fnmatch.fnmatch(file_path, '*.csv'):
                loaded_data = list(csv.DictReader(fr, delimiter=";"))
            else:
                logger.info("Unsupported file format: {0}".format(file_path))
                return None

            # Optionally validate against the provided JSON Schema
            if schema is not None:
                try:
                    jsonschema.validate(loaded_data, schema)
                except jsonschema.ValidationError as e:
                    logger.error("JSON Schema validation error: {0}".format(e))
                    return None

            return loaded_data
    except IOError as e:
        logger.error("I/O error({0}): {1}".format(e.errno, e.strerror))
        logger.error("The file path does not exist: {0}".format(file_path))
    except Exception as e:
        logger.error("Error reading file: {0}".format(e))


def write_data_to_disk(file_path, data_structure, mode='w'):
    """Writes a data structure to either JSON or Yaml file.
    :param file_path: The path (dir + file name) where to save your file.
    :param data_structure: The file you need to store on disk.
    :param mode: Write text 'w' (default) or binary 'wb' files.
    """
    try:
        with open(file_path, mode) as fw:
            if 'wb' in mode:
                fw.write(file_path)
            elif 'w 'in mode:
                if fnmatch.fnmatch(file_path, '*.json'):
                    json.dump(data_structure, fw, indent=4, separators=(',', ': '), ensure_ascii=False)
                if fnmatch.fnmatch(file_path, '*.yaml'):
                    yaml.dump(data_structure, fw)
                else:
                    fw.write(file_path)
    except IOError as e:
        logger.error("I/O error({0}): {1}".format(e.errno, e.strerror))
        logger.error("The path does not exist: {0}".format(file_path))
