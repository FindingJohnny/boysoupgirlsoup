"""Rebuild the SOUPS list inside index.html from scripts/soups.json.

Looks up each soup's Wikipedia article for its photo, so the game itself never
has to call Wikipedia. Run: python3 scripts/build_soups.py
"""
import json, pathlib, re, sys, urllib.parse, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
UA = "GirlSoupBoySoup/1.0 (https://github.com/FindingJohnny/boysoupgirlsoup)"


def lookup(titles):
    """Map each requested title to (canonical title, photo url) for articles that exist."""
    found = {}
    for i in range(0, len(titles), 40):
        batch = titles[i:i + 40]
        q = urllib.parse.urlencode({
            "action": "query", "format": "json", "formatversion": 2, "redirects": 1,
            "prop": "pageimages", "piprop": "thumbnail", "pithumbsize": 320,
            "titles": "|".join(batch),
        })
        req = urllib.request.Request("https://en.wikipedia.org/w/api.php?" + q, headers={"User-Agent": UA})
        data = json.load(urllib.request.urlopen(req))["query"]
        alias = {t: t for t in batch}
        for step in ("normalized", "redirects"):
            for m in data.get(step, []):
                for k, v in alias.items():
                    if v == m["from"]:
                        alias[k] = m["to"]
        pages = {p["title"]: p for p in data["pages"] if not p.get("missing") and not p.get("invalid")}
        for t, canon in alias.items():
            if canon in pages:
                found[t] = (canon, pages[canon].get("thumbnail", {}).get("source", ""))
    return found


def main():
    soups = json.loads((ROOT / "scripts" / "soups.json").read_text())
    names = [s["name"].lower() for s in soups]
    dupes = {n for n in names if names.count(n) > 1}
    if dupes:
        sys.exit("duplicate soups: " + ", ".join(sorted(dupes)))
    info = lookup(sorted({s["wiki"] for s in soups if s.get("wiki")}))
    rows, missing, nophoto = [], [], []
    for kind in ("girl", "boy"):
        side = sorted((s for s in soups if s["kind"] == kind), key=lambda s: s["rank"])
        for rank, s in enumerate(side, 1):  # renumber so ranks are always 1..N
            title, img = info.get(s.get("wiki", ""), ("", ""))
            if s.get("wiki") and not title:
                missing.append(s["wiki"])
            elif title and not img:
                nophoto.append(title)
            rows.append([s["name"], kind, rank, title, img, s.get("recipe", "")])
    body = ",\n".join(" " + json.dumps(r, ensure_ascii=False) for r in rows)
    page = ROOT / "index.html"
    html = page.read_text()
    new = re.sub(r"(// SOUPS:BEGIN\n).*?(\n// SOUPS:END)", lambda m: m.group(1) + "const SOUPS=[\n" + body + "\n];" + m.group(2), html, count=1, flags=re.S)
    if new == html and "// SOUPS:BEGIN" not in html:
        sys.exit("SOUPS markers not found in index.html")
    page.write_text(new)
    print(f"{len(rows)} soups ({sum(r[1] == 'girl' for r in rows)} girl, {sum(r[1] == 'boy' for r in rows)} boy), "
          f"{sum(bool(r[4]) for r in rows)} with photos")
    if missing:
        print("no such Wikipedia article:", ", ".join(missing))
    if nophoto:
        print("article has no photo:", ", ".join(nophoto))


main()
