from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml


def load_yaml_config(path: str | Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    return data


if __name__ == "__main__":
    config = load_yaml_config(Path(__file__).with_name("crawl_config.yaml"))
    print(json.dumps(config, ensure_ascii=False, indent=2))
