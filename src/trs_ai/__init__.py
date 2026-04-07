"""TRS-AI appliance: AI program generation backends for AILOAD."""

from src.trs_ai.backends import (
    FixtureBackend,
    RemoteChatBackend,
    load_backend_from_env,
)
from src.trs_ai.types import GenerationResult

__all__ = [
    "GenerationResult",
    "FixtureBackend",
    "RemoteChatBackend",
    "load_backend_from_env",
]
