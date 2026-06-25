"""
csv_to_party_json.py

Converts a party CSV (in the Book1.csv format) to a JSON party entry
ready to paste into data.json.

Usage:
    python3 csv_to_party_json.py Book1.csv

The CSV format expected:
  Rows 0-N:  key/value metadata pairs (name, leader, color, bloc, Website, Top Line, ...)
             until a row where column B is "Title" (the positions header)
  After that: position rows (number, title, summary, source, tags)
"""

import sys
import json
import re
import pandas as pd

def slugify(text):
    return re.sub(r'[^a-z0-9]+', '_', text.lower()).strip('_')

def parse_source(raw):
    if not raw or str(raw).strip() in ('', 'nan', 'add'):
        return []
    raw = str(raw).strip()
    try:
        parsed = json.loads(raw)
        if isinstance(parsed, list):
            return [s.strip() for s in parsed if s.strip()]
        return [raw]
    except json.JSONDecodeError:
        return [raw]

def parse_tags(raw):
    if not raw or str(raw).strip() in ('', 'nan'):
        return []
    return [t.strip() for t in str(raw).split(',') if t.strip()]

def convert(csv_path):
    df = pd.read_csv(csv_path, header=None)

    # ── Find where metadata ends and positions begin ──
    positions_start = None
    for i, row in df.iterrows():
        if str(row.iloc[1]).strip() == 'Title':
            positions_start = i + 1
            break

    if positions_start is None:
        print("ERROR: Could not find 'Title' header row in CSV", file=sys.stderr)
        sys.exit(1)

    # ── Party metadata: all rows before the Title header ──
    meta = {}
    for _, row in df.iloc[:positions_start - 1].iterrows():
        key = str(row.iloc[0]).strip()
        val = str(row.iloc[1]).strip() if not pd.isna(row.iloc[1]) else ''
        if key and key != 'nan':
            meta[key] = val

    party_id = slugify(meta.get('name', 'party'))
    topline  = meta.get('Top Line', '').replace('\\n', '\n')
    website  = meta.get('Website', '')

    # ── Positions ──
    positions = []
    for _, row in df.iloc[positions_start:].iterrows():
        pos_num = str(row.iloc[0]).strip()
        title   = str(row.iloc[1]).strip() if not pd.isna(row.iloc[1]) else ''
        summary = str(row.iloc[2]).strip() if len(row) > 2 and not pd.isna(row.iloc[2]) else ''
        source  = parse_source(row.iloc[3] if len(row) > 3 else None)
        tags    = parse_tags(row.iloc[4] if len(row) > 4 else None)

        if not title or title == 'nan':
            continue

        summary = summary.replace('\\n', '\n')
        pos_id  = f"{party_id}_{pos_num}"

        entry = {
            "id": pos_id,
            "title": title,
            "summary": summary,
            "topics": tags
        }
        if source:
            entry["source"] = source if len(source) > 1 else source[0]

        positions.append(entry)

    # ── Assemble output ──
    out = {"id": party_id, "name": meta.get('name', ''), "color": meta.get('color', '#888888'),
           "leader": meta.get('leader', ''), "bloc": meta.get('bloc', '')}
    if website:
        out["website"] = website
    if topline:
        out["topline"] = topline
    out["positions"] = positions

    print(json.dumps(out, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    path = r"C:\Users\MaxwellLightstone\Desktop\Book1.csv"
    convert(path)