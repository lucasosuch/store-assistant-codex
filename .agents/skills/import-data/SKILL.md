---
name: import-data
description: Get store data from a file when the Hub has none. Use when a question needs sales, catalog, traffic or search data and the Hub is not connected, has no source for it, or returned nothing; and whenever the owner drops a CSV, TSV, XLSX or JSON export into data/inbox.
---

# Import data from an export

Use this instead of guessing. The owner exports a file, you register it, then every number comes
from `scripts/csv_summary.py`.

## 1. Ask for exactly what you need

Say which export, from where, for which period, with which columns. One request, not a list of
possibilities.

| Need | Export | Columns that must be there |
|---|---|---|
| Sales | orders, best with line items | order id, date, status, total, currency (+ SKU, quantity, unit price) |
| Catalog and stock | products | SKU, name, price, stock, category (+ purchase cost for margin) |
| Traffic | analytics report | date, page or source, sessions, page views |
| Search | Search Console performance | query, page, clicks, impressions, position |

Ask the owner to leave out customer names, emails, phone numbers and addresses if the platform
lets them choose columns. Ask them to save the file in `data/inbox/`.

CSV or TSV is best. If only XLSX or JSON is available, take it, convert it to CSV with a short
script (not by hand), and keep the original beside it.

## 2. Profile the file before trusting it

```
python3 scripts/csv_summary.py profile data/inbox/<file>
```

Check: row count is plausible, the date column covers the period you asked for, the money column
is read as a number, and how many values are unreadable. If the date format is ambiguous (for
example 03/04/2026), ask the owner which is the day and use `--date-format`.

## 3. Register it

Add a row to `data/_index.md`: file name, what it is, period covered, export date, and the column
mapping (which column is the date, the total, the status, the SKU). Write down which status values
count as revenue, taken from `store/profile.md` or confirmed with the owner.

## 4. Compute

```
python3 scripts/csv_summary.py sum data/inbox/<file> --value <total> --date <date> --period month --where <status>=<value>
```

Use `--distinct <order id>` when the file has one row per line item, so orders are not counted
once per product. Report every `SKIPPED` line from the output to the owner; skipped rows are
missing money.

## 5. Say what the answer rests on

File name, export date, period, filters. An export is a snapshot: say that it does not include
anything after the export date.
