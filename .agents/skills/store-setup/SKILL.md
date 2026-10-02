---
name: store-setup
description: First-run setup of the store assistant. Use when store/profile.md has status empty, when the owner says "set up my store" or "get started", or when the platform, costs or data sources of the store change.
---

# Store setup

Goal: a filled `store/profile.md`, so every later answer uses the right currency, costs and
revenue statuses.

1. **Check the Hub.** If an MCP server named `hub` is connected, call `get_sync_status`. Note each
   source, what it covers and when it last synced. If there is no Hub, say so in one sentence: the
   assistant works from exports, and a Hub removes the exporting. Do not push it.
2. **Read what the data already says.** With a Hub: `list_products` (limit 5) and `get_categories`
   show the platform's shape; `get_sales_summary` shows which order statuses count as revenue.
   Without a Hub: skip to step 3.
3. **Ask only what you could not read.** Go through `store/profile.md` section by section. Ask a
   few questions at a time, never the whole form at once. Accept "unknown" and write it down as
   unknown.
4. **Money section matters most.** Which order statuses count as revenue, packaging and fulfillment
   cost per order, payment fee percent, and where purchase costs are kept. Without these, sales
   figures and margins are wrong or impossible. Say that plainly if the owner wants to skip it.
5. **Write the profile.** Fill `store/profile.md`, set `status: ready`. Put product nicknames and
   status meanings in `memory/glossary.md`.
6. **If there is no Hub data for sales or catalog**, offer the `import-data` skill next.
7. Run `python3 scripts/graph_audit.py` and finish with three lines: what you know, what is still
   unknown, what the owner can ask you now.
