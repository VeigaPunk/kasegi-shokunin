# ReviewC1Instrument — C1 instrument review (round 99, w1)

Seat: ReviewC1Instrument (leaf; no subagent dispatch).
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Base `b9411a6b530e486180cf14c72fccc46668dcf5ee`; freeze `6195db307c1cb101eba1d268f8cbfc1578d2caf7`;
C2 landing `a3db47e71fe292c03b00ba11f38cccbec45d3966`; C1 landing `35e3ab6041ff8690b00d831f27b93d08101fd16a`.
Instrument under review: `corpus/instruments/census-at-rev.py` at the C1 landing, 384 lines,
sha256 `6d68d9555b9be5a75bfefb27ee8cf531bc97dd540c954cc2da56581e6a68f041` (receipt 01).
Scratch `S=/fast/scratch/hyaku/kasegi-r99/ReviewC1Instrument` (removed before yield; receipts copied here).

All commands below were run from the lane root unless the command names another cwd. Every
number in this report is an observed output, not a restatement of the claim.

---

## 1. Pin verification

```
$ git show 35e3ab6041ff8690b00d831f27b93d08101fd16a:corpus/instruments/census-at-rev.py | sha256sum
6d68d9555b9be5a75bfefb27ee8cf531bc97dd540c954cc2da56581e6a68f041  -
$ git show 35e3ab6041ff8690b00d831f27b93d08101fd16a:corpus/instruments/census-at-rev.py | wc -l
384
$ sha256sum corpus/instruments/census-at-rev.py          # worktree at HEAD 29cd3058
6d68d9555b9be5a75bfefb27ee8cf531bc97dd540c954cc2da56581e6a68f041  corpus/instruments/census-at-rev.py
```

The instrument bytes are unchanged between the C1 landing and HEAD. The committed census of
record is also unchanged (`git show HEAD:...` and `git show 35e3ab60:...` both hash
`211818db7ed71ae2eebfe7fa02890faab7302915c66fc9929be9a44e984859e3`).

## 2. Independent re-derivation of the pinned numbers

Method: `receipts/indep-census.py` — my own script, written from the extraction rule documented
in `resolve.py`'s module docstring; it does **not** import or copy the lane instrument. Input:
`git archive a3db47e71fe292c03b00ba11f38cccbec45d3966 | tar -x` under a private parent, with
`HOME=<scratch>/home` (empty `Projects/`). It counts distinct backticked path-like citations per
scope, classifies lane-relative tokens that exist in the extract as INTERNAL, and reclassifies a
`..` walk-out whose `realpath` leaves the extract as HOST-OWNED (out of the numerator, kept in the
denominator).

```
$ env HOME=$S/home python3 -B $S/indep-census.py $S/extract $S/home
distinct=8026
SKILL pinned INTERNAL 162/732
CORPUS pinned INTERNAL 2569/7624
LANE pinned INTERNAL 2607/8026
host_owned=76 confined=1
SKILL host-incl 165/732
CORPUS host-incl 2645/7624
LANE host-incl 2683/8026
```

The instrument itself, same revision, same confined HOME:

```
$ python3 -B corpus/instruments/census-at-rev.py --lane . --rev a3db47e71fe292c03b00ba11f38cccbec45d3966 --work $S/cwork
CENSUS rev=a3db47e71fe292c03b00ba11f38cccbec45d3966 skill=162/732 corpus=2569/7624 lane=2607/8026 host_owned=76 confined=1
```

| quantity | census of record (header) | my independent script | instrument run |
|---|---|---|---|
| SKILL pinned | 162/732 | 162/732 | 162/732 |
| corpus pinned | 2569/7624 | 2569/7624 | 2569/7624 |
| lane pinned | 2607/8026 | 2607/8026 | 2607/8026 |
| host-owned | 76 | 76 | 76 |
| confined (reclassified) | not in the header | 1 | 1 |

The census header's digests recompute exactly over the five lines and the body:

```
recomputed header-sha256: ddad876669a002f3509bd0366f24b70f4bc45bc01b946d8cac7f0b5611f70379
stored     header-sha256: ddad876669a002f3509bd0366f24b70f4bc45bc01b946d8cac7f0b5611f70379
recomputed body-sha256:   0375a382de6d3282c98920d4748a3b4300a5133cf4e80188fdc25b5348c6c87a
stored     body-sha256:    0375a382de6d3282c98920d4748a3b4300a5133cf4e80188fdc25b5348c6c87a
```

The census body's raw totals (8026 distinct, INTERNAL 2608, GONE 5342, RESOLVES 76) match the
extract's `citation-survival.tsv` exactly (8026 rows, 2608 INTERNAL, 5342 GONE, 76 RESOLVES).

**Discrepancy (low).** `resolve.py`'s own stdout at the same rev/HOME prints
`skill=165/732 corpus=2646/7624 all=2684/8026`, while the census's
`host-inclusive rate (resolve.py's definition, confined HOME):` line says
`165/732 | 2645/7624 | 2683/8026`. The one-row difference is the reclassified `../` row: the
instrument's `host_incl` counts only `INTERNAL|RESOLVES|MIRROR-EQUIVALENT`, so the row it renamed
HOST-OWNED is dropped from the host-inclusive numerator as well. The line's parenthetical
"(resolve.py's definition)" is therefore off by one; the pinned line (the claim's number) is not
affected. The same root cause makes the body's "lane total 2684/8026" disagree with the header's
2683/8026, and the census file carries no `confined:` line explaining the difference — `confined=1`
appears only in the `--write`/`--check` stdout.

## 3. Line-by-line review of the instrument

Key lines (file:line at the landing bytes):

- `extract()` `:79` — `if os.path.isfile(os.path.join(d, RESOLVE)): return d, None`. A pre-existing
  extract under `<work>/extract-<rev12>/tree` is trusted without re-extraction (finding F1).
- `measure()` `:115` — `cache = os.path.join(work, "cache", rev + "-" + instrument_digest() + ".json")`;
  `:116` `if cache_ok and os.path.isfile(cache)`. The key includes the instrument content digest.
- `measure()` `:152-156` — confinement: `rp = os.path.realpath(resolved)`; reclassified only when
  `klass == "INTERNAL" and walkout(cit)`. The realpath test follows symlinks, but the gate is the
  citation's `..` segment (finding F2).
- `measure()` `:200-201` — the cache is written even when `cache_ok=False` (i.e. by `--check`).
- `header_lines()` `:231` and `write_census()` `:265-266` — `header-sha256` over the five header
  lines, `body-sha256` over the body.
- `write_census()` `:256` — `rates, body, err = measure(lane, rev, work)` with the default
  `cache_ok=True`: `--write` reads the measurement cache (finding F3).
- `ancestor_of_tip()` `:239-250` — tips = `rev-parse HEAD` + `for-each-ref refs/heads`; each tested
  with `git merge-base --is-ancestor rev tip`.
- `check()` `:283` — measured-at regex `^measured-at: ([0-9a-f]{40})$`; ancestor gate; header digest;
  body digest; then `measure(..., cache_ok=False)` at `:322`.
- `check()` `:326/:331/:334` — compares `hdr[2]` (pinned), `hdr[3]` (host), `hdr[4]` (host-owned) to
  fresh lines. `hdr[0]` (measured-at) selects the rev; `hdr[1]` (home) is never compared (finding F4).

## 4. The five requested checks

### 4.1 Symlink bypass of the confinement — **partial**

Fixture `$S/fix1.*` (git repo; `link -> ../outside-abs`, `abslink -> $S/outside-abs`, both committed
as mode-120000 symlinks; `SKILL.md` cites `link/secret.md`, `abslink/secret.md`,
`../outside/secret.md`, `link/../outside2/secret.md`, `corpus/real.md`). After creating the targets
outside the extract and re-running:

```
CENSUS rev=f5f7fa86cea3a76c1ef00a8eaa1ae6c146c110a8 skill=3/5 corpus=0/0 lane=3/5 host_owned=0 confined=2
--- realpath check (INTERNAL rows) ---
'../outside/secret.md'      INTERNAL realpath_inside= False -> .../extract-f5f7fa86cea3/outside/secret.md
'abslink/secret.md'         INTERNAL realpath_inside= False -> .../outside-abs/secret.md
'corpus/real.md'            INTERNAL realpath_inside= True
'link/../outside2/secret.md' INTERNAL realpath_inside= False -> .../extract-f5f7fa86cea3/outside2/secret.md
'link/secret.md'            INTERNAL realpath_inside= False -> .../extract-f5f7fa86cea3/outside-abs/secret.md
```

The raw TSV classes both `..` rows INTERNAL; the instrument reclassifies them (`confined=2`), so the
pinned numerator is 3/5 — but the two symlink rows without a `..` segment (`abslink/secret.md`,
`link/secret.md`) stay INTERNAL with a `realpath` outside the extract. The confinement is therefore
**not** a general "every relative citation stays in the tree" property: it is gated on
`walkout(cit)` (a literal `..` segment), so a committed symlink that escapes is host-dependent and
still counted. A `..` citation that resolves *through* a symlink is caught (realpath is followed).

Revision-specific impact: at `a3db47e7` there is exactly one INTERNAL row whose realpath leaves the
extract — `'../'` — and it has a `..` segment and is reclassified. No INTERNAL row's resolved path
is itself a symlink. So the pinned numbers at the measured revision are unaffected; the gap is a
future-revision risk and contradicts the statement's first clause ("confines every relative
citation to the measured tree"), not its `..`-specific parenthetical. The instrument's own extract
comment (`:88-90`) already declares committed absolute symlinks out of scope.

### 4.2 Cache key includes the instrument digest — **pass**

`:115` builds `<rev>-<sha256(instrument)[:12]>.json`. Observed:

```
$ ls $S/fix1work/cache/
f5f7fa86cea3a76c1ef00a8eaa1ae6c146c110a8-6d68d9555b9b.json
$ cp census-at-rev.py census-modified.py; append one comment line   # sha256 prefix d93686e5ff22
$ python3 -B census-modified.py --lane $D --rev $REV --work $S/fix1work
$ ls $S/fix1work/cache/
f5f7fa86cea3a76c1ef00a8eaa1ae6c146c110a8-6d68d9555b9b.json
f5f7fa86cea3a76c1ef00a8eaa1ae6c146c110a8-d93686e5ff22.json
```

### 4.3 `--check` never reads the cache — **pass for reading; it writes the cache, and `--write` reads it**

Poisoned-cache test in the fixture work dir (`$C=<rev>-6d68d9555b9b.json`, rates set to 99/99 and
body to `POISONED-BODY`):

```
$ python3 -B census-at-rev.py --lane $D --check $W/census.md --work $W
CENSUS-CHECK pass rev=f5f7fa86... skill=3/5 corpus=0/0 lane=3/5 host_owned=0 confined=2   # rc=0
# re-poison, then the same instrument in --rev mode:
$ python3 -B census-at-rev.py --lane $D --rev $REV --work $W
CENSUS rev=f5f7fa86... skill=99/99 corpus=99/99 lane=99/99 host_owned=0 confined=2
```

`--check` ignores the poison (line `:322` `cache_ok=False`) while `--rev` reads it, so the bypass is
real and the cache file is the one the code would otherwise use. Two caveats, both observed:
`measure()` still writes the cache on the `--check` path (`:200-201`), and `--write` calls
`measure()` with the default `cache_ok=True` (`:256`), so a poisoned cache **does** produce a
census of record: after poisoning, `--write` emitted
`CENSUS-WRITE ok ... skill=99/99 ...` (finding F3). The check then rejects that census
(`pinned-mismatch`), so it cannot be admitted silently, but the write path is not cache-free.

### 4.4 Header digest covers every line the check compares — **pass for the five header lines; the `home:` line is bound but not verified**

The digest is computed over `header_lines()` = measured-at, home, pinned, host, host-owned; the
check reconstructs the same five by `HEADER_FIELDS` (`:55`, `:298`) and compares `hdr[2..4]` to a
fresh measurement. Recomputation matches (section 2). Tamper tests on the fixture census:

| tamper | digest | result |
|---|---|---|
| pinned line edited | header-sha256 recomputed | `CENSUS-CHECK fail reason=pinned-mismatch rc=1` |
| host-owned line edited | header-sha256 recomputed | `CENSUS-CHECK fail reason=host-owned-mismatch rc=1` |
| `home:` line edited to "real host" | header-sha256 recomputed | **`CENSUS-CHECK pass`** (rc=0) |
| title + "round 99" prose edited | untouched | **`CENSUS-CHECK pass`** (rc=0) |

So every line the check *compares* is covered, but the `home:` line is only digest-bound, and the
digest is attacker-recomputable: a census claiming `home: real host` while the measurement was
confined passes. The title and the "Census of record — regenerated in round 99" prose are not
covered by any digest and are not compared (cosmetic). Finding F4/F5.

### 4.5 `ancestor_of_tip` cannot be satisfied by a foreign object — **pass**

Fixture A (real repo with a `side` branch) and a second repo B:

```
$ python3 -B census-at-rev.py --lane $D --check $W/mt-foreign.md --work $W    # measured-at = repo B commit
CENSUS-CHECK fail reason=measured-at-not-ancestor rc=1
$ ... --check $W/mt-dangling.md ...                                          # commit in A, on no ref
CENSUS-CHECK fail reason=measured-at-not-ancestor rc=1
$ ... --check $W/mt-blob.md ...                                              # blob sha in A
CENSUS-CHECK fail reason=measured-at-not-ancestor rc=1
$ ... --check $W/mt-nontip.md ...                                            # non-tip ancestor of side
CENSUS-CHECK fail reason=header-sha-mismatch rc=1        # ancestor gate passed, digest then failed
$ ... --rev $NONTIP --write $W/nontip-census.md --work $W
CENSUS-WRITE ok rev=fa23385b... rc=0                     # true ancestor accepted
$ ... --rev $FOREIGN --write $W/foreign-census.md --work $W
CENSUS-WRITE error reason=rev-not-ancestor rc=2
```

Observed exit codes: foreign sha (not in the repository) `128` ("Not a valid commit name"), blob
`128` ("is a blob, not a commit"), dangling commit `1` (not an ancestor), non-tip ancestor vs
`side` `0`, tip vs `main` `0`. `ancestor_of_tip` accepts only `0`, so none of the foreign/dangling/
blob cases can satisfy it; a real non-tip ancestor does. The 40-hex validation (`:362`, `:367`)
prevents a ref-name or option from reaching `merge-base`.

## 5. Findings by severity

**F1 (high under the harness's own threat model; medium in a fresh-verifier flow) — a planted
extract bypasses `--check`.** `extract()` (`:79`) returns a pre-existing
`<work>/extract-<rev12>/tree` whenever `corpus/instruments/resolve.py` exists, without comparing it
to `git archive`. `--check`'s "fresh measurement" therefore runs whatever `resolve.py` the work dir
contains. Reproduction on the **real lane** at `a3db47e7` (receipt 11): plant a fake
`resolve.py` that writes a one-row TSV and a fixed body, and a census whose five header lines,
digests and body agree with it:

```
CENSUS-CHECK pass rev=a3db47e71fe292c03b00ba11f38cccbec45d3966 skill=0/0 corpus=1/1 lane=1/1 host_owned=0 confined=0
```

The same construction passes on the fixture (`skill=0/0 corpus=1/1 lane=1/1`). The 12-class harness
has no class for this; T09's own comment states the attacker controls the work dir, and a poisoned
extract is the same capability as a poisoned cache. The round-98 instrument has the identical
early-return (`tree-<rev12>`, `git show e2d3de7b:...:60`), so this is inherited, not a regression —
but the round-99 claim "the census of record becomes tamper-evident" is not met while the check
trusts a work-dir tree. Because `measure` executes `<extract>/corpus/instruments/resolve.py` with
the verifier's own interpreter, a work-dir writer also gets code execution as the verifier; the
spoof is a symptom of that. Fix direction: always re-extract in `--check`, or bind the extract to
the archive digest.

**F2 (medium) — symlink escape without a `..` stays INTERNAL** (section 4.1). No effect at
`a3db47e7` (0 such rows); the pinned numbers are safe at this revision.

**F3 (medium) — `--write` reads the measurement cache** (`:256`). A poisoned cache produced
`CENSUS-WRITE ok ... skill=99/99 ...`; the check rejects the result, but the write path is not
cache-free, contrary to the claim's "no cache warm-up counted as a measurement".

**F4 (low-medium) — the `home:` line is not cross-checked.** A census claiming `home: real host`
with a recomputed header digest passes `--check` (section 4.4). The check could compare `hdr[1]` to
`HOME_LINE`; it does not.

**F5 (low) — title and prose are unbound.** Editing the title and "round 99" prose leaves the check
passing. Not claimed, cosmetic.

**F6 (low) — the host-inclusive line is labelled "resolve.py's definition" but is one lower**
(2683 vs resolve.py's 2684; 2645 vs 2646) because the confined row is excluded from `host_incl`.
The census body (raw resolve.py) and the header therefore disagree by one with no `confined:` line
in the file to explain it (section 2).

**F7 (low, pre-existing) — ten trailing-space citation keys.** `resolve.py`'s
`t.strip().rstrip(".,;:")` leaves the space when the source token is `` `x .` ``; ten keys
(`'resolve.py '`, `'census-freshness-check.py '`, eight shell-command variants) are all GONE and
inflate the denominator by 10. My first independent run got 8024/7622 until I replicated the
re-strip; this is a resolve.py artifact inherited by the census, not a C1 change.

**F8 (info) — a sibling seat transiently mutated the lane worktree census during this review.**
At 19:27 `corpus/instruments/citation-survival.md` in the worktree was overwritten by
`CriticClaimsC1`'s direct `resolve.py` run (its body named
`/fast/scratch/hyaku/kasegi-r99/CriticClaimsC1/D2/w/extract-a3db47e71fe2/tree`, 8041 citations);
`git status` showed it modified. By 19:36 the worktree file is back to the committed bytes
(sha256 `211818db...`, identical to HEAD and the landing). The committed census of record was never
changed, and every number in this review comes from `git archive`, not the worktree. I did not
revert or restore the peer's change.

## 6. Predicate reproduction

**P1** — tamper harness at the landing instrument (receipt 05):

```
TAMPER-RESULT killed=12 total=12 evaluated=12 instrument_sha256=6d68d9555b9be5a75bfefb27ee8cf531bc97dd540c954cc2da56581e6a68f041 rc=0
```

with the round-98 bytes (`sha256 66383371...`):

```
TAMPER-RESULT killed=5 total=12 evaluated=12 instrument_sha256=66383371211bf4b801df608d5e20c23e2b51457717fcb1b76de471b8feb62502 rc=0
```

The five passes on the base are T01, T02, T03, T04, T10; T05-T09, T11, T12 are accepted — exactly
the claim's do-nothing control.

**P2** — clean work dir:

```
CENSUS-CHECK pass rev=b9411a6b530e486180cf14c72fccc46668dcf5ee skill=162/732 corpus=2569/7620 lane=2607/8022 host_owned=76 confined=1
```

dirty work dir carrying `MISSION.md` and
`.ufo/waves/shokunin12h-20261014-p1-repair/members/KasegiGateRepair.md` (both the work dir itself
and the dirty scratch parent were tested):

```
CENSUS-CHECK pass rev=b9411a6b530e486180cf14c72fccc46668dcf5ee skill=162/732 corpus=2569/7620 lane=2607/8022 host_owned=76 confined=1
```

Identical triple, rc=0, matching the control receipt. A stronger contamination — the same files in
the extract's **private parent** (`work/extract-<rev12>/`) — changes the raw body
(`../MISSION.md:49-56` flips GONE→INTERNAL) and the check fails closed with
`body-mismatch rc=1`; the pinned triple would still be stable, but the claim's "private parent
holds only the extract" is not enforced. This is a fail-closed robustness note, not a false accept.

**P3** — on the committed census of record:

```
$ grep -c 'fast/scratch' census-head.md      -> 0
$ grep -c 'tree-b9411a6b530e' census-head.md -> 0
$ grep -c 'extract-' census-head.md          -> 0
```

`measured-at` is `a3db47e7...`, an ancestor of the branch tips (the check passes its gate).

**P4** — `/usr/bin/time -v` on the clean `--check` at `a3db47e7`:

```
CENSUS-CHECK pass rev=a3db47e71fe292c03b00ba11f38cccbec45d3966 skill=162/732 corpus=2569/7624 lane=2607/8026 host_owned=76 confined=1
Elapsed (wall clock) time (h:mm:ss or m:ss): 0:04.56
Maximum resident set size (kbytes): 514696
```

Under 60 s and 1 GiB. (The control receipt records 2.29 s / 512064 KB; the difference is
[INFERENCE] wave load, not a code change — the instrument bytes are identical.)

## 7. Residual risk and verification gaps

1. The 12 classes are not exhaustive: F1 (planted extract) defeats `--check` on the real lane and
   is not in the harness. A T13 class should be added before "tamper-evident" is claimed without
   qualification.
2. The check's fresh measurement is only as fresh as the work-dir extract; a verifier must use a
   fresh `--work` (the harness does) or the instrument must re-extract.
3. The `home:` line is a claim about the environment that the check does not verify (F4).
4. Symlink confinement is `..`-gated (F2); the extract comment already concedes it.
5. `--write` is cache-trusting (F3); a census of record can be written with numbers no measurement
   supports, though `--check` rejects it.
6. C2 (`capture-secret-scan`) is outside this seat's scope; not reviewed here.

## 8. Verdicts

VERDICT: instrument pin — PASS (384 lines, sha256 6d68d9555b9be5a75bfefb27ee8cf531bc97dd540c954cc2da56581e6a68f041 at the C1 landing and at HEAD).
VERDICT: independent numbers — MATCH (SKILL 162/732, corpus 2569/7624, lane 2607/8026, host-owned 76, confined 1; header and body digests recompute).
VERDICT: P1 tamper — PASS (12/12 at the landing, 5/12 on the round-98 bytes; the five base passes are T01/T02/T03/T04/T10).
VERDICT: P2 layout equality — PASS for the stated clean/dirty layouts (identical triple, rc=0); a contaminated private parent fails closed (body-mismatch), not open.
VERDICT: P3 measured-at and scratch paths — PASS (ancestor gate holds; 0 `fast/scratch`, 0 `tree-`, 0 `extract-` in the committed census).
VERDICT: P4 memory — PASS (4.56 s wall, 514696 KB peak RSS, under 60 s / 1 GiB).
VERDICT: cache key includes the instrument digest — PASS (observed two cache files, 6d68d9555b9b and d93686e5ff22).
VERDICT: `--check` never reads the cache — PASS for reading (poisoned cache ignored; `--rev` reads it); it writes the cache and `--write` reads it (F3).
VERDICT: header digest coverage — PASS for the five header lines (pinned/host/host-owned cross-checked; recomputation matches); the `home:` line is bound but not verified (F4), and the title/prose are unbound (F5).
VERDICT: `ancestor_of_tip` vs a foreign object — PASS (foreign commit, dangling commit and blob all rejected; a true non-tip ancestor accepted; `--write` refuses a foreign rev with rc=2).
VERDICT: symlink confinement — FAIL for a citation without a `..` segment whose resolved path is a committed symlink escaping the extract (fixture: 3/5 instead of 1/5); no such row at a3db47e7, so the pinned numbers are unaffected at this revision.
VERDICT: tamper-evidence of `--check` under a controlled work dir — FAIL (F1: a planted `resolve.py` plus a fabricated census passes `--check` on the real lane with `skill=0/0 corpus=1/1 lane=1/1`).
VERDICT: depth:verifiability — the pinned numbers and the 12/12-vs-5/12 delta are independently reproduced and the digests bind the record; the "tamper-evident" claim is overstated while F1 (planted extract) and F3 (`--write` cache) stand.
VERDICT: coverage — the 12-class harness is reproduced but not exhaustive; F1 is an unclosed class under the harness's own attacker model.
