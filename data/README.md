# ANR live data (2026-07-01)

Real Google Shopping data for **Estée Lauder Advanced Night Repair Synchronized Multi-Recovery Complex — 50ml Serum**,
pulled via Apify actor `johnvc/google-shopping-api-...` across FR/DE/CZ/PL/RO.

- `anr_<cc>.json` — raw Apify dataset per country
- `parse_anr.py` — cleans the data:
  - **50ml serum only** — excludes 65ml Overnight Treatment (a cream), Concentrate, Intense Reset, Recovery Complex II, Power Pair, sets/duos/mini.
  - **Aggregators excluded** — Heureka, Zboží, Idealo, Ceneo, Geizhals etc. are price-comparison portals, NOT sellers (they only advertise & redirect). The actual shop behind a Heureka listing is unknown from the feed, so the row is dropped.
  - FX→EUR, avg/min/#sellers per market.

Chart values (order FR,DE,CZ,PL,RO):
- avg€    = [85, 80, 86, 66, 69]
- min€    = [62, 43, 59, 48, 41]
- #shops  = [8, 4, 4, 6, 6]

Cheapest per market: FR Olara €62 · DE Amazon.de €43 · CZ eBay €59 · PL Stylevana €48 · RO eBay €41.
Spread: CZ avg €86 → RO min €41.

⚠️ Notes:
- Direct e-shop URLs are NOT available via Google Shopping API (only Google redirects). Deck links open Google Shopping search per market.
- Marketplaces (eBay, Allegro, Lamoda, Trendyol) ARE kept — they are real points of sale (third parties sell on them).
- FX approximate (CZK 25, PLN 4.3, RON 4.97). For the pitch, use ECB daily from the EcomRadar DB.
- Dropping Heureka changed CZ materially: the false €43 "Heureka" datapoint was an aggregator, not a seller. CZ is now avg €86 / min €59.
