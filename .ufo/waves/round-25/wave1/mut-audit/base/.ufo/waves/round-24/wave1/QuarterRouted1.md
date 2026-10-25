# QuarterRouted1 — routed defect 1: F01–F05 `recheck:` against the round-23 manifest

Measurement base: lane HEAD `c2480b143120364728b40397926ffcf30a7309c8`.
`git -C <lane> status --porcelain corpus/` → `M corpus/instruments/resolve.py`,
`?? corpus/instruments/resolve-dispatch-check.py`, `?? corpus/instruments/resolve-dispatch-fixtures.json`
— a peer seat's C1-B work, untouched by me. `corpus/knowledge/`, `corpus/source-snapshots/round-23/`
and `corpus/instruments/source-recheck.py` are clean at HEAD, so every number below is from committed bytes.
All commands were run from `/home/vgpnk/Projects/shokunin/kasegi-shokunin` unless a line says otherwise.
This seat is read-only: no file outside this report was written; no install was performed.

## Verdict on the round-23 spot-check's defect 1

**It matches.** `corpus/lessons/round-23-verifier-spotcheck.md:119-121` says "F01–F05 `recheck:` lines
exit 2 `not-listed` — no capture exists for S001–S015". Both halves reproduce:

- All five entry recheck lines exit **2**; each emits `S0xx:source UNAVAILABLE reason=not-listed`.
- `corpus/source-snapshots/` holds exactly one directory (`round-23`) and one manifest
  (`corpus/source-snapshots/round-23/manifest.json`, ids `S018, S029, S030, S031`);
  `find . -type f \( -name 'S00[1-9]*' -o -name 'S01[0-5]*' \)` outside `.git` → **no files**.
  No S001–S015 capture exists anywhere in the lane **at HEAD and at my measurement time**, not merely
  "absent from this manifest". (An uncommitted round-24 capture set appeared while I was measuring —
  see *In-flight delta* below; it is not committed and carries no manifest.)

Four things the sentence does not say, each verified below: the recheck base is a manifest whose own
`purpose` excludes these five entries (F1); the `&&` chain hides 10 of the 15 ids (F2); exit 2 is
overloaded and the F01–F05 lines are lane-root-relative unlike F06–F08 (F3); the diagnostic is on
**stdout**, stderr is empty (F4).

## Findings

### F1 — HIGH — the five recheck lines point at a manifest that declares itself scoped to other entries

`corpus/source-snapshots/round-23/manifest.json:3`:

```
"purpose": "Round-23 F06-F08 captured-source assertions. Each quote is an exact substring of the pinned excerpt beside this manifest; ..."
```

F01–F05 cite that path in their `recheck:` field. So this is not a coverage hole inside a shared
manifest — it is a **mis-pointed recheck**: the carrier says in its first field that those ids are not
its subject. Fixing it needs a capture set for S001–S015 (or a re-pointed/retired recheck line), not an
edit to this manifest.

### F2 — HIGH — `&&` short-circuits, so each line exercises 1 of its 2–4 ids

The chained form reports only the first missing id; the remaining ids are never evaluated by the
entry's own command. Ids *never reached* by the entry command (verified separately, all exit 2
`not-listed`): S002, S004, S005, S007, S008, S010, S011, S012, S014, S015 — 10 of 15.

Consequence for the round-24 write seat: capturing one id flips the *entry* count only when it is the
entry's first id. Capturing S002 alone would leave F01 at exit 2, so counter A (entries at exit 0)
does not measure per-id capture progress — it measures "first uncaptured id is captured".

### F3 — MEDIUM — exit 2 is overloaded and the F01–F05 lines are CWD-dependent

`corpus/instruments/source-recheck.py` returns 2 for `reason=not-listed` (lines 160-161, inside
`recheck()` at line 151), for `manifest UNAVAILABLE reason=missing` (lines 49-52), and for a listed
source whose snapshot file is absent (`S0xx:source UNAVAILABLE reason=missing`, line 114). Bare "exit 2"
pins none of them; only the status string does.

The F01–F05 lines begin `python3 corpus/instruments/...` with no `cd`, while F06–F08 begin
`cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && ...`. Run verbatim from a foreign cwd:

```
$ cd /tmp && bash -c "python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-23/manifest.json --source S001 && python3 ... --source S002"
python3: can't open file '/tmp/corpus/instruments/source-recheck.py': [Errno 2] No such file or directory
exit=2
```

Same exit code, entirely different cause, and the cause lands on **stderr**. A consumer that records
`$?` only cannot tell a wrong-cwd failure from the real `not-listed`.

### F4 — MEDIUM — the diagnostic is on stdout; stderr is empty

`emit()` writes to `out=sys.stdout` (source-recheck.py:32-35, called with the default at :160).
Separated capture for F01:

```
exit=2
STDOUT:[S001:source UNAVAILABLE reason=not-listed]
STDERR:[]
STDERR byte count: 0
```

Every "full stderr" for the eight entries is the empty string. A harness that captures stderr as the
failure reason records nothing.

### F5 — LOW — S030's seven assertions are now orphaned, and they are the only ones exercising the normalization fallback

F07 (`cna-assignment-and-vulnerability-rules.md:5`) runs `--source S031`; `grep -rn -- '--source S030' corpus/`
→ no hits in `corpus/`. S030 stays in the manifest with 7 quotes + digest that no knowledge entry's
recheck executes (only round-23 wave artifacts, e.g. `.ufo/waves/round-23/falsify/ControlsRerun.md:266`,
ran it).

That matters more than it looks, because S030 is also the only source whose recheck does not pass on
plain substring matching:

```
S030:sha256 OK
S030:rule-3-1-1-scope-definition OK
S030:rule-3-1-4-covered-products OK
S030:rule-4-1-2-security-impact OK
S030:rule-4-1-9-independently-fixable OK normalized=markup-whitespace
S030:rule-4-2-1-1-first-opportunity OK
S030:rule-4-2-11-separate-ids OK
S030:rule-4-2-12-uncertainty OK
exit 0
```

S018, S029 and S031 print no `normalized=` marker on any assertion. So after F07 moved to S031, the
single assertion that depends on the whitespace/`<u>` normalization path is exercised by nothing a
frontier entry rechecks — a regression in that path would no longer be caught by counter A. Assertion-id
coverage itself is complete: for every manifest source the ids printed equal the manifest's ids
(S018 6/6, S029 9/9, S030 7/7, S031 10/10), and stderr was 0 bytes in every run.

## Per-entry reproduction (verbatim, lane root)

Each command is the entry's own `recheck:` line; `2>&1` merge shown, with stderr separately proven
empty for F01 (F4) — stderr is empty for all eight for the same reason.

### F01 `cvss-v4-severity-and-vector` — recheck at `:4`, 2 ids → exit **2**

cmd: `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-23/manifest.json --source S001 && python3 ... --source S002`

stdout:
```
S001:source UNAVAILABLE reason=not-listed
```
Missing from `round-23/manifest.json`: **S001** (emitted) and **S002** (chain aborted, verified
separately: exit 2, `S002:source UNAVAILABLE reason=not-listed`).

### F02 `coordinated-disclosure-timelines` — recheck at `:4`, 3 ids → exit **2**

```
S003:source UNAVAILABLE reason=not-listed
```
Missing: **S003** (emitted), S004, S005 (chain aborted; each verified exit 2 individually).

### F03 `authorization-safe-harbor-and-scope` — recheck at `:4`, 3 ids → exit **2**

```
S006:source UNAVAILABLE reason=not-listed
```
Missing: **S006** (emitted), S007, S008.

### F04 `ai-assisted-finding-validation` — recheck at `:4`, 4 ids → exit **2**

```
S009:source UNAVAILABLE reason=not-listed
```
Missing: **S009** (emitted), S010, S011, S012.

### F05 `cwe-top25-2025-methodology` — recheck at `:4`, 3 ids → exit **2**

```
S013:source UNAVAILABLE reason=not-listed
```
Missing: **S013** (emitted), S014, S015.

Per-id sweep of all fifteen (each run in isolation):

```
S001 exit=2 out=[S001:source UNAVAILABLE reason=not-listed]
S002 exit=2 out=[S002:source UNAVAILABLE reason=not-listed]
S003 exit=2 out=[S003:source UNAVAILABLE reason=not-listed]
S004 exit=2 out=[S004:source UNAVAILABLE reason=not-listed]
S005 exit=2 out=[S005:source UNAVAILABLE reason=not-listed]
S006 exit=2 out=[S006:source UNAVAILABLE reason=not-listed]
S007 exit=2 out=[S007:source UNAVAILABLE reason=not-listed]
S008 exit=2 out=[S008:source UNAVAILABLE reason=not-listed]
S009 exit=2 out=[S009:source UNAVAILABLE reason=not-listed]
S010 exit=2 out=[S010:source UNAVAILABLE reason=not-listed]
S011 exit=2 out=[S011:source UNAVAILABLE reason=not-listed]
S012 exit=2 out=[S012:source UNAVAILABLE reason=not-listed]
S013 exit=2 out=[S013:source UNAVAILABLE reason=not-listed]
S014 exit=2 out=[S014:source UNAVAILABLE reason=not-listed]
S015 exit=2 out=[S015:source UNAVAILABLE reason=not-listed]
```

Emitting line for every one of the fifteen: `corpus/instruments/source-recheck.py:160`
`emit(out, f"{source_id}:source", "UNAVAILABLE", "reason=not-listed")`, exit at `:161` `return 2`.
That branch is only reached when the filtered `records` list is empty — i.e. the requested id is absent
from the manifest's `sources`. It is not the mismatch path (`MISMATCH reason=quote-not-found` → exit 1,
`:143`), and it is not the only exit-2 cause (see F3).

## F06–F08 confirmation — exit **0**, full stdout

### F06 `multiparty-vulnerability-coordination` (`:4`, S018) — exit **0**

```
S018:sha256 OK
S018:comms-prior-to-disclosure OK
S018:coordinator-def OK
S018:coordinator-lead OK
S018:finder-documentation OK
S018:minimize-exposure OK
S018:upstream-vendor-def OK
```
7 lines = 1 digest + 6 quotes (`manifest.json` S018 `quotes`: 6). No `normalized=markup-whitespace`
fallback anywhere, so every quote matched as an exact substring.

### F07 `cna-assignment-and-vulnerability-rules` (`:5`, S031) — exit **0**

```
S031:sha256 OK
S031:effective-date OK
S031:rule-3-1-1-scope-definition OK
S031:rule-3-1-4-covered-products OK
S031:rule-3-2-4-2-request-method OK
S031:rule-4-1-2-security-impact OK
S031:rule-4-1-9-independently-fixable OK
S031:rule-4-2-1-1-first-opportunity OK
S031:rule-4-2-11-separate-ids OK
S031:rule-4-2-12-uncertainty OK
S031:version-4-2-6 OK
```
11 lines = 1 digest + 10 quotes (manifest S031: 10). Quote ids printed sorted, hence
`rule-...` before `version-...`.

### F08 `cra-manufacturer-reporting-duties` (`:4`, S029) — exit **0**

```
S029:sha256 OK
S029:art14-2a-early-warning OK
S029:art14-2a-track-context OK
S029:art14-2b-vulnerability-notification OK
S029:art14-2c-final-report OK
S029:art14-4a-early-warning OK
S029:art14-4b-incident-notification OK
S029:art14-4c-incident-final-report OK
S029:art71-article-14-start OK
S029:art71-general-application OK
```
10 lines = 1 digest + 9 quotes (manifest S029: 9).

## Cross-check against the frozen claim

`claims.json` C1 `counter_A.before_expected` = "3/8 exit 0 (F06, F07, F08); F01-F05 exit 2 not-listed"
— reproduces exactly, and matches the pre-existing receipt
`.ufo/waves/round-24/c1-counterA-before.txt` line for line (five `2`s then three `0`s). The do-nothing
control therefore starts at 3/8 as claimed, not at some higher number.

## In-flight delta (uncommitted peer work — not part of my committed-byte measurement)

While I measured, a writer seat created `corpus/source-snapshots/round-24/` (mtime 04:15) containing
`S001.txt` … `S015.txt` (15 files) and `corpus/instruments/capture-source.py`. **No `manifest.json`**:
`ls corpus/source-snapshots/round-24/manifest.json` → `No such file or directory`.

Consequences a round-level reader must not miss:

1. **The defect still reproduces.** The five entries' `recheck:` lines still name
   `corpus/source-snapshots/round-23/manifest.json`. Landing capture files moves counter A by zero until
   (a) a round-24 manifest exists, and (b) the five `recheck:` lines or the manifest path is re-pointed.
   Pointing at the new directory today: `--manifest corpus/source-snapshots/round-24/manifest.json --source S001`
   → `manifest UNAVAILABLE reason=missing`, exit 2 — indistinguishable by exit code from `not-listed` (F3).
2. **One capture does not carry its entry's anchor.** F02's cited location is the CISA **PDF p. 6**
   ("Establish Reasonable Time Frames for Remediation and Disclosure of Reported Vulnerabilities").
   `corpus/source-snapshots/round-24/S003.txt` is 4,392 bytes of the resources-tools **HTML landing page**
   (head shows `Skip to main content`, `.gov` banner, `Search` / `Menu`), it contains no `%PDF` / `Adobe`
   marker, and `grep -c 'Reasonable Time Frames' S003.txt` → **0**. A manifest built from this file with
   F02's quote bound to S003 would return `MISMATCH reason=quote-not-found` (exit **1**), not exit 0.
   The other four anchors are present in the in-flight set (`CVSS Base Score (CVSS-B)` → S001,
   `Removal of CWE Mapping Normalization` → S013, `Where should I start` → S009,
   `How to Enable Safe Harbors` → S006), so this is one missing capture, not a set-wide failure.
   Status: uncommitted bytes at 04:15, may change; reported because it decides whether C1's
   after-target is reachable from this capture set.

## Residual risk and verification gaps

- **Not attempted:** fetching S001–S015 to see whether the cited quotes exist upstream. The item is
  capture-side only; I make no claim about whether these five admissions are substantively true.
- **Instrument ceiling applies to my exit-0 confirmations too.** `manifest.json:3` states the instrument
  asserts substring containment only and does not machine-check that a sentence sits at the article or
  rule the entry names. My F06–F08 exit 0 confirms captured bytes match; it does **not** confirm
  location. The r23 lesson's M18 capture-gap disclosures are the only location evidence.
- **F2 makes a per-entry counter lossy.** Anything the write seat reports as "N/8 entries exit 0" cannot
  distinguish "captured every id" from "captured the first id of each entry". If C1's after-target is to
  mean 15 captures, the counter needs the per-id sweep above, not the entry chain.
- **`corpus/instruments/resolve.py` is dirty in the working tree** (peer C1-B). It does not affect any
  measurement here (knowledge/manifest/instrument bytes are clean), but a round-level "committed bytes"
  receipt for counter B must be taken from HEAD, not the tree. The tree kept growing during this seat
  (`corpus/instruments/capture-source.py`, `corpus/source-snapshots/round-24/` appeared at 04:15); a
  later reader should re-run `git status --porcelain` rather than trust the snapshot above.
- **No install or upgrade was performed** this seat; nothing outside the report was written.
