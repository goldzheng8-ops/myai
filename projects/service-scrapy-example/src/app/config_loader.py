from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml


def load_yaml_config(path: str | Path) -> dict[str, Any]:
    with open(path, "r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    return data


def load_yaml_config_from_request(payload: dict[str, Any]) -> dict[str, Any]:
    if payload.get("config_file"):
        config_path = Path(payload["config_file"])
        return load_yaml_config(config_path)

    if payload.get("config_yaml"):
        return yaml.safe_load(payload["config_yaml"]) or {}

    return {}
