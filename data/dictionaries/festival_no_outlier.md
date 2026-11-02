# `festival_no_outlier`

810 rows x 5 columns.

> Festival data with the day-1 outlier corrected; used to show outlier impact.

| Variable | Type | Complete | Values |
|---|---|---|---|
| `ticknumb` | numeric | 810 / 810 | 2111 to 4765 (median 3620.5) |
| `location` | text | 810 / 810 | `City`, `Rural` |
| `day1` | numeric | 810 / 810 | 0.02 to 3.69 (median 1.79) |
| `day2` | numeric | 264 / 810 | 0 to 3.44 (median 0.79) |
| `day3` | numeric | 123 / 810 | 0.02 to 3.41 (median 0.76) |

Load it with:

```python
import math9102 as m9
df = m9.load("festival_no_outlier")
```
