---
name: margin-check
description: Work out the margin of a product or a group of products from price, purchase cost and the store's fixed costs. Use for "what do I earn on this", "margin on product X", "which products lose money", "is this price enough".
---

# Margin check

1. **Fixed costs** come from `store/profile.md`: packaging, fulfillment, payment fee percent, VAT.
   If they are missing, run `store-setup` for the money section first.
2. **Purchase cost** per product: Hub `get_product` (`cost_price`) or the cost column of a
   registered products export. An empty or zero cost means "not entered", never "free".
3. **No cost, no margin.** If the cost is unknown, say which products lack it and ask the owner
   where it is kept (store field, spreadsheet, supplier invoices). Do not estimate it from the
   price or from similar products.
4. **Calculate with the script**, one product at a time:

   ```
   python3 scripts/margin.py --price <price> --cost <cost> --packaging <p> --fulfillment <f> --payment-fee-pct <pct> [--vat-pct <rate>]
   ```

   Packaging and fulfillment are per order. For a single-product order they are charged in full,
   which is the cautious case; say that orders with several products spread them.
5. **Report** the breakdown, not only the result: price, each cost, margin in money and in percent.
   For a group of products give a table sorted from the lowest margin, and count how many could not
   be calculated.
6. **Do not change prices.** You can show what price would give a target margin. Changing it in
   the store is the owner's decision and the owner's click.
7. Save group analyses in `analyses/` with the source of costs in the frontmatter.
