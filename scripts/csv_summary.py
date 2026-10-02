#!/usr/bin/env python3
"""Deterministic numbers from a CSV export, so no figure is ever added up by eye.

  python3 scripts/csv_summary.py profile data/inbox/orders.csv
  python3 scripts/csv_summary.py sum data/inbox/orders.csv --value Total --date "Created at" --period month
  python3 scripts/csv_summary.py sum data/inbox/orders.csv --value Total --by Status
  python3 scripts/csv_summary.py sum data/inbox/items.csv --value "Line total" --by SKU \
      --where Status=Completed --distinct "Order ID" --top 20

Reads comma, semicolon, tab or pipe separated files in UTF-8 or Windows-1250.
Numbers may use a decimal comma, thousands separators and currency symbols.
A value with a single dot and no comma (1.234) is read as a decimal - check `profile` first.
Rows whose number or date cannot be read are counted and reported, never silently dropped.
"""
import argparse
import csv
import io
import re
import sys
from collections import defaultdict
from datetime import datetime
from decimal import Decimal, InvalidOperation

ENCODINGS = ("utf-8-sig", "cp1250", "latin-1")
DATE_FORMATS = ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d", "%Y/%m/%d",
                "%d.%m.%Y %H:%M:%S", "%d.%m.%Y %H:%M", "%d.%m.%Y")
PERIODS = {"day": "%Y-%m-%d", "week": "%G-W%V", "month": "%Y-%m", "year": "%Y"}


def read_rows(path):
    raw = open(path, "rb").read()
    for enc in ENCODINGS:
        try:
            text = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    try:
        dialect = csv.Sniffer().sniff(text[:20000], delimiters=",;\t|")
    except csv.Error:
        dialect = csv.excel
    reader = csv.DictReader(io.StringIO(text), dialect=dialect)
    return list(reader.fieldnames or []), list(reader)


def number(raw):
    s = re.sub(r"[^\d,.\-]", "", raw or "")
    if not re.search(r"\d", s):
        return None
    if "," in s and "." in s:   # the later separator is the decimal one
        s = s.replace(".", "").replace(",", ".") if s.rfind(",") > s.rfind(".") else s.replace(",", "")
    elif "," in s:              # 12,50 is a decimal; 1,234 is a thousands separator
        head, _, tail = s.rpartition(",")
        s = head.replace(",", "") + (tail if len(tail) == 3 else "." + tail)
    try:
        return Decimal(s)
    except InvalidOperation:
        return None


def parse_date(raw, fmt=None):
    s = (raw or "").strip()
    if not s:
        return None
    if fmt:
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00")).replace(tzinfo=None)
    except ValueError:
        pass
    for f in DATE_FORMATS:
        try:
            return datetime.strptime(s, f)
        except ValueError:
            continue
    return None


def need(columns, *names):
    missing = [n for n in names if n and n not in columns]
    if missing:
        sys.exit(f"No such column: {', '.join(missing)}. Columns in the file: {', '.join(columns)}")


def profile(args):
    columns, rows = read_rows(args.file)
    print(f"file: {args.file}\nrows: {len(rows)}\ncolumns: {len(columns)}")
    for c in columns:
        values = [r[c] for r in rows if (r.get(c) or "").strip()]
        nums = [n for n in map(number, values) if n is not None]
        dates = [d for d in map(parse_date, values) if d is not None]
        # mostly-readable columns are reported as what they are, with the unreadable count
        if values and len(dates) >= 0.8 * len(values):
            kind = f"date {min(dates):%Y-%m-%d}..{max(dates):%Y-%m-%d}, {len(values) - len(dates)} unreadable"
        elif values and len(nums) >= 0.8 * len(values):
            kind = f"number min {min(nums)} max {max(nums)} sum {sum(nums)}, {len(values) - len(nums)} unreadable"
        else:
            kind = f"text, {len(set(values))} distinct"
        print(f"  {c!r}: filled {len(values)}/{len(rows)}, {kind}")


def summarise(args):
    columns, rows = read_rows(args.file)
    wheres = [w.split("=", 1) for w in args.where]
    if any(len(w) != 2 for w in wheres):
        sys.exit("--where takes COLUMN=VALUE")
    need(columns, args.value, args.by, args.date, args.distinct, *[w[0] for w in wheres])
    if (args.period or args.date_from or args.date_to) and not args.date:
        sys.exit("--period, --from and --to need --date COLUMN")
    lo = parse_date(args.date_from) if args.date_from else None
    hi = parse_date(args.date_to) if args.date_to else None

    groups = defaultdict(lambda: {"rows": 0, "sum": Decimal(0), "distinct": set()})
    matched = bad_number = bad_date = 0
    for r in rows:
        if any((r.get(col) or "").strip().lower() != val.strip().lower() for col, val in wheres):
            continue
        key = []
        if args.date:
            d = parse_date(r.get(args.date), args.date_format)
            if d is None:
                bad_date += 1
                continue
            if (lo and d.date() < lo.date()) or (hi and d.date() > hi.date()):
                continue
            if args.period:
                key.append(d.strftime(PERIODS[args.period]))
        value = Decimal(0)
        if args.value:
            value = number(r.get(args.value))
            if value is None:
                bad_number += 1
                continue
        if args.by:
            key.append((r.get(args.by) or "").strip() or "(empty)")
        matched += 1
        g = groups[" | ".join(key) or "all"]
        g["rows"] += 1
        g["sum"] += value
        if args.distinct:
            g["distinct"].add(r.get(args.distinct))

    print(f"file: {args.file}\nrows in file: {len(rows)}\nrows counted: {matched}")
    if bad_number:
        print(f"SKIPPED {bad_number} rows: unreadable number in {args.value!r}")
    if bad_date:
        print(f"SKIPPED {bad_date} rows: unreadable date in {args.date!r} (try --date-format)")
    ordered = sorted(groups.items()) if args.period else sorted(groups.items(), key=lambda kv: -kv[1]["sum"])
    shown = ordered[:args.top] if args.top else ordered
    head = ["group", "rows"] + ([f"distinct {args.distinct}"] if args.distinct else []) + ([f"sum {args.value}"] if args.value else [])
    print(" | ".join(head))
    for name, g in shown:
        cells = [name, str(g["rows"])] + ([str(len(g["distinct"]))] if args.distinct else []) + ([str(g["sum"])] if args.value else [])
        print(" | ".join(cells))
    if len(shown) < len(ordered):
        print(f"... {len(ordered) - len(shown)} more groups not shown (--top {args.top})")
    if args.value:
        print(f"TOTAL sum {args.value}: {sum(g['sum'] for g in groups.values())}")


def main():
    parser = argparse.ArgumentParser(description="Deterministic numbers from a CSV export.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("profile", help="columns, fill rate, value ranges")
    p.add_argument("file")
    s = sub.add_parser("sum", help="count rows and sum a column, optionally grouped")
    s.add_argument("file")
    s.add_argument("--value", help="column to sum; omit to only count rows")
    s.add_argument("--by", help="column to group by")
    s.add_argument("--date", help="date column")
    s.add_argument("--period", choices=sorted(PERIODS), help="group by period of --date")
    s.add_argument("--date-format", help="strptime format when the date is ambiguous, e.g. %%d/%%m/%%Y")
    s.add_argument("--from", dest="date_from", help="first day, YYYY-MM-DD")
    s.add_argument("--to", dest="date_to", help="last day, YYYY-MM-DD")
    s.add_argument("--where", action="append", default=[], metavar="COLUMN=VALUE", help="keep matching rows (repeatable)")
    s.add_argument("--distinct", help="count distinct values of this column, e.g. the order id in a line-item file")
    s.add_argument("--top", type=int, help="show only the N largest groups")
    args = parser.parse_args()
    profile(args) if args.cmd == "profile" else summarise(args)


if __name__ == "__main__":
    main()
