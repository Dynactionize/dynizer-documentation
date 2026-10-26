# Backend Overview

This backend provides an MCP server that exposes Dynizer API endpoints and knowledge documents as MCP tools.

## Components

- **Spec Loader (`spec_loader.py`)**: Parses Markdown API specs into MCP tool metadata and an endpoint map.
- **Knowledge Loader (`knowledge_loader.py`)**: Loads Markdown files from `knowledge/` and exposes them as `knowledge_`-prefixed tools.
- **MCP Server (`mcp_server.py`)**: Exposes all tools via MCP (stdio or FastMCP transport).
- **HTTP Server (`server.py`)**: Optional FastAPI wrapper for HTTP access.

## How It Fits Together

1. On startup the server syncs knowledge files from GitHub (if configured) and loads all API specs and knowledge documents.
2. Each spec endpoint becomes an MCP tool that returns documentation describing how to call that endpoint (method, URL, parameters, curl example).
3. Each knowledge markdown file becomes one or more `knowledge_*` tools (see [Knowledge Tools](#knowledge-tools) below).
4. Discovery tools (`list_apis`, `list_endpoints`, `describe_endpoint`) let clients browse APIs without knowing tool names upfront.
5. `search_knowledge` provides server-side keyword search across all docs when the client doesn't know where to look.

## Setup

Install dependencies (from repo root):

```bash
python -m pip install -r requirements.txt
```

## Configuration

Optional environment variables (or `.env`):

```bash
export DYNIZER_SPEC_PATH="knowledge/dynizer_swagger.openapi.md"
export MCP_SERVER_IMPL="stdio"   # or "fastmcp"
export MCP_TRANSPORT="stdio"     # or "sse"
export MCP_HOST="0.0.0.0"       # SSE bind address
export MCP_PORT="8000"           # SSE port

# GitHub-based knowledge sync
export DYNIZER_KNOWLEDGE_GITHUB_REPO="owner/repo"
export DYNIZER_KNOWLEDGE_GITHUB_PATH="docs/knowledge"
export DYNIZER_KNOWLEDGE_GITHUB_BRANCH="main"
export DYNIZER_KNOWLEDGE_GITHUB_TOKEN=""              # optional, for private repos
export DYNIZER_KNOWLEDGE_GITHUB_CACHE_TTL="300"       # re-sync interval in seconds

# Section splitting threshold (chars) — docs larger than this are split into TOC + section tools
export DYNIZER_KNOWLEDGE_SPLIT_THRESHOLD="3000"
```

## Running

### Stdio transport (default — for CLI / local use)

```bash
# Low-level stdio server
python -m backend.mcp_server

# FastMCP stdio server
python -m backend.mcp_server --impl fastmcp
```

### SSE transport (for remote / Docker deployments)

```bash
python -m backend.mcp_server --impl fastmcp --transport sse --host 0.0.0.0 --port 8000
```

This starts an SSE endpoint at `http://<host>:<port>/sse` that MCP clients can connect to remotely.

### Docker

```bash
docker build -t dynizer-mcp .
docker run -p 8000:8000 dynizer-mcp
```

The Docker image runs SSE transport by default on port 8000.

### Connecting from Claude Code

For a **local** (stdio) server, add to `.mcp.json`:

```json
{
  "mcpServers": {
    "dynizer-mcp": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "dynizer-mcp",
        "python", "-m", "backend.mcp_server"
      ]
    }
  }
}
```

For a **remote** (SSE) server, add to `.mcp.json`:

```json
{
  "mcpServers": {
    "dynizer-mcp": {
      "type": "sse",
      "url": "https://mcp.dynizer.com/sse"
    }
  }
}
```

### Connecting from Claude Desktop

Claude Desktop requires stdio transport. Use `mcp-remote` (requires Node.js) to bridge to the remote SSE server.

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "dynizer-mcp": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://mcp.dynizer.com/sse"]
    }
  }
}
```

## Key Functions

- `list_tools(spec_path=None)` — returns all available tools (API + knowledge + utility) as dicts.
- `describe_tool(tool_name, spec_path=None)` — returns structured documentation for an API tool, or content for a knowledge tool.

## Utility / Discovery Tools

| Tool | Parameters | Description |
| ---- | ---------- | ----------- |
| `list_apis` | — | List all API specs with titles, summaries, and endpoint counts |
| `list_endpoints` | `api` | List all endpoints (method, path, description) for a specific API |
| `describe_endpoint` | `api`, `method`, `path` | Full docs for one endpoint (params, schemas, curl example) |
| `search_knowledge` | `query` | Keyword search across all knowledge docs and API specs. Returns matching sections with context, ranked by heading relevance |
| `refresh_knowledge` | — | Force re-sync from GitHub and reload all knowledge |

## Tool Name Rules

Tool names must match `^[a-zA-Z0-9_-]{1,64}$` (required by Claude Desktop). Names are auto-sanitised by the spec loader and knowledge loader.

## Error Format

```json
{
  "error": {
    "message": "Unknown tool: foo",
    "type": "tool_not_found"
  }
}
```

## Updating Knowledge Docs

When API endpoints or documentation change, update the markdown files in `knowledge/` and push to GitHub. You do **not** need to restart the server — just call the `refresh_knowledge` MCP tool from any connected client. It will pull the latest files from GitHub and reload the in-memory cache immediately.

**From Claude Code CLI:** Simply ask Claude to refresh the knowledge, e.g.:

> "Call refresh_knowledge to pull the latest docs"

Claude will invoke the MCP tool automatically.

**From Claude Desktop:** Same approach — ask Claude in the chat to call `refresh_knowledge` and it will execute it via the MCP connection.

**Programmatically (direct HTTP/SSE):** Send a `tools/call` JSON-RPC request to the MCP server:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "refresh_knowledge",
    "arguments": {}
  }
}
```

Alternatively, you can rebuild and restart the container for a clean slate:

```bash
docker build -t dynizer-mcp .
docker run -p 8000:8000 dynizer-mcp
```

## Knowledge Tools

Markdown files in `knowledge/` are automatically loaded as tools prefixed with `knowledge_`. You can set a custom name via frontmatter:

```markdown
---
name: my_topic
description: Overview of my topic
---

Content here...
```

### Section splitting

Large documents (body > `DYNIZER_KNOWLEDGE_SPLIT_THRESHOLD`, default 3000 chars) with 2+ headings are automatically split into two tools:

- **`knowledge_<name>_toc`** — returns a table of contents with section slugs
- **`knowledge_<name>_section`** — accepts a `section` parameter, returns that section's content

Small documents remain a single `knowledge_<name>` tool returning full content.

This lets the MCP client browse the TOC first, then fetch only the section it needs, avoiding context overflow on large docs.

### OpenAPI specs

Files ending in `.openapi.md` are parsed by the spec loader (not the knowledge loader) into per-endpoint tools. When multiple spec files define endpoints with the same name, a short disambiguator suffix is appended automatically (e.g. `check_healthz_pipeline`).
