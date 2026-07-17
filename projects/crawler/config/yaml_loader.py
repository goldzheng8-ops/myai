# config/yaml_loader.py

from pathlib import Path

import yaml

from config.loader import ConfigLoader
from config.config import CrawlerConfig


class YamlConfigLoader(ConfigLoader):

    def __init__(self, directory: str | Path):
        self.directory = Path(directory)

    def load(self):

        for file in self.directory.glob("*.yaml"):

            with file.open(
                "r",
                encoding="utf-8"
            ) as f:

                data = yaml.safe_load(f)

            yield CrawlerConfig.model_validate(data)