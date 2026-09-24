# `websatisfaction`

73 rows x 31 columns.

> Web design survey used by CA Phase 2 Task 4, 73x31.

| Variable | Type | Complete | Values |
|---|---|---|---|
| `user_id` | text | 73 / 73 | `045dc0f3-a730-4d03-a615-f51814e5b04f`, `080c468b-27c0-455c-aa63-b8f807f2e3d7`, `092f2ee7-5281-4a09-9bce-e5523b95b53b`, `0b0379c7-04db-4c85-84bd-a2bd55329e29`, `0e623280-b28b-4d4a-8eea-0732f09ed497`, `10e9b324-156e-4eb5-aec5-04d8a4d7124c`, `11cbc3a6-1c92-4f10-abe6-27def200d91d`, `1331586c-ee72-4fc1-b622-812f54a49f6c`, ... (73 in total) |
| `language` | text | 73 / 73 | `en`, `es` |
| `platform` | text | 65 / 73 | `Desktop`, `Mobile` |
| `gender` | text | 73 / 73 | `female`, `male`, `other` |
| `age` | numeric | 73 / 73 | 1 to 55 (median 20) |
| `q1` | numeric | 73 / 73 | 1 to 10 (median 9) |
| `q2` | numeric | 73 / 73 | 1 to 10 (median 8) |
| `q3` | numeric | 73 / 73 | 1 to 10 (median 9) |
| `q4` | numeric | 73 / 73 | 2 to 10 (median 8) |
| `q5` | numeric | 73 / 73 | 2 to 10 (median 8) |
| `q6` | numeric | 73 / 73 | 2 to 10 (median 8) |
| `q7` | numeric | 73 / 73 | 1 to 10 (median 8) |
| `q8` | numeric | 73 / 73 | 2 to 10 (median 8) |
| `q9` | numeric | 73 / 73 | 1 to 10 (median 7) |
| `q10` | numeric | 73 / 73 | 1 to 10 (median 6) |
| `q11` | numeric | 73 / 73 | 1 to 10 (median 7) |
| `q12` | numeric | 73 / 73 | 1 to 10 (median 7) |
| `q13` | numeric | 73 / 73 | 1 to 10 (median 8) |
| `q14` | numeric | 73 / 73 | 1 to 10 (median 8) |
| `q15` | numeric | 73 / 73 | 1 to 10 (median 8) |
| `q16` | numeric | 73 / 73 | 1 to 10 (median 7) |
| `q17` | numeric | 73 / 73 | 1 to 10 (median 8) |
| `q18` | numeric | 73 / 73 | 1 to 10 (median 8) |
| `q19` | numeric | 73 / 73 | 1 to 10 (median 8) |
| `q20` | numeric | 73 / 73 | 1 to 10 (median 8) |
| `q21` | numeric | 73 / 73 | 1 to 10 (median 8) |
| `q22` | numeric | 73 / 73 | 1 to 10 (median 8) |
| `q23` | numeric | 73 / 73 | 1 to 10 (median 8) |
| `q24` | numeric | 73 / 73 | 1 to 10 (median 8) |
| `q25` | numeric | 73 / 73 | 1 to 10 (median 8) |
| `q26` | numeric | 73 / 73 | 1 to 10 (median 8) |

Load it with:

```python
import math9102 as m9
df = m9.load("websatisfaction")
```
