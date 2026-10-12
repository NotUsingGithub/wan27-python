# LangChain Wan27 tools

LangChain integration for [Wan27](https://wan2-7.io/) image and video generation. Uses the `wan27` Python SDK and `langchain-core`, without requiring the full LangChain package.

**MIT client; paid hosted service.** API access requires an active paid Wan27 subscription and generation consumes credits. This package does not provide free model inference.

PyPI publication is pending. For local development, install the root `wan27` project first, then this package.

```python
import os
from wan27 import Wan27
from langchain_wan27 import create_wan27_tools

client = Wan27(os.environ["WAN27_ACCESS_TOKEN"])
tools = create_wan27_tools(client)
models_tool = next(t for t in tools if t.name == "wan27_list_models")
print(models_tool.invoke({}))
```

The default tool set includes account status, model listing, model schema, credit estimation, task listing and task status. Tokens are kept in the client object and are not tool arguments exposed to the model.

To add the `wan27_generate_media` tool, pass `allow_generation=True`. **This flag does not implement spending approval.** Your application must enforce the user's approved budget or a human approval step before invoking generation. Persist `request_id` and the input before submission. Retry ambiguous submissions only with the same ID; never generate a new ID simply because a network call timed out.

The tools return the service's JSON object. Errors propagate as `Wan27Error`. A task is only complete when it is `succeeded`; return actual outputs, not fabricated URLs. Bound polling and report pending task IDs after timeout.

## Testing

Install the root package and this adapter in an isolated environment, then run `python -m unittest discover -s tests -v` in this directory. Tests use a mocked client, validate tool schemas and invocation, and never generate paid media.

[Website](https://wan2-7.io/) · [Workflow guide](https://wan2-7.io/mcp/guide/) · [MCP setup](https://wan2-7.io/mcp/) · [Source](https://github.com/NotUsingGithub/wan27-python)
