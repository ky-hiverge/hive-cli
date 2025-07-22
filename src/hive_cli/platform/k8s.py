from calendar import c
from kubernetes.client.rest import ApiException
from kubernetes.client.api_client import ApiClient

from hive_cli.config import HiveConfig
from hive_cli.platform.base import Platform
from hive_cli.utils.logger import logger

GROUP = "core.hiverge.ai"
VERSION = "v1alpha1"
RESOURCE = "Experiment"
RESOURCE_PLURAL = "experiments"
# TODO: remove this once we support custom namespace
NAMESPACE = "default"


class K8sPlatform(Platform):
    def __init__(self, name: str):
        super().__init__(name)

    def create(self, config: HiveConfig):
        logger.info(f"Creating experiment '{self.experiment_name}' on Kubernetes...")

        config = self.setup_environment(config)
        deploy("CREATE", self.k8s_client, self.experiment_name, config)

        logger.info(f"Launch experiment '{self.experiment_name}' successfully on Kubernetes.")

    def update(self, name: str, config: HiveConfig):
        logger.info(f"Updating experiment '{name}' on Kubernetes...")

        deploy("UPDATE", self.k8s_client, name, config)

        logger.info(f"Launch experiment '{name}' successfully on Kubernetes.")


    def delete(self, name: str):
        logger.info(f"Deleting experiment '{name}' on Kubernetes...")
        try:
            # Attempt to delete the experiment by its name
            self.k8s_client.delete_namespaced_custom_object(
                group=GROUP,
                version=VERSION,
                namespace=NAMESPACE,
                plural=RESOURCE_PLURAL,
                name=name,
            )
            logger.info(f"Experiment '{name}' deleted successfully on Kubernetes.")
        except ApiException as e:
            logger.error(f"Failed to delete experiment '{name}' on Kubernetes: {e}")
        except Exception as e:
            logger.error(f"An unexpected error occurred while deleting experiment '{name}': {e}")

    def login(self, args):
        logger.info(f"Logging in to hive on {args.platform} platform...")

    def show_experiments(self, args):
        logger.info(f"Showing experiments on {args.platform} platform...")

def deploy(op: str, client: ApiClient, name: str, config: HiveConfig):
    logger.info(f"Applying experiment '{name}' on Kubernetes...")

    body = construct_experiment(name, NAMESPACE, config)

    try:
        if op == "CREATE":
            resp = client.create_namespaced_custom_object(
                group=GROUP, version=VERSION, namespace=NAMESPACE, plural=RESOURCE_PLURAL, body=body
            )
            logger.info(
                f"Experiment '{name}' created successfully on Kubernetes with name {resp['metadata']['name']}."
            )
        # TODO: add validation for op, only replicas can be updated
        elif op == "UPDATE":
            current_exp = client.get_namespaced_custom_object(
                group=GROUP, version=VERSION, namespace=NAMESPACE, plural=RESOURCE_PLURAL, name=name
            )

            # Populate some fields manually because they're generated in creation.
            if body["spec"]["evaluator"].get("image") is None:
                body["spec"]["evaluator"]["image"] = current_exp["spec"]["evaluator"]["image"]

            resp = client.patch_namespaced_custom_object(
                group=GROUP, version=VERSION, namespace=NAMESPACE, plural=RESOURCE_PLURAL, name=name, body=body
            )
            logger.info(
                f"Experiment '{name}' updated successfully on Kubernetes with name {resp['metadata']['name']}."
            )
        else:
            raise ValueError(f"Unsupported operation: {op}. Supported operations are 'CREATE' and 'UPDATE'.")
    except ApiException as e:
        logger.error(f"Failed to deploy experiment '{name}' on Kubernetes: {e}")
    except Exception as e:
        logger.error(
            f"An unexpected error occurred while deploying experiment '{name}': {e}"
        )

def construct_experiment(name: str, namespace: str, config: HiveConfig) -> dict:
    """
    Constructs a Kubernetes custom resource definition (CRD) for an experiment.

    Args:
        name (str): The name of the experiment.
        namespace (str): The Kubernetes namespace where the experiment will be deployed.

    Returns:
        dict: A dictionary representing the CRD for the experiment.
    """
    return {
        "apiVersion": f"{GROUP}/{VERSION}",
        "kind": RESOURCE,
        "metadata": {
            "name": name,
            "namespace": namespace,
        },
        "spec": {
            "evaluator": {
                "image": config.evaluator.image,
                "replicas": config.evaluator.replicas,
                "timeout": config.evaluator.timeout,
            },
            "coordinator": {
                "image": config.coordinator.image,
            },
        },
    }
