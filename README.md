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
- For GCP users, ensure you have `gcloud` installed and logged in to your GCP account.

Support commands:
```
create              Create resources
update              Update resources
delete              Delete resources
```

See `hive -h` for more details.
