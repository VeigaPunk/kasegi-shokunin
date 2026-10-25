# C2SiblingOverlap — wave-2 falsification of wave-1 ConnectorSiblings.md

seat: falsifier | scope: READ-ONLY | item under attack: `.ufo/waves/round-25/wave1/ConnectorSiblings.md`
two findings re-verified: **(F1) no F10 sibling collision** and **(F2) recheck convention is lane-local**.
lane tip at measurement: `b49948f` (committed tree) + live untracked round-25 files.

## Verdict: **CONFIRMED on both findings** — no correction needed to either verdict;
two live-drift deltas and one cosmetic ledger nit recorded below.

### F1 — no F10 sibling collision: CONFIRMED

Re-ran the vendor-name sweep over every sibling `corpus/SOURCES.md`, `corpus/knowledge/`,
`PROVINCE.md`, `SKILL.md`, `corpus/README.md` (wave-1 method, ConnectorSiblings.md:31-34):

```
cd /home/vgpnk/Projects/shokunin && for name in Cybozu 'GMO Pepabo' Pepabo HIRT Hitachi JPCERT JVN IPA Cisco; do
  grep -rIl --exclude-dir=.git "$name" */corpus/SOURCES.md */corpus/knowledge */PROVINCE.md */SKILL.md */corpus/README.md | grep -v '^kasegi-shokunin'
done
→ Cybozu, GMO Pepabo, Pepabo, HIRT, Hitachi, JPCERT, JVN, Cisco: ZERO hits outside kasegi. exit 0.
```

`IPA` hits are all false positives, matching wave-1's note — I classified each:
- `mori-shokunin/corpus/SOURCES.md:126` — substring inside `CapabilityBoundingSet=CAP_KILL CAP_IPC_LOCK` (earlyoom unit template).
- `kaidoku-shokunin/…/2026-10-13-rea-skill-contract.md:19` — `IPA` = iOS archive format in a file-extension list.
- `kama-shokunin/…/listener-census.md:220` — `IPAddress` (docker inspect).
- `kotodama` hits — phonetic IPA / *Journal of the International Phonetic Association*.
None is Japan's IPA security agency or a disclosure policy.

Province/refusal lines verified verbatim:
- `chousa-shokunin/PROVINCE.md:10` — `**Refuses:** bounty-program scope and claim packages (→ kasegi)` — cedes by name. ✓
- `kake-shokunin/PROVINCE.md:283-288` — refuses "disclosure timing, bounty and policy operation" **without naming kasegi** (wave-1's R4 caveat is accurate: adjacency, not assignment). ✓

### F2 — recheck convention lane-local: CONFIRMED (with live-drift deltas)

Re-ran wave-1's per-lane census: `bash -n -c "<recheck value>"` on every `^recheck:` line in each
lane's `corpus/knowledge/`, plus a `cd <prefix>` flag. My measurements vs wave-1's table
(ConnectorSiblings.md:41-64):

| lane | w1 lines/ok/fail/cd | w2 lines/ok/fail/cd | delta |
|---|---|---|---|
| kasegi | 37/37/0/36 | 37/37/0/36 | none |
| souji | 13/12/1/0 | 13/10/**3**/0 | +2 fail — live commit `466f539` (2026-10-25T08:56Z) rewrote `repo-size-census-readonly.md` rechecks to cadence prose (`180d — …`, `` `jj --version; git --version`. Source: `curl …` ``, `on-release — …`); all three fail `bash -n`. Explained drift, not a wave-1 error. |
| kengaku | 24/16/8/0 | **25**/16/9/0 | untracked `benchmark-verifier-execution-model.md:5` added (`recheck: 180d — re-run the three pinned fetches…`), fails `bash -n`. Explained drift. |
| other 17 lanes | identical | identical | — |

Both deltas are *new cadence-style rechecks* in siblings — they **strengthen** the finding that the
fleet norm is recheck-as-cadence, not recheck-as-command.

Aggregate: outside kasegi, **221 of 485 sibling recheck lines fail `bash -n`** (my sum;
wave-1 said 221/486 — the denominator shifted by the kengaku +1, the fail count is coincidentally
identical) and **0 of 485 carry a `cd <lane-root> &&` prefix**. In kasegi, 36/37 are `cd`-prefixed;
the one exception is `corpus/knowledge/root-loss-2026-10-12.md:76`
(`recheck: test ! -e ~/Projects/bounties && …`), the `~/Projects/` base-test limb the frozen
predicate explicitly allows — so even it satisfies the convention without `cd`.

Ledger nit (cosmetic, no correction required): the table's own row sum is 522 lines/301 ok/221 fail,
but its footer prints 523/302; the "outside kasegi" row (486→now 485, 221, 0) is consistent.
The finding rests on the outside-kasegi figures, which hold.

Convention-uniqueness supports:
- Fleet contract frozen meaning verified: `scripts/sources-census.sh:4` — "recheck carries **cadence**"; `:28` — `E09 invalid recheck (ISO date, NNd, or symbolic cadence)`. ✓
- sha256 `3fb7261569f4…` (fleet) vs `8d30d627021c…` (kagi copy) — divergent implementations confirmed. ✓
- `grep -nE 'knowledge|handshake' scripts/sources-census.sh` — hits only inside embedded selftest fixture strings (:323, :329); no real `corpus/knowledge` gate in the fleet copy. ✓ (Refines wave-1's "returns no knowledge read": there are fixture-only matches — the script *emits* the string `corpus/knowledge/missing-…` in a selftest but never reads that directory.)
- `corpus/instruments/recheck-audit.py` absent at base: `git cat-file -e b49948f:corpus/instruments/recheck-audit.py` → `fatal: path … exists on disk, but not in 'b49948f'` (exit 128). Untracked, built this round. ✓
- Base tree `corpus/knowledge/` = 35 entries (`git ls-tree --name-only b49948f corpus/knowledge/ | wc -l` → 35); live tree = 37 (2 untracked F10 entries). ✓

### C2 predicate limbs spot-check (context)

- `awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++}' corpus/README.md` → **frontier=10** (F10 row at `corpus/README.md:211`, admits both entries, cites S036–S040). ✓
- `grep -lE '^source: S0(3[6-9]|[4-9][0-9])' corpus/knowledge/*.md` → exactly the two new entries (`vendor-disclosure-policies-as-corpus-objects.md` cites S036–S039; `vendor-disclosure-policy-commitments-crosswalk.md:2` cites S040 Cisco + S036/S038/S039). ✓
- `./scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` → **exit 0**, `W04 S028`, `W04 S029` (pre-existing duplicates), `ok …/corpus/SOURCES.md`. Registry now carries S036–S040 at `corpus/SOURCES.md:42-46`. ✓

### Wave-1 contradiction #2 is stale — resolved upstream

ConnectorSiblings.md:82-85 flagged `claims.json` saying "S068 Cisco policy unreachable this round"
while the crosswalk cites S040. The committed wave-1 `claims.json` now reads
(`claims.json:44-45`): "…crosswalk… refused as staged … **Cisco source itself was reachable and
admitted as S040**" — consistent with the landed entry's `source: S040` line and `SOURCES.md:46`.
The contradiction was repaired between the wave-1 report and the current claims file; no residual.

## Smallest correction required: none

Both targeted findings survive falsification. Observations only:
1. Wave-1's per-lane table footer (523/302) mis-sums its own rows (522/301); the decision-relevant
   outside-kasegi figures (221 fail, 0 cd-prefix) are correct in both measurements.
2. The fleet census script does contain `corpus/knowledge/` strings — selftest fixtures only, not a
   real gate (wave-1's grep returned no hit likely because of a narrower pattern; the substance —
   no knowledge-dir read — is confirmed).
3. Souji's new cadence-style rechecks (`466f539`) postdate wave-1 and are a live example of exactly
   the homonym hazard wave-1 named: sibling `recheck:` means cadence.

## Tool install record

None — no tool installed or upgraded. `bc` was absent on one pipeline; arithmetic redone in awk.
Only read-only commands run: `grep`, `awk`, `bash -n -c` (parse-only), `git cat-file -e`,
`git ls-tree`, `git status`, `git log`, `sha256sum`, and the read-only fleet census
`scripts/sources-census.sh validate` (no sibling gate executed, no file written outside this report).
