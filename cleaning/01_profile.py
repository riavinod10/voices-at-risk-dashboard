# cleaning/01_profile.py
"""Step 1: profile the raw dataset. Read-only. Writes documentation/data_profile.md."""
import pandas as pd, numpy as np, hashlib, re
from pathlib import Path

RAW = Path("data/raw/endangered_languages_raw.csv")
OUT = Path("documentation/data_profile.md")
OUT.parent.mkdir(parents=True, exist_ok=True)

raw_bytes = RAW.read_bytes()
sha = hashlib.sha256(raw_bytes).hexdigest()[:16]

# Try encodings in order; record which one worked.
df, used_enc = None, None
for enc in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
    try:
        df = pd.read_csv(RAW, encoding=enc); used_enc = enc; break
    except UnicodeDecodeError:
        continue
assert df is not None, "Could not read file with any candidate encoding."

L = []
w = L.append
w(f"# Data Profile — Endangered Languages\n")
w(f"- File: `{RAW.name}`  \n- SHA-256 (first 16): `{sha}`  \n- Encoding that read successfully: `{used_enc}`\n")

# --- shape / schema ---
w(f"## 1. Shape & schema\n")
w(f"Rows: **{len(df)}**  |  Columns: **{df.shape[1]}**\n")
w("| # | Column | dtype | non-null | null | null % | distinct |")
w("|---|--------|-------|----------|------|--------|----------|")
for i, c in enumerate(df.columns, 1):
    nn = df[c].notna().sum()
    w(f"| {i} | `{c}` | {df[c].dtype} | {nn} | {len(df)-nn} | "
      f"{100*(len(df)-nn)/len(df):.1f}% | {df[c].nunique(dropna=True)} |")

# --- mojibake detection ---
w(f"\n## 2. Encoding / mojibake check\n")
w(f"Read as `{used_enc}`. Heuristic: count of `Ã`, `Â`, `â€` per text column.\n")
w("| Column | Ã | Â | â€ | sample suspect value |")
w("|--------|---|---|-----|----------------------|")
for c in df.select_dtypes(include="object").columns:
    s = df[c].dropna().astype(str)
    a, b, d = s.str.count("Ã").sum(), s.str.count("Â").sum(), s.str.count("â€").sum()
    if a + b + d:
        bad = s[s.str.contains("Ã|Â|â€", regex=True, na=False)]
        w(f"| `{c}` | {a} | {b} | {d} | `{bad.iloc[0][:60]}` |")
w("\n> Columns absent from this table showed no mojibake markers.")

# --- endangerment categories (verbatim) ---
cat_col = next((c for c in df.columns if "endanger" in c.lower()), None)
if cat_col:
    w(f"\n## 3. `{cat_col}` — verbatim value counts\n")
    w("Raw strings, unmodified. Watch for case/whitespace variants.\n")
    w("| value | count | repr |")
    w("|-------|-------|------|")
    for v, n in df[cat_col].value_counts(dropna=False).items():
        w(f"| {v} | {n} | `{repr(v)}` |")

# --- number of speakers ---
spk = next((c for c in df.columns if "speaker" in c.lower()), None)
if spk:
    s = df[spk]
    nonnum = s.dropna().astype(str)[~s.dropna().astype(str).str.fullmatch(r"\d+(\.\d+)?")]
    w(f"\n## 4. `{spk}` — numeric parseability\n")
    w(f"- Non-null: {s.notna().sum()} / {len(df)}  |  dtype read as: `{s.dtype}`")
    w(f"- Values failing a strict `\\d+` test: **{len(nonnum)}**")
    if len(nonnum):
        w(f"- Distinct offending patterns (up to 20): `{sorted(nonnum.unique())[:20]}`")
    num = pd.to_numeric(s.astype(str).str.replace(r"[,\s]", "", regex=True), errors="coerce")
    if num.notna().any():
        w(f"- After stripping commas: min={num.min():,.0f}  median={num.median():,.0f}  max={num.max():,.0f}")

# --- coordinates ---
lat = next((c for c in df.columns if "lat" in c.lower()), None)
lon = next((c for c in df.columns if "lon" in c.lower()), None)
if lat and lon:
    la, lo = pd.to_numeric(df[lat], errors="coerce"), pd.to_numeric(df[lon], errors="coerce")
    w(f"\n## 5. Coordinates\n")
    w(f"- `{lat}` null: {la.isna().sum()} | out of [-90,90]: {((la<-90)|(la>90)).sum()}")
    w(f"- `{lon}` null: {lo.isna().sum()} | out of [-180,180]: {((lo<-180)|(lo>180)).sum()}")
    w(f"- Exact (0,0) rows: {((la==0)&(lo==0)).sum()}")
    w(f"- Distinct coordinate pairs: {df[[lat,lon]].drop_duplicates().shape[0]} of {len(df)} rows")

# --- countries field ---
cty = next((c for c in df.columns if "countr" in c.lower() and "code" not in c.lower()), None)
if cty:
    s = df[cty].dropna().astype(str)
    w(f"\n## 6. `{cty}` — multi-value structure\n")
    for delim, name in [(r";", "semicolon"), (r",", "comma"), (r"\|", "pipe"), (r"/", "slash")]:
        w(f"- Rows containing `{name}`: {s.str.contains(delim, regex=True).sum()}")
    w(f"- Max values in one row (comma-split): {s.str.count(',').max() + 1}")
    w(f"- Example multi-value row: `{s[s.str.count(',')>0].iloc[0][:120] if (s.str.count(',')>0).any() else 'n/a'}`")

# --- duplicates ---
idc = next((c for c in df.columns if c.lower() in ("id", "language_id")), None)
w(f"\n## 7. Duplicates\n")
w(f"- Fully duplicated rows: {df.duplicated().sum()}")
if idc:
    w(f"- Duplicated `{idc}`: {df[idc].duplicated().sum()}")

w("\n## 8. Sample rows\n")
w(df.head(5).to_markdown(index=False))

OUT.write_text("\n".join(L), encoding="utf-8")
print(f"Wrote {OUT} | rows={len(df)} cols={df.shape[1]} enc={used_enc}")