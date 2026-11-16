import re
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

API = "https://oldschool.runescape.wiki/api.php"
HEADERS = {
    # The wiki asks for a descriptive User-Agent with contact info
    "User-Agent": "WebDataScience course project - your_name@colorado.edu"
}

_session = requests.Session()
_session.headers.update(HEADERS)

# Items to skip entirely (lowercase)
SKIP_ITEMS = {
    "amulet of torture",
    "necklace of anguish",
    "ring of suffering",
    "tormented bracelet",
    "prayer scroll",
    "zenyte",
    "uncut zenyte",
    "spectral spirit shield",
}

# Item in your dataframe (lowercase) -> wiki page that actually has the drop sources
PAGE_ALIASES = {
    "abyssal bludgeon": "Unsired",
    "ancient godsword": "Ancient hilt",
    "armadyl godsword": "Armadyl hilt",
    "bandos godsword": "Bandos hilt",
    "saradomin godsword": "Saradomin hilt",
    "zamorak godsword": "Zamorak hilt",
    "kodai wand": "Kodai insignia",
    "masori body (f)": "Masori body",
    "masori chaps (f)": "Masori chaps",
    "masori mask (f)": "Masori mask",
    "toxic blowpipe (empty)": "Tanzanite fang",
    "zaryte crossbow": "Nihil horn",
}


def _api(**params):
    params.update(format="json", formatversion=2, redirects=1)
    r = _session.get(API, params=params, timeout=30)
    r.raise_for_status()
    return r.json()


def _find_item_sources_index(page):
    """Return the section index of 'Item sources' for a wiki page (or None)."""
    data = _api(action="parse", page=page, prop="sections")
    if "error" in data:
        return None
    for sec in data["parse"]["sections"]:
        if sec["line"].strip().lower() == "item sources":
            return sec["index"]
    return None


def _parse_rarity(cell):
    """Turn a rarity cell into (raw_text, numeric_probability)."""
    raw = cell.get_text(" ", strip=True)
    raw = re.sub(r"\[\d+\]", "", raw).strip()  # drop footnote markers

    frac = cell.get("data-drop-fraction") or raw
    frac = frac.replace(",", "").replace("~", "").strip()

    m = re.search(r"(\d+(?:\.\d+)?)\s*/\s*(\d+(?:\.\d+)?)", frac)
    if m:
        return raw, float(m.group(1)) / float(m.group(2))
    if raw.lower() == "always":
        return raw, 1.0
    return raw, None  # e.g. "Common", "Rare", "Varies"


def get_item_drop_rates(item_name, page_name=None):
    """
    Scrape the 'Item sources' tables from an OSRS wiki item page.
    item_name is the label kept in the output; page_name (optional) is the
    wiki page to scrape when it differs (e.g. 'Ancient hilt' for 'ancient godsword').
    Returns a DataFrame with one row per source/drop-table row.
    """
    page = (page_name or item_name).replace(" ", "_")
    idx = _find_item_sources_index(page)
    if idx is None:
        return pd.DataFrame()

    data = _api(action="parse", page=page, section=idx, prop="text")
    soup = BeautifulSoup(data["parse"]["text"], "lxml")

    rows = []
    for table in soup.select("table.item-drops"):
        heading = table.find_previous(["h2", "h3", "h4"])
        category = heading.get_text(" ", strip=True) if heading else None
        category = re.sub(r"\[.*?\]", "", category or "").strip()

        headers = [th.get_text(" ", strip=True).lower() for th in table.select("tr th")]

        for tr in table.select("tr"):
            cells = tr.find_all("td")
            if not cells or len(cells) < len(headers):
                continue
            rec = dict(zip(headers, cells))

            rarity_raw, rarity_num = (None, None)
            if "rarity" in rec:
                rarity_raw, rarity_num = _parse_rarity(rec["rarity"])

            rows.append({
                "item": item_name,
                "wiki_page": page_name or item_name,
                "category": category,
                "source": rec["source"].get_text(" ", strip=True) if "source" in rec else None,
                "level": rec["level"].get_text(" ", strip=True) if "level" in rec else None,
                "quantity": rec["quantity"].get_text(" ", strip=True) if "quantity" in rec else None,
                "rarity_raw": rarity_raw,
                "drop_rate": rarity_num,  # probability per roll, e.g. 1/34.5 -> 0.029
                "one_in_x": (1 / rarity_num) if rarity_num else None,
            })

    return pd.DataFrame(rows)


def scrape_drop_rates(df, item_col="item", delay=0.5,
                      skip=SKIP_ITEMS, aliases=PAGE_ALIASES):
    """
    Loop over every item in df[item_col] and return one combined DataFrame
    of drop rates from each item's 'Item sources' section.
    Items in `skip` are ignored; items in `aliases` are scraped from the
    mapped wiki page but keep their original name in the 'item' column.
    """
    frames, failed = [], []
    for name in df[item_col].dropna().unique():
        key = name.strip().lower()
        if key in skip:
            continue
        try:
            out = get_item_drop_rates(name, page_name=aliases.get(key))
            if out.empty:
                failed.append(name)
            else:
                frames.append(out)
        except Exception as e:
            print(f"{name}: {e}")
            failed.append(name)
        time.sleep(delay)  # be polite to the wiki

    if failed:
        print("No item sources found for:", failed)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


if __name__ == "__main__":
    items = pd.read_csv("ItemSinkList.csv")
    item_col = "Item"  # change to the column in your CSV that holds item names

    items[item_col] = items[item_col].astype(str).str.strip()

    drops = scrape_drop_rates(items, item_col=item_col)
    print(drops.head(20))

    drops.to_csv("item_drop_rates.csv", index=False)
