# claims erratum D5 (fixture payload)

Committed test fixture for the C1 closure check D5. The live erratum is
`.ufo/waves/round-35/claims-erratum-d5.md` at the lane root; this file is the pinned payload.

## 1. The frozen predicate wording gets a discriminating invocation

The frozen phrase `source-recheck exit != 0 on the twin; reviewer REFUSE` names no runnable command.
The **discriminating invocation** is:

```
python3 corpus/instruments/source-recheck.py --manifest <manifest> --source <id>
```

run against a manifest whose declared quote the candidate bytes do not contain: it exits 1 with
`reason=quote-not-found`, while the real capture exits 0. The claim is read under that invocation and
no other.

## 2. Occurrence counts are per assertion id, not per quote

`every assertion occurrences=1` is false as written: Q9 and Q17 appear twice each and are
anchor-verified instead of unique, while every other assertion appears exactly once.
