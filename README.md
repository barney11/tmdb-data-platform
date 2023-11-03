# Serverless movies data platform
Movies data platform on Google Cloud Platform (GCP), using serverless services.

# Overview

This platform automatically extracts and processes movie-related data from The Movie Database (TMDb) API, with the following steps :

- Data <u>extraction</u> from TMDb API and storage in a __Cloud Storage__ bucket
- Data <u>migration</u> from the bucket to __BigQuery__ tables
- Data <u>transformation</u> in __BigQuery__ to extract specific information in new tables

These steps are deployed to GCP as __Cloud functions__. A workflow runs each cloud function sequentially, using the GCP __Workflows__ tool. A __Cloud Scheduler__ is used to trigger the workflow every day, at 9am.

Curated data rendering can be done with __Looker Studio__. The following looker studio report is updated when new curated data is available: https://lookerstudio.google.com/reporting/734e22f6-09ae-4210-a47d-40d88755ebb2

# Getting started

This sections explains how to reproduce the data platform with your own Google account. It is made for Linux.

### Clone the project and install dependancies

Clone the github repository:

```
git clone https://github.com/barney11/tmdb-data-platform.git
```

Build a Python virtual environment and activate it:

```
sudo apt install python3.8 python3.8-dev
python3 -m venv platform_venv
platform_venv/bin/activate
```

Move into the repository:

```
cd tmdb-data-platform
```

Install the dependancies:

```
pip install -e .
```

__Optional__ : If you plan to make a fork of this project and keep maximum code quality level, install the dev dependancies and activate pre-commit :

```
pip install -e .[dev]
pre-commit install
```

### Generate a TMDb API key

Create an account and generate an API key on _The Movie Database_ : https://www.themoviedb.org/

Export your API key :

```
export TF_VAR_TMDB_API_KEY=<your-api-key>
```

### Build a GCP project

Make sure you have a valid google account. The go to the Google Cloud Platform console and create a new project. Export the project id and the project number:

```
export TF_VAR_PROJECT_ID=<your-project-id>
export TF_VAR_PROJECT_NUMBER=<your-project-number>
```

Create a service account on GCP with the following roles :

- Storage objects admin
- Bigquery admin
- Cloud functions admin
- Workflows admin
- Cloud scheduler admin
- Secret manager admin
- Service account user

Build the JSON key file that corresponds to this account. Export the path to this file:

```
export TF_VAR_GCP_CREDENTIALS=$(realpath <path/to/your/json/key/file>)
```

### Install Terraform

```
curl -LO https://releases.hashicorp.com/terraform/1.6.2/terraform_1.6.2_linux_amd64.zip
unzip terraform_1.6.2_linux_amd64.zip
sudo mv terraform /usr/local/bin/
```

### Additional environment variables

Choose names for:

- The bigquery dataset
- The data storage bucket
- The cloud functions storage bucket
- The terraform states storage bucket

Export those names:

```
export TF_VAR_DATASET_NAME="<your-dataset-name>"
export TF_VAR_DATA_STORAGE_BUCKET_NAME="<your-data-storage-bucket-name>"
export TF_VAR_CF_BUCKET_NAME="<your-cloud-functions-bucket-name>"
export TF_VAR_TF_STATES_BUCKET_NAME="<your-terraform-states-bucket-name>"
```

### Use terraform to deploy the data platform

Move to the terraform directory:

```
cd platform/terraform
```

Init terraform:

```
terraform init
```

Build terraform plan:

```
terraform plan \
    -out=tfplan \
    -var tmdb_api_key=$TF_VAR_TMDB_API_KEY \
    -var gcp_credentials_json=$TF_VAR_GCP_CREDENTIALS \
    -var project_id=$TF_VAR_PROJECT_ID \
    -var project_number=$TF_VAR_PROJECT_NUMBER \
    -var dataset_name=$TF_VAR_DATASET_NAME \
    -var data_storage_bucket_name=$TF_VAR_DATA_STORAGE_BUCKET_NAME \
    -var terraform_states_bucket_name=$TF_VAR_TF_STATES_BUCKET_NAME \
    -var cloud_functions_bucket_name=$TF_VAR_CF_BUCKET_NAME
```

Deploy:

```
terraform apply "tfplan"
```

### Build dashboard with Looker Studio

You can easily build a Looker Studio report with charts from the curated bigquery tables.

---
_This project was developed by listening to the album "Looping", a collaboration between Rone and the Orchestre National de Lyon._
