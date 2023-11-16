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

"""Constant project variables."""

import os

# Project ID and number
GCP_PROJECT_ID = os.environ.get("TF_VAR_PROJECT_ID")
GCP_PROJECT_NUMBER = os.environ.get("TF_VAR_PROJECT_NUMBER")

# Bigquery dataset name
GCP_DATASET_NAME = os.environ.get("TF_VAR_DATASET_NAME")

# Bucket name for data storage
GCP_DATA_STORAGE_BUCKET_NAME = os.environ.get("TF_VAR_DATA_STORAGE_BUCKET_NAME")
