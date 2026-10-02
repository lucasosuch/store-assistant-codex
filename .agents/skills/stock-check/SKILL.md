---
name: stock-check
description: Find products that are out of stock or about to run out, and products that tie up stock without selling. Use for "what is running out", "what should I reorder", "low stock", "dead stock".
---

# Stock check

1. **Data.** Follow the data protocol in the project instructions.
   - Hub: `get_low_stock(threshold_qty, days_window)`. It returns stock, units sold in the window
     and `days_left`. Use the threshold from `memory/rules.md` if the owner set one.
   - Files: a products export with SKU, name and stock, profiled and registered through
     `import-data`. Days of stock left need sales per SKU as well; without an orders export, report
     stock levels only and say that the run-out date cannot be worked out.
2. **Three lists**, each sorted by urgency:
   - out of stock and it was selling (lost sales now)
   - will run out soon, with days left
   - stock that has not sold in the window (money on the shelf)
3. **`days_left` is an extrapolation** from recent sales, not a forecast. Say so once. A product
   with no sales in the window has no `days_left`; do not invent one.
4. **Do not reorder.** You list what to reorder and how many units would cover a period the owner
   names. Placing the order with a supplier is the owner's job.
5. Changing a stock number in the store goes through propose, approve, apply, like any change.
6. Save the result in `analyses/` when the owner will act on it; a quick check does not need a note.
