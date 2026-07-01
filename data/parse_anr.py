#!/usr/bin/env python3
"""Parse Apify Google Shopping ANR results → clean avg/min EUR + seller count per country.
STRICT: only the 50ml Advanced Night Repair Serum (Synchronized Multi-Recovery Complex).
Excludes 65ml Overnight Treatment (a cream), Concentrate, Intense Reset, Recovery Complex II, Power Pair, sets."""
import json, re, statistics

DIR = "/private/tmp/claude-501/-Users-petrrohan-Developer-DEV-products-ecomradar/37528dc7-95ed-4614-87b2-14e9b82d33e9/scratchpad"

FX = {"fr": 1.0, "de": 1.0, "cz": 1/25.0, "pl": 1/4.3, "ro": 1/4.97, "at": 1.0}
CURR = {"fr": "EUR", "de": "EUR", "cz": "CZK", "pl": "PLN", "ro": "RON", "at": "EUR"}

CORE = re.compile(r"advanced\s*night\s*repair", re.I)
# HARD exclude — different products / sizes / bundles
EXCLUDE = re.compile(
    r"\b(overnight\s*treatment|65\s*ml|intense\s*reset|concentr|koncentr|"
    r"recovery\s*complex\s*ii|complex\s*ii|power\s*pair|day\s*wear|daywear|"
    r"duo|coffret|set|gift|geschenk|zestaw|coffre|kit|"
    r"eye|augen|yeux|oczy|"
    r"7\s*ml|15\s*ml|20\s*ml|30\s*ml|100\s*ml|"
    r"sample|probe|muster|próbka|miniatur|\bmini\b)\b", re.I)

BAND_EUR = (40, 130)

def size_of(title):
    m = re.search(r"(\d+)\s*ml", title, re.I)
    return int(m.group(1)) if m else None

def clean_country(gl):
    d = json.load(open(f"{DIR}/anr_{gl}.json"))
    offers = []
    seen = set()
    for page in d:
        for r in page.get("shopping_results", []):
            title = r.get("title", "") or ""
            src = (r.get("source", "") or "").strip()
            price = r.get("extracted_price")
            if price is None:
                continue
            if not CORE.search(title):
                continue
            if EXCLUDE.search(title):
                continue
            sz = size_of(title)
            # if a size is stated, it MUST be 50ml; if no size stated, keep (default ANR serum = 50ml)
            if sz is not None and sz != 50:
                continue
            eur = round(price * FX[gl], 2)
            if not (BAND_EUR[0] <= eur <= BAND_EUR[1]):
                continue
            offers.append({"eur": eur, "src": src, "title": title[:55], "local": price, "size": sz})
            seen.add(src.lower())
    return offers, seen

print("STRICT 50ml Advanced Night Repair Serum only\n")
print(f"{'CTY':<4} {'CURR':<5} {'#offer':>6} {'#shop':>6} {'avg€':>7} {'min€':>7} {'max€':>7}")
print("-" * 52)
result = {}
order = ["fr", "de", "cz", "pl", "ro", "at"]
for gl in order:
    import os
    if not os.path.exists(f"{DIR}/anr_{gl}.json"):
        continue
    offers, sources = clean_country(gl)
    if not offers:
        print(f"{gl.upper():<4} {CURR[gl]:<5} {'0':>6}  — no clean 50ml offers")
        continue
    eurs = [o["eur"] for o in offers]
    result[gl.upper()] = {"avg": round(statistics.mean(eurs)), "min": round(min(eurs)),
                          "max": round(max(eurs)), "offers": len(offers), "shops": len(sources)}
    print(f"{gl.upper():<4} {CURR[gl]:<5} {len(offers):>6} {len(sources):>6} "
          f"{result[gl.upper()]['avg']:>7} {result[gl.upper()]['min']:>7} {result[gl.upper()]['max']:>7}")

print("\n=== JS chart arrays ===")
oc = [c.upper() for c in order if c.upper() in result]
print("labels =", oc)
print("avg    =", [result[c]["avg"] for c in oc])
print("min    =", [result[c]["min"] for c in oc])
print("sellers=", [result[c]["shops"] for c in oc])

print("\n=== all clean 50ml offers (verify apples-to-apples) ===")
for gl in order:
    import os
    if not os.path.exists(f"{DIR}/anr_{gl}.json"):
        continue
    offers, _ = clean_country(gl)
    if not offers: continue
    print(f"\n{gl.upper()}:")
    for o in sorted(offers, key=lambda x: x["eur"]):
        sz = f"{o['size']}ml" if o['size'] else "(no size)"
        print(f"  {o['eur']:>7}€ | {sz:<10} | {o['src'][:22]:<22} | {o['title']}")
