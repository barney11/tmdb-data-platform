# Copyright 2023 Maximilien Soviche.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Bigquery tables creation script from GCP bucket json files."""

import logging
import os

from google.cloud import bigquery
from google.cloud.exceptions import NotFound
from google.cloud.bigquery import LoadJobConfig
from google.cloud import storage
from decouple import config


# Create a logger for this module
logger = logging.getLogger(__name__)


GCP_CREDENTIALS_JSON = config("GCP_CREDENTIALS_JSON")
GCP_BIGQUERY_ADMIN_CREDENTIALS_JSON = config("GCP_BIGQUERY_ADMIN_CREDENTIALS_JSON")


# Function to create a table from a JSON file
def create_table_from_json(json_file, bigquery_client, dataset_id, bucket_name):
    """Creates a BigQuery table from a json file."""

    dataset_ref = bigquery_client.dataset(dataset_id)
    table_id = json_file.split('.')[0]  # Use the file name as the table name

    print(f"table_id = {table_id}")

    # Check if the table already exists, and delete it if it does
    table_ref = dataset_ref.table(table_id)
    try:
        bigquery_client.get_table(table_ref)
        bigquery_client.delete_table(table_ref)
    except NotFound:
        pass

    # Define the load job configuration with schema auto-detection
    job_config = LoadJobConfig(
        autodetect=True,
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
    )

    # Load data from Google Cloud Storage into BigQuery
    uri = f'gs://{bucket_name}/{json_file}'
    load_job = bigquery_client.load_table_from_uri(
        uri,
        table_ref,
        job_config=job_config,
    )

    load_job.result()  # Wait for the job to complete

    logger.info(f'Table {table_id} created successfully from {json_file}')

def create_bigquery_tables():
    """Create biquery tables from json files in a GCP bucket."""

    # Set your project and bucket information
    project_id = 'movies-data-platform'
    bucket_name = 'movies-bucket-11'
    dataset_id = 'tmdb_dataset'

    # Initialize the BigQuery client
    # client = bigquery.Client(project=project_id)
    storage_client = storage.Client.from_service_account_json(GCP_CREDENTIALS_JSON)
    bigquery_client = bigquery.Client.from_service_account_json(GCP_BIGQUERY_ADMIN_CREDENTIALS_JSON)

    # List JSON files in your Google Cloud Storage bucket
    blobs = storage_client.list_blobs(bucket_name)
    json_files = [blob.name for blob in blobs if blob.name.endswith('.json')]

    logger.info(f"json files = {json_files}")
    print(f"json files = {json_files}")

    # Create BigQuery tables for each JSON file
    for json_file in json_files:
        create_table_from_json(
            json_file=json_file,
            bigquery_client=bigquery_client, 
            dataset_id=dataset_id,
            bucket_name=bucket_name
        )

if __name__ == "__main__":
    create_bigquery_tables()