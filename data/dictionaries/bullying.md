# `bullying`

819 rows x 11 columns.

> Bullying survey, 819x11.

| Variable | Type | Complete | Values |
|---|---|---|---|
| `id` | numeric | 818 / 819 | 1 to 819 (median 410.5) |
| `rsex` | text | 817 / 819 | `Female`, `Male` |
| `typeschl` | text | 804 / 819 | `Grammar`, `Other`, `Planned Integrated`, `Secondary` |
| `sclotbul` | text | 805 / 819 | `A little`, `A lot`, `Don't know`, `Not at all` |
| `stfbuljb` | text | 797 / 819 | `Don't know`, `No`, `Yes` |
| `gotostaf` | text | 548 / 819 | `Don't know`, `It depends`, `Would not talk to them`, `Would talk to them` |
| `schlbul` | text | 789 / 819 | `Don't know`, `No`, `Yes` |
| `ubullsch` | text | 803 / 819 | `No`, `Yes` |
| `oftenbul` | text | 242 / 819 | `A little`, `A lot`, `Not at all` |
| `ubulloth` | text | 800 / 819 | `No`, `Yes` |
| `oftenub` | text | 59 / 819 | `A little`, `A lot`, `Not at all ` |

Load it with:

```python
import math9102 as m9
df = m9.load("bullying")
```
