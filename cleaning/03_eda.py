"""
Step 5: exploratory data analysis on the cleaned dataset.
Purpose: produce the numbers needed to finalize the 7 charts before Tableau.

Inputs:
    data/processed/endangered_languages_clean.csv
    data/processed/endangered_languages_countries_long.csv

Output:
    documentation/eda_report.md
"""
import pandas as pd
from pathlib import Path

CLEAN = Path("data/processed/endangered_languages_clean.csv")
LONG  = Path("data/processed/endangered_languages_countries_long.csv")
OUT   = Path("documentation/eda_report.md")

df = pd.read_csv(CLEAN, encoding="utf-8")
lng = pd.read_csv(LONG, encoding="utf-8")

L = []
def w(s=""): L.append(s)

w("# EDA Report — Voices at Risk\n")
w(f"- Clean dataset rows: {len(df)}")
w(f"- Country-long rows: {len(lng)}\n")

# 1. Category counts (KPI 3 input)
w("## 1. Category counts (KPI 3 input)\n")
w("| Category | Count | % |")
w("|---|---|---|")
for v, n in df["Degree of endangerment"].value_counts().items():
    w(f"| {v} | {n} | {100*n/len(df):.1f}% |")

# 2. Speaker stats (KPI 2 input)
w("\n## 2. Speakers — overall (KPI 2 input)\n")
s = df["Number of speakers"]
w(f"- Non-null: {s.notna().sum()} / {len(df)}")
w(f"- Min: {s.min()} | Median: {int(s.median())} | Max: {int(s.max()):,}")
w(f"- Sum of reported speakers: {int(s.sum()):,}")
w(f"- Records with exactly 0 speakers: {(s==0).sum()}")

# 3. Speaker distribution by order of magnitude (Chart 6 input)
w("\n## 3. Speakers by order of magnitude (Chart 6 bin design)\n")
bins = [0, 1, 10, 100, 1_000, 10_000, 100_000, 1_000_000, 10_000_000]
labels = ["0", "1–9", "10–99", "100–999", "1k–9,999", "10k–99,999", "100k–999,999", "1M+"]
b = pd.cut(s.dropna(), bins=bins, labels=labels, right=False)
w("| Range | Count |")
w("|---|---|")
for v, n in b.value_counts().sort_index().items():
    w(f"| {v} | {n} |")

# 4. Top 15 languages by speakers (Chart 3 input)
w("\n## 4. Top 15 languages by reported speakers (Chart 3 input)\n")
w("| # | Language | Speakers | Category |")
w("|---|---|---|---|")
top = df.nlargest(15, "Number of speakers")[["Name in English","Number of speakers","Degree of endangerment"]]
for i, (_, r) in enumerate(top.iterrows(), 1):
    w(f"| {i} | {r['Name in English']} | {int(r['Number of speakers']):,} | {r['Degree of endangerment']} |")

# 5. Top countries (Chart 4 input — from long table only)
w("\n## 5. Top 15 countries by distinct language records (Chart 4 input)\n")
w("| # | Country | Language records |")
w("|---|---|---|")
for i, (c, n) in enumerate(lng["Country"].value_counts().head(15).items(), 1):
    w(f"| {i} | {c} | {n} |")

# 6. Category × speaker range
w("\n## 6. Category × speaker range (Chart 5 / 6 input)\n")
df["_bin"] = pd.cut(df["Number of speakers"], bins=bins, labels=labels, right=False)
ct = pd.crosstab(df["Degree of endangerment"], df["_bin"])
w(ct.to_markdown())

# 7. Map coverage
w("\n## 7. Map coverage (Chart 1)\n")
w(f"- Records with coordinates: {df['Has coordinates'].sum()} / {len(df)}")
w(f"- Records missing coordinates: {(~df['Has coordinates']).sum()}")

# 8. Extinct records with nonzero speakers
w("\n## 8. Extinct records with nonzero reported speakers (interpretation flag)\n")
ext = df[(df["Degree of endangerment"] == "Extinct") & (df["Number of speakers"].fillna(0) > 0)]
w(f"- Count: {len(ext)}")
if len(ext):
    w("| ID | Language | Speakers |")
    w("|---|---|---|")
    for _, r in ext.iterrows():
        w(f"| {r['ID']} | {r['Name in English']} | {int(r['Number of speakers'])} |")

# 9. Null speaker rate by category
w("\n## 9. Speaker nulls by category (data-quality flag)\n")
w("| Category | Total | Null speakers | Null % |")
w("|---|---|---|---|")
for cat, grp in df.groupby("Degree of endangerment"):
    nnull = grp["Number of speakers"].isna().sum()
    w(f"| {cat} | {len(grp)} | {nnull} | {100*nnull/len(grp):.1f}% |")

OUT.write_text("\n".join(L), encoding="utf-8")
print(f"Wrote {OUT}")