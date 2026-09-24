# `wine`

178 rows x 14 columns.

> UCI wine, 178x14.

| Variable | Type | Complete | Values |
|---|---|---|---|
| `wine` | numeric | 178 / 178 | 1 to 3 (median 2) |
| `alcohol` | numeric | 178 / 178 | 11.03 to 14.83 (median 13.05) |
| `malic_acid` | numeric | 178 / 178 | 0.74 to 5.8 (median 1.865) |
| `ash` | numeric | 178 / 178 | 1.36 to 3.23 (median 2.36) |
| `acl` | numeric | 178 / 178 | 10.6 to 30 (median 19.5) |
| `mg` | numeric | 178 / 178 | 70 to 162 (median 98) |
| `phenols` | numeric | 178 / 178 | 0.98 to 3.88 (median 2.355) |
| `flavanoids` | numeric | 178 / 178 | 0.34 to 5.08 (median 2.135) |
| `nonflavanoid_phenols` | numeric | 178 / 178 | 0.13 to 0.66 (median 0.34) |
| `proanth` | numeric | 178 / 178 | 0.41 to 3.58 (median 1.555) |
| `color_int` | numeric | 178 / 178 | 1.28 to 13 (median 4.69) |
| `hue` | numeric | 178 / 178 | 0.48 to 1.71 (median 0.965) |
| `od` | numeric | 178 / 178 | 1.27 to 4 (median 2.78) |
| `proline` | numeric | 178 / 178 | 278 to 1680 (median 673.5) |

Load it with:

```python
import math9102 as m9
df = m9.load("wine")
```
