#!/usr/bin/env python3
"""Knowledge-graph audit: every .md must be reachable from the root `_index.md`.

Reachability, not degree: two notes that link only to each other have edges,
but they are an island cut off from the graph - the same defect as an orphan.
Links count in either direction.

  python3 scripts/graph_audit.py          # full audit: orphans + broken links, exit 1 on any
  python3 scripts/graph_audit.py --hook   # after-edit hook: reads the tool call on stdin,
                                          # exit 2 with a message when a note is left unlinked
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROOT_NODE = "_index.md"
IGNORE_PARTS = {"node_modules", "__pycache__"}   # plus every dot-directory
IGNORE_PREFIXES = ("data/inbox",)                # raw exports, not knowledge

MD_LINK = re.compile(r"\[[^\]]*\]\(([^)#\s]+\.md)(?:#[^)]*)?\)")
WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]")
FENCE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE = re.compile(r"`[^`\n]*`")


def collect_files():
    files = []
    for p in ROOT.rglob("*.md"):
        rel = p.relative_to(ROOT)
        if any(part.startswith(".") or part in IGNORE_PARTS for part in rel.parts):
            continue
        if rel.as_posix().startswith(IGNORE_PREFIXES):
            continue
        files.append(p.resolve())
    return files


def build_graph(files):
    known = set(files)
    by_name = {}
    for p in files:
        by_name.setdefault(p.stem.lower(), []).append(p)

    edges = {p: set() for p in files}   # undirected
    broken = []
    for p in files:
        try:
            text = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        # examples inside code are not links
        text = INLINE_CODE.sub("", FENCE.sub("", text))
        for m in MD_LINK.finditer(text):
            if m.group(1).startswith(("http:", "https:", "mailto:")):
                continue
            target = (p.parent / m.group(1)).resolve()
            if target in known:
                edges[p].add(target)
                edges[target].add(p)
            else:
                broken.append((p, m.group(1)))
        for m in WIKILINK.finditer(text):
            for target in by_name.get(m.group(1).strip().lower(), []):
                if target != p:
                    edges[p].add(target)
                    edges[target].add(p)
    return edges, broken


def orphans(edges):
    root = (ROOT / ROOT_NODE).resolve()
    if root not in edges:
        return []   # no root, nothing to measure from
    seen, stack = {root}, [root]
    while stack:
        for nxt in edges[stack.pop()]:
            if nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)
    return sorted(p.relative_to(ROOT).as_posix() for p in edges if p not in seen)


def main():
    hook = "--hook" in sys.argv[1:]
    if hook:
        try:
            call = json.dumps(json.load(sys.stdin).get("tool_input", {}))
        except (ValueError, AttributeError):
            call = ".md"
        if ".md" not in call:
            return 0   # the edit did not touch a note

    edges, broken = build_graph(collect_files())
    islands = orphans(edges)

    if hook:
        if not islands:
            return 0
        print(f"UNLINKED NOTES (not reachable from {ROOT_NODE}): {', '.join(islands)}. "
              f"Link each one from the nearest _index.md now, in this step - not later.",
              file=sys.stderr)
        return 2

    print(f"notes: {len(edges)}")
    print(f"orphans (not reachable from {ROOT_NODE}): {len(islands)}")
    for o in islands:
        print(f"  - {o}")
    print(f"broken links: {len(broken)}")
    for src, link in broken:
        print(f"  - {src.relative_to(ROOT).as_posix()} -> {link}")
    return 1 if islands or broken else 0


if __name__ == "__main__":
    sys.exit(main())
