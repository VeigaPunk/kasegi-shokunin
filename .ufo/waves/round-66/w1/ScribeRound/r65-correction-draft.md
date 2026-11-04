# DRAFT — append-only correction of the filed round-65 report (scribe draft)

**Draft only. Not in production.** The filed report at
`/home/vgpnk/Projects/shokunin/.ufo/reports/round-65/kasegi.md` is **not rewritten** by
this seat and is not touched here. Every correction below is additive: it states what the
filed report says, what the committed bytes actually show, and what the round-66 records
cite instead. No round-65 number is restated as if it had been re-measured, and no
previously uncaptured value is invented.

The six items are the defects the round-65 verifier routed to the lane
(`corpus/lessons/round-65-verifier-spotcheck.md` § Routed defects, lines 132-152). Each is
status-neutral: the round-65 **verdicts** are unaffected, and only the report's
commit→LOG ties, its commit coverage, its receipt citation, its revision naming, its exit
code and its helper-count phrasing are corrected.

---

## Correction 1 — commit→LOG ties cite bullets, not "bolts"

**Filed report says:** the Landed-changes table's second column reads "LOG bolts 1–3",
"LOG bolt 2", "LOG bolts 4, 8", "LOG bolts 5, 10", "LOG bolt 6", "LOG bolt 12" etc.

**Committed bytes show:**

```
$ awk 'NR>2667 && /^## /{exit} NR>2667 && /^- /{n++} END{print n}' LOG.md
10
$ grep -c 'bolt' LOG.md
0
```

`LOG.md`'s Round 65 section has **10 bullets**, and the string `bolt` occurs **nowhere**
in `LOG.md`. The report's table also cites a "bolt 12", which does not exist — the round
has ten.

**Correction:** the round-66 Landed-changes table cites bullet indices ("§ Round 65
bullet 4"), never the word "bolt". The filed table is left as filed.

## Correction 2 — two round commits were missing from the Landed-changes table

**Filed report's table names** 13 commits. **The lane contains 15:**

```
$ git rev-list --count a283189b6c8d86ee1a06e4aa2b701a2b6c6b068b..a33573291dd1867eed2c283516fc1ce38b7dae69
15
```

The two commits absent from the table are:

- **`1929a47449513afe0d0f2105d7d75663aaf1baa0`** — "round-65: widen the S098 body range
  and record the capture-range defect" (the M65-9 fix).
- **`68245227bd4cbc4c485247a0fc10c5223edc7b98`** — "round-65: record the final tip
  verification receipt".

Both exist in the lane and both are ancestors of the tip.

**Correction:** the round-66 Landed-changes table lists all 15 commits, including these two.
The filed table is left as filed.

## Correction 3 — the "exact final driver" label was wrong for the receipt it cited

**Filed report's before block says** "before (a283189, exact final driver)" and cites the
workdir `/fast/scratch/hyaku/kasegi-r65/L1/base-finaldrv2`, then prints
`→ VERIFY measurements=8 failures=3   (exit 1)`.

**Committed bytes show** that the receipt for that workdir records a *different* driver:

```
$ head -2 .ufo/waves/round-65/controls/driver-base-donothing-finaldrv-r65.txt
$ python3 -B .ufo/waves/round-65/verify-r65.py --revision a283189… --work /fast/scratch/hyaku/kasegi-r65/L1/base-finaldrv2
driver_sha256=5aa842abdceac676ff8c0a1b90f641bbad93a9505161f192dde85b1a1d06aaaf
```

`5aa842ab…` is the **erratum-1** driver. A same-result base receipt taken with the
**final** driver exists and is self-pinned:

```
$ head -3 .ufo/waves/round-65/controls/driver-base-donothing-r65.txt
$ python3 -B .ufo/waves/round-65/verify-r65.py --revision a283189… --work /fast/scratch/hyaku/kasegi-r65/L1/base-v6
driver_sha256=7f27c4d2fe43db875453478983faa39d44d7aa8ae82b455fb3ff8f039e9f6172
GUARD driver-self-pin PASS
```

and `sha256sum .ufo/waves/round-65/verify-r65.py` = `7f27c4d2…` = the file
`.ufo/waves/round-65/driver.sha256`, so the counter's identity is checkable. The same
receipt ends `VERIFY measurements=8 failures=3 revision=a283189…`.

**Correction:** the round-66 records cite
`.ufo/waves/round-65/controls/driver-base-donothing-r65.txt` (`7f27c4d2…`, 8/3,
self-pin PASS) for the base state measured with the final driver, and describe the
`base-finaldrv2` receipt as the erratum-1-driver receipt it is. The filed report is left
as filed.

## Correction 4 — "Final tip" was not the lane tip

**Filed report says** "after (final tip 03a23921, carrying the gate, the pins, the driver
and its self-pin)" and cites
`.ufo/waves/round-65/controls/final-verification-tip-r65.txt` → 8/0 exit 0.

**Committed bytes show** the measured revision is `03a23921` and the lane tip is
`a3357329`, two commits later:

```
$ git log --oneline 03a239212633411cf2dbc96beedc672b9c3d0790..a33573291dd1867eed2c283516fc1ce38b7dae69
6824522 round-65: record the final tip verification receipt
a335732 round-65: commit the census-after and fresh-clone receipts
$ git diff --stat 03a23921 a3357329
 .ufo/waves/round-65/controls/census-after-r65.txt     |  9 ++++++++
 .ufo/waves/round-65/controls/final-verification-tip-r65.txt        |  4 ++--
 .ufo/waves/round-65/controls/fresh-clone-r65.txt       | 24 ++++++++++++++
```

The delta is **receipt-only**; the gate and the counter bytes are identical at both
revisions.

**Correction:** the round-66 records name the revision **as measured** (`03a23921`) and
state the delta to the lane tip (`a3357329`, two receipt-only commits later) rather than
calling `03a23921` the tip. The verdict is unaffected. The filed report is left as filed.

## Correction 5 — the base receipts record no exit code

**Filed report says** the base ran "`VERIFY measurements=8 failures=3`, exit 1" (twice:
§ Work items item 5 and the before→after block).

**Committed bytes show** the base receipts end without the **driver's own** exit status:

```
$ tail -1 .ufo/waves/round-65/controls/driver-base-donothing-r65.txt
VERIFY measurements=8 failures=3 revision=a283189b6c8d86ee1a06e4aa2b701a2b6c6b068b
$ tail -1 .ufo/waves/round-65/controls/driver-base-donothing-finaldrv-r65.txt
VERIFY measurements=8 failures=3 revision=a283189b6c8d86ee1a06e4aa2b701a2b6c6b068b
$ tail -1 .ufo/waves/round-65/controls/driver-base-donothing-prefreeze-r65.txt
VERIFY measurements=8 failures=3 revision=a283189b6c8d86ee1a06e4aa2b701a2b6c6b068b
```

The three base receipts carry `exit=` values for **individual sub-results** (lines 6, 7,
10, 11 — the probe audit exits, the selftest exit, the ledger exit and the
collector-selfcheck exit), but **no line records the driver's own process exit status**,
which is what the filed report's "exit 1" asserts. The candidate receipt
`controls/final-verification-tip-r65.txt` *does* end with a bare `exit=0` (line 15); the
base receipts do not. **The driver's own exit status on the base runs was never captured
and is not invented here.**

**Correction:** the round-66 records describe the round-65 base receipts as recording
`VERIFY measurements=8 failures=3` with the **driver's own exit code absent** (the
sub-result exit values that *are* present are cited as such), and every round-66 receipt
captures the exit status of its own run — the round-66 driver receipts do carry a final
`exit=` line. The filed report is left as filed.

## Correction 6 — the helper count spans two gate runs

**Filed report says** "an unscreened `sort` invocation executed a helper 121900 times
while the audit read `ok`".

**Committed bytes show:**

```
$ cat .ufo/waves/round-65/w1/SentinelScope/07-parser-sort-compress-exec.txt
…
marker lines=121900 (two gate runs appended; ~60950 program invocations per run)
```

The 121 900 marker lines were appended by **two** gate runs.

**Correction:** the round-66 records cite the count as **121 900 across two runs**
(~60 950 program invocations per run), not as a single run's count. The filed report is
left as filed.

---

## What this correction does **not** touch

- The round-65 **verdicts**: C1 improved (base 8/3 falsified by the same counter, base
  false greens → after 8/0), score held at 4 nominal per R58; C2 improved (frontier 43→44
  with S098 admitted); depth:density 9 held. The verifier found the round-65 verdict
  evidence-verified. None of the six corrections changes a verdict.
- The round-65 **source row S098** and its 18 anchored quotes; the S099 row opened by this
  round is separate and own-work.
- Any **production file**. The filed report, `LOG.md`, `SCORECARD.md`, `corpus/QUALITY.md`
  and `corpus/SOURCES.md` are the L1 integrator's to change; this seat wrote drafts only,
  under `.ufo/waves/round-66/w1/ScribeRound/`.
- **Promotion.** No SHONEN box is claimed or moved; box 2 remains `[ ]`.
