variable "tmdb_api_key" {
    type        = string
    description = "TMDb API key."
}

variable "gcp_credentials_json" {
    type        = string
    description = "GCP credentials"
}

variable "project_id" {
    type        = string
    description = "Project ID"
}

variable "project_number" {
    type        = number
    description = "Project number"
}

variable "region" {
    type        = string
    description = "Region"
    default     = "us-central1"
}

variable "dataset_name" {
    type        = string
    description = "Dataset name"
}

variable "archive_name" {
    type        = string
    description = "Cloud functions code archive"
    default     = "source"
}

variable "data_storage_bucket_name" {
  type          = string
  description   = "Data storage bucket name"
}

variable "terraform_states_bucket_name" {
  type          = string
  description   = "Terraform states bucket name"
}

variable "cloud_functions_bucket_name" {
    type        = string
    description = "Cloud functions bucket name"
}

variable "cloud_functions_bucket_location" {
    type        = string
    description = "Cloud functions bucket location"
    default     = "US"
}

variable "bucket_storage_class" {
  type        = string
  description = "The bucket storage class where the cloud function code will be stored"
  default     = "STANDARD"
}

variable "bucket_versioning" {
  description = "Enable the versioning on the bucket where the cloud function code will be stored"
  type        = bool
  default     = true
}

variable "excludes" {
  description = "Files to exclude from the cloud function src directory"
  type        = list(string)
  default     = [
    "keys",
    "looker",
    "dags",
    "__pycache__"
  ]
}