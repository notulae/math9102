# `experim_clean`

300 rows x 18 columns.

> Expanded experim used in the week 6 CA demo, 300x18.

| Variable | Type | Complete | Values |
|---|---|---|---|
| `group` | text | 300 / 300 | `confidence building`, `maths skills` |
| `sex` | text | 300 / 300 | `female`, `male` |
| `id` | numeric | 300 / 300 | 1 to 300 (median 150.5) |
| `age` | numeric | 300 / 300 | 18 to 51 (median 24) |
| `fost1` | numeric | 300 / 300 | 1.14651 to 4.78212 (median 2.95095) |
| `confid1` | numeric | 300 / 300 | 1.13446 to 4.84761 (median 2.93227) |
| `depress1` | numeric | 300 / 300 | 0.29985 to 25.2986 (median 13.1485) |
| `fost2` | numeric | 300 / 300 | 1 to 5 (median 2.98448) |
| `confid2` | numeric | 300 / 300 | 1 to 5 (median 3.14501) |
| `depress2` | numeric | 300 / 300 | 0 to 27 (median 12.3511) |
| `fost3` | numeric | 300 / 300 | 1 to 5 (median 2.99909) |
| `confid3` | numeric | 300 / 300 | 1 to 5 (median 3.52986) |
| `depress3` | numeric | 300 / 300 | 0 to 27 (median 11.2903) |
| `exam` | numeric | 300 / 300 | 23.5096 to 100 (median 67.7559) |
| `mah_1` | numeric | 300 / 300 | 0.346998 to 10.2402 (median 2.45421) |
| `dept1gp2` | text | 300 / 300 | `depressed`, `not depressed` |
| `dept2gp2` | text | 300 / 300 | `depressed`, `not depressed` |
| `dept3gp2` | text | 300 / 300 | `depressed`, `not depressed` |

Load it with:

```python
import math9102 as m9
df = m9.load("experim_clean")
```
