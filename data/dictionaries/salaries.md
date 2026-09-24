# `salaries`

397 rows x 6 columns.

> US academic salaries 2008-09, 397x6 (carData::Salaries, Fox & Weisberg). Vendored from Rdatasets (vincentarelbundock/Rdatasets, csv/carData/Salaries.csv) on 2026-08-16; carData is GPL-2/GPL-3. Not in the legacy corpus - the week 1 lecture loaded it from the R package.

| Variable | Type | Complete | Values |
|---|---|---|---|
| `rank` | text | 397 / 397 | `AssocProf`, `AsstProf`, `Prof` |
| `discipline` | text | 397 / 397 | `A`, `B` |
| `yrs_since_phd` | numeric | 397 / 397 | 1 to 56 (median 21) |
| `yrs_service` | numeric | 397 / 397 | 0 to 60 (median 16) |
| `sex` | text | 397 / 397 | `Female`, `Male` |
| `salary` | numeric | 397 / 397 | 57800 to 231545 (median 107300) |

Load it with:

```python
import math9102 as m9
df = m9.load("salaries")
```
