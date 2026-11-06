| mutant | own selftest | forgery rcs (F1..F5) | forgery rc0 | real 59-row battery |
|---|---|---|---|---|
| V1-drop-killcases-filter | rc=1 | 1,1,1,1,1 | none | not run (selftest rc=1) |
| V2-miskilled-as-killed | rc=1 | 1,1,1,1,1 | none | not run (selftest rc=1) |
| V3-exc-any | rc=0 | 1,1,1,1,1 | none | rc=0 ok rows=59 killed=56 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3 |
| V4-exc-class-unguarded | rc=1 | 1,1,1,1,1 | none | not run (selftest rc=1) |
| P1-drop-nofail-conjunct | rc=1 | 1,1,1,1,1 | none | not run (selftest rc=1) |
| P2-drop-exact-line | rc=0 | 1,1,1,1,1 | none | rc=0 ok rows=59 killed=56 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3 |
| P3-drop-traceback | rc=0 | 1,1,1,1,1 | none | rc=0 ok rows=59 killed=56 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3 |
| B1-neutral-broken-as-ok | rc=1 | 1,1,1,1,0 | F5-allcases | not run (selftest rc=1) |
| B2-drop-nneutral | rc=0 | 1,1,1,1,1 | none | rc=0 ok rows=59 killed=56 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3 |
| B3-drop-nkill | rc=0 | 1,1,1,1,1 | none | rc=0 ok rows=59 killed=56 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3 |
| B4-neutral-in-place | rc=1 | 1,1,1,1,0 | F5-allcases | not run (selftest rc=1) |
| R1-drop-killcases-validation | rc=1 | 1,1,1,1,1 | none | not run (selftest rc=1) |
| F1-failline-drop-caret | rc=0 | 1,1,1,1,1 | none | rc=0 ok rows=59 killed=56 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3 |
| F2b-exc-substring | rc=0 | 1,1,1,1,1 | none | rc=1 ok rows=59 killed=55 survived=0 miskilled=0 dirty=1 notderived=0 neutral_ok=3/3 |
| F2-failline-drop-detail | rc=1 | 1,1,1,1,1 | none | not run (selftest rc=1) |
