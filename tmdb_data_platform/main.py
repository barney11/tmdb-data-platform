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

"""Cloud functions file."""


from requests import request

from scripts.extract_data import extract_tmdb_data
from scripts.migrate_data import create_bigquery_tables
from scripts.transform_data import create_curated_tables


def extract_data_function(request):
    """Data extraction cloud function"""

    extract_tmdb_data()

    return "Data extraction : Done."


def migrate_data_function(request):
    """Data migration cloud function"""

    create_bigquery_tables()

    return "Data migration : Done."


def transform_data_function(request):
    """Data transformation cloud function"""

    create_curated_tables()

    return "Data transformation : Done."
