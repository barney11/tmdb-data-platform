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
from decouple import config


# Define TMDb API information
TMDB_API_KEY = config("TMDB_API_KEY") #"d274a3c0c4dffc5f520a2356280b8198"
TMDB_BASE_URL = "https://api.themoviedb.org/3"

# Define GCP bucket information
GCP_BUCKET_NAME = "movies-bucket-11"
GCP_CREDENTIALS_JSON = config("GCP_CREDENTIALS_JSON")

# Set a logger for this module
logger = logging.getLogger(__name__)


def request_tmdb_api(request_url: str) -> dict:
    """Fetch data from TMDb API."""

    # HTTP GET request
    response = requests.get(f"{request_url}?api_key=" + TMDB_API_KEY)
    
    if response.status_code == 200:
        return response.json()
    
    else:
        logger.critical(f"Error fetching data from TMDb: {response.status_code}")
        return None


def upload_json_data_to_gcp(name: str, data: dict):
    """Upload data to GCP bucket."""
    
    client = storage.Client.from_service_account_json(GCP_CREDENTIALS_JSON)
    bucket = client.get_bucket(GCP_BUCKET_NAME)
    
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
        upload_json_data_to_gcp(request_key, response)
        logger.info(f"TMDb {request_key} data downloaded and successfully stored in the GCP bucket.")


if __name__ == "__main__":
    extract_tmdb_data()