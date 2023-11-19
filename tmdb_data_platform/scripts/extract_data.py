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


"""Data extraction script that takes data from TMDb API and stores data in a GCP Storage bucket."""


# pylint: disable=logging-fstring-interpolation
import json
import logging

import requests
from google.cloud import secretmanager, storage

from . import constants

# Set a logger for this module
logger = logging.getLogger(__name__)


def request_tmdb_api(request_url: str) -> dict:
    """Fetch data from TMDb API."""

    # Get API key from the secret manager
    secret_name = f"projects/{constants.GCP_PROJECT_NUMBER}/secrets/TMDB_API_KEY/versions/latest"
    client = secretmanager.SecretManagerServiceClient()
    response = client.access_secret_version(name=secret_name)
    tmdb_api_key = response.payload.data.decode("UTF-8")

    # HTTP GET request
    response = requests.get(f"{request_url}?api_key={tmdb_api_key}", timeout=30)

    if response.status_code == 200:
        return response.json()

    logger.critical(f"Error fetching data from TMDb: {response.status_code}")
    logger.critical(response.reason)
    return response.json()


def request_all_pages_tmdb_api(request_url: str) -> dict:
    """Fetch data from TMDb API after merging all pages."""

    # Get API key from the secret manager
    secret_name = f"projects/{constants.GCP_PROJECT_NUMBER}/secrets/TMDB_API_KEY/versions/latest"
    client = secretmanager.SecretManagerServiceClient()
    response = client.access_secret_version(name=secret_name)
    tmdb_api_key = response.payload.data.decode("UTF-8")

    # Extract first page of data
    json_response = request_tmdb_api(request_url)

    # Extract total numer of pages
    total_pages = json_response["total_pages"]

    if total_pages > 1:
        # Expend results list in the json file with next pages
        for page_index in range(2, total_pages + 1):
            next_response = requests.get(f"{request_url}?api_key={tmdb_api_key}&page={page_index}", timeout=30)
            next_json_response = next_response.json()

            json_response["results"] += next_json_response["results"]

    return json_response


def upload_json_data_to_gcp(name: str, data: dict):
    """Upload data to GCP bucket."""

    secret_name = f"projects/{constants.GCP_PROJECT_NUMBER}/secrets/GCP_CREDENTIALS_JSON/versions/latest"
    client = secretmanager.SecretManagerServiceClient()
    response = client.access_secret_version(name=secret_name)
    payload = response.payload.data.decode("UTF-8")
    gcp_credentials_json = json.loads(payload)

    client = storage.Client.from_service_account_info(gcp_credentials_json)
    bucket = client.get_bucket(constants.GCP_DATA_STORAGE_BUCKET_NAME)

    # File name in the bucket
    blob = bucket.blob(f"{name}.json")

    # Convert data to JSON format and upload it to the bucket
    blob.upload_from_string(json.dumps(data))


def extract_tmdb_data():
    """Extract TMDb movies lists and load it to GCP bucket."""

    movie_requests = {
        "now_playing": "https://api.themoviedb.org/3/movie/now_playing",
        "popular": "https://api.themoviedb.org/3/movie/popular",
        "top_rated": "https://api.themoviedb.org/3/movie/top_rated",
        "upcoming": "https://api.themoviedb.org/3/movie/upcoming",
        "genres": "https://api.themoviedb.org/3/genre/movie/list",
    }

    for request_key, request_url in movie_requests.items():
        # TMDb API JSON response
        if request_key == "now_playing":
            response = request_all_pages_tmdb_api(request_url)
        else:
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
