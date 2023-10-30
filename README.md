# Serverless movies data platform
Movies data platform on Google Cloud Platform (GCP), using serverless services.

# Overview

This platform automatically extracts and processes movie-related data from The Movie Database (TMDb) API, with the following steps :

- Data <u>extraction</u> from TMDb API and storage in a __Cloud Storage__ bucket
- Data <u>migration</u> from the bucket to __BigQuery__ tables
- Data <u>transformation</u> in __BigQuery__ to extract specific information in new tables

These steps are deployed to GCP as __Cloud functions__. A workflow runs each cloud function sequentially, using the GCP __Workflows__ tool. A __Cloud Scheduler__ is used to trigger the workflow every day, at 9am.

Curated data rendering can be done easily with __Looker Studio__.

# Getting started

### Clone the project and install dependancies

TODO

### TMDb API key

&rarr; Create an account and generate an API key on _The Movie Database_ : https://www.themoviedb.org/

&rarr; Export your API key :

```
export TMDB_API_KEY=<your-api-key>
```

### GCP project

&rarr; Make sure you have a valid google account. The go to the Google Cloud Platform console and create a project called `movies-data-platform`

### Install dependancies



## Manage your TMDb API Key



---
_This project was developed by listening to the album "Looping", a collaboration between Rone and the Orchestre National de Lyon._
