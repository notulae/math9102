# `experim`

30 rows x 18 columns.

> Experimental study, 30x18.

| Variable | Type | Complete | Values |
|---|---|---|---|
| `id` | numeric | 30 / 30 | 1 to 30 (median 15.5) |
| `sex` | text | 30 / 30 | `female`, `male` |
| `age` | numeric | 30 / 30 | 19 to 46 (median 23) |
| `group` | text | 30 / 30 | `confidence building`, `maths skills` |
| `fost1` | numeric | 30 / 30 | 30 to 50 (median 40) |
| `confid1` | numeric | 30 / 30 | 11 to 29 (median 20) |
| `depress1` | numeric | 30 / 30 | 33 to 50 (median 43) |
| `fost2` | numeric | 30 / 30 | 28 to 48 (median 38) |
| `confid2` | numeric | 30 / 30 | 13 to 35 (median 21) |
| `depress2` | numeric | 30 / 30 | 30 to 49 (median 41) |
| `fost3` | numeric | 30 / 30 | 23 to 46 (median 35.5) |
| `confid3` | numeric | 30 / 30 | 14 to 34 (median 26) |
| `depress3` | numeric | 30 / 30 | 29 to 50 (median 40) |
| `exam` | numeric | 30 / 30 | 52 to 90 (median 65.5) |
| `mah_1` | numeric | 30 / 30 | 0.346998 to 10.2402 (median 1.7122) |
| `dept1gp2` | text | 30 / 30 | `depressed`, `not depressed` |
| `dept2gp2` | text | 30 / 30 | `depressed`, `not depressed` |
| `dept3gp2` | text | 30 / 30 | `depressed`, `not depressed` |

Load it with:

```python
import math9102 as m9
df = m9.load("experim")
```
