# MutK18K19 — mutation probe, K18 and K19 (round 43)

Seat: MutK18K19 (mutation-tester, leaf). Lane: kasegi-shokunin.
Base: `ab98fac9dce87130bc4f66de89e30650d63943dc`. Claims read from
`.ufo/waves/round-43/claims.json` (sha256 `a4c03e1e…a6630`, never edited).
Verdict: **5/5 assigned mutants killed**; 2/2 applicable classes on K18, 3/3 on K19,
the other five class/limb pairs are not applicable to the limb they were aimed at
(evidence below, not an assumption).

## 1. Bytes under test

| artifact | lines | sha256 (bytes tested) |
|---|---|---|
| `.ufo/waves/round-43/w1/ExecK18Transcript.sh` | 260 | `8b797e424d5d3f35da0897fb36e7b3c294f3aa7f445e9313163e4170f0cfd029` |
| `.ufo/waves/round-43/w1/ExecK19Freeze.sh` | 243 | `8e6b124feb975469e0837de4a3998ccf6a940543a19bfae93b9ec73d5165d7f2` |

Both files were revised twice by their executor while this seat was probing
(K18 `838fc25d` → `3d92d8ae` → `8b797e42`; K19 `b9b6d387` → `8e6b124f`). The baseline,
every mutant and every restore run below were re-executed from scratch on the
final bytes; the earlier revisions' results were discarded, not carried forward.
Both hashes were re-read at `2026-10-28T16:47:45Z` and are the bytes measured here.

## 2. Detector

One detector per limb: a fixed fixture set, run once as `bash -c '. "$1"; check_kN "$2"'`
per fixture, recording the printed line and the return status. A mutant is **killed**
when at least one fixture's (line, status) differs from the pristine run; a fixture that
is red in the baseline can only be flipped to green by a weakened check, so each kill
names the direction. Fixtures are scratch trees built with `git archive` (read-only)
of the lane plus hand-written record/transcript bytes; no lane byte was altered.

K18 fixtures (`fix18/`), each a minimal tree of `corpus/lessons/` + `.ufo/waves/round-43/`:

| fixture | content | expected |
|---|---|---|
| `g-green` | record quotes `closed=19/19`; `final-gates/run.txt` has `export-ref=<40hex>` + summary line `closed=19/19 exit=0` | green |
| `g-reportonly` | record line `draft tally \`closed=7/7\` report-only`, no transcript | green (exemption) |
| `g-filename` | record quotes `selftest cases=19 failures=0`; the only occurrence of that string is the FILE NAME `final-gates/selftest cases=19 failures=0.txt`, contents have no summary line | red (filename must not bind) |
| `g-unbound` | record quotes `closed=5/9`, nothing binds it | red |
| `g-fenced` | record contains a fenced block with `closed=11/13 exit=1`; the record is never its own transcript | red |

K19 fixtures (`fix/`): `base` = export of `ab98fac9` (no round-43 record);
`live` = export of HEAD `4cb6d4a` (committed freeze record, green);
`f-digest` (one nibble of `claims-sha256` flipped), `f-early` (claims `frozen_at_utc`
and record `frozen-at` both `2026-10-28T16:30:00Z`, four minutes before the c2 control
`16:34:15Z`, digest regenerated), `f-calendar` (`2026-13-45T99:99:99Z`, regex-clean,
calendar-invalid, digest regenerated), `f-offset` (`2026-10-28T08:00:01-03:00`, both
records agreeing on the string), `f-dupe` (second `measured-at=` line in c1),
`f-maxdrift` (`measured-at-max=2026-10-28T16:34:16Z`).

### Baseline (pristine, per limb)

```
g-green       rc=0  K18 payload=quotes=1,bound=1,report-only=0,superseded=0,unbound=0 closed=1
g-reportonly  rc=0  K18 payload=quotes=1,bound=0,report-only=1,superseded=0,unbound=0 closed=1
g-filename    rc=1  K18 payload=quotes=1,bound=0,report-only=0,superseded=0,unbound=1 closed=0
g-unbound     rc=1  K18 payload=quotes=1,bound=0,report-only=0,superseded=0,unbound=1 closed=0
g-fenced      rc=1  K18 payload=quotes=1,bound=0,report-only=0,superseded=0,unbound=1 closed=0

base          rc=1  K19 payload=freeze=absent,order=bad,sha=mismatch closed=0
live          rc=0  K19 payload=freeze=present,order=ok,sha=match closed=1
f-digest      rc=1  K19 payload=freeze=present,order=ok,sha=mismatch closed=0
f-early       rc=1  K19 payload=freeze=present,order=bad,sha=match closed=0
f-calendar    rc=1  K19 payload=freeze=present,order=bad,sha=match closed=0
f-offset      rc=1  K19 payload=freeze=present,order=bad,sha=match closed=0
f-dupe        rc=1  K19 payload=freeze=present,order=bad,sha=match closed=0
f-maxdrift    rc=1  K19 payload=freeze=present,order=bad,sha=match closed=0
```

## 3. Mutants

All five are one-limb, one-behaviour patches applied to a scratch copy of the limb;
the lane file was never written. Patches quoted as produced by `diff -u`.

### M18-1 — drop the report-only exception → KILLED (false positive)

```diff
@@ -217,8 +217,6 @@
             quotes += 1
             if tok in bound:
                 bcount += 1
-            elif "report-only" in line:
-                rcount += 1
             elif tok in superseded:
                 scount += 1
             else:
```
mutant sha256 `99600ad3c2170e533b848da106c653beac50545fb272618099acc444e8cdc755`

```
g-reportonly  pristine[rc=0] K18 payload=quotes=1,bound=0,report-only=1,superseded=0,unbound=0 closed=1
              mutant  [rc=1] K18 payload=quotes=1,bound=0,report-only=0,superseded=0,unbound=1 closed=0
```
The detector sees the exemption disappear and the count move from `report-only=1` to
`unbound=1`; the mutant reds a record the frozen rule exempts. Killed.

### M18-2 — accept a token that occurs only in a filename → KILLED (false negative)

```diff
@@ -130,6 +130,9 @@
         if not text:
             continue
         transcripts.append(rel)
+        for rx in (CLOSED_RX, SUMMARY_RX):
+            for m in rx.finditer(os.path.basename(rel)):
+                bound.add(m.group(0))
         for line in text.split("\n"):
```
mutant sha256 `94de90ce5e95be9500812b1cc435f339236dd7194feee12e93affc1f7096315e`

```
g-filename    pristine[rc=1] K18 payload=quotes=1,bound=0,report-only=0,superseded=0,unbound=1 closed=0
              mutant  [rc=0] K18 payload=quotes=1,bound=1,report-only=0,superseded=0,unbound=0 closed=1
```
A value that exists only as a file name is accepted as evidence; the unbound quote
turns green while `g-unbound` and `g-fenced` stay red. Killed.

### M19-1 — skip the claims-digest comparison → KILLED (false negative)

```diff
@@ -209,11 +209,7 @@
     claims_base = claims.get("base")
-    digest_match = (
-        claims_bytes is not None
-        and HEX64_RX.match(record["claims-sha256"]) is not None
-        and hashlib.sha256(claims_bytes).hexdigest() == record["claims-sha256"]
-    )
+    digest_match = True  # M19-1: digest comparison skipped
```
mutant sha256 `fb020d7732c632a5eb7474bed7b3fbb99f1b2800b9dacb1e9745313b9d1219eb`

```
f-digest      pristine[rc=1] K19 payload=freeze=present,order=ok,sha=mismatch closed=0
              mutant  [rc=0] K19 payload=freeze=present,order=ok,sha=match closed=1
```
A freeze record whose `claims-sha256` does not cover the claims bytes is accepted and
the payload claims `sha=match`. Killed by `f-digest`.

### M19-2 — accept a timestamp that does not parse → KILLED (false negative)

```diff
@@ -82,11 +82,7 @@
     if not isinstance(value, str) or not ISO_Z_RX.match(value):
         return None
-    try:
-        stamp = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
-    except ValueError:
-        return None
-    return stamp if stamp.strftime("%Y-%m-%dT%H:%M:%SZ") == value else None
+    return tuple(int(part) for part in re.split(r"[-T:Z]", value) if part)
```
mutant sha256 `c33f7ecb0208c8c010499d68a8ff4ce698114e1ffa012dc1d66e3b3f90343854`

```
f-calendar    pristine[rc=1] K19 payload=freeze=present,order=bad,sha=match closed=0
              mutant  [rc=0] K19 payload=freeze=present,order=ok,sha=match closed=1
```
With calendar validation replaced by a lexical tuple, `2026-13-45T99:99:99Z` parses,
orders after the controls and closes; the strict limb rejects it. The regex gate on
its own (`f-offset`, `2026-…-03:00`) stays red under the mutant, so the kill is
attributable to the removed calendar check. Killed.

### M19-3 — accept a freeze record whose label precedes the controls → KILLED (false negative)

```diff
@@ -221,7 +221,6 @@
         and claims_frozen is not None
         and frozen_at == claims_frozen          # (3) record label == claims label
-        and frozen_at >= measured_max           # (2) label not earlier than controls
         and stated_max == measured_max          # (4) record states the real max
```
mutant sha256 `711c6c3e45d283216ddd5dbf25615a3370d0d988824a67e5836c5a1ce85901bb`

```
f-early       pristine[rc=1] K19 payload=freeze=present,order=bad,sha=match closed=0
              mutant  [rc=0] K19 payload=freeze=present,order=ok,sha=match closed=1
```
The RD42-6 defect itself — a freeze record labelled four minutes before the control
it freezes — is accepted. `f-digest`, `f-calendar`, `f-offset`, `f-dupe` and
`f-maxdrift` stay red, so the kill is the removed ordering relation, not a
side effect. Killed.

## 4. Battery classes with no limb point (not skipped silently)

| class | limb | evidence |
|---|---|---|
| drop the report-only exception | K19 | `grep -c 'report-only' limb/k19.sh` → 0; K19 has no exemption path, its only acceptance predicate is `order_ok and digest_match`. |
| accept a token that occurs only in a filename | K19 | `grep -cE 'listdir\|glob\|walk\|basename\|scandir'` → 0 for each; K19 reads exactly two files named in claims (`controls.c1`, `controls.c2`) plus the fixed claims/freeze paths — no directory enumeration, no name matching. |
| skip the claims-digest comparison | K18 | `grep -c 'sha256\|hashlib'` → 0 / 0; K18 has no digest input. |
| accept a timestamp that does not parse | K18 | `grep -c 'iso\|datetime'` → 0 / 0; K18 reads no timestamp. |
| accept a freeze record whose label precedes the controls | K18 | `grep -c 'freeze\|measured-at\|claims.json'` → 0 / 0 / 0; K18 does not read the freeze record. |

## 5. Base-red corroboration (the frozen K14–K19 requirement)

`git -C <lane> archive ab98fac9… | tar -x -C <scratch>/fix/base` (and `HEAD` → `fix/live`):

```
--- K18 at base ab98fac9 (must be open)
base  rc=1  K18 payload=quotes=22,bound=19,report-only=0,superseded=0,unbound=3 closed=0
--- K18 at live HEAD 4cb6d4a
live  rc=1  K18 payload=quotes=22,bound=19,report-only=0,superseded=0,unbound=3 closed=0
--- K19 at base ab98fac9 (must be open)
base  rc=1  K19 payload=freeze=absent,order=bad,sha=mismatch closed=0
--- K19 at live HEAD 4cb6d4a (must be closed)
live  rc=0  K19 payload=freeze=present,order=ok,sha=match closed=1
```
K18 is open at base and still open at HEAD — correct while the RD42-5 correction and
the `r42-at-de09313` transcript are unlanded (the head-green state belongs to J, not
to this commit). K19 is open at base and closed at HEAD.

## 6. Restoration evidence

- Mutants lived only under the seat scratch dir; the lane limb files were opened
  read-only and copied. `sha256sum` of the lane limbs before the battery and at
  `2026-10-28T16:47:45Z` after it are the same pair printed in §1
  (`8b797e42…d029`, `8e6b124f…d7f2`), i.e. no byte of either lane file changed.
- The pristine detector was re-run after each battery: `diff -u` of
  pristine vs restored output is empty for both limbs
  (`restored18=identical`, `restored19=identical`).
- Scratch removed after the measurements:
  `rm -rf -- /fast/scratch/hyaku/kasegi-r43/MutK18K19` →
  `ls: cannot access '/fast/scratch/hyaku/kasegi-r43/MutK18K19': No such file or directory`.

## 7. Notes for the L1 (observations, no recommendation to change the contract)

- Both limbs were edited twice mid-wave. Any verdict in the round report must name
  the limb sha it was measured on; this receipt pins `8b797e42…` (K18) and
  `8e6b124f…` (K19). A later edit invalidates §3 and needs a re-run, not a re-quote.
- The current K19 enforces three relations beyond its item spec: claims identity
  (`round == 43`, `lane == "kasegi"`), two distinct control files, and an optional
  caller-supplied commit-instant bound that is red when present-but-unparseable.
  Each is extra strictness directed at the same RD42-6 class; none weakened any of
  the five probed classes (all baselines above hold with those relations active).
- The current K18 no longer requires an `export-ref=` header on a transcript; every
  committed file under the two wave dirs that is not a record is evidence, and only a
  summary-shaped line binds. `g-filename` and `g-fenced` are the two fixtures that
  keep that rule honest after the change; both are red in the baseline.

## 8. Tooling, network, hygiene

No tool installed or upgraded (bash, python3 3.x and read-only `git archive` sufficed);
no network fetch was made, so no HTTP status/byte count applies. Disk guard checked
before the heavy pass: `/fast/scratch/hyaku` 26% used, 600.8G free. No mutating git/jj
command was run anywhere; the only git use was `rev-parse` and `archive` on the lane.
No lane file other than this receipt was written.
