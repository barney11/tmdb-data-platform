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

import os
import json
import requests
import logging

from google.cloud import storage
from google.cloud import secretmanager
from decouple import config

from . import constants


# Set a logger for this module
logger = logging.getLogger(__name__)


def request_tmdb_api(request_url: str) -> dict:
    """Fetch data from TMDb API."""

    # GCP_PROJECT_NUMBER = os.environ["TF_VAR_PROJECT_NUMBER"]
    
    # Get API key from the secret manager
    secret_name = f"projects/{constants.GCP_PROJECT_NUMBER}/secrets/TMDB_API_KEY/versions/latest"
    client = secretmanager.SecretManagerServiceClient()
    response = client.access_secret_version(name=secret_name)
    TMDB_API_KEY = response.payload.data.decode("UTF-8")

    # HTTP GET request
    response = requests.get(f"{request_url}?api_key={TMDB_API_KEY}")
    
    if response.status_code == 200:
        return response.json()
    
    else:
        logger.critical(f"Error fetching data from TMDb: {response.status_code}")
        logger.critical(response.reason)
        return response.json()


def upload_json_data_to_gcp(name: str, data: dict):
    """Upload data to GCP bucket."""

    # GCP_BUCKET_NAME = "movies-bucket-11"
    # GCP_BUCKET_NAME = os.environ["TF_VAR_DATA_STORAGE_BUCKET_NAME"]

    secret_name = f"projects/{constants.GCP_PROJECT_NUMBER}/secrets/GCP_CREDENTIALS_JSON/versions/latest"
    client = secretmanager.SecretManagerServiceClient()
    response = client.access_secret_version(name=secret_name)
    payload = response.payload.data.decode("UTF-8")
    GCP_CREDENTIALS_JSON = json.loads(payload)
    # GCP_CREDENTIALS_JSON = os.environ.get("GCP_CREDENTIALS_JSON")
    
    client = storage.Client.from_service_account_info(GCP_CREDENTIALS_JSON)
    bucket = client.get_bucket(constants.GCP_DATA_STORAGE_BUCKET_NAME)
    
    # File name in the bucket
    blob = bucket.blob(f"{name}.json")

    # Convert data to JSON format and upload it to the bucket
    blob.upload_from_string(json.dumps(data))


def extract_tmdb_data():
    """Extract TMDb movies lists and load it to GCP bucket."""

    movie_requests = {
        "now_playing" : "https://api.themoviedb.org/3/movie/now_playing",
        "popular" : "https://api.themoviedb.org/3/movie/popular",
        "top_rated" : "https://api.themoviedb.org/3/movie/top_rated",
        "upcoming" : "https://api.themoviedb.org/3/movie/upcoming",
        "genres" : "https://api.themoviedb.org/3/genre/movie/list"
    }

    for request_key, request_url in movie_requests.items():
        # TMDb API JSON response
        response = request_tmdb_api(request_url)

        # Upload extracted data to GCP bucket
        if response is not None:
            upload_json_data_to_gcp(request_key, response)
            logger.info(f"TMDb {request_key} data downloaded and successfully stored in the GCP bucket.")

        else:
            logger.info(f"Failed to extract TMDb {request_key} data.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    extract_tmdb_data()