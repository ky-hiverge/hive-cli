from enum import Enum
from typing import Optional

from pydantic import BaseModel, field_validator

import yaml
from pydantic import BaseModel


class PlatformType(str, Enum):
    K8S = "k8s"
    ON_PREM = "on-prem"


class ResourceConfig(BaseModel):
    requests: Optional[dict] = {"cpu": "100m", "memory": "256Mi"}
    limits: Optional[dict] = {"cpu": "500m", "memory": "512Mi"}


class SandboxConfig(BaseModel):
    image: Optional[str] = None
    replicas: int = 1
    timeout: int = 60
    resources: ResourceConfig = ResourceConfig()


class RepoConfig(BaseModel):
    url: str
    branch: str = "main"


class WanDBConfig(BaseModel):
    enabled: bool = False


class GCPConfig(BaseModel):
    enabled: bool = False
    project_id: str


class HiveConfig(BaseModel):
    project_name: (
        str  # project_name is for a specific project, like the beluga-direct-plan-project.
    )

    platform: PlatformType = PlatformType.K8S

    repo: RepoConfig
    sandbox: SandboxConfig
    wandb: WanDBConfig

    # cloud vendor configuration
    gcp: Optional[GCPConfig] = None

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
