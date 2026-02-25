import json
from pathlib import Path

_config_path = Path(__file__).parent / "config.json"

with open(_config_path) as f:
    GUARDRAILS_CONFIG = json.load(f)

__all__ = ["GUARDRAILS_CONFIG"]
