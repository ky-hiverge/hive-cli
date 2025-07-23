# Hive-CLI

Hive-CLI is a command-line interface for managing and deploying Hive agent and experiments on Kubernetes and other platforms.

```bash
     ███          █████   █████  ███
    ░░░███       ░░███   ░░███  ░░░
      ░░░███      ░███    ░███  ████  █████ █████  ██████
        ░░░███    ░███████████ ░░███ ░░███ ░░███  ███░░███
         ███░     ░███░░░░░███  ░███  ░███  ░███ ░███████
       ███░       ░███    ░███  ░███  ░░███ ███  ░███░░░
     ███░         █████   █████ █████  ░░█████   ░░██████
    ░░░          ░░░░░   ░░░░░ ░░░░░    ░░░░░     ░░░░░░
```

## Installation

### Install via pip (TBD)

```bash
pip install hive-cli
```

### Install from source

```bash
source start.sh
```

## How to Run

### Pre-requisites

- kubectl installed
- kubeconfig file (~/.kube/config) to communicate with your cluster
- For GCP users:
  - Ensure you have `gcloud` installed and logged in to your GCP account,
    because Hive CLI will build and push Docker images to GCP Container Registry.
  - Create a Kubernetes Secret `hive-image-puller` with image pull credentials, basically you should create a service account [here](https://console.cloud.google.com/iam-admin/serviceaccounts), and then download the JSON key file, you may be asked to disable the `Disable service account creation` and `Disable service account key creation` policies. Finally, use the following command to create the secret:

    ```bash
    kubectl create secret docker-registry hive-image-puller \
      --docker-server=gcr.io \
      --docker-username=_json_key \
      --docker-password="$(cat <your-credential-jsonfile>)" \
      --docker-email=<your-email-address>
    ```

## Usage

Support commands:
```
create              Create resources
update              Update resources
delete              Delete resources
```

See `hive -h` for more details.
