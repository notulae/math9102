# `regression`

4,059 rows x 15 columns.

> Goldstein et al. exam results, 4059x15 in 65 schools. CLUSTERED - see docs/DECISIONS.md ADR-007.

| Variable | Type | Complete | Values |
|---|---|---|---|
| `school` | numeric | 4,059 / 4,059 | 1 to 65 (median 29) |
| `student` | numeric | 4,059 / 4,059 | 1 to 198 (median 33) |
| `normexam` | numeric | 4,059 / 4,059 | -3.66607 to 3.66609 (median 0.00432175) |
| `cons` | numeric | 4,059 / 4,059 | 1 to 1 (median 1) |
| `standlrt` | numeric | 4,059 / 4,059 | -2.93495 to 3.01595 (median 0.040499) |
| `girl` | text | 4,059 / 4,059 | `boy`, `girl` |
| `schgend` | text | 4,059 / 4,059 | `boysch`, `girlsch`, `mixedsch` |
| `avslrt` | numeric | 4,059 / 4,059 | -0.75596 to 0.637656 (median -0.0201981) |
| `schav` | text | 4,059 / 4,059 | `high`, `low`, `mid` |
| `vrband` | text | 4,059 / 4,059 | `vb1`, `vb2`, `vb3` |
| `boys_sch` | numeric | 4,059 / 4,059 | 0 to 1 (median 0) |
| `girls_sch` | numeric | 4,059 / 4,059 | 0 to 1 (median 0) |
| `interaction` | numeric | 4,059 / 4,059 | -2.93495 to 3.01595 (median 0) |
| `intgirls_sch` | numeric | 4,059 / 4,059 | -2.93495 to 3.01595 (median 0) |
| `intboys_sch` | numeric | 4,059 / 4,059 | -2.93495 to 2.9333 (median 0) |

Load it with:

```python
import math9102 as m9
df = m9.load("regression")
```
