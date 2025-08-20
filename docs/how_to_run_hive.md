# How to Run Hive

This document provides instructions on how to run experiments on Hive cloud with Hive CLI.

## Prerequisites

Before you begin, ensure you have the following:

- Run `brew install gcloud`


## Connect to Hive Cloud

- Run `gcloud container clusters get-credentials hive --region us-central1 --project quantinuum-469520`
- The Google Cloud SDK installed and configured.
- A Hive-compatible metastore (e.g., Google Cloud Bigtable, Google Cloud Spanner).