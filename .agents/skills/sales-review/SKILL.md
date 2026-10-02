---
name: sales-review
description: Review store sales for a period - revenue, orders, average order value, best and worst products, change versus the previous period. Use for "how did we sell", "sales this week/month", "what sold best", daily or weekly reviews.
---

# Sales review

1. **Period.** Use the one the owner named. If none, use the last 7 days and say so. Always compare
   with the previous period of the same length.
2. **Data.** Follow the data protocol in the project instructions.
   - Hub: `get_sales_summary(period, group_by="day")`, then `group_by="product"`, and
     `group_by="channel"` when the store sells in more than one place. Check that
     `revenue_statuses` in the result match `store/profile.md`. If they do not, stop and tell the
     owner; revenue would be wrong.
   - Files: `scripts/csv_summary.py sum` with `--where` on the revenue statuses, by period and by
     SKU. Use `--distinct` on the order id for line-item files.
   - Neither: run `import-data`. Do not produce a review without data.
3. **Work out** revenue, order count, average order value (revenue divided by orders, computed by
   the tool or script, not by you), top 5 and bottom 5 products, and the change against the
   previous period in absolute numbers and percent.
4. **Zero is an answer.** If there were no orders, say so and check the obvious causes before
   speculating: source not synced, wrong revenue statuses, export from the wrong period.
5. **Say what it means.** Two or three observations the owner can act on, each tied to a number
   from step 3. No generic advice.
6. **Save it** as `analyses/YYYY-MM-DD-sales-<period>.md` with `type: analysis`, `source` and
   `period` in the frontmatter. Add the row to `analyses/_index.md` first. Link earlier reviews and
   any rule or decision you relied on.
