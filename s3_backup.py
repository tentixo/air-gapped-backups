#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Nice header

A module for fixing stuff

More descriptions"""

__author__ = "Lars Mårelius <morre@tentixo.com>"

import argparse
import settings
import utilities
import json
import os
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from boto3.s3.transfer import TransferConfig
from dotenv import load_dotenv

import logging
from logging.config import dictConfig

load_dotenv()
ENV = os.getenv("ENV")

# Set up logging
LOGGING_CONFIG_PATH = os.path.join(settings.CONFIG_DIR, f"{ENV}-logging-config.json")
with open(LOGGING_CONFIG_PATH, 'r') as log_json:
    log_cfg = json.load(log_json)
logging.config.dictConfig(log_cfg)
logger = logging.getLogger(__name__)

# Get the configs
CONFIG_PATH = os.path.join(settings.CONFIG_DIR, f"{ENV}-config.json")
CONFIG_SECRETS_PATH = os.path.join(settings.CONFIG_DIR, f"{ENV}-secrets.json")
bkp_config = utilities.load_data_from_disk(CONFIG_PATH)
bkp_secrets = utilities.load_data_from_disk(CONFIG_SECRETS_PATH)

# Custom configuration for retries and timeouts
custom_config = Config(
    retries={
        'max_attempts': bkp_config['client-max-attempts'],  # Maximum retry attempts
        'mode': 'adaptive'  # Use the adaptive retry mode
    },
    connect_timeout=bkp_config['client-connect-timeout-s'],  # How long to wait for the connection to the server (s)
    read_timeout=bkp_config['client-read-timeout-s'],  # How long to wait for a response from the server (s)
)

# Create an STS client using the loaded credentials
sts_client = boto3.client(
    'sts',
    region_name=bkp_config['aws-region'],
    aws_access_key_id=bkp_secrets['aws-key-id'],
    aws_secret_access_key=bkp_secrets['aws-secret-key']
)

# Assume the role
assumed_role_object = sts_client.assume_role(
    RoleArn=bkp_secrets['sts-role'],
    RoleSessionName="AssumeRoleSession1"
)

# Credentials to use with the assumed role
temp_credentials = assumed_role_object['Credentials']

# Use the temporary credentials to create a session
session = boto3.Session(
    region_name=bkp_config['aws-region'],
    aws_access_key_id=temp_credentials['AccessKeyId'],
    aws_secret_access_key=temp_credentials['SecretAccessKey'],
    aws_session_token=temp_credentials['SessionToken']
)

# Now you can use this session to interact with AWS services
s3_resource = session.resource('s3',
                               config=custom_config)


def upload_file_to_s3(local_file_dir, file_name, s3_folder_name, s3_object_name=None):
    """Upload a file to an S3 bucket
        :param local_file_dir: The sub-folder in the base dir containing the file to upload
        :param file_name: File to upload
        :param s3_folder_name: Folder in the bucket to upload to
        :param s3_object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """
    try:
        # If S3 object_name was not specified, use file_name
        if s3_object_name is None:
            s3_object_name = file_name

        bucket = s3_resource.Bucket(bkp_secrets['s3-bucket-name'])
        folder_path = f"{s3_folder_name}/"

        # Check if folder exists by trying to list objects with its prefix
        objects = list(bucket.objects.filter(Prefix=folder_path))
        if not objects:
            # Folder does not exist, so create it by uploading an empty file
            logger.info(f"Folder did not exist in S3. Creating {s3_folder_name}")
            bucket.put_object(Key=folder_path)
        else:
            logger.debug(f"Folder {s3_folder_name} exists in S3")

        file_path_locally = os.path.join(local_file_dir, file_name)
        logger.debug(f"Created local file path: {file_path_locally}")

        object_path_in_s3 = f"{folder_path}{s3_object_name}"
        logger.debug(f"Crated S3 object path: {object_path_in_s3}")

        # Configure the multipart upload
        transfer_config = TransferConfig(multipart_threshold=1024 * bkp_config['multipart-threshold-mb'],
                                         max_concurrency=bkp_config['max-concurrency'],
                                         multipart_chunksize=1024 * bkp_config['multipart-chunksize-mb'],
                                         use_threads=True)

        s3_resource.meta.client.upload_file(file_path_locally, bkp_secrets['s3-bucket-name'], object_path_in_s3,
                                            Config=transfer_config)
        logger.info(f"Successfully uploaded {file_name} to {object_path_in_s3}")
    except ClientError as e:
        logger.error(f"Failed to upload {file_name} to {s3_folder_name}/{s3_object_name}: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Upload files to S3')
    parser.add_argument('local_file_dir', type=str, help='Local path to directory with file to upload.')
    parser.add_argument('file_name', type=str, help='The name of the file to upload.')
    parser.add_argument('s3_folder_name', type=str, help='The S3 folder name.')

    args = parser.parse_args()

    upload_file_to_s3(args.local_file_dir, args.file_name, args.s3_folder_name)
