# Voices at Risk: Mapping the World's Endangered Languages

An interactive Tableau dashboard exploring the global distribution, endangerment severity, and reported speaker populations of the world's endangered languages.

**CA3 Data Visualization Project**

---

## Overview

This project analyses **2,722 language records** from the UNESCO Atlas of the World's Languages in Danger. It visualises where endangered languages are located, how severe their endangerment is, and how reported speaker populations relate to endangerment category.

The final deliverable is a **two-page interactive Tableau Public dashboard** plus a third page documenting methodology, ethics, and limitations.

**Live dashboard:** _link added at completion_

---

## Research Question

> How are endangered languages distributed across the world, how does their degree of endangerment vary, and what patterns can be observed between endangerment, geography, and reported number of speakers?

---

## Objectives

1. Visualise the global geographic distribution of endangered languages.
2. Compare the five UNESCO endangerment categories by frequency.
3. Identify languages with the largest reported speaker populations despite being classified as endangered.
4. Examine the observed relationship between speaker counts and endangerment severity.
5. Provide an interactive exploration tool with filters, parameters, and cross-chart actions.

---

## Dataset

| | |
|---|---|
| **Name** | Extinct Languages — Kaggle |
| **Original source** | UNESCO Atlas of the World's Languages in Danger |
| **URL** | https://www.kaggle.com/datasets/the-guardian/extinct-languages |
| **Size** | 2,722 records × 15 columns |
| **Raw file SHA-256** | `26b55da75fc5a567a974c2c97b0a3f65a951def69da4875ac69696b3dabd0b9f` |

The Kaggle title is broader than the dataset's actual contents — every record is either an endangered language or an extinct one, not exclusively extinct.

---

## Repository Structure

```
Voices-at-Risk/
├── data/
│   ├── raw/
│   │   └── endangered_languages_raw.csv              # Unmodified source
│   └── processed/
│       ├── endangered_languages_clean.csv            # 2,722 rows, 15 + 4 derived cols
│       └── endangered_languages_countries_long.csv   # 3,074 rows, Chart 4/7 only
├── cleaning/
│   ├── 01_profile.py                                 # Raw data profiling
│   ├── 02_clean.py                                   # Cleaning pipeline
│   └── 03_eda.py                                     # Exploratory analysis
├── documentation/
│   ├── data_profile.md                               # Raw data profile
│   ├── cleaning_notes.md                             # Cleaning decisions
│   ├── cleaning_log.txt                              # Run log with SHA
│   ├── eda_report.md                                 # EDA output
│   ├── data_dictionary.md                            # Column reference
│   ├── tableau_calculated_fields.md                  # Tableau calc fields
│   ├── dashboard_spec.md                             # Full chart specification
│   ├── dashboard3_about_ethics.md                    # About/Methodology/Ethics copy
│   └── tableau_build_guide.md                        # Step-by-step build instructions
├── tableau/
│   └── Voices_at_Risk.twbx                           # Final workbook
├── .gitignore
└── README.md
```

---

## Data Pipeline

```
RAW DATA
    ↓
DATA QUALITY CHECK      (cleaning/01_profile.py)
    ↓
DATA CLEANING           (cleaning/02_clean.py)
    ↓
DATA VALIDATION         (integrity asserts in 02_clean.py)
    ↓
CLEAN DATASET           (data/processed/*.csv)
    ↓
EDA                     (cleaning/03_eda.py)
    ↓
TABLEAU                 (tableau/Voices_at_Risk.twbx)
    ↓
INTERACTIVE DASHBOARD
```

The raw file is never modified. All work occurs on a cleaned copy.

---

## Data Cleaning Summary

| Area | Decision |
|------|----------|
| Encoding | UTF-8 read/write. No mojibake detected. |
| Missing values | Retained as null. Never fabricated or imputed. |
| Number of speakers | Cast to nullable `Int64`. Zero preserved as recorded (257 records). |
| Coordinates | Cast to float. Nulls retained (3 records). |
| Endangerment categories | Verbatim — 5 values, no variants found. |
| Duplicates | None removed — 0 duplicates found. |
| Country codes | Originals preserved. `BRB`→`BLR` (Belarus), `ZAI`→`COD` (DR Congo) added in a corrected column. |
| Country names | Preserved as published (UN-era naming). |
| Multi-country rows | Split into a separate long table for Chart 4/7 only. Never used for KPIs or speaker sums. |

Full detail in [`documentation/cleaning_notes.md`](documentation/cleaning_notes.md).

---

## Dashboard

### Dashboard 1 — Global Overview

Immediate overview of the global situation.

- **4 KPI cards:** Total languages · Total reported speakers · Endangered languages · Countries represented
- **Chart 1:** World map — one circle per language, sized by speakers, coloured by endangerment
- **Chart 2:** Languages by endangerment category
- **Chart 3:** Top N languages by reported speaker count (parameter-driven)
- **Chart 4:** Geographic distribution by country (Top 20)

### Dashboard 2 — Language Risk Explorer

Deeper analytical exploration.

- **Chart 5:** Speakers vs endangerment — box plot with jittered points, log scale
- **Chart 6:** Speaker distribution across order-of-magnitude bins
- **Chart 7:** Endangerment composition by country (100% stacked)
- **Language Detail Panel:** Shows selected language's full metadata

### Dashboard 3 — About / Methodology / Ethics

Text-only page covering provenance, cleaning, ethics, privacy, security, limitations, and Tableau Creator vs Viewer.

---

## Visualizations (7 charts + 4 KPIs)

| # | Chart | Type |
|---|-------|------|
| 1 | World Map | Symbol map |
| 2 | Languages by Category | Horizontal bar |
| 3 | Top N by Speakers | Horizontal bar + parameter |
| 4 | Geographic Distribution | Horizontal bar (Top 20) |
| 5 | Speakers vs Endangerment | Box plot + jitter |
| 6 | Speaker Distribution | Stacked bar |
| 7 | Endangerment Composition | 100% stacked bar |

Full spec: [`documentation/dashboard_spec.md`](documentation/dashboard_spec.md).

---

## Interactivity

- **Global filters:** Degree of endangerment · Country · Speaker range
- **Parameters:** Top N (5 / 10 / 15 / 20) · Speaker range (All / 0 / 1–999 / 1k–99,999 / 100k+)
- **Dashboard actions:** Map click → cross-filter · Category hover → highlight · Reset button

---

## Key Findings

1. **Critically endangered languages in this dataset never exceed 100,000 reported speakers.** No record in that category has a six-figure speaker count. The pattern reverses smoothly across categories.
2. **The largest "endangered" languages by speaker count are in the mildest category.** The Top-15 by speakers is entirely Vulnerable and Definitely endangered — 0 records from Critically endangered.
3. **Language diversity concentrates in five countries:** the USA (227 records), India (199), Brazil (190), Indonesia (149), and Russia (148). This reflects survey coverage as much as actual linguistic diversity.
4. **Extinct does not mean zero.** 239 of 253 Extinct records have zero reported speakers; 5 retain a nonzero count, likely reflecting last-speaker documentation.

Full analysis: [`documentation/eda_report.md`](documentation/eda_report.md).

---

## Ethics, Privacy, and Security

Full discussion on Dashboard 3 and in [`documentation/dashboard3_about_ethics.md`](documentation/dashboard3_about_ethics.md). Summary:

- **Cultural sensitivity:** Language endangerment is treated as a documented phenomenon, not a spectacle. Terminology follows the source.
- **Classification:** Categories are the source dataset's own. This project does not independently classify languages.
- **Privacy:** No personal data. Geographic values describe language areas, not individuals.
- **Security:** Raw data unchanged, hash-pinned, and preserved. All transformations documented.
- **Speaker-count uncertainty:** Reported values are estimates, not current census figures.

---

## Limitations

- The dataset is not a live census of global language vitality.
- 183 of 2,722 records lack speaker counts. Totals exclude these.
- 3 records lack coordinates and do not appear on the map.
- Country totals count language records, not distinct languages — multilingual records appear under each listed country.
- UNESCO classifications reflect the assessment at time of publication, not a live assessment.

---

## Tableau Creator vs Viewer

**Creator** — the authoring licence used to build and publish dashboards.

**Viewer** — the consumption licence used to open, filter, and interact with published dashboards. Relevant to anyone opening the Tableau Public link, including the course instructor and the public.

The interactivity built here — filters, parameters, cross-chart actions — is designed to be meaningful to a Viewer, not just a Creator. This is the point of the dashboard: exploration without authoring.

---

## Reproducing This Project

```bash
git clone https://github.com/riavinod10/voices-at-risk-dashboard.git
cd voices-at-risk-dashboard
python -m venv .venv

# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# macOS / Linux
# source .venv/bin/activate

pip install pandas tabulate
python cleaning/01_profile.py
python cleaning/02_clean.py
python cleaning/03_eda.py
```

Then open `tableau/Voices_at_Risk.twbx` in Tableau Public or Tableau Desktop.

---

## Licence and Attribution

Data source: UNESCO Atlas of the World's Languages in Danger, distributed via Kaggle as "Extinct Languages" (https://www.kaggle.com/datasets/the-guardian/extinct-languages).

Project code and documentation: created for academic coursework, CA3.