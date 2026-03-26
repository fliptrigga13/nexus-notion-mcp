"""
nexus_notion_mcp_bridge.py
══════════════════════════════════════════════════════════════════
NEXUS Swarm → Notion via MCP
Connects an autonomous AI outreach swarm to Notion using the
official Notion MCP server (stdio transport).

Each swarm cycle (score, copy, context) becomes a Notion page
automatically — no REST API, pure MCP protocol.

Setup:
    npm install -g @notionhq/notion-mcp-server
    export NOTION_API_KEY=your_token
    export NOTION_DATABASE_ID=your_db_id

Run (sidecar, polls every 60s):
    python nexus_notion_mcp_bridge.py

Run once:
    python nexus_notion_mcp_bridge.py --once
══════════════════════════════════════════════════════════════════
"""

import json
import os
import subprocess
import time
import argparse
import logging
from datetime import datetime, timezone
from pathlib import Path

log = logging.getLogger("NEXUS_MCP")
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(message)s")

# ── Config ────────────────────────────────────────────────────────────────────

BASE          = Path(__file__).parent
CYCLES_FILE   = BASE / "cycles.json"          # swarm output (see example_cycles.json)
STATE_FILE    = BASE / "mcp_bridge_state.json" # tracks logged cycle IDs
POLL_INTERVAL = 60  # seconds

NOTION_API_KEY   = os.environ.get("NOTION_API_KEY", "")
DATABASE_ID      = os.environ.get("NOTION_DATABASE_ID", "")

# ── State ─────────────────────────────────────────────────────────────────────

def load_state() -> set:
    if STATE_FILE.exists():
        try:
            return set(json.loads(STATE_FILE.read_text())["logged"])
        except Exception:
            pass
    return set()

def save_state(logged: set):
    STATE_FILE.write_text(json.dumps({"logged": sorted(logged)}, indent=2))

# ── MCP Client (stdio transport) ──────────────────────────────────────────────

class NotionMCPClient:
    """
    Minimal MCP client that spawns @notionhq/notion-mcp-server as a subprocess
    and communicates over stdin/stdout using JSON-RPC 2.0.
    """

    def __init__(self, api_key: str):
        self._api_key = api_key
        self._proc    = None
        self._msg_id  = 0

    def _next_id(self) -> int:
        self._msg_id += 1
        return self._msg_id

    def start(self):
        env = {**os.environ, "NOTION_API_KEY": self._api_key}
        self._proc = subprocess.Popen(
            ["notion-mcp-server", "--transport", "stdio"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            env=env,
            text=True,
            bufsize=1,
        )
        self._initialize()
        log.info("[MCP] Connected to notion-mcp-server via stdio")

    def stop(self):
        if self._proc:
            self._proc.stdin.close()
            self._proc.terminate()
            self._proc = None

    def _send(self, msg: dict) -> dict | None:
        line = json.dumps(msg) + "\n"
        self._proc.stdin.write(line)
        self._proc.stdin.flush()
        raw = self._proc.stdout.readline()
        if raw.strip():
            return json.loads(raw)
        return None

    def _initialize(self):
        self._send({
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "nexus-notion-mcp-bridge", "version": "1.0"},
            },
        })
        # Send initialized notification (no response expected)
        self._proc.stdin.write(json.dumps({
            "jsonrpc": "2.0",
            "method": "notifications/initialized",
            "params": {},
        }) + "\n")
        self._proc.stdin.flush()

    def create_page(self, database_id: str, cycle: dict) -> bool:
        """Create a Notion database page for one swarm cycle."""
        ts_raw = cycle.get("ts", datetime.now(timezone.utc).isoformat())
        try:
            ts = datetime.fromisoformat(
                ts_raw.replace("Z", "+00:00")
            ).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        except Exception:
            ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")

        cycle_id = cycle.get("cycle_id", cycle.get("cycle", "unknown"))
        score    = cycle.get("score", 0.0)
        body     = (cycle.get("body") or "")[:2000]
        context  = (cycle.get("context") or cycle.get("scout_ctx") or "")[:500]
        posted   = cycle.get("posted", False)

        title = f"{cycle_id} | score={score:.2f}"

        resp = self._send({
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": "tools/call",
            "params": {
                "name": "notion_create_page",
                "arguments": {
                    "parent": {"database_id": database_id},
                    "properties": {
                        "Name": {
                            "title": [{"text": {"content": title}}]
                        },
                        "Score": {"number": round(score, 3)},
                        "Posted": {"checkbox": posted},
                        "Timestamp": {"date": {"start": ts}},
                        "Context": {
                            "rich_text": [{"text": {"content": context}}]
                        },
                    },
                    "children": [
                        {
                            "object": "block",
                            "type": "heading_2",
                            "heading_2": {
                                "rich_text": [{"text": {"content": "Outreach Copy"}}]
                            }
                        },
                        {
                            "object": "block",
                            "type": "paragraph",
                            "paragraph": {
                                "rich_text": [{"text": {"content": body or "(no copy)"}}]
                            }
                        }
                    ]
                },
            },
        })

        if resp and not resp.get("error"):
            log.info(f"[MCP] ✅ Page created: {title}")
            return True
        else:
            log.error(f"[MCP] ❌ Failed: {resp}")
            return False

# ── Sync loop ─────────────────────────────────────────────────────────────────

def sync_once(client: NotionMCPClient):
    if not CYCLES_FILE.exists():
        log.info("[BRIDGE] No cycles file yet — waiting for swarm output.")
        return 0

    try:
        cycles = json.loads(CYCLES_FILE.read_text(encoding="utf-8"))
    except Exception as e:
        log.warning(f"[BRIDGE] Could not read cycles file: {e}")
        return 0

    logged = load_state()
    new_count = 0

    for cycle in cycles:
        cid = cycle.get("cycle_id") or cycle.get("cycle")
        if not cid or cid in logged:
            continue
        if not cycle.get("body") and not cycle.get("score"):
            continue

        if client.create_page(DATABASE_ID, cycle):
            logged.add(cid)
            new_count += 1
            time.sleep(0.4)  # gentle rate limiting

    save_state(logged)
    if new_count:
        log.info(f"[BRIDGE] Synced {new_count} new cycle(s). Total: {len(logged)}")
    return new_count

def main():
    parser = argparse.ArgumentParser(description="NEXUS Swarm → Notion MCP Bridge")
    parser.add_argument("--once", action="store_true", help="Sync once and exit")
    args = parser.parse_args()

    if not NOTION_API_KEY:
        log.error("NOTION_API_KEY not set. Export it or add to .env")
        return
    if not DATABASE_ID:
        log.error("NOTION_DATABASE_ID not set. Export it or add to .env")
        return

    client = NotionMCPClient(NOTION_API_KEY)
    client.start()

    try:
        if args.once:
            synced = sync_once(client)
            log.info(f"[BRIDGE] Done. {synced} entries logged to Notion.")
        else:
            log.info(f"[BRIDGE] Polling every {POLL_INTERVAL}s — Ctrl+C to stop.")
            while True:
                try:
                    sync_once(client)
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    log.error(f"[BRIDGE] Error: {e}")
                time.sleep(POLL_INTERVAL)
    finally:
        client.stop()

if __name__ == "__main__":
    main()
