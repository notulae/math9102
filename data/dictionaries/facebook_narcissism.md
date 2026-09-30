# `facebook_narcissism`

776 rows x 4 columns.

> Used for week 2 plotting, 776x4.

| Variable | Type | Complete | Values |
|---|---|---|---|
| `id` | numeric | 776 / 776 | 1 to 275 (median 139) |
| `npqc_r_total` | numeric | 776 / 776 | 14 to 52 (median 33) |
| `rating_type` | text | 776 / 776 | `Attractive`, `Cool`, `Fashionable`, `Glamourous` |
| `rating` | numeric | 776 / 776 | 1 to 5 (median 3) |

Load it with:

```python
import math9102 as m9
df = m9.load("facebook_narcissism")
```
