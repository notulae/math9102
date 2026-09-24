# `romcom_urbanrural`

40 rows x 3 columns.

> As romcom but with location instead of gender.

| Variable | Type | Complete | Values |
|---|---|---|---|
| `location` | text | 40 / 40 | `City`, `Rural` |
| `film` | text | 40 / 40 | `Bridget Jones' Diary`, `Memento` |
| `interest` | numeric | 40 / 40 | 3 to 37 (median 19.5) |

Load it with:

```python
import math9102 as m9
df = m9.load("romcom_urbanrural")
```
