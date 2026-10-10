---
name: doctor
description: Check that the store assistant is set up correctly and say how to fix what is not. Use for "check my setup", "is everything working", "why is this not working", after connecting or changing a Hub, and when a script, the graph hook or a Hub tool fails.
---

# Doctor

Check, do not repair. Run every step even when an earlier one fails, then report.

1. **Python.** Run `python3 scripts/graph_audit.py`. If `python3` is missing or is not Python 3.9 or
   newer, the scripts and the graph hook cannot run, so no figure from files can be trusted. Say
   how to install Python for the owner's system. Otherwise report orphans and broken links.
2. **Graph hook.** Confirm the hook that runs `graph_audit.py --hook` after edits is still in the
   settings folder of this workspace (`.claude/` or `.codex/`). In Codex it loads only when the
   project is trusted and git is installed.
3. **Hub connection.** Look at the tools you actually have. No Hub tools: say the assistant works
   from exports, and stop the Hub checks here. That is a valid setup, not a fault.
4. **Hub name and approval.** The Hub tools must come from an MCP server named `hub`. The setting
   that makes the tool ask before `apply_change` is written for that name. Under any other name
   (including a connector added in a web or desktop app) that setting does not apply: say so
   plainly and tell the owner to reconnect the Hub as `hub`, following the README. Then confirm the
   setting is still there: `mcp__hub__apply_change` under `ask` in `.claude/settings.json`, or
   `approval_mode = "prompt"` for `apply_change` in `.codex/config.toml`.
5. **Sources.** Call `get_sync_status`. For each source give its status and `last_sync_at`. A
   source with an error or a sync older than a day is a problem: quote `last_error` and say that
   fixing it is the job of whoever runs the Hub. An authorization error on the call itself means
   the token is wrong or expired.
6. **Profile.** If `store/profile.md` has `status: empty`, offer `store-setup`. List the money
   fields still marked unknown.
7. **Exports.** Without Hub data for sales or catalog, check that `data/_index.md` registers at
   least one export and that the file is still in `data/inbox/`.

Report three short lists: works, does not work, how to fix each item. Never print a token. Do not
call any `propose_*` tool or `apply_change` as a test.
