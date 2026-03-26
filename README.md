# NEXUS → Notion MCP Bridge

Connects an autonomous AI outreach swarm to Notion using the **official Notion MCP server** over stdio transport — no REST API, pure Model Context Protocol.

Every swarm cycle (score, copy, context) becomes a Notion database page in real-time.

## How It Works

```
AI Swarm (Python) → cycles.json → MCP Bridge → notion-mcp-server (stdio) → Notion DB
```

The bridge:
1. Spawns `@notionhq/notion-mcp-server` as a subprocess
2. Initializes the MCP session via JSON-RPC 2.0 over stdin/stdout
3. Calls `notion_create_page` for each new cycle
4. Tracks logged cycles in state file to avoid duplicates

## Setup

```bash
# 1. Install the Notion MCP server
npm install -g @notionhq/notion-mcp-server

# 2. Set credentials
export NOTION_API_KEY=your_notion_integration_token
export NOTION_DATABASE_ID=your_database_id

# 3. Install Python deps
pip install -r requirements.txt

# 4. Point the bridge at your swarm output
# In nexus_notion_mcp_bridge.py, set CYCLES_FILE to your swarm's output JSON

# 5. Run
python nexus_notion_mcp_bridge.py          # continuous polling
python nexus_notion_mcp_bridge.py --once   # sync once and exit
```

## Notion Database Schema

| Field | Type | Description |
|-------|------|-------------|
| Name | Title | cycle_id + score |
| Score | Number | 0.0–1.0 reward score |
| Posted | Checkbox | Whether the copy was posted |
| Timestamp | Date | Cycle timestamp |
| Context | Text | Thread title + subreddit |
| Body | Page block | Full outreach copy |

## Swarm Cycle Format

See `example_cycles.json` for the expected input format. The bridge handles both `cycle_id` and `cycle` field names for compatibility.

## Requirements

- Node.js 18+ (for notion-mcp-server)
- Python 3.10+

## License

MIT
