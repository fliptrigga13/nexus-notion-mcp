# NEXUS ULTRA ⚡
### *Your workflows, as a brain that learns, forgets, and corrects itself.*

**SINGLE-Clarity** — One brain. Your work. $0 per cycle. 100% local.

[![Demo](https://img.shields.io/badge/Live_Demo-Loom-00e5ff?style=flat-square)](https://www.loom.com/share/887b9464508240ecbd4adb1c07a26ae0)
[![pip](https://img.shields.io/badge/pip_install-veilpiercer-00ff88?style=flat-square)](https://pypi.org/project/veilpiercer/)
[![License](https://img.shields.io/badge/license-MIT-white?style=flat-square)](LICENSE)

---

## 🎬 Live Demo

> 11 agents. 1,885+ cycles logged to Notion. Fully autonomous. Watch it run in real time:

**[▶ Watch the live demo on Loom](https://www.loom.com/share/887b9464508240ecbd4adb1c07a26ae0)**

---

## What Is NEXUS ULTRA?

NEXUS ULTRA is a **self-evolving, multi-agent AI swarm** built on the SINGLE-Clarity architecture. It runs entirely on local hardware — no cloud, no API costs, no subscriptions.

11 specialized agents collaborate in timed cycles, scouting live signals from Reddit and HackerNews, writing outreach copy, critiquing each other's outputs, and logging every cycle to Notion via MCP in real time.

```
GENERATOR tier  →  COMMANDER · SCOUT · COPYWRITER · CONVERSION_ANALYST
CRITIC tier     →  VALIDATOR · SENTINEL_MAGNITUDE · METACOG · EXECUTIONER
OPTIMIZER tier  →  SUPERVISOR · REWARD · CLOSER
     ↑                                                          |
     └──────────── scores, lessons, memory, KG injection ──────┘
```

Every cycle, the REWARD agent scores performance. Top lessons are promoted into the next cycle's context. The swarm rewrites its own operating instructions based on what works.

---

## SINGLE-Clarity Architecture

SINGLE-Clarity is the cognitive system powering NEXUS ULTRA. It is not a framework or SaaS product — it is a **unified local brain** with five layered organs.

| | |
|---|---|
| **One Brain** | Single source of truth across all agents — `nexus_kg.json` |
| **Your Work** | Runs locally, $0 cloud, no API dependency |
| **Self-Calibrating** | 1,885+ cycles in production — smarter every run |

### The Five Organs

| Organ | Role | Description |
|---|---|---|
| **KG** | Memory | Knowledge Graph — typed, time-aware, 9,000+ nodes |
| **CHRONOS** | Brain | Temporal confidence engine — half-lives and decay |
| **Swarm** | Nervous System | 11 agents, 3 tiers, self-scored cycles |
| **VeilPiercer** | Immune System | Divergence detection, session tracing, FAILURE_MEMORY |
| **NeuralMind** | Interface | Force-directed KG graph, swarm health display |

---

## Why Not Just Use ChatGPT?

| | NEXUS ULTRA | ChatGPT / Claude |
|--|-------------|-----------------|
| Your prompts stay private | ✅ | ❌ sent to servers |
| Works with no internet | ✅ | ❌ |
| Monthly cost | $0 | $20+/mo |
| Learns from your sessions | ✅ persistent KG | ❌ resets |
| Multi-agent reasoning | ✅ 11 agents | ❌ single model |
| Notion live reporting | ✅ via MCP | ❌ |

---

## Quick Start

**1. Install Ollama and pull models**
```bash
ollama pull qwen3:8b
ollama pull phi4-mini-reasoning
ollama pull llama3.1:8b
```

**2. Install Python dependencies**
```bash
pip install httpx requests python-dotenv psutil
```

**3. Configure `.env`**
```bash
cp .env.example .env
# Add your NOTION_TOKEN and NOTION_DATABASE_ID
```

**4. Launch the swarm**
```bash
python nexus_swarm_loop.py
```

---

## Notion MCP Integration

Every swarm cycle is logged to Notion in real time via the [Model Context Protocol](https://modelcontextprotocol.io).

**What gets pushed (every ~35 seconds):**
- 🔄 Cycle score, MVP agent, cycle type
- 🏆 Agent leaderboard — all 11 agents scored per cycle
- 🎯 Buyer intelligence signals from Reddit/HN scout

**Setup:**

1. Create a Notion integration at [notion.so/my-integrations](https://www.notion.so/my-integrations)
2. Add your token and database IDs to `.env`:
```
NOTION_TOKEN=ntn_your_token_here
NOTION_CYCLES_DB=your_database_id
NOTION_AGENTS_DB=your_agents_db_id
NOTION_BUYERS_DB=your_buyers_db_id
```
3. Run the sync services:
```bash
python nexus_notion_sync.py
python nexus_notion_reporter.py
```

---

## VeilPiercer — MCP Tools for Claude Desktop

VeilPiercer exposes per-step agent tracing as native tools for Claude Desktop via the [Model Context Protocol](https://modelcontextprotocol.io).

### Register in Claude Desktop

Edit `%APPDATA%\Claude\claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "veilpiercer": {
      "command": "python",
      "args": ["path/to/nexus-ultra/mcp/server.py"]
    }
  }
}
```

Restart Claude Desktop. VeilPiercer appears in the tools panel.

### Available MCP Tools

| Tool | What it does |
|------|-------------|
| `start_session` | Start a new trace session for an agent run |
| `trace_step` | Log one agent step — captures prompt in, response out |
| `diff_sessions` | Compare two sessions — returns fork step and divergence |

```bash
pip install veilpiercer    # free for local use
```

→ [PyPI](https://pypi.org/project/veilpiercer/) · [MCP Setup Guide](mcp/SETUP.md)

---

## License

MIT — do whatever you want with it.

---

*Built on: Ollama · Python · Qwen3 · Phi-4 · Llama · Notion MCP*  
*SINGLE-Clarity architecture · March 2026*
