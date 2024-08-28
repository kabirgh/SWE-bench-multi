## Setup

Create a `.env` file with your GitHub token.

1. Install [uv](https://docs.astral.sh/uv)
2. `uv venv`
3. `source .venv/bin/activate`
4. `uv pip install -e .` // maybe unnecessary?
5. `pip install -e .`
6. `python swebench/collect/get_tasks_pipeline.py --repos caddyserver/caddy --path_prs caddy/prs --path_tasks caddy/tasks --max_pulls 10 --fast`

### Improvements
Uses graphql api to get issue linked to pull - less brittle than parsing pull body to find issue numbers.
E.g. [this issue](https://github.com/caddyserver/caddy/pull/6362) is not found by `extract_resolved_issues` and so pull is filtered out.
