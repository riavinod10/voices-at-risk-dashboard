# Tableau Calculated Fields — Voices at Risk

Paste these into Tableau when building. Field names match the ones referenced in `dashboard_spec.md`.

---

## 1. `Speaker bin` — for Chart 6

Data type: String
Purpose: Groups languages into order-of-magnitude ranges.

Formula:
    IF ISNULL([Number of speakers]) THEN 'Unknown'
    ELSEIF [Number of speakers] = 0 THEN '0'
    ELSEIF [Number of speakers] < 10 THEN '1–9'
    ELSEIF [Number of speakers] < 100 THEN '10–99'
    ELSEIF [Number of speakers] < 1000 THEN '100–999'
    ELSEIF [Number of speakers] < 10000 THEN '1k–9,999'
    ELSEIF [Number of speakers] < 100000 THEN '10k–99,999'
    ELSEIF [Number of speakers] < 1000000 THEN '100k–999,999'
    ELSE '1M+'
    END

---

## 2. `Speaker bin (sort)` — for Chart 6 sort order

Data type: Integer
Purpose: Forces descending order from 1M+ down to 0.

Formula:
    IF [Speaker bin] = '1M+' THEN 8
    ELSEIF [Speaker bin] = '100k–999,999' THEN 7
    ELSEIF [Speaker bin] = '10k–99,999' THEN 6
    ELSEIF [Speaker bin] = '1k–9,999' THEN 5
    ELSEIF [Speaker bin] = '100–999' THEN 4
    ELSEIF [Speaker bin] = '10–99' THEN 3
    ELSEIF [Speaker bin] = '1–9' THEN 2
    ELSEIF [Speaker bin] = '0' THEN 1
    ELSE 0
    END

Right-click this field in the data pane -> Convert to Dimension. Use as a hidden sort key on the Rows shelf.

---

## 3. `Category sort` — for all charts showing categories

Data type: Integer
Purpose: Forces Vulnerable -> Extinct order. Tableau sorts alphabetically by default.

Formula:
    CASE [Degree of endangerment]
    WHEN 'Vulnerable' THEN 1
    WHEN 'Definitely endangered' THEN 2
    WHEN 'Severely endangered' THEN 3
    WHEN 'Critically endangered' THEN 4
    WHEN 'Extinct' THEN 5
    END

Right-click -> Convert to Dimension. Use as hidden sort key on any view showing categories.

---

## 4. `Top N` parameter — for Chart 3

Create Parameter:
    Name: Top N
    Data type: Integer
    Allowable values: List
    Values: 5, 10, 15, 20
    Current value: 10

---

## 5. `Top N Rank` — for Chart 3

Data type: Integer (table calculation)
Purpose: Ranks languages by speaker count.

Formula:
    RANK_DESC(SUM([Number of speakers]))

After creating, right-click -> Edit Table Calculation -> Compute Using -> Name in English.

---

## 6. `Top N Filter` — for Chart 3

Data type: Boolean
Purpose: Filters to the top N languages.

Formula:
    [Top N Rank] <= [Top N]

Drag to Filter shelf -> keep True.

---

## 7. `Speaker range` parameter — global filter

Create Parameter:
    Name: Speaker range
    Data type: String
    Allowable values: List
    Values: All, 0, 1–999, 1k–99,999, 100k+
    Current value: All

---

## 8. `Speaker range match` — global filter boolean

Data type: Boolean
Purpose: Applies the Speaker range parameter.

Formula:
    CASE [Speaker range]
    WHEN 'All' THEN TRUE
    WHEN '0' THEN [Number of speakers] = 0
    WHEN '1–999' THEN [Number of speakers] >= 1 AND [Number of speakers] <= 999
    WHEN '1k–99,999' THEN [Number of speakers] >= 1000 AND [Number of speakers] <= 99999
    WHEN '100k+' THEN [Number of speakers] >= 100000
    ELSE TRUE
    END

Drag to Filter shelf -> keep True. Show the parameter control on the dashboard.

---

## 9. `Language display` — tooltip / Detail Panel

Data type: String
Purpose: Falls back to English name when the endonym is missing.

Formula:
    IF ISNULL([Name in the language]) OR [Name in the language] = ''
    THEN [Name in English]
    ELSE [Name in English] + ' (' + [Name in the language] + ')'
    END

---

## 10. `Speakers (formatted)` — tooltip / labels

Data type: String
Purpose: Renders speaker count with a fallback for missing values.

Formula:
    IF ISNULL([Number of speakers]) THEN 'Not reported'
    ELSE STR(INT([Number of speakers]))
    END

After creating, right-click the resulting pill in the view -> Format -> Number -> Custom -> #,###

---

## 11. `Category (display)` — legends / tooltips

Data type: String
Purpose: Consistent capitalization in case the source changes.

Formula:
    [Degree of endangerment]

(The source values are already clean. This field exists so future edits to the source don't break consistency.)

---

## 12. `Detail field (null-safe)` — Detail Panel text

Data type: String
Purpose: One concatenated string for the language Detail Panel.

Formula:
    'Country/Countries: ' + IFNULL([Countries], 'Not available') + CHAR(10) +
    'Speakers: ' + IFNULL([Speakers (formatted)], 'Not available') + CHAR(10) +
    'Endangerment: ' + IFNULL([Degree of endangerment], 'Not available') + CHAR(10) +
    'ISO code: ' + IFNULL([ISO639-3 codes], 'Not available') + CHAR(10) +
    'Coordinates: ' + IFNULL(STR([Latitude]) + ', ' + STR([Longitude]), 'Not available') + CHAR(10) +
    'Location: ' + IFNULL([Description of the location], 'Not available') + CHAR(10) +
    'Alternate names: ' + IFNULL([Alternate names], 'Not available')

Use as a text mark or tooltip in the Detail Panel worksheet.

---

## 13. Chart 5 — log-scale + zero-filter

On Chart 5 (box plot with jitter), Tableau's log axis breaks on 0.
Add a filter: [Number of speakers] > 0
Add a caption note: "Displayed on log scale; 257 records with 0 speakers excluded."

Do NOT create a calculated field for this — use the built-in filter.