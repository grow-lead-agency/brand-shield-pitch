# ANR live data (2026-07-01) — comparison-portal method

Real data for **ONE exact SKU: Estée Lauder Advanced Night Repair Synchronized Multi-Recovery Complex 50ml**
(NOT the older "Synchro Recovery Complex II" — that's a different, pricier variant with far fewer sellers).

## Why comparison portals, not Google Shopping API
Google Shopping API (Apify) only returns "sponsored products" — a handful of paid listings, NOT the real market.
It showed 3–8 sellers per country. The real market (what a brand manager sees on Heureka) is 20–47 sellers.
So seller counts + price ranges come from **price-comparison portals**, scraped per product-detail page.

## Sources & numbers (order FR,DE,CZ,PL,RO)
| Market | Source | Sellers | min€ | avg€ | max€ |
|---|---|---|---|---|---|
| FR | idealo.fr (product 200519186) | 25 | 47 | 79 | 124 |
| DE | idealo.de (product 200519186) | 47 | 41 | 70 | 101 |
| CZ | Heureka (detail page) | 21 | 43 | 58 | 72 |
| PL | Ceneo (product 96401250) | 22 | 47 | 66 | 94 |
| RO | Google Shopping* | 5 | 64 | 81 | 116 |

- avg€    = [79, 70, 58, 66, 81]
- min€    = [47, 41, 43, 47, 64]
- sellers = [25, 47, 21, 22, 5]

*RO investigated thoroughly: price.ro/compari.ro blocked (cookie-wall), eMAG has NO clean ANR 50ml serum listing (luxury beauty sells via Notino.ro/Douglas, not eMAG). Real RO market = 5 sellers (Notino.ro, Fragrance.com, Creme de la Creme, 2x eBay). This thinness is a genuine market fact, not a scraping gap — and itself an insight (few authorized sellers = coverage risk).

## Notes
- Aggregators themselves (Heureka/idealo/Ceneo as a "seller") are excluded — they advertise, they don't sell.
- FX approximate (CZK 25, PLN 4.3, RON 4.97). For pitch, use ECB daily from EcomRadar DB.
- Raw: det_de.json, det_fr.json, det_pl.json (idealo/ceneo), heureka_detail.json. Older Apify pulls: anr_*.json.
- Product variant distinction (Multi-Recovery vs Complex II) is itself a product feature: "we tell apart SKUs that blur together for you."
