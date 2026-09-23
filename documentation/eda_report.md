# EDA Report — Voices at Risk

- Clean dataset rows: 2722
- Country-long rows: 3074

## 1. Category counts (KPI 3 input)

| Category | Count | % |
|---|---|---|
| Definitely endangered | 680 | 25.0% |
| Vulnerable | 628 | 23.1% |
| Critically endangered | 607 | 22.3% |
| Severely endangered | 554 | 20.4% |
| Extinct | 253 | 9.3% |

## 2. Speakers — overall (KPI 2 input)

- Non-null: 2539 / 2722
- Min: 0.0 | Median: 800 | Max: 7,500,000
- Sum of reported speakers: 136,239,957
- Records with exactly 0 speakers: 257

## 3. Speakers by order of magnitude (Chart 6 bin design)

| Range | Count |
|---|---|
| 0 | 257 |
| 1–9 | 145 |
| 10–99 | 328 |
| 100–999 | 583 |
| 1k–9,999 | 676 |
| 10k–99,999 | 373 |
| 100k–999,999 | 144 |
| 1M+ | 33 |

## 4. Top 15 languages by reported speakers (Chart 3 input)

| # | Language | Speakers | Category |
|---|---|---|---|
| 1 | South Italian | 7,500,000 | Vulnerable |
| 2 | Sicilian | 5,000,000 | Vulnerable |
| 3 | Low Saxon | 4,800,000 | Vulnerable |
| 4 | Belarusian | 4,000,000 | Vulnerable |
| 5 | Lombard | 3,500,000 | Definitely endangered |
| 6 | Romani | 3,500,000 | Definitely endangered |
| 7 | Yiddish (Israel) | 3,000,000 | Definitely endangered |
| 8 | Gondi | 2,713,790 | Vulnerable |
| 9 | Limburgian-Ripuarian | 2,600,000 | Vulnerable |
| 10 | Quechua of Southern Bolivia | 2,300,000 | Vulnerable |
| 11 | Kumaoni | 2,003,783 | Vulnerable |
| 12 | Aymara | 2,000,000 | Vulnerable |
| 13 | Emilian-Romagnol | 2,000,000 | Definitely endangered |
| 14 | Piedmontese | 2,000,000 | Definitely endangered |
| 15 | Venetan | 2,000,000 | Vulnerable |

## 5. Top 15 countries by distinct language records (Chart 4 input)

| # | Country | Language records |
|---|---|---|
| 1 | United States of America | 227 |
| 2 | India | 199 |
| 3 | Brazil | 190 |
| 4 | Indonesia | 149 |
| 5 | Russian Federation | 148 |
| 6 | China | 148 |
| 7 | Mexico | 143 |
| 8 | Australia | 108 |
| 9 | Papua New Guinea | 98 |
| 10 | Canada | 93 |
| 11 | Nepal | 71 |
| 12 | Colombia | 69 |
| 13 | Sudan | 65 |
| 14 | Peru | 62 |
| 15 | Vanuatu | 47 |

## 6. Category × speaker range (Chart 5 / 6 input)

| Degree of endangerment   |   0 |   1–9 |   10–99 |   100–999 |   1k–9,999 |   10k–99,999 |   100k–999,999 |   1M+ |
|:-------------------------|----:|------:|--------:|----------:|-----------:|-------------:|---------------:|------:|
| Critically endangered    |  12 |   141 |     209 |       115 |         52 |           15 |              0 |     0 |
| Definitely endangered    |   4 |     0 |      16 |       142 |        257 |          156 |             53 |     7 |
| Extinct                  | 239 |     3 |       0 |         0 |          1 |            1 |              0 |     0 |
| Severely endangered      |   1 |     1 |      92 |       183 |        169 |           48 |             11 |     0 |
| Vulnerable               |   1 |     0 |      11 |       143 |        197 |          153 |             80 |    26 |

## 7. Map coverage (Chart 1)

- Records with coordinates: 2719 / 2722
- Records missing coordinates: 3

## 8. Extinct records with nonzero reported speakers (interpretation flag)

- Count: 5
| ID | Language | Speakers |
|---|---|---|
| 2618 | Tobada' | 12000 |
| 2059 | Tamazight (Ait Rouadi) | 1637 |
| 580 | Canichana | 3 |
| 2112 | Lae | 1 |
| 661 | Uru | 1 |

## 9. Speaker nulls by category (data-quality flag)

| Category | Total | Null speakers | Null % |
|---|---|---|---|
| Critically endangered | 607 | 63 | 10.4% |
| Definitely endangered | 680 | 45 | 6.6% |
| Extinct | 253 | 9 | 3.6% |
| Severely endangered | 554 | 49 | 8.8% |
| Vulnerable | 628 | 17 | 2.7% |