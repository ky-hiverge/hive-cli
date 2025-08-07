from enum import Enum
from typing import Optional

import yaml
from pydantic import BaseModel, field_validator


class PlatformType(str, Enum):
    K8S = "k8s"
    ON_PREM = "on-prem"


class ResourceConfig(BaseModel):
    requests: Optional[dict] = {"cpu": "100m", "memory": "256Mi"}
    limits: Optional[dict] = {"cpu": "500m", "memory": "512Mi"}
    accelerators: Optional[str] = None  # e.g., "a100-80gb:8"
    shmsize: Optional[str] = None


class SandboxConfig(BaseModel):
    image: Optional[str] = None
    replicas: int = 1
    timeout: int = 60
    resources: ResourceConfig = ResourceConfig()

class RepoConfig(BaseModel):
    url: str
    branch: str = "main"
    evaluation_script: str = "evaluator.py"
    evolve_files_and_ranges: str

class WanDBConfig(BaseModel):
    enabled: bool = False


class GCPConfig(BaseModel):
    enabled: bool = False
    project_id: str


class DashboardConfig(BaseModel):
    enabled: bool = False

class CloudProviderConfig(BaseModel):
    spot: bool = False
    gcp: Optional[GCPConfig] = None

class HiveConfig(BaseModel):
    project_name: (
        str  # project_name is for a specific project, like the beluga-direct-plan-project.
    )

    coordinator_config_name: str = "default-coordinator-config"
    dashboard: DashboardConfig

    platform: PlatformType = PlatformType.K8S

    repo: RepoConfig
    sandbox: SandboxConfig
    wandb: WanDBConfig

    # cloud vendor configuration
    cloud_provider: CloudProviderConfig

    @field_validator("project_name")
    def must_be_lowercase(cls, v):
        if not v.islower():
            raise ValueError("project_name must be all lowercase")
        return v


def load_config(file_path: str) -> HiveConfig:
    """Load configuration from a YAML file."""
    with open(file_path, "r") as file:
        config_data = yaml.safe_load(file)
    return HiveConfig(**config_data)
