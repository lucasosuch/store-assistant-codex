# Store assistant for Codex

A ready-made workspace that turns Codex into an assistant for your online store. It knows what your
store is, works on your real numbers, remembers what you taught it, and changes nothing in the
store without your approval.

It works with any platform. Start with CSV exports; connect a Hub later to skip the exporting.

Using Claude Code instead? The same workspace is available as [store-assistant-claude-code](https://github.com/lucasosuch/store-assistant-claude-code).

## What you get

- **Skills** for the recurring jobs: sales review, stock check, margin check, product descriptions,
  traffic review, importing an export, first-run setup.
- **Three roles**: sales analyst, catalog editor, traffic analyst.
- **A knowledge graph.** Every analysis, decision and rule is a linked Markdown note. A check runs
  after each edit, so nothing the assistant writes ends up unlinked and forgotten.
- **Numbers from data, not from the model.** Figures come from Hub tools or from the scripts in
  `scripts/`. If the data is missing, the assistant asks for an export instead of guessing.
- **Approval before any change.** The assistant proposes, you approve, then it is applied.

## Requirements

- [Codex](https://developers.openai.com/codex) with a ChatGPT plan that includes it
- Python 3.9 or newer, available as `python3` (standard library only, nothing to install)
- git (the graph hook finds the workspace through it)
- Optional: VS Code with the [Foam](https://foambubble.github.io/foam/) extension to see the graph

## Quick start

```bash
git clone https://github.com/lucasosuch/store-assistant-codex.git my-store-assistant
cd my-store-assistant
codex
```

Trust the project when Codex asks. The roles, hook and settings in `.codex/` load only for
trusted projects.

Then type: `set up my store`. The assistant asks about your platform, costs and which order
statuses count as revenue, and saves the answers in `store/profile.md`.

After that, ask in plain words:

- "How did we sell last month compared with the month before?"
- "What is about to run out?"
- "What do I earn on product X after packaging and payment fees?"
- "Write descriptions for the five products that have none."

To call a skill by name, type `$` and pick it, or use `/skills`.

## Two ways to give it data

**Exports.** Without a Hub the assistant tells you exactly which export it needs (orders, products,
analytics, Search Console) and which columns. Save the file in `data/inbox/`. It profiles the file,
records the column mapping in `data/_index.md`, and computes with `scripts/csv_summary.py`. CSV and
TSV work directly; XLSX and JSON are converted first.

**A Hub.** A Hub is an MCP server that keeps your store, marketplace and analytics data in sync and
applies changes to the store only after you approve them. With a Hub connected the assistant reads
live data and can put an approved description, stock level or category straight into the store.

Open `.codex/config.toml`, uncomment the `[mcp_servers.hub]` block, set the address, and export the
token before starting Codex:

```bash
export HUB_TOKEN="your-token"
codex
```

The server must be named `hub`. The token lives in your environment, not in this repository.

No Hub yet? See [how a Hub is set up for an online store](https://lumato.tech/for-online-stores/).

## Approval

The Hub block in `.codex/config.toml` sets `approval_mode = "prompt"` for the tool `apply_change`,
so Codex asks you before anything is written to the store. The assistant is also instructed to show
you the before and after first and to wait for your answer. It will not change prices, cancel or
refund orders, change order statuses, touch ad budgets or order from suppliers, even when asked.

## The knowledge graph

```
_index.md        root of the graph
store/           profile: platform, channels, costs, revenue statuses
memory/          rules, decisions, glossary - what you taught the assistant
analyses/        dated analyses, each with its source and period
drafts/          proposed content waiting for you
knowledge/       your reference material: courses, supplier terms, policies
data/            register of exports; the files themselves stay in data/inbox/
scripts/         graph_audit.py, csv_summary.py, margin.py
.agents/skills/  skills
.codex/          roles, settings and the graph hook
```

Every note is linked from the `_index.md` of its folder. Check the graph at any time:

```bash
python3 scripts/graph_audit.py
```

Open the folder in VS Code with Foam and run "Foam: Show Graph" to see it. Notes are coloured by
their `type`.

## Your data

Everything stays on your computer and in your own git repository. `data/inbox/` is ignored by git
because exports can contain customer data; ask your platform for exports without names, emails and
addresses where you can. What you send to the model is governed by your ChatGPT plan and its data
controls.

## Make it yours

Edit `AGENTS.md` for how the assistant should behave, add skills under `.agents/skills/`, and put
your own reference material in `knowledge/`. Keep every new note linked from an `_index.md`.

## License

MIT - see [LICENSE](LICENSE). Use it, change it, build on it.

Map of this workspace: [`_index.md`](_index.md).
