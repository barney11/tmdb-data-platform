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

"""Transform bigquery tables into curated data tables."""

import logging
import os
from google.cloud import bigquery
from google.api_core.exceptions import NotFound
from decouple import config


# Create a logger for this module
logger = logging.getLogger(__name__)


GCP_BIGQUERY_ADMIN_CREDENTIALS_JSON = os.environ.get("GCP_BIGQUERY_ADMIN_CREDENTIALS_JSON")


AVG_VOTES_ORDERED_QUERY = f"""
    SELECT
        result.title AS movie_title,
        result.release_date AS release_date,
        CAST(result.vote_average AS FLOAT64) AS vote_average
    FROM
        `movies-data-platform.tmdb_dataset.now_playing_table`,
        UNNEST(results) AS result
    ORDER BY vote_average DESC
"""

AVG_VOTES_BY_GENRES = f"""
    WITH GenreData AS (
        SELECT
            g.name AS genre_name,
            ROUND(AVG(CAST(result.vote_average AS FLOAT64)), 2) AS average_vote
        FROM
            `movies-data-platform.tmdb_dataset.now_playing_table`,
            UNNEST(results) AS result,
            UNNEST(result.genre_ids) AS genre_id
        CROSS JOIN
            `movies-data-platform.tmdb_dataset.genres_table`,
            UNNEST(genres) AS g
        WHERE
            g.id = genre_id
        GROUP BY
            genre_name
    )
    SELECT
        genre_name,
        average_vote
    FROM
        GenreData
"""

MOVIE_COUNT_BY_RELEASE_MONTH_QUERY = f"""
    SELECT
        FORMAT_DATE('%b %Y', DATE(result.release_date)) AS release_month,
        COUNT(*) AS movie_count
    FROM
        `movies-data-platform.tmdb_dataset.now_playing_table`,
        UNNEST(results) AS result
    GROUP BY
        release_month
"""

def create_new_table_from_query(destination_dataset, destination_table, sql_query):
    """Create new table from a source table using a SQL query."""

    # Initialize a BigQuery client
    bigquery_client = bigquery.Client.from_service_account_json(GCP_BIGQUERY_ADMIN_CREDENTIALS_JSON)

    # Check if the table already exists, and delete it if it does
    dataset_ref = bigquery_client.dataset(destination_dataset)
    table_ref = dataset_ref.table(destination_table)
    try:
        bigquery_client.get_table(table_ref)
        bigquery_client.delete_table(table_ref)
    except NotFound:
        pass

    # Create a BigQuery job to run the SQL query and save the results to the new table
    job_config = bigquery.QueryJobConfig(destination=f'{"movies-data-platform"}.{destination_dataset}.{destination_table}')
    query_job = bigquery_client.query(sql_query, job_config=job_config)

    # Wait for the query job to complete
    query_job.result()

    logger.info(f'Table {destination_dataset}.{destination_table} created successfully.')


def create_curated_tables():
    """Create the movies curated bigquery tables."""

    # Define the source dataset
    source_dataset_name = 'tmdb_dataset'
    
    # Define the destination dataset
    destination_dataset_name = 'tmdb_dataset'

    # Define queries corresponding to each new curated table
    sql_queries = {
        "avg_votes_ordered" : AVG_VOTES_ORDERED_QUERY,
        "avg_votes_by_genres" : AVG_VOTES_BY_GENRES,
        "movie_count_by_release_month" : MOVIE_COUNT_BY_RELEASE_MONTH_QUERY
    }

    # Call the function to create the new tables from SQL queries
    for table_name, table_query in sql_queries.items():
        create_new_table_from_query(
            destination_dataset_name, table_name, table_query
        )

if __name__ == '__main__':
    create_curated_tables()
