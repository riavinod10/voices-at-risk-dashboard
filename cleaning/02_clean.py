"""
Step 4: clean the raw dataset and produce Tableau-ready outputs.

Inputs:
    data/raw/endangered_languages_raw.csv   (never modified)

Outputs:
    data/processed/endangered_languages_clean.csv
    data/processed/endangered_languages_countries_long.csv
    documentation/cleaning_log.txt

Rules are documented in documentation/cleaning_notes.md.
"""
import pandas as pd
import hashlib
from pathlib import Path

RAW = Path("data/raw/endangered_languages_raw.csv")
PROC = Path("data/processed")
DOC = Path("documentation")
PROC.mkdir(parents=True, exist_ok=True)
DOC.mkdir(parents=True, exist_ok=True)

LOG = []
def log(msg):
    LOG.append(msg)
    print(msg)

# --- 1. Read ---------------------------------------------------------------
raw_bytes = RAW.read_bytes()
sha = hashlib.sha256(raw_bytes).hexdigest()
log(f"Read raw file: {RAW}")
log(f"SHA-256: {sha}")

df = pd.read_csv(RAW, encoding="utf-8")
log(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns")

# --- 2. Enforce dtypes -----------------------------------------------------
df["Number of speakers"] = pd.to_numeric(df["Number of speakers"], errors="coerce").astype("Int64")
df["Latitude"]  = pd.to_numeric(df["Latitude"],  errors="coerce")
df["Longitude"] = pd.to_numeric(df["Longitude"], errors="coerce")
log("Casted: Number of speakers -> Int64, Latitude/Longitude -> float64")

# --- 3. Derived columns (do NOT alter originals) ---------------------------
df["Country count"] = (
    df["Countries"].fillna("").str.split(",").apply(lambda parts: len([p for p in parts if p.strip()]))
)
df["Has coordinates"]   = df["Latitude"].notna() & df["Longitude"].notna()
df["Has speaker count"] = df["Number of speakers"].notna()
log("Added derived columns: Country count, Has coordinates, Has speaker count")

# --- 4. Corrected country codes (source errors preserved separately) -------
CODE_FIXES = {"BRB": "BLR", "ZAI": "COD"}
def fix_codes(s):
    if pd.isna(s):
        return s
    return ", ".join(CODE_FIXES.get(c.strip(), c.strip()) for c in s.split(","))

df["Country codes alpha 3 (corrected)"] = df["Country codes alpha 3"].apply(fix_codes)
log(f"Added corrected country codes. Fix map: {CODE_FIXES}")

# --- 5. Write cleaned language-level dataset -------------------------------
clean_path = PROC / "endangered_languages_clean.csv"
df.to_csv(clean_path, index=False, encoding="utf-8")
log(f"Wrote cleaned dataset: {clean_path}")

# --- 6. Country-expanded long table (for Chart 4 ONLY) ---------------------
long_rows = []
for _, row in df.iterrows():
    if pd.isna(row["Countries"]):
        continue
    countries = [c.strip() for c in str(row["Countries"]).split(",") if c.strip()]
    codes = ([c.strip() for c in str(row["Country codes alpha 3 (corrected)"]).split(",")]
             if pd.notna(row["Country codes alpha 3 (corrected)"]) else [])
    for i, country in enumerate(countries):
        long_rows.append({
            "ID": row["ID"],
            "Name in English": row["Name in English"],
            "Degree of endangerment": row["Degree of endangerment"],
            "Country": country,
            "Country code alpha 3": codes[i] if i < len(codes) else None,
        })

long_df = pd.DataFrame(long_rows)
long_path = PROC / "endangered_languages_countries_long.csv"
long_df.to_csv(long_path, index=False, encoding="utf-8")
log(f"Wrote country-long dataset: {long_path} ({len(long_df)} rows)")

# --- 7. Integrity checks ---------------------------------------------------
assert df["ID"].is_unique, "ID must be unique"
assert len(df) == 2722, f"Row count changed: {len(df)}"
assert df["Degree of endangerment"].nunique() == 5, "Category count changed"
log("Integrity checks passed: unique IDs, 2722 rows, 5 categories.")

# --- 8. Write the log ------------------------------------------------------
(DOC / "cleaning_log.txt").write_text("\n".join(LOG), encoding="utf-8")
print("\nDone. Cleaning log written to documentation/cleaning_log.txt")