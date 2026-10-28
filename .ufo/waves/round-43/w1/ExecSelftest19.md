# ExecSelftest19 — kasegi-shokunin round 43, wave 1

Seat: `ExecSelftest19` (executor, instrument QA — the graded selftest runner block).
Axes: `depth:verifiability`, `coverage`.
Lane: `/home/vgpnk/Projects/shokunin/kasegi-shokunin`.
Base `ab98fac9dce87130bc4f66de89e30650d63943dc`; lane HEAD at read time
`4cb6d4ae768481e1a14afbedc2d865a060ebacfd` (round-43 frozen claims + controls +
freeze record). Frozen claims read first (`.ufo/waves/round-43/claims.json`,
sha256 `a4c03e1e…a6630`), not edited. Controls read, not edited.

Deliverables written (this seat's only writes besides this receipt):

| file | lines | sha256 |
|---|---:|---|
| `.ufo/waves/round-43/w1/ExecSelftest19.sh` | 999 | `d2c947b4a5004d49f9677479f6142a10b1d796f638da3fd3481863ffb5a11848` |
| `.ufo/waves/round-43/w1/ExecSelftest19.cases.txt` | 19 | `91b3add4f1d42a0966bbad627755963e848d7448bc1d9c8dacf7643ed9ec509a` |

---

## 1. What the block is

`ExecSelftest19.sh` is the runner the r43 suite embeds to grade K1–K19. It prints
exactly the grammar the frozen C1 predicate names, and nothing else:

```
selftest case=K<n> mutants=<good>/<total> positive=<pass|fail> payload-match=<0|1> verdict=<pass|fail>
selftest cases=19 failures=<k>
```

Exit `0` only when every selected case prints `verdict=pass`; `1` when any case
fails; `2` on a usage error; `3` when the runner's own degenerate-control probe
accepts a degenerate (nothing is written to stdout then — a degraded runner must
never emit a green summary).

Per case, four private trees under `<work>/selftest/case-<id>/`, never inside
the export:

| tree | content | required verdict |
|---|---|---|
| `pos/` | the case's correction present | `closed=1` |
| `mut-committed/` | the **committed** r42 defeat bytes, installed by `git cat-file -p <base>:<path>` and re-verified against the committed sha256 after every builder ran | `closed=0` |
| `mut-shape/` | the committed defect **duplicated verbatim and only its first occurrence rewritten** | `closed=0` |
| `pos/` again | second dispatch of the same tree | payload must equal the first (drift = red) |

`mutants=<good>/2` for K14–K19, so a check that accepts either the committed
defeat or its duplicated shape cannot print `verdict=pass`. K1–K13 are graded
through the suite's carried battery hook and require `total >= 1`: **a zero-mutant
battery is a red**, so a summary-only line can never satisfy a case.

Isolation, asserted on every dispatch (`probe()`), not asserted by convention:

* the tree handed to the check resolves **inside** the case's own directory and is
  not the directory itself;
* exactly **one** `case-*` directory exists under `<work>/selftest` at dispatch
  time (cases are serial and each directory is removed before the next is made,
  then its absence is re-asserted), so a sibling's tree does not exist to be read;
* every case directory carries a unique canary; a canary appearing in a payload is
  a leak and reds the case.

Dispatch contract: `--check-cmd TEMPLATE` is run as
`bash -c TEMPLATE es19 <case-id> <tree>` (`$1` = `K14`, `$2` = tree) and must
print one line `K<n> payload=... closed=0|1` whose `n` is the case's own — a
missing line, two lines, or another case's id is a red. Embedded, the engine is
called as `main(argv, dispatch_fn)` with an in-process callable and needs no
`--check-cmd`.

`payload-match`: with `--run-transcript <run output>`, each positive payload must
equal that transcript's payload for the same id (`,replay=` stripped). Without it,
the positive tree is dispatched twice and the payloads must be identical and
non-empty — a check whose payload drifts between two identical trees is reading
state it does not own.

---

## 2. Evidence (commands and their real output)

Scratch: `/fast/scratch/hyaku/kasegi-r43/ExecSelftest19/` (`$S` below), removed
before yield. Two exports were used, both created with read-only git:

```
$ git -C <lane> archive ab98fac9dce87130bc4f66de89e30650d63943dc | tar -x -C $S/base
$ git -C <lane> archive 4cb6d4ae768481e1a14afbedc2d865a060ebacfd | tar -x -C $S/head
$ du -sh $S/head
153M	/fast/scratch/hyaku/kasegi-r43/ExecSelftest19/head
```

`base` supplies the committed defect bytes; `head` supplies the round-43 tree
(claims, controls, freeze record) the positive fixtures are built on.

Two dispatchers were used for the demo, both recorded by digest:

```
fc205772d8148551bea3c526d1058aec32782f5ef2f3896561e0d85fd968c0c7  $S/ref-k14.sh
b9b6d387d9bdd8b799045b71f9d5b7871eb1b9e64f479ef7d5a3be43277940d2  $S/k19.sh
```

`$S/k19.sh` is the wave-1 sibling limb `.ufo/waves/round-43/w1/ExecK19Freeze.sh`
as read at 13:5x UTC (copied, not modified). `$S/ref-k14.sh` is **my own scratch
stand-in** for the K14 limb — the real K14 limb is a sibling's; the runner does
not embed either.

### 2.1 Controls (deliverable bytes)

```
$ bash .ufo/waves/round-43/w1/ExecSelftest19.sh --export $S/head --work $S/f1 \
    --check-cmd '<K14->ref-k14.sh, K19->k19.sh>' --probe-controls
control=D-STUB expected=reject observed=reject
control=D-SUMMARY expected=reject observed=reject
control=D-DUPLICATE expected=reject observed=reject
control=ACCEPT expected=accept observed=accept
rc=0
```

`ACCEPT` exists so a reject-everything acceptor cannot pass: the runner's own
well-formed nineteen-line transcript is accepted.

### 2.2 Two cases end to end (deliverable bytes)

```
$ bash .ufo/waves/round-43/w1/ExecSelftest19.sh --export $S/head --work $S/f4 \
    --check-cmd '<K14->ref-k14.sh, K19->k19.sh>' --cases K14,K19
selftest case=K14 mutants=2/2 positive=pass payload-match=1 verdict=pass
selftest case=K19 mutants=2/2 positive=pass payload-match=1 verdict=pass
selftest cases=2 failures=0
rc=0
```

The dispatch log proves each probe is handed its own private tree:

```
ARGV K14 …/case-K14/pos
K14 payload=literals=1,stale=0,truth=35 closed=1
ARGV K14 …/case-K14/mut-committed
K14 payload=literals=1,stale=1,truth=34 closed=0
ARGV K14 …/case-K14/mut-shape
K14 payload=literals=2,stale=2,truth=35 closed=0
ARGV K14 …/case-K14/pos
K14 payload=literals=1,stale=0,truth=35 closed=1
ARGV K19 …/case-K19/pos
K19 payload=freeze=present,order=ok,sha=match closed=1
ARGV K19 …/case-K19/mut-committed
K19 payload=freeze=absent,order=bad,sha=mismatch closed=0
ARGV K19 …/case-K19/mut-shape
K19 payload=freeze=present,order=bad,sha=match closed=0
ARGV K19 …/case-K19/pos
K19 payload=freeze=present,order=ok,sha=match closed=1
```

### 2.3 Mutant evidence measured outside the runner

```
$ sha256sum m14/SCORECARD.md          # after `git cat-file -p ab98fac9:SCORECARD.md`
d46a8c3645e58f566725b8a3ea318aeb95b597234d8908456c08e2b65e827cc3  m14/SCORECARD.md
--- K14 committed mutant ---
K14 payload=literals=1,stale=1,truth=34 closed=0      (rc=1)
--- K14 shape mutant (dup line 1634, first rewritten, defect kept=True) ---
K14 payload=literals=2,stale=2,truth=35 closed=0      (rc=1)
--- K14 shape mutant, first-occurrence-only check ---
K14 payload=first=34 closed=1                          <-- the escape the control catches
--- K19 committed mutant (freeze record removed) ---
K19 payload=freeze=absent,order=bad,sha=mismatch closed=0   (rc=1)
--- K19 stale-label shape (committed r42 label 12:05:00Z) ---
K19 payload=freeze=present,order=bad,sha=match closed=0      (rc=1)
--- K19 positive ---
K19 payload=freeze=present,order=ok,sha=match closed=1       (rc=0)
```

The committed-defect provenance is real, not asserted: `git cat-file -e` on the
base ref refuses the round-43 freeze record, which is exactly the K19 mutant —

```
$ git -C <lane> cat-file -e ab98fac9…:.ufo/waves/round-43/freeze.txt
fatal: path '.ufo/waves/round-43/freeze.txt' exists on disk, but not in 'ab98fac9…'
rc=128
```

and the one `corrections=` literal in the three records at base is the RD42-1
defect (`corrections=33` at `SCORECARD.md:1634`, against 34 `Correction (` lines
in `SCORECARD.md`/`LOG.md`/`SHONEN.md`).

### 2.4 Degenerate controls rejected end to end

Always-pass stub (D-STUB), on the case whose mutant battery it cannot see:

```
$ … --check-cmd 'printf "K18 payload=always-pass closed=1\n"' --cases K18
selftest case=K18 mutants=0/2 positive=pass payload-match=1 verdict=fail
selftest cases=1 failures=1
ExecSelftest19: K18 red: mutant:accepted;shape:accepted
rc=1
```

First-occurrence-only check (D-DUPLICATE), on K14's duplicated-block mutant — it
accepts the positive and rejects the committed defect, and it is caught **only**
by the shape mutant:

```
$ … --check-cmd '<first-occurrence reader>' --cases K14
selftest case=K14 mutants=1/2 positive=pass payload-match=1 verdict=fail
selftest cases=1 failures=1
ExecSelftest19: K14 red: shape:accepted
rc=1
```

Summary-only transcript (D-SUMMARY): `accept_selftest("selftest cases=19 failures=0\n", 19)`
returns false — no case line, no acceptance (measured through `--probe-controls`,
§2.1).

### 2.5 Every K14–K19 builder builds; the runner discriminates

Stub that always closes (only "mutant accepted" may be reported — no builder
error):

```
selftest case=K14 mutants=0/2 positive=pass payload-match=1 verdict=fail
selftest case=K15 mutants=0/2 positive=pass payload-match=1 verdict=fail
selftest case=K16 mutants=0/2 positive=pass payload-match=1 verdict=fail
selftest case=K17 mutants=0/2 positive=pass payload-match=1 verdict=fail
selftest case=K18 mutants=0/2 positive=pass payload-match=1 verdict=fail
selftest case=K19 mutants=0/2 positive=pass payload-match=1 verdict=fail
ExecSelftest19: K14 red: mutant:accepted;shape:accepted   (same for K15..K19)
```

Stub that never closes — both mutants rejected, the positive fails:

```
selftest case=K15 mutants=2/2 positive=fail payload-match=1 verdict=fail
ExecSelftest19: K15 red: positive:closed=0
```

### 2.6 Transcript path

```
$ … --run-transcript tr-ok.txt   # payloads taken from §2.2's positive probes
selftest case=K14 mutants=2/2 positive=pass payload-match=1 verdict=pass
selftest case=K19 mutants=2/2 positive=pass payload-match=1 verdict=pass
selftest cases=2 failures=0   (rc=0)

$ … --run-transcript tr-bad.txt  # forged payloads
selftest case=K14 mutants=2/2 positive=pass payload-match=0 verdict=fail
selftest case=K19 mutants=2/2 positive=pass payload-match=0 verdict=fail
selftest cases=2 failures=2   (rc=1)
```

### 2.7 Isolation assertions bite (non-vacuity)

A dispatch that creates a sibling `case-K99/` is caught structurally:

```
selftest case=K14 mutants=0/2 positive=pass payload-match=1 verdict=fail
ExecSelftest19: K14 red: mutant:accepted;shape:accepted;isolation
```

A dispatch that reads its own fixture canary is caught as a leak:

```
selftest case=K14 mutants=0/2 positive=fail payload-match=1 verdict=fail
ExecSelftest19: K14 red: mutant:accepted;shape:accepted;positive:leak
```

### 2.8 Carried cases fail closed without their battery

```
$ … --check-cmd 'printf "K1 payload=records=1 closed=1\n"' --cases K1
selftest case=K1 mutants=0/0 positive=pass payload-match=1 verdict=fail
selftest cases=1 failures=1
ExecSelftest19: K1 red: hook-absent
rc=1
```

### 2.9 Embedded callable path

The engine body was extracted (`awk` between the heredoc markers) and called as
the suite will call it:

```
$ python3 embed_driver.py     # e.main([...], dispatch_fn=dispatch)
selftest case=K14 mutants=2/2 positive=pass payload-match=1 verdict=pass
selftest case=K19 mutants=2/2 positive=pass payload-match=1 verdict=pass
selftest cases=2 failures=0
embedded rc=0
```

### 2.10 Cost

`/fast/scratch` is XFS; `cp -a --reflink=auto` of the 153 MB export measured
`copy-ms=443`. Four copies per narrative case ⇒ ~1.8 s of copying per case plus
check time; the demonstrated two-case run took ~7 s wall.

---

## 3. Integration notes for the L1 / suite seat

1. Embed the Python body (between the `ES19_PY` markers) in `r43-closure.sh`'s
   engine and call `main(["--export", EXPORT, "--work", WORK,
   "--run-transcript", RUN_TRANSCRIPT], dispatch_fn=check_dispatch)` from
   `--selftest`. `check_dispatch(case_id, tree)` must return the one graded line
   the suite's K<n> limb prints for that tree.
2. Define `CARRIED_BATTERY` as a module-level dict
   `{"K1": fn(export, case_dir) -> (good, total), …}` wiring the r42 wave-1
   mutant batteries (`ExecSelftest.mutants.txt` families) and the replay limbs.
   Without it K1–K13 print `mutants=0/0 verdict=fail` by design.
3. Keep the case loop serial: `probe()` asserts a single live `case-*` directory.
4. The K14–K19 positive fixtures are runner-owned and deliberately quote the
   token they supersede on the `Correction (round 43)` line. The limbs must
   therefore exclude `Correction (round 43)` lines (and, for K17, claims-erratum
   lines) from their assertion sets — otherwise no correction can ever name the
   defect it supersedes. This is the one reading of the frozen predicate that is
   self-consistent; the K14 stand-in implements it that way.

---

## 4. Risks and honest limits

1. **K1–K13 are not graded here.** No suite exists yet at read time, so their
   batteries are wired, not executed. The block fail-closes on a missing hook,
   and the r42 mutant labels/artifact digests it reports are the r42 suite's own
   (`DEFEAT_ARTIFACTS`, copied, not re-derived).
2. **The K14 demo used my scratch stand-in**, not the real K14 limb (no sibling
   K14 deliverable existed when this seat closed). The K19 demo used the sibling
   `ExecK19Freeze.sh` at sha `b9b6d387…`; if that sibling revises its limb, this
   receipt's digest no longer binds, though the runner embeds neither.
3. **`payload-match` without `--run-transcript` is a determinism check**, not a
   transcript check. The suite must pass `--run-transcript` for the frozen
   `payload-match=1` to mean "matches the run".
4. **Per-case cost scales with the export** (four full copies). With reflink this
   is ~1.8 s/case at 153 MB; without reflink it would be ~600 MB/case.
5. The K14 stand-in's `truth` moves when the shape mutant duplicates a
   `Correction (` line (35 in the shape mutant): that is a property of the
   stand-in's counter, not of the runner, and it only makes the mutant easier to
   reject, never easier to accept.

## 5. Hygiene

* Scratch `/fast/scratch/hyaku/kasegi-r43/ExecSelftest19/` — removed before yield.
* Disk guard before and after the pass: `/fast/scratch/hyaku 27% 590.2G free`,
  `/tmp 17% 106.8G`, `/var/tmp 38% 557.1G` (no capacity warning).
* No mutating git/jj anywhere: the lane was only read
  (`archive`, `cat-file -p`, `cat-file -e`); the only git writes in this seat
  were the scratch exports' extraction. No fixture repo was created.
* No tool installs (python3, git, tar, cp, awk all present). `pacman` not touched
  (host-wide pause). `~/.omp/agent/RULES.md` read.
* No network fetches by this seat.
* Fleet-root tracked files untouched; lane writes are the two deliverables and
  this receipt, all under `.ufo/waves/round-43/w1/`.

Report: `.ufo/waves/round-43/w1/ExecSelftest19.md`
