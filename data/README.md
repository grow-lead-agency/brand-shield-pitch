# ANR live data (2026-07-01)

Real Google Shopping data for **Estée Lauder Advanced Night Repair Synchronized Multi-Recovery Complex — 50ml Serum**,
pulled via Apify actor `johnvc/google-shopping-api-...` across FR/DE/CZ/PL/RO.

- `anr_<cc>.json` — raw Apify dataset per country
- `parse_anr.py` — STRICT filter: 50ml serum only. Excludes 65ml Overnight Treatment (a cream),
  Concentrate, Intense Reset, Recovery Complex II, Power Pair, sets/duos/mini. FX→EUR, avg/min/#sellers.

Chart values (order FR,DE,CZ,PL,RO):
- avg€    = [85, 80, 78, 66, 69]
- min€    = [62, 43, 43, 48, 41]
- #shops  = [8, 4, 5, 6, 6]

Cheapest per market: FR Olara €62 · DE Amazon.de €43 · CZ Heureka €43 · PL Stylevana €48 · RO eBay €41.
Spread: FR avg €85 → RO min €41.

⚠️ Notes:
- Direct e-shop URLs are NOT available via Google Shopping API (only Google Shopping redirects).
  Seller links in the deck open Google Shopping search per market.
- FX approximate (CZK 25, PLN 4.3, RON 4.97). For the pitch, use ECB daily from the EcomRadar DB.
- A few Pink Ribbon / Limited Edition 50ml serums remain (same volume, comparable price) — kept intentionally.
