"""LangChain tools for the Wan27 hosted image/video service."""

from typing import Any
from langchain_core.tools import StructuredTool
from wan27 import Wan27

__all__ = ["create_wan27_tools"]


def create_wan27_tools(client: Wan27, *, allow_generation: bool = False) -> list[StructuredTool]:
    """Create six read/estimate tools, optionally adding one paid generation tool.

    Enabling generation is an application configuration decision, not proof of
    user spending approval. Applications must enforce the approved credit budget
    or a human-in-the-loop confirmation before invoking that tool.
    """

    def account_status() -> dict[str, Any]:
        """Read Wan27 subscription eligibility and credit balance."""
        return client.account()

    def list_models() -> dict[str, Any]:
        """Discover currently supported Wan27 models."""
        return client.models()

    def get_model(model_id: str) -> dict[str, Any]:
        """Read a Wan27 model's input schema before building an input object."""
        return client.model(model_id)

    def estimate_generation(input: dict[str, Any]) -> dict[str, Any]:
        """Estimate the credits needed by a Wan27 generation without creating it."""
        return client.estimate(input)

    def list_tasks(limit: int = 20, cursor: str | None = None) -> dict[str, Any]:
        """Read up to 50 Wan27 tasks; use this to investigate ambiguous requests."""
        return client.tasks(limit=limit, cursor=cursor)

    def get_task(task_id: str) -> dict[str, Any]:
        """Read a Wan27 task's current status and actual output URLs."""
        return client.task(task_id)

    def generate_media(input: dict[str, Any], request_id: str) -> dict[str, Any]:
        """Create an authorized PAID Wan27 image/video task. Estimate first and enforce the user's spending approval. Persist a unique 16–128 character request_id before submission; reuse the same ID/input on an ambiguous retry. No automatic retry or polling."""
        return client.generate(input, request_id=request_id)

    functions = [account_status, list_models, get_model, estimate_generation, list_tasks, get_task]
    if allow_generation:
        functions.append(generate_media)
    return [StructuredTool.from_function(function, name="wan27_" + function.__name__) for function in functions]
