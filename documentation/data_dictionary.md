# Data Dictionary — Voices at Risk

**Source:** UNESCO Atlas of the World's Languages in Danger
(Kaggle: "Extinct Languages" — title is broader than contents)

**Clean rows:** 2722 · **Source SHA-256:** `26b55da75fc5a567a974c2c97b0a3f65a951def69da4875ac69696b3dabd0b9f`

The raw dataset is preserved unchanged at `data/raw/endangered_languages_raw.csv`.
The cleaned version adds 4 derived columns (documented below).

---

## Original columns (15)

| # | Column | Type | Null % | Description | Notes |
|---|--------|------|--------|-------------|-------|
| 1 | `ID` | integer | 0.0% | Unique record identifier | 2722 unique values |
| 2 | `Name in English` | string | 0.0% | Language name in English | 2715 distinct — 7 names repeat across countries (e.g. Mohawk variants) |
| 3 | `Name in French` | string | 0.8% | Language name in French | Some records lack a French form |
| 4 | `Name in Spanish` | string | 0.8% | Language name in Spanish | Some records lack a Spanish form |
| 5 | `Countries` | string | 0.0% | Comma-separated country names | Max 29 countries in one record (Romani) |
| 6 | `Country codes alpha 3` | string | 0.0% | Comma-separated ISO 3166-1 alpha-3 codes | Two source errors, see below |
| 7 | `ISO639-3 codes` | string | 9.7% | Comma-separated ISO 639-3 language codes | Blank for some extinct/undocumented languages |
| 8 | `Degree of endangerment` | string | 0.0% | UNESCO classification | 5 values verbatim: Vulnerable, Definitely endangered, Severely endangered, Critically endangered, Extinct |
| 9 | `Alternate names` | string | 41.8% | Semicolon-separated alternate names | Often in native script |
| 10 | `Name in the language` | string | 99.0% | Endonym (name in the language itself) | Almost always blank — handle gracefully in Detail Panel |
| 11 | `Number of speakers` | integer | 6.7% | Reported speaker count | Integer, no commas. 0 is a real value (257 records). Do not impute. |
| 12 | `Sources` | string | 23.6% | Bibliographic citations | Free-form; multi-line in some rows |
| 13 | `Latitude` | decimal | 0.1% | WGS-84 latitude | 3 nulls; all values within [-90, 90] |
| 14 | `Longitude` | decimal | 0.1% | WGS-84 longitude | 3 nulls; all values within [-180, 180] |
| 15 | `Description of the location` | string | 31.3% | Geographic scope description | Multi-line; often lists regions/provinces |

---

## Derived columns added during cleaning (4)

| # | Column | Type | Description | Rule |
|---|--------|------|-------------|------|
| 16 | `Country count` | integer | Number of countries in the `Countries` field | Split on `, `, count non-empty |
| 17 | `Has coordinates` | boolean | True if both lat and lon are non-null | Map-readiness flag |
| 18 | `Has speaker count` | boolean | True if `Number of speakers` is non-null | Speaker-completeness flag |
| 19 | `Country codes alpha 3 (corrected)` | string | Source country codes with two errors fixed | `BRB`→`BLR` (Belarus), `ZAI`→`COD` (DR Congo) |

The original `Country codes alpha 3` column is preserved unchanged. Use the corrected column for any downstream analysis; cite the original when discussing data provenance.

---

## Country-long table (separate file)

`data/processed/endangered_languages_countries_long.csv`

One row per (language record × country). 3074 rows. Columns:

| Column | Description |
|--------|-------------|
| `ID` | Foreign key to the clean dataset |
| `Name in English` | Language name |
| `Degree of endangerment` | Category |
| `Country` | Single country |
| `Country code alpha 3` | Corrected code |

**Use this table for Chart 4 and Chart 7 ONLY.** Never for KPI sums — it double-counts multilingual records.

---

## Interpretation rules

1. **One row = one language record.** ISO code count and country count do not change this.
2. **Speaker sums exclude nulls, not treat them as 0.** Null ≠ 0. The 257 records with `0` have a recorded zero; the 183 null records have no count.
3. **Two source errors are preserved in the original column** and corrected in a separate column. Do not silently edit the original.
4. **Country names use UN-era naming** (`Iran (Islamic Republic of)`, `Bolivia (Plurinational State of)`). Preserve as published for fidelity.
5. **Extinct does not always mean 0 speakers.** 5 records marked Extinct have nonzero counts (listed in `eda_report.md` §8). Treat as source-recorded last-speaker counts, not errors.