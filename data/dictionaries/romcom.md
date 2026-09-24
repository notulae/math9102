# `romcom`

40 rows x 3 columns.

> Film interest by gender, 40x3. Tab-separated with unquoted strings containing spaces and an apostrophe, so whitespace splitting fails.

| Variable | Type | Complete | Values |
|---|---|---|---|
| `gender` | text | 40 / 40 | `Female`, `Male` |
| `film` | text | 40 / 40 | `Bridget Jones' Diary`, `Memento` |
| `interest` | numeric | 40 / 40 | 3 to 37 (median 19.5) |

Load it with:

```python
import math9102 as m9
df = m9.load("romcom")
```
