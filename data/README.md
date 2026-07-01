# ANR live data (2026-07-01)

Real Google Shopping data for Estée Lauder Advanced Night Repair 50ml,
pulled via Apify actor `johnvc/google-shopping-api-...` across FR/DE/CZ/PL/RO.

- `anr_<cc>.json` — raw Apify dataset per country
- `parse_anr.py` — cleans noise (Duo/set/mini/edition), FX→EUR, computes avg/min/#sellers

Chart values (order FR,DE,CZ,PL,RO):
- avg€    = [86, 100, 86, 67, 80]
- min€    = [62, 76, 51, 48, 55]
- #shops  = [8, 5, 7, 10, 8]

⚠️ FX is approximate (CZK 25, PLN 4.3, RON 4.97). For the real pitch, use ECB daily from the EcomRadar DB.
Minor noise may remain (occasional Overnight Treatment / Limited Edition); order of magnitude is faithful.
