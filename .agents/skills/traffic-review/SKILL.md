---
name: traffic-review
description: Review where store visitors come from, which pages they see, where they drop off before buying, and how the store shows up in search. Use for "where does my traffic come from", "which pages get visits", "why do visits not turn into orders", "what do people search for".
---

# Traffic review

1. **Data.** Follow the data protocol in the project instructions.
   - Hub: `get_traffic_summary(period, by)` with `by` set to `path`, `referrer` or `utm_source`;
     `get_conversion_funnel(period)`; `get_search_summary(period)` for search queries and pages.
   - If the Hub answers that traffic comes from several sources, pick one with `source_kind` and
     name it. Two analytics tools on one store count the same visits differently; never add them
     and do not average them. If they differ a lot, report both numbers and the gap.
   - Files: an analytics export and a Search Console export, registered through `import-data`.
2. **Small numbers.** With a few dozen sessions, percentages mislead. Report counts, and say when
   the sample is too small to conclude anything.
3. **Fresh sources.** A source connected a few days ago has a few days of data. Search data usually
   arrives two or three days late. State the first and last day you actually have.
4. **Connect traffic to sales** only when both exist for the same period: sessions, orders, and
   the share of sessions that ordered. Take the orders from the sales data, not from analytics
   events, unless the owner confirmed that purchase tracking works.
5. **Answer three questions:** where visitors come from, where they land, where they leave. Then
   two or three things worth checking, each tied to a number.
6. Save as `analyses/YYYY-MM-DD-traffic-<period>.md`, with the source named in the frontmatter.
