# Wan27 Python client

A dependency-free Python 3.10+ client for [Wan27](https://wan2-7.io/) AI image and video generation. Read your account, discover models and input schemas, estimate credit costs, create tasks with retained request IDs, and retrieve actual outputs.

The client is MIT licensed. **The hosted API requires an active paid Wan27 subscription; generation spends credits.** Credit packs alone do not enable API access. This is a service client, not a distribution of Alibaba model weights.

## Usage

PyPI publication is pending. Install from the checked-out source with `pip install .` until the registry release is available.

```python
import os
from uuid import uuid4
from wan27 import Wan27

client = Wan27(os.environ["WAN27_ACCESS_TOKEN"])
print(client.account())
print(client.model("wan2.7-image"))
request = {"modelId": "wan2.7-image", "prompt": "A paper crane on a desk", "resolution": "2K"}
print(client.estimate(request))

# Only after the estimated credit spend has been authorized:
request_id = str(uuid4())  # persist this ID and input before submitting
created = client.generate(request, request_id=request_id)
task_id = created["task"]["id"]
print(client.task(task_id))
```

Use an existing access token in your server environment. The SDK does not read or export the CLI credential vault. Use the [CLI](https://wan2-7.io/cli/) for interactive browser authentication and image uploads. Do not paste tokens into chats or commit them to source control.

Responses preserve the service's JSON object. Read each model's current schema; do not assume unsupported options or fixed credit prices. `Wan27Error` exposes `code` and HTTP `status`.

There is no automatic generation retry. On an ambiguous network error, inspect `tasks()` and reuse the original `request_id` and input. Poll `task()` with a bounded wait. Pending tasks are not finished results; a polling timeout does not cancel them. A new generation after a failed task is a new spend.

All requests use the official HTTPS origin, reject redirects, and enforce request/response size limits. The default network timeout is 120 seconds. No token is saved by this package.

## Development

```sh
PYTHONPATH=src python -m unittest discover -s tests -v
python -m build
```

Tests use offline fixtures and do not perform paid generations. Live authenticated generation is not included in this test suite.

[Website](https://wan2-7.io/) · [API workflow guide](https://wan2-7.io/mcp/guide/) · [MCP setup](https://wan2-7.io/mcp/) · [Pricing](https://wan2-7.io/pricing/) · [Source](https://github.com/NotUsingGithub/wan27-python)
