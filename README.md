# TMDb data platform
Simple movies data platform on GCP

# Overview

This platform extracts and process movi-related data from The Movie Database (TMDb) API, with the following steps :

- Data extraction from TMDb API and storage in a google cloud storage bucket
- Data migration from the bucket to BigQuery tables
- Data transformation in BigQuery to extract specific information
- Render these informations in Looker with charts

These steps are scheduled with an Airflow DAG, using google cloud composer.

# Getting started

## Install dependancies

## Manage your API Keys

---
_This project was developed by listening to the album "Looping", a collaboration between Rone and the Orchestre National de Lyon._
