# ScribeLOG — round-38 `LOG.md` entry (draft)

Seat `ScribeLOG`, role scribe, leaf (no subagent dispatch). Axes owned by the round:
depth:verifiability, coverage. Item: draft the round-38 entry that appends to
`/home/vgpnk/Projects/shokunin/kasegi-shokunin/LOG.md` and write the landable bytes to
`.ufo/waves/round-38/wave1/ScribeLOG.block.md`.

## Deliverable

| Field | Value |
|---|---|
| Path | `.ufo/waves/round-38/wave1/ScribeLOG.block.md` |
| Lines | **15** (`wc -l` → `15`; line 15 is the Tooling bullet, file ends with one `\n`) |
| Bytes | **10810** (`stat -c %s` → `10810`) |
| sha256 | **`7396b8d29d53bd4502fcb614202033026bffcbb5ff27b40a24a1afdba020a01d`** (`sha256sum`) |

The file contains only the landable entry: one `## Round 38 — …` heading, one unlabelled
preamble paragraph, and the six bullets `C1`, `C2`, `Corrections (round 38)`, `Frontier items`,
`Wave`, `Tooling`. No validation table, no seat notes, no `## DELIVERABLE` fence, no headings
that are not part of the landed text.

Landing note: the file carries **no leading blank line**. `LOG.md` today is 1692 lines ending with
the round-37 Tooling bullet + `\n` (`tail -c 300 LOG.md | od -c` → `… (host-wide pause).\n`), and the
file separates entries with one or two blank lines — two precede the round-37 heading (`LOG.md:1676`
and `:1677` are blank, `:1678` is `## Round 37 — …`). The L1 should append one blank line (or two, to
match the round-37 spacing) and then these 15 lines verbatim; the entry's own bytes then land
unchanged.

## What I measured (commands and their real output)

All commands were read-only; none wrote outside the deliverable and this receipt. Scratch was
`S=/fast/scratch/hyaku/kasegi-r38/ScribeLOG` (created with `mkdir -p`, empty at removal).

### Claims and controls

- `python3 -c "import json; …"` over `.ufo/waves/round-38/claims.json` → read in full: base
  `a173b0c2b98c5ae39599fa9be76027fbbead0b9e`, `frozen_at_utc 2026-10-26T18:17:40Z`, C1 contract
  (8 checks G1–G8, `closed=8/8 exit=0`, `selftest cases=8 failures=0`, base and r37-head exports red),
  C2 contract (F21/S055, frontier 20→21, registry 54→55, knowledge 49→50, harness 24/24,
  binding 45/45, audit `expected=50`), and the judged-head rule (J = `export-ref=` in
  `final-gates/all-gates.txt`; Y = J + that receipt only).
- `cat c1-controls/before.txt c2-controls/before.txt census-before.txt` → read verbatim; quoted
  values used in the entry: suite `ls` exit 2; `Correction (round 38)` counts 0/0; PROVINCE fences
  `81:``` 96:```text 124:``` `; README fence `426:``` ` unclosed; r37 appends `L79-L152 (74 lines)`
  / `L399-L454 (56 lines)`; pending count 7 (lines 10 90 95 216 265 300 320); L85 “is not landed” 1;
  r37 head results.json 0; SCORECARD `Final lane commit:` 1; scratch survivor
  `/fast/scratch/hyaku/kasegi-r37/build-spec.py`; ledger rows 0; G8 freeze reading 14/14.
  C2: frontier 20, registry 54, S055 rows 0, entries citing S055 0, knowledge 49, harness 23/23,
  binding 44/44, audit `expected=49`.

### Base-state re-measurements (mine, not taken on trust)

```
$ git -C . show a173b0c2b98c5ae39599fa9be76027fbbead0b9e:corpus/lessons/round-37.md | grep -c '⟨pending'
7
$ git -C . show a173b0c2b98c5ae39599fa9be76027fbbead0b9e:corpus/knowledge/considerthese-proposals-ledger.md \
    | awk '/^## Round-37 dispositions/{f=1;next} /^## /{f=0} f && /^\|/' | wc -l
0
$ git -C . ls-tree -r --name-only a173b0c2b98c5ae39599fa9be76027fbbead0b9e | grep -c 'r38-closure'
0
$ awk '/^## Round-37 dispositions/{f=1;next} /^## /{f=0} f && /^\|/' corpus/knowledge/considerthese-proposals-ledger.md | wc -l
0            # the L1's discovery command, run live on the current worktree
$ git -C . diff -U0 b56a41680cefd391868c1c370dc063c69d827e7d a173b0c2b98c5ae39599fa9be76027fbbead0b9e -- PROVINCE.md | grep -E '^@@'
@@ -78,0 +79,74 @@ against the round-31 capture `corpus/source-snapshots/round-31/S048.txt`.
$ git -C . diff -U0 b56a41680cefd391868c1c370dc063c69d827e7d a173b0c2b98c5ae39599fa9be76027fbbead0b9e -- corpus/README.md | grep -E '^@@'
@@ -398,0 +399,56 @@ stays outside it.
$ git -C . show a173b0c2b98c5ae39599fa9be76027fbbead0b9e:corpus/README.md | grep -nE '^ {0,3}```'
426:```
$ git -C . show a173b0c2b98c5ae39599fa9be76027fbbead0b9e:corpus/README.md | wc -l
454          # one fence line in the whole file, at 426, and the file ends at 454 -> OPEN at EOF
```

The ledger section is confirmed empty in the live tree too: `grep -n '^## ' …ledger.md` →
`18:Limits`, `22:Round-31 status flips (appended 2026-10-25)`, `37:## Round-37 dispositions
(appended 2026-10-26, R31 home)`, `41:## Re-pin note (appended 2026-10-26)`; lines 38–40 are blank.
The round-37 lesson's claim is at `corpus/lessons/round-37.md:329`: “extended this round with the
18-row disposition table and the re-pin note” — that is the sentence the zero row count contradicts.

### Round-37 spot-check §5

`read corpus/lessons/round-37-verifier-spotcheck.md:157-186` → read the six routed defects verbatim
(D-A, D-B, D-C, D3, D-D, D-E). The entry's one-line paraphrase of each follows that text:
D-A “receipt scaffolding pasted into front-door files”, D-B “final-head positive run not committed”,
D-C “unresolved markers in the round lesson” (7 lines, plus L85), D3 “closure order”, D-D “label
drift”, D-E “scratch not empty”.

### C2 capture (wave-1 artifact, digest re-verified by me)

```
$ sha256sum ExecC2Capture.S055.txt
63c8ad5271ef5dfb7edcf2c65b4555a2d81a82682fe4d31058d542880e11cd42  ExecC2Capture.S055.txt
$ wc -l ExecC2Capture.S055.txt
5146 ExecC2Capture.S055.txt
$ stat -c '%s bytes' ExecC2Capture.S055.txt
272441 bytes
```

Those three match `ExecC2Capture.manifest.json` (`sha256`, `lines`, `snapshot_bytes`). The manifest
supplies the rest of the entry's capture sentence: `http.status=200`, `redirects=0`,
`user_agent=kasegi-shokunin/1.0`, `fetched_bytes=414858`, `fetched_utc=2026-10-26T18:25:51Z`,
`last_modified=Sun, 05 Apr 2026 13:17:09 GMT`, `server=cloudflare`.

Anchor lines quoted in the entry, verified against the capture bytes themselves:

```
$ sed -n '2134,2136p' ExecC2Capture.S055.txt
4.5 Profile 5: VEX
This profile SHOULD be used to provide information of the "Vulnerability Exploitability eXchange". …
A CSAF document SHALL fulfill the following requirements to satisfy the profile "VEX":
$ sed -n '2156p' ExecC2Capture.S055.txt
The value of /document/category SHALL be csaf_vex.
$ sed -n '1854,1855p' ExecC2Capture.S055.txt
3.2.3.9 Vulnerabilities Property - Product Status
Product status (product_status) … The eight defined properties are First affected (first_affected), …
$ sed -n '1885p;1894p' ExecC2Capture.S055.txt
First affected (first_affected) of value type Products (products_t) represents …
Under investigation (under_investigation) of value type Products (products_t) represents …
```

So the SHALL requirement list of the VEX profile spans L2136–L2156 and the eight per-status
definitions span L1885–L1894, as the entry states.

### Frontier / assimilation numbers

- `wc -l ExecIdCollision.collisions` → `24`; `head -3` → `S031 S032 S033`; `tail -2` → `S053 S054`
  (contiguous); `wc -l ExecIdCollision.staged-ids ExecIdCollision.reg-ids` → `94` / `54`; the same
  seat's receipt records `reg=54 staged=94 collisions=24` at lane HEAD `7001535…` and rules staged
  `S055` a duplicate-by-document of `S036` and an id collision with the incoming CSAF row
  (“reject, do not renumber”). The entry states `24` standing collisions and no new ones.
- `grep -nE '^#|^[0-9]+\.' considerthese/2026-10-26.md` → the 2026-10-26 file carries seven
  self-improvement proposals; number 3 is the quiescence gate and number 7 the proposal-status
  ledger, which is what the entry names.

### Scratch state (live, at draft time)

```
$ for d in /fast/scratch/hyaku/kasegi-r36 /fast/scratch/hyaku/kasegi-r37; do printf '%s: ' "$d"; test -d "$d" && echo present || echo absent; done
/fast/scratch/hyaku/kasegi-r36: absent
/fast/scratch/hyaku/kasegi-r37: absent
$ ls -1 /fast/scratch/hyaku/kasegi-r38
ExecC2Harness  ExecQuarantine  ExecRefChecker  ExecSchemaCross  ExecSuiteBuild  L1  RevClaimsFreeze  …
```

`kasegi-r36`/`kasegi-r37` are gone (the D-E survivor `kasegi-r37/build-spec.py` that the
before-controls record is no longer on disk). `kasegi-r38` holds the live wave's seat dirs **and an
`L1/` dir** (`L1/csaf.html`, `L1/r37w/live-lines.txt`, `L1/build-spec.py`); G6 accepts only the
suite's own work dir under `kasegi-r38`, so that `L1/` entry must be removed before the final gate
run or G6 stays red — flagging it here because it is not a seat's scratch and I cannot remove it.

### Why the G8 sentence is qualified

The freeze control records `r37-closure.sh --export-ref a173b0c2… → closed=14/14 exit=0` (lane clean
then). `ExecBaseRed.base-red-transcript.txt` shows the same instrument at the same ref reading
`closed=13/14 exit=1` once the wave's untracked `.ufo/waves/round-38/**` files exist, because E9's
`status-dirty` limb reads the **live** worktree (`E9 payload=status-read=ok,status-dirty=3,…`). The
entry therefore says the carry-over is `closed=14/14 exit=0` and that this holds only on a clean
lane, rather than asserting the base ref is unconditionally green.

## Validation of the deliverable

| Check | Command | Result |
|---|---|---|
| Lines / bytes / digest | `wc -l`, `stat -c %s`, `sha256sum` | `15` / `10810` / `7396b8d2…a01d` |
| G3 fixed-string vocabulary | `grep -cF` for the five fixed strings | `0 0 0 0 0` |
| G3 word-bounded tokens | `grep -cE '(^\|[^A-Za-z0-9_])TBD([^A-Za-z0-9_]\|$)'` and same for `TODO` | `0` / `0` |
| Any angle-bracket token at all | `grep -oE '<[A-Za-z0-9_.\|/-]+>' \| sort \| uniq -c` | no output (none) |
| Fenced blocks | `grep -cE '^ {0,3}```'` | `0` |
| Heading count | `grep -c '^## '` | `1` |
| Deferred-value markers | `grep -o '\[L1-MEASURE\]' \| wc -l` | `5` (heading 1, preamble 1, Wave 3) |

The five `[L1-MEASURE]` slots are the ones the item reserves: seat count (heading + Wave), role mix,
adversarial share, and the landed-commit list. Every other figure in the entry is either a frozen
claims contract value or a value measured above; no slot in the entry is prose scaffolding.

## Evidence classes (what is contract, what is measured)

- **Measured by this seat:** base pending count 7; ledger rows 0; suite absent 0; the two r37 append
  ranges and their line counts; README fence OPEN at EOF at L426; the capture digest/bytes/lines and
  every anchor line quoted in the C2 bullet; the ledger heading layout; the 24 collisions and the
  staged-`S055` verdict; `kasegi-r36`/`kasegi-r37` absent and the `kasegi-r38` entry list; the
  round-37 lesson sentence at `:329`; the spec's 73 items and the wave name `kasegi-r38-build`.
- **Frozen claims contract values, labelled as such in the entry:** `closed=8/8 exit=0`,
  `selftest cases=8 failures=0`, the two required reds, `all-gates v2` contents, the SCORECARD/SHONEN
  reference form, `harness entries=24 pass=24`, `source-recheck` exit 0, `capture-binding` 45/45,
  `recheck-audit expected=50`, `census` exit 0, `knowledge 49→50`, `junk-f21` rejection.
- **Taken from a sibling wave-1 receipt, not re-run by me:** census `rows=54 … with-row rows=55`
  (`ExecC2Census.md:68`) and the id-collision counts (`ExecIdCollision.md:83`). Neither seat's run was
  repeated here; the L1's own gate run is the evidence of record at REF.

## Not done (deliberately, out of my item)

- I did not build, run, or grade `r38-closure.sh`; at draft time
  `.ufo/waves/round-38/wave1/ExecSuiteBuild.r38-closure.sh` did not exist in the wave dir, so the
  entry's green figures are the claims' contract values by design.
- I did not run `frontier-recheck-count.py`, `source-recheck.py`, `capture-binding-check.py`,
  `recheck-audit.py`, `sources-census.sh` or `r37-closure.sh` — no reruns to decorate this report.
- I did not read or write any file outside the lane repo except the two read-only scratch listings;
  no network fetch was made by this seat (the capture was fetched by `ExecC2Capture` at
  `2026-10-26T18:25:51Z`, and its bytes, not a live URL, are what I verified).
- No git mutation of any kind: every git call was `log`, `show`, `diff -U0`, `ls-tree`, `rev-parse`
  style read-only, always with `-C /home/vgpnk/Projects/shokunin/kasegi-shokunin`.

## Tooling

No installs, no upgrades, no `pacman` transaction of any kind (host-wide pause respected). Nothing
was written to `~/.omp/agent/`, `~/.local/bin`, or any source tree.

## Scratch

`S=/fast/scratch/hyaku/kasegi-r38/ScribeLOG` was created with `mkdir -p` and used only as the
nominal work dir (it stayed empty — every command above ran read-only against the lane and the wave
dir). Removed with `rm -rf -- "$S"` before this receipt was written; verified:

```
$ test -e /fast/scratch/hyaku/kasegi-r38/ScribeLOG && echo SURVIVED || echo "absent after rm"
absent after rm
$ ls -d /fast/scratch/hyaku/kasegi-r38/*/
… ExecQuarantine/ ExecRefChecker/ ExecSchemaCross/ ExecSuiteBuild/ L1/ RevClaimsFreeze/ … ScribeSourcesLog/
```

`ScribeLOG` no longer appears under `kasegi-r38`. The remaining entries belong to live seats and to
the L1's own `L1/` dir (see the G6 note above).
