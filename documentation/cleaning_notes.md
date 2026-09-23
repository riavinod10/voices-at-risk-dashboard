# Cleaning Notes — Voices at Risk

## Source
- Raw file: `data/raw/endangered_languages_raw.csv`
- SHA-256: 26b55da75fc5a567… (see `cleaning_log.txt` for full hash)
- Rows: 2722 · Columns: 15
- Read and written as UTF-8.

## Decisions

| Area | Decision | Reason |
|------|----------|--------|
| Encoding | Read/write as UTF-8, no repair | Profile showed zero mojibake markers. |
| Missing values | Retained as null; no fabrication | Preserve provenance. Nulls are informative. |
| `Number of speakers` | Cast to nullable `Int64`; keep 0 as 0 | 0 is a recorded value, not missing. |
| `Latitude` / `Longitude` | Cast to float; keep nulls | 3 records lack coordinates; they simply won't appear on the map. |
| `Degree of endangerment` | Used verbatim (5 values) | No whitespace or case variants found. |
| Duplicates | None removed | 0 duplicate IDs, 0 duplicate rows. |
| `Country codes alpha 3` | Original preserved; corrected column added | Fix: `BRB`→`BLR` (Belarus), `ZAI`→`COD` (DR Congo). |
| Country names | Preserved as published | UN-era naming; do not normalize. |
| Country expansion | Separate long-format table for Chart 4 only | Splitting multi-country rows would double-count KPIs. |

## Derived columns added to the cleaned dataset
- `Country count` — integer, number of comma-separated countries in the record
- `Has coordinates` — boolean
- `Has speaker count` — boolean
- `Country codes alpha 3 (corrected)` — original codes with the two fixes applied

## Row-level interpretation rules
- **One row = one language record.** ISO code count and country count do not change this.
- **Country-long table** (`endangered_languages_countries_long.csv`) must only be used for Chart 4 (geographic distribution). Not for sums, counts, or KPIs.
- Speaker sums use only `Number of speakers`; missing values are excluded, never treated as 0.

## Known limitations
- The dataset is not a live census. Speaker counts are as reported by the source, not current.
- Some records retain source-side naming ("Iran (Islamic Republic of)") for fidelity.
- Two country-code errors in the source were corrected; the originals are preserved in the as-published column.