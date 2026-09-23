# Data Profile — Endangered Languages

- File: `endangered_languages_raw.csv`  
- SHA-256 (first 16): `26b55da75fc5a567`  
- Encoding that read successfully: `utf-8`

## 1. Shape & schema

Rows: **2722**  |  Columns: **15**

| # | Column | dtype | non-null | null | null % | distinct |
|---|--------|-------|----------|------|--------|----------|
| 1 | `ID` | int64 | 2722 | 0 | 0.0% | 2722 |
| 2 | `Name in English` | str | 2722 | 0 | 0.0% | 2715 |
| 3 | `Name in French` | str | 2699 | 23 | 0.8% | 2691 |
| 4 | `Name in Spanish` | str | 2701 | 21 | 0.8% | 2683 |
| 5 | `Countries` | str | 2721 | 1 | 0.0% | 252 |
| 6 | `Country codes alpha 3` | str | 2721 | 1 | 0.0% | 252 |
| 7 | `ISO639-3 codes` | str | 2458 | 264 | 9.7% | 2104 |
| 8 | `Degree of endangerment` | str | 2722 | 0 | 0.0% | 5 |
| 9 | `Alternate names` | str | 1583 | 1139 | 41.8% | 1527 |
| 10 | `Name in the language` | str | 27 | 2695 | 99.0% | 26 |
| 11 | `Number of speakers` | float64 | 2539 | 183 | 6.7% | 791 |
| 12 | `Sources` | str | 2079 | 643 | 23.6% | 780 |
| 13 | `Latitude` | float64 | 2719 | 3 | 0.1% | 2577 |
| 14 | `Longitude` | float64 | 2719 | 3 | 0.1% | 2616 |
| 15 | `Description of the location` | str | 1870 | 852 | 31.3% | 1578 |

## 2. Encoding / mojibake check

Read as `utf-8`. Heuristic: count of `Ã`, `Â`, `â€` per text column.

| Column | Ã | Â | â€ | sample suspect value |
|--------|---|---|-----|----------------------|

> Columns absent from this table showed no mojibake markers.

## 3. `Degree of endangerment` — verbatim value counts

Raw strings, unmodified. Watch for case/whitespace variants.

| value | count | repr |
|-------|-------|------|
| Definitely endangered | 680 | `'Definitely endangered'` |
| Vulnerable | 628 | `'Vulnerable'` |
| Critically endangered | 607 | `'Critically endangered'` |
| Severely endangered | 554 | `'Severely endangered'` |
| Extinct | 253 | `'Extinct'` |

## 4. `Number of speakers` — numeric parseability

- Non-null: 2539 / 2722  |  dtype read as: `float64`
- Values failing a strict `\d+` test: **0**
- After stripping commas: min=0  median=800  max=7,500,000

## 5. Coordinates

- `Latitude` null: 3 | out of [-90,90]: 0
- `Longitude` null: 3 | out of [-180,180]: 0
- Exact (0,0) rows: 0
- Distinct coordinate pairs: 2719 of 2722 rows

## 6. `Countries` — multi-value structure

- Rows containing `semicolon`: 0
- Rows containing `comma`: 212
- Rows containing `pipe`: 0
- Rows containing `slash`: 0
- Max values in one row (comma-split): 29
- Example multi-value row: `Germany, Denmark, Netherlands, Poland, Russian Federation`

## 7. Duplicates

- Fully duplicated rows: 0
- Duplicated `ID`: 0

## 8. Sample rows

|   ID | Name in English   | Name in French   | Name in Spanish     | Countries                                                       | Country codes alpha 3        | ISO639-3 codes                                   | Degree of endangerment   | Alternate names                                                              | Name in the language   |   Number of speakers | Sources                                                                                                                                                                                                                           |   Latitude |   Longitude | Description of the location                                                                                                                                                                                                    |
|-----:|:------------------|:-----------------|:--------------------|:----------------------------------------------------------------|:-----------------------------|:-------------------------------------------------|:-------------------------|:-----------------------------------------------------------------------------|:-----------------------|---------------------:|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------:|------------:|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 1022 | South Italian     | italien du sud   | napolitano-calabrés | Italy                                                           | ITA                          | nap                                              | Vulnerable               | Neapolitan; Neapolitan-Calabrese; неаполитанский; неаполитанско-калабрийский | nan                    |              7.5e+06 | nan                                                                                                                                                                                                                               |    40.9798 |     15.249  | Campania, Lucania (Basilicata), Abruzzi (Abruzzo), Molise, northern Calabria, northern and central Apulia (Puglia), southern Lazio and Marche as well as easternmost Umbria                                                    |
| 1023 | Sicilian          | sicilien         | siciliano           | Italy                                                           | ITA                          | scn                                              | Vulnerable               | nan                                                                          | nan                    |              5e+06   | nan                                                                                                                                                                                                                               |    37.4399 |     14.5019 | Sicily (Sicilia), southern and central Calabria and southern Apulia (Puglia); a large number of émigré communities                                                                                                             |
|  383 | Low Saxon         | bas-saxon        | bajo sajón          | Germany, Denmark, Netherlands, Poland, Russian Federation       | DEU, DNK, NLD, POL, RUS      | act, drt, frs, gos, nds, sdz, stl, twd, vel, wep | Vulnerable               | Low German, Niedersächsisch, Nedersaksisch, Niederdeutsch, Plattdeutsch      | Neddersassisch         |              4.8e+06 | nan                                                                                                                                                                                                                               |    53.4029 |     10.3601 | northern Germany, the north-eastern part of the Netherlands, border regions of Denmark and Poland; émigré communities in the Russian Federation and elsewhere                                                                  |
|  335 | Belarusian        | biélorusse       | bielorruso          | Belarus, Latvia, Lithuania, Poland, Russian Federation, Ukraine | BRB, LVA, LTU, POL, RUS, UKR | bel                                              | Vulnerable               | nan                                                                          | nan                    |              4e+06   | Hienadź Cychun: Weißrussisch. — Lexikon der Sprachen des europäischen Ostens. Herausgegeben von Miloš Okuka unter Mitwirkung von Gerald Krenn. Wieser Enzyklopädie des europäischen Ostens 10; Klagenfurt: Wieser, 2002. 563–579. |    53.956  |     27.5756 | Belarus except the Polesian-speaking south-west as well as adjacent regions of neighbouring countries                                                                                                                          |
|  382 | Lombard           | lombard          | lombardo            | Italy, Switzerland                                              | ITA, CHE                     | lmo                                              | Definitely endangered    | nan                                                                          | nan                    |              3.5e+06 | nan                                                                                                                                                                                                                               |    45.7215 |      9.3273 | the region of Lombardy (except the southernmost border areas) and the Novara province in Piedmont, Italy; Ticino Canton and the Mesolcina District and two districts south of St. Moritz in Graubünden (Grigioni), Switzerland |