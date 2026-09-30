# `youthcohort`

13,201 rows x 27 columns.

> UK Youth Cohort Study (Connolly), 13201x27. The .dat export lowercases gradIT/satIT and drops value labels.

| Variable | Type | Complete | Values |
|---|---|---|---|
| `serial` | numeric | 13,201 / 13,201 | 20008 to 312611 (median 169300) |
| `s1gender` | text | 13,201 / 13,201 | `Female`, `Male` |
| `ethsfr` | text | 12,952 / 13,201 | `Bangladeshi`, `Black`, `Indian`, `Other Asian (inc Chinese)`, `Other ethnic group(inc mixed)`, `Pakistani`, `White` |
| `famsec` | text | 13,201 / 13,201 | `Intermediate occupations`, `Large employers and higher professionals`, `Lower professional and higher technical occupations`, `Lower supervisory occupations`, `Other`, `Semi routine and routine occupations` |
| `s1pared` | text | 13,201 / 13,201 | `At least one parent with A-level`, `At least one parent with degree`, `Neither parent with A-level` |
| `s1expel` | text | 13,069 / 13,201 | `Expelled`, `Not excluded`, `Suspended` |
| `s1truan` | text | 13,044 / 13,201 | `No truancy`, `Occasional truancy`, `Persistant truancy` |
| `s1weight` | numeric | 13,201 / 13,201 | 0.371096 to 4.31235 (median 0.880208) |
| `s1peta2` | text | 13,005 / 13,201 | `1-4 A*-C`, `1-4 D-G`, `5+ A*-C`, `5+ D-G` |
| `gcsepts` | numeric | 13,201 / 13,201 | 0 to 117 (median 51) |
| `graddsci` | text | 13,201 / 13,201 | `A`, `A*`, `B`, `C`, `D`, `E`, `F`, `Fail`, ... (9 in total) |
| `satdsci` | text | 13,201 / 13,201 | `No`, `Yes` |
| `gradfren` | text | 7,363 / 13,201 | `A`, `A*`, `B`, `C`, `D`, `E`, `F`, `Fail`, ... (9 in total) |
| `satfren` | text | 13,201 / 13,201 | `No`, `Yes` |
| `gradit` | text | 1,761 / 13,201 | `A`, `A*`, `B`, `C`, `D`, `E`, `F`, `Fail`, ... (9 in total) |
| `satit` | text | 13,201 / 13,201 | `No`, `Yes` |
| `gradphys` | text | 1,268 / 13,201 | `A`, `A*`, `B`, `C`, `D`, `E`, `F`, `G` |
| `satphys` | text | 13,201 / 13,201 | `No`, `Yes` |
| `gradchem` | text | 1,303 / 13,201 | `A`, `A*`, `B`, `C`, `D`, `E`, `F`, `G` |
| `satchem` | text | 13,201 / 13,201 | `No`, `Yes` |
| `gradbiol` | text | 1,290 / 13,201 | `A`, `A*`, `B`, `C`, `D`, `E`, `F`, `Fail` |
| `satbiol` | text | 13,201 / 13,201 | `No`, `Yes` |
| `gradmath` | text | 12,956 / 13,201 | `A`, `A*`, `B`, `C`, `D`, `E`, `F`, `Fail`, ... (9 in total) |
| `satmath` | text | 13,201 / 13,201 | `No`, `Yes` |
| `gradeng` | text | 12,906 / 13,201 | `A`, `A*`, `B`, `C`, `D`, `E`, `F`, `Fail`, ... (9 in total) |
| `sateng` | text | 13,201 / 13,201 | `No`, `Yes` |
| `pcschtype` | text | 13,201 / 13,201 | `CTC/Other maintained`, `Comprehensive 16`, `Comprehensive 18`, `Grammar`, `Independent`, `Modern` |

Load it with:

```python
import math9102 as m9
df = m9.load("youthcohort")
```
