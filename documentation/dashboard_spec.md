# Dashboard Specification — Voices at Risk

Frozen contract for Persons 2 and 3. Data comes from:
- `data/processed/endangered_languages_clean.csv` (language-level)
- `data/processed/endangered_languages_countries_long.csv` (country-level, Chart 4 & 7 ONLY)

All calculated fields are defined in `tableau_calculated_fields.md`.

---

## Workbook structure

| Sheet | Type | Owner |
|-------|------|-------|
| KPI cards (4 separate sheets) | Text/Tile | Person 1 |
| Chart 1 — World Map | Worksheet | Person 2 |
| Chart 2 — Languages by Category | Worksheet | Person 1 |
| Chart 3 — Top Languages by Speakers | Worksheet | Person 1 |
| Chart 4 — Geographic Distribution | Worksheet | Person 2 |
| Chart 5 — Speakers vs Endangerment | Worksheet | Person 3 |
| Chart 6 — Speaker Distribution | Worksheet | Person 3 |
| Chart 7 — Endangerment Composition by Country | Worksheet | Person 3 |
| Dashboard 1 — Global Overview | Dashboard | Person 2 |
| Dashboard 2 — Language Risk Explorer | Dashboard | Person 3 |
| Dashboard 3 — About / Methodology / Ethics | Dashboard | Person 3 |

---

## Dashboard 1 — Global Overview

**Purpose:** Immediate overview of the global situation.

**Layout (top → bottom):**
1. Title bar with project name and reset button
2. KPI strip (4 cards, horizontal row)
3. Chart 1 (world map) — full width, hero
4. Row of 3 charts: Chart 2 (left), Chart 3 (middle), Chart 4 (right)

**Global filters (top of dashboard):**
- `Degree of endangerment` (multi-select)
- `Country` (multi-select — from country-long table)
- `Speaker range` (parameter)

---

## Dashboard 2 — Language Risk Explorer

**Purpose:** Deeper exploration of relationships and individual languages.

**Layout:**
1. Title bar
2. Row 1: Chart 5 (left, wide) | Detail Panel (right)
3. Row 2: Chart 6 (left) | Chart 7 (right)

**Global filters (same as Dashboard 1):**
- `Degree of endangerment`
- `Country`
- `Speaker range`

**Actions:**
- Map on Dashboard 1 → "Use as Filter" → cross-dashboard filter
- Chart 5 → select a language → Detail Panel updates

---

## Dashboard 3 — About / Methodology / Ethics

**Purpose:** Text-only page (Person 3 writes the copy from the framework below).

**Sections:**
1. Project overview (2 paragraphs)
2. Dataset provenance (source, SHA, row count)
3. Cleaning summary (link to `cleaning_notes.md`)
4. Ethics and cultural sensitivity
5. Privacy considerations
6. Security and data integrity
7. Known limitations
8. Tableau Creator vs Viewer comparison
9. Team members

---

## KPI cards — locked definitions

| KPI | Calculated Field | Value | Footnote |
|-----|-----------------|-------|----------|
| Total languages | `COUNTD([ID])` | **2,722** | Full dataset |
| Total reported speakers | `SUM([Number of speakers])` | **136,239,957** | Excludes 183 records with no count |
| Endangered languages | `COUNTD(IF [Degree of endangerment] <> 'Extinct' THEN [ID] END)` | **2,469** | Excludes 253 Extinct records. Total incl. Extinct: 2,722 |
| Countries represented | `COUNTD([Country])` from long table | **252** | Distinct from the country-long table |

---

## Chart specifications

### Chart 1 — World Map

| Property | Value |
|----------|-------|
| Marks | Circle |
| Detail | `ID` |
| Columns | `Longitude` (continuous) |
| Rows | `Latitude` (continuous) |
| Size | `SUM([Number of speakers])`, log scale, range 2–18 px |
| Color | `Degree of endangerment` (5-color palette below) |
| Opacity | 65% |
| Map style | Light / standard |
| Tooltip | `Language display`, Country/Countries, `Speakers (formatted)`, Category, ISO, Location |
| Filters | Category, Country, Speaker range |
| Note | 3 records lack coordinates and won't appear |

**Palette:**
- Vulnerable → `#FEE08B`
- Definitely endangered → `#FDAE61`
- Severely endangered → `#F46D43`
- Critically endangered → `#D73027`
- Extinct → `#67001F`

---

### Chart 2 — Languages by Category

| Property | Value |
|----------|-------|
| Type | Horizontal bar |
| Rows | `Degree of endangerment` (sorted by `Category sort` descending) |
| Columns | `CNT([ID])` |
| Label | `[Count] (XX.X%)` — put count on label, % in tooltip |
| Color | Same 5-color palette |
| Data | 680 / 628 / 607 / 554 / 253 |

---

### Chart 3 — Top N Languages by Speakers

| Property | Value |
|----------|-------|
| Type | Horizontal bar |
| Rows | `Name in English` |
| Columns | `SUM([Number of speakers])` |
| Filter | `Top N Filter = True` (see calc fields doc) |
| Sort | Descending by speaker count |
| Label | Speaker count, thousands-separated |
| Color | Same 5-color palette by category |
| Parameter control | Show `Top N` on dashboard |

---

### Chart 4 — Geographic Distribution

| Property | Value |
|----------|-------|
| Source | Country-long table ONLY |
| Type | Horizontal bar |
| Rows | `Country` |
| Columns | `CNT([ID])` |
| Filter | Top 20 by count |
| Tooltip must say | "Counts language records, not distinct languages." |
| Warning | Do NOT use for KPIs or speaker sums |

---

### Chart 5 — Speakers vs Endangerment

| Property | Value |
|----------|-------|
| Type | Box plot with jittered point overlay |
| Columns | `Degree of endangerment` (sorted by `Category sort`) |
| Rows | `Number of speakers` — **log scale**, range 1 to 10,000,000 |
| Detail | `ID` (for jitter points) |
| Jitter | Enabled on Rows axis, 0.5 |
| Point opacity | 30% |
| Box color | Same 5-color palette |
| Median line | White, thick |
| Filter | `[Number of speakers] > 0` |
| Caption | "Displayed on log scale; 257 records with 0 speakers excluded." |

**Insight to surface:** Median speaker count drops sharply as endangerment rises.

---

### Chart 6 — Speaker Distribution

| Property | Value |
|----------|-------|
| Type | Stacked horizontal bar |
| Rows | `Speaker bin` (sorted by `Speaker bin (sort)` descending) |
| Columns | `CNT([ID])` |
| Color | Same 5-color palette, stacked by `Degree of endangerment` |
| Label | Total per bin, outside bar |
| Data anchors | Peak at 1k–9,999 (676); 100–999 (583); 10–99 (328); 0 (257) |

---

### Chart 7 — Endangerment Composition by Country

| Property | Value |
|----------|-------|
| Source | Country-long table ONLY |
| Type | 100% stacked horizontal bar |
| Rows | Top 10 countries by total language records |
| Columns | Percent of total (each row sums to 100%) |
| Color | Same 5-color palette |
| Tooltip | Country, count per category, percentage |
| Purpose | Different insight from Chart 4 — shows severity mix, not raw totals |

---

## Interactivity (locked)

**Global filters on Dashboard 1 and 2:**
- `Degree of endangerment` (multi-select)
- `Country` (multi-select)
- `Speaker range` (parameter control)

**Dashboard actions:**
1. Map point click → filter all charts on that dashboard to that language's country
2. Category bar hover → highlight matching marks in other charts
3. Reset button → "Show All" clear-filters action

**Parameter controls placed on both dashboards:**
- `Top N` (list selector)
- `Speaker range` (list selector)

---

## Design consistency (integration phase)

All charts must use:
- Same 5-color palette
- Same font family and size scale
- Same number formatting (thousands separator, no decimals on counts)
- Same category labels (verbatim from source)
- Same filter behaviors
- Same tooltip structure

Consistency is a rubric item. Do not deviate.