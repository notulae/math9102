# `bdi`

20 rows x 4 columns.

> Field BDI drink study, 20x4. Designed to be non-normal.

| Variable | Type | Complete | Values |
|---|---|---|---|
| `participant` | numeric | 20 / 20 | 1 to 20 (median 10.5) |
| `drink` | text | 20 / 20 | `DrinkX`, `DrinkY` |
| `bdisun` | numeric | 20 / 20 | 13 to 35 (median 16.5) |
| `bdiwed` | numeric | 20 / 20 | 3 to 39 (median 25.5) |

Load it with:

```python
import math9102 as m9
df = m9.load("bdi")
```
