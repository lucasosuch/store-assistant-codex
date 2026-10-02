---
name: product-content
description: Write or improve product descriptions, short descriptions and category assignment, and put them in the store only after the owner approves. Use for "fix this description", "write descriptions for products without one", "assign categories".
---

# Product content

1. **Read before writing.** `memory/rules.md` for tone and banned claims, `memory/glossary.md` for
   names, and `knowledge/` for brand voice or supplier material. Then the current content:
   Hub `get_product_content` or `get_product`; without a Hub, a products export or text the owner
   pastes.
2. **Find what to work on.** With a Hub, `list_products` with `missing` set to description, image
   or category finds the gaps. Work in small batches the owner can actually read: five products,
   not fifty.
3. **Write from facts you have.** Product attributes, the supplier's material, the owner's notes.
   Do not invent materials, sizes, origin, certificates, health or safety effects. If a fact is
   missing, leave it out and list what you would need.
4. **Show before and after** for each product, side by side, with what changed and why.
5. **Wait for approval.** Then:
   - With a Hub: `propose_product_update` for that product, show the returned change, and only
     after an explicit yes call `apply_change`. One approval covers the changes the owner saw, not
     the next batch.
   - Without a Hub: save each text in `drafts/YYYY-MM-DD-<product-slug>.md` with the product name
     and SKU, add it to `drafts/_index.md`, and tell the owner where to paste it.
6. **Record** what was applied (product, change id or draft file, date) in the note for this batch.
7. If the owner corrects your style, save the correction to `memory/rules.md` before continuing.
