#!/usr/bin/env python3
"""Parse Apify Google Shopping ANR results → clean avg/min EUR + seller count per country."""
import json, re, statistics

DIR = "/private/tmp/claude-501/-Users-petrrohan-Developer-DEV-products-ecomradar/37528dc7-95ed-4614-87b2-14e9b82d33e9/scratchpad"

# FX to EUR (approx, 2026-07-01 — konzervativní; při finálu použít ECB daily z DB)
FX = {"fr": 1.0, "de": 1.0, "cz": 1/25.0, "pl": 1/4.3, "ro": 1/4.97}
CURR = {"fr": "EUR", "de": "EUR", "cz": "CZK", "pl": "PLN", "ro": "RON"}

# šum: vyhodit sety, dua, mini, edice, koncentráty, jiné objemy
NOISE = re.compile(r"\b(duo|coffret|set|gift|geschenk|zestaw|coffre|kit|"
                   r"pink ribbon|eye|augen|yeux|oczy|concentr|koncentr|"
                   r"7ml|7 ml|15ml|15 ml|20ml|20 ml|30ml|30 ml|100ml|100 ml|"
                   r"sample|probe|muster|próbka|miniatur|mini)\b", re.I)
# musí obsahovat advanced night repair
CORE = re.compile(r"advanced\s*night\s*repair", re.I)

# sanity price band per country (EUR ekvivalent) — ANR 50ml RRP ~90-105€, gray dolů k ~55
BAND_EUR = (45, 130)

def clean_country(gl):
    d = json.load(open(f"{DIR}/anr_{gl}.json"))
    offers = []
    seen_sources = set()
    for page in d:
        for r in page.get("shopping_results", []):
            title = r.get("title", "") or ""
            src = (r.get("source", "") or "").strip()
            price = r.get("extracted_price")
            if price is None:
                continue
            if not CORE.search(title):
                continue
            if NOISE.search(title):
                continue
            eur = round(price * FX[gl], 2)
            if not (BAND_EUR[0] <= eur <= BAND_EUR[1]):
                continue
            offers.append({"eur": eur, "src": src, "title": title[:50], "local": price})
            seen_sources.add(src.lower())
    return offers, seen_sources

print(f"{'CTY':<4} {'CURR':<5} {'#offer':>6} {'#shop':>6} {'avg€':>7} {'min€':>7} {'max€':>7}")
print("-" * 52)
result = {}
for gl in ["fr", "de", "cz", "pl", "ro"]:
    offers, sources = clean_country(gl)
    if not offers:
        print(f"{gl.upper():<4} {CURR[gl]:<5} {'0':>6}  — no clean offers")
        continue
    eurs = [o["eur"] for o in offers]
    avg = round(statistics.mean(eurs))
    mn = round(min(eurs))
    mx = round(max(eurs))
    nshop = len(sources)
    result[gl.upper()] = {"avg": avg, "min": mn, "max": mx, "offers": len(offers), "shops": nshop}
    print(f"{gl.upper():<4} {CURR[gl]:<5} {len(offers):>6} {nshop:>6} {avg:>7} {mn:>7} {mx:>7}")

print("\n=== JS chart arrays (order FR,DE,CZ,PL,RO) ===")
order = ["FR", "DE", "CZ", "PL", "RO"]
print("avg    =", [result.get(c, {}).get("avg", 0) for c in order])
print("min    =", [result.get(c, {}).get("min", 0) for c in order])
print("sellers=", [result.get(c, {}).get("shops", 0) for c in order])

print("\n=== sample clean offers per country (verify) ===")
for gl in ["fr", "de", "cz", "pl", "ro"]:
    offers, _ = clean_country(gl)
    print(f"\n{gl.upper()}:")
    for o in sorted(offers, key=lambda x: x["eur"])[:6]:
        print(f"  {o['eur']:>7}€ ({o['local']} {CURR[gl]}) | {o['src'][:24]:<24} | {o['title']}")
