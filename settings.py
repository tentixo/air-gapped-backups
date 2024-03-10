#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  Copyright (c) 2019. Tentixo NG AB GLN 7350108000000´

import os

# Full filesystem path to the Python app.
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Name of the directory for the project.
PROJECT_DIRNAME = PROJECT_ROOT.split(os.sep)[-1]

# Directories and paths
CONFIG_DIR = os.path.join(PROJECT_ROOT, "config")
LOGGING_CONFIG_PATH = os.path.join(CONFIG_DIR, "logging-config.json")
CONFIG_PATH = os.path.join(CONFIG_DIR, "bkp-config.json")
CONFIG_SECRETS_PATH = os.path.join(CONFIG_DIR, "bkp-secrets.json")
TEMP_DIR = os.path.join(PROJECT_ROOT, "tmp")
LOGS_DIR = os.path.join(PROJECT_ROOT, "logs")
FILES_DIR = os.path.join(PROJECT_ROOT, "files")
TEMPLATES_DIR = os.path.join(PROJECT_ROOT, "templates")
SCHEMAS_DIR = os.path.join(PROJECT_ROOT, "schemas")
