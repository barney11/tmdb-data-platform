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

"""Airflow DAG for data patform tasks scheduling."""

from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator

from platform.scripts.extract_data import extract_tmdb_data
from platform.scripts.migrate_data import create_bigquery_tables
from platform.scripts.transform_data import create_curated_movies_tables


# Define the default arguments for the DAG
default_args = {
    'owner': 'your_name',
    'depends_on_past': False,
    'start_date': days_ago(1),  # Adjust the start date as needed
    'retries': 1,
}

# Create a DAG instance
with DAG(
    'data_extraction_dag',
    default_args=default_args,
    schedule_interval='@daily',  # Adjust the schedule as needed
    catchup=False,
    tags=['data-extraction'],
) as dag:

    # Task to extract data from TMDb API to google cloud storage bucket
    data_extraction_task = PythonOperator(
        task_id='data_extraction_task',
        python_callable=extract_tmdb_data,
        provide_context=True,
    )

    # Task to migrate bucket data into bigquery tables
    data_migration_task = PythonOperator(
        task_id='data_migration_task',
        python_callable=create_bigquery_tables,
        provide_context=True,
    )

    data_curating_task = PythonOperator(
        task_id='data_transformation_task',
        python_callable=create_curated_tables,
        provide_context=True,
    )

    data_extraction_task >> data_migration_task >> data_curating_task

if __name__ == '__main__':
    dag.cli()
    