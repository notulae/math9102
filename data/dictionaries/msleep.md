# `msleep`

83 rows x 11 columns.

> Mammal sleep times, 83x11 (ggplot2::msleep, after Savage & West 2007). Vendored from Rdatasets (csv/ggplot2/msleep.csv) on 2026-08-16; ggplot2 is MIT. Not in the legacy corpus - the week 1 lab loaded it from the R package. Retains its genuine missingness: vore, conservation, sleep_rem, sleep_cycle and brainwt are all incomplete.

| Variable | Type | Complete | Values |
|---|---|---|---|
| `name` | text | 83 / 83 | `African elephant`, `African giant pouched rat`, `African striped mouse`, `Arctic fox`, `Arctic ground squirrel`, `Asian elephant`, `Baboon`, `Big brown bat`, ... (83 in total) |
| `genus` | text | 83 / 83 | `Acinonyx`, `Aotus`, `Aplodontia`, `Blarina`, `Bos`, `Bradypus`, `Callorhinus`, `Calomys`, ... (77 in total) |
| `vore` | text | 76 / 83 | `carni`, `herbi`, `insecti`, `omni` |
| `order` | text | 83 / 83 | `Afrosoricida`, `Artiodactyla`, `Carnivora`, `Cetacea`, `Chiroptera`, `Cingulata`, `Didelphimorphia`, `Diprotodontia`, ... (19 in total) |
| `conservation` | text | 54 / 83 | `cd`, `domesticated`, `en`, `lc`, `nt`, `vu` |
| `sleep_total` | numeric | 83 / 83 | 1.9 to 19.9 (median 10.1) |
| `sleep_rem` | numeric | 61 / 83 | 0.1 to 6.6 (median 1.5) |
| `sleep_cycle` | numeric | 32 / 83 | 0.116667 to 1.5 (median 0.333333) |
| `awake` | numeric | 83 / 83 | 4.1 to 22.1 (median 13.9) |
| `brainwt` | numeric | 56 / 83 | 0.00014 to 5.712 (median 0.0124) |
| `bodywt` | numeric | 83 / 83 | 0.005 to 6654 (median 1.67) |

Load it with:

```python
import math9102 as m9
df = m9.load("msleep")
```
