from typing import Any

from config.browser import BrowserConfig
from config.detail import DetailConfig
from config.discovery.base import DiscoveryConfig
from config.list import ListConfig
from config.output import OutputConfig
from config.pipeline import PipelineConfig
from config.workflow import WorkflowConfig
from pydantic import BaseModel, Field

class SpiderConfig(BaseModel):

    name: str

    browser: BrowserConfig = Field(default_factory=BrowserConfig)

    list: ListConfig = Field(default_factory=ListConfig)

    detail: DetailConfig = Field(default_factory=DetailConfig)

    discovery: DiscoveryConfig = Field(default_factory=DiscoveryConfig)

    pipeline: PipelineConfig = Field(default_factory=PipelineConfig)

    workflow: WorkflowConfig = Field(default_factory=WorkflowConfig)

    output: OutputConfig = Field(default_factory=OutputConfig)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SpiderConfig":
        return cls.model_validate(data)