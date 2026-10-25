# Round-28 census note — ScribeCensusNote

Round: kasegi-shokunin round 28, wave 1. Seat: ScribeCensusNote (scribe, coverage).
Last updated 2026-10-25T17:27Z (UTC). Lane base `c9f8b115a098c65356e4b3b6048af45a37ab8395`.
Consumer: ScribeLesson, as the input to the Compliance census block in `corpus/lessons/round-28.md`.

Scope of this seat: read-only. No production file was edited and no instrument was modified; the only
write made by this seat is this file. No tool was installed; no pacman/`uv`/`npx` transaction was
attempted (host-wide pacman pause respected).

**State: POST-STATE — the round-end census was executed live and exported 0.** The S042 row and the
F12 entry landed while this seat was open; §4 is the live run. §1 and §3 stay in the note because the
before-reading is what makes the delta checkable, and §6 records a transient failure actually observed
in the lane between the row landing and the entry landing.

---

## 1. Pre-state — observed, live, exit 0

Command (lane root, absolute paths):

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
echo census_exit=$?
```

Full output, verbatim (2026-10-25T17:22Z):

```
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
census_exit=0
```

Byte-identical to the frozen before-receipt `.ufo/waves/round-28/census-before.txt`
(sha256 `6c1cf886c580eaa0ce57dbe26fb4c1a5adc1b8cc873640f270a620e3cf3d4675`), except that the receipt
carries the wrapper's trailing `census_exit=0` line, which the direct invocation does not print. A
fresh run through the same wrapper differs only in that trailer:

```
--- .ufo/waves/round-28/census-before.txt	2026-10-25 13:58:56.264939890 -0300
+++ /tmp/census-now.txt	2026-10-25 14:22:50.335138928 -0300
@@ -1,4 +1,3 @@
 kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
 kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
 kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
-census_exit=0
```

Pre-state histogram, from the census tool's own counters (`census` mode, exit 0):

```
kasegi	rows	41
kasegi	tier.A	38
kasegi	tier.B	1
kasegi	tier.C	2
kasegi	status.mined	29
kasegi	status.queued	9
kasegi	status.rejected	3
FLEET	rows	41
FLEET	tier.A	38
FLEET	tier.B	1
FLEET	tier.C	2
FLEET	tier.invalid	0
FLEET	status.queued	9
FLEET	status.mined	29
FLEET	status.rejected	3
FLEET	status.invalid	0
FLEET	missing	0
```

`FLEET` equals `kasegi` because kasegi is the only child lane counted (`shokunin.conf` rows with repo
`.` are excluded from default targets). An independent `awk -F'|'` count over the Registry table gave
`rows=41`, `tier A=38, B=1, C=2`, `mined=29, queued=9, rejected=3` — the tool's `rows` metric and the
table row count agreed at pre-state.

Pre-state anchors:

| item | value |
|---|---|
| `corpus/SOURCES.md` sha256 | `fe14821388269f04c5da665ed4181ac04a9762197de0900b57ab5057f384481b` |
| `grep -cE '^\|[[:space:]]*S042[[:space:]]*\|' corpus/SOURCES.md` | `0` |

## 2. W04 status — pre-existing, unchanged by the round

W04 is "same URL across scopes"; it is a warning class and does not change the exit code
(`sources-census.sh` header: "W-codes and unlisted lanes never change status"). Both lines pre-date
round 28: they are in the round-28 before-receipt `.ufo/waves/round-28/census-before.txt` (frozen
13:58Z) and, earlier, verbatim in `.ufo/waves/round-24/assimilation/census-before.txt` (lines 1–2) and
in the round-23 falsify receipts (`.ufo/waves/round-23/falsify/RegistryR8.md` lines 196–197). The
round-27 `census-before.txt` is not a witness either way — it holds only the wrapper's trailing
`census_exit=0` line (14 bytes).

| code | row | collides with | relationship |
|---|---|---|---|
| W04 | S028 | S006 | S028 is the rejected duplicate-row proposal for the same HackerOne URL |
| W04 | S029 | S024 | S029 supersedes S024 on the same EUR-Lex CRA URL |

Round-28 relevance: the S042 URL `https://www.ipa.go.jp/security/todokede/vuln/process.html` occurred
`0` times in the registry before the append (`grep -c 'ipa.go.jp/security/todokede'`), so S042 could
not add a W04 line — and the post-state run in §4 confirms W04 is still exactly these two rows. No new
W04 exists in this round.

## 3. Row count and the census-relevant cells of the landed rows

`corpus/SOURCES.md` at the round-end run: sha256
`e59240f8e9842535e815f7d4575be7ea11a6a57a7bbaead43cbea92bd013945d`, 42 Registry rows by the tool and
by `awk` independently.

| id | tier | status | opened | recheck | used-by |
|---|---|---|---|---|---|
| S041 | A | mined | 2026-10-25 | 180d | `…/iso-29147-and-30111-division-of-labour.md`, `…/iso-29147-divergence-and-clause-crosswalk.md`, `…/japanese-domestic-disclosure-workflow.md` |
| S042 | A | mined | 2026-10-25 | 180d | `corpus/knowledge/japanese-domestic-disclosure-workflow.md` (exactly one) |

S041's `used-by` gained the F12 entry as its third item; S042's `used-by` is exactly the admitted
entry. The entry `corpus/knowledge/japanese-domestic-disclosure-workflow.md` (sha256
`a0f8e6172110c8419bdc1ea39823736b0b066e6155fc9a3f6f89cf7f4c260b59`) declares both headers — `source:
S041 …` (line 3) and `source: S042 …` (line 4). Those cells are the ones the census reads; the prose in
`scope`/`anchor`/`teaches` is not load-bearing for any counter here.

The entry was still being finalised under this seat: it read sha256 `55cf660f…` when the census first
passed at 17:26Z and `a0f8e617…` at 17:27Z, with the two `source:` headers unchanged at lines 3–4 and
`^source: S042 ` occurring exactly once in both. Census exit stayed 0 across the change — the entry's
bytes are not a census input, only its existence at the `used-by` path, which is why this note binds
the counters to `corpus/SOURCES.md` and quotes the entry digest only as of the last check (17:27Z).

## 4. Round-end census — live, exit 0

Command and full output, verbatim (2026-10-25T17:26Z):

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
echo census_exit=$?
```

```
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
census_exit=0
```

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin kasegi
echo census_mode_exit=$?
```

```
kasegi	rows	42
kasegi	tier.A	39
kasegi	tier.B	1
kasegi	tier.C	2
kasegi	status.mined	30
kasegi	status.queued	9
kasegi	status.rejected	3
FLEET	rows	42
FLEET	tier.A	39
FLEET	tier.B	1
FLEET	tier.C	2
FLEET	tier.invalid	0
FLEET	status.queued	9
FLEET	status.mined	30
FLEET	status.rejected	3
FLEET	status.invalid	0
FLEET	missing	0
census_mode_exit=0
```

Delta, observed:

| metric | before | after | delta |
|---|---|---|---|
| rows | 41 | 42 | **+1** |
| tier.A | 38 | 39 | **+1** |
| tier.B | 1 | 1 | 0 |
| tier.C | 2 | 2 | 0 |
| status.mined | 29 | 30 | **+1** |
| status.queued | 9 | 9 | 0 |
| status.rejected | 3 | 3 | 0 |
| W04 | 2 (S028, S029) | 2 (S028, S029) | 0 |
| E-codes | 0 | 0 | 0 |
| exit | 0 | 0 | 0 |

One new tier-A mined row, no warning delta, no error codes, exit 0 both before and after.

The `grep -cE '^\|[[:space:]]*S042[[:space:]]*\|' corpus/SOURCES.md` counter moved `0` → `1`.

Provenance of the two runs, because the registry moved once under this seat (ScribeRegistryC2 was
still finalising the row):

| run | UTC | `corpus/SOURCES.md` sha256 | validate | census counters |
|---|---|---|---|---|
| A | 17:26Z | `6e225bfdac7f46778b032f21746f97154eba2bdba62569add8652b0ecfa9f0f6` | exit 0, same 3 lines | 42 / A 39 / B 1 / C 2 / mined 30 / queued 9 / rejected 3 |
| B | 17:27Z | `e59240f8e9842535e815f7d4575be7ea11a6a57a7bbaead43cbea92bd013945d` | exit 0, same 3 lines | identical line-for-line |

Outputs above are run B's; run A's were byte-identical, so the delta table holds on both byte states.
The quoted blocks are not a composite.

## 5. Corroborating scratch projection (not the gate)

Before the row landed, the same append was exercised in a `mktemp -d` tree under `/tmp` — a copy of
the pre-state registry, `corpus/knowledge/` as per-file symlinks to the real files, plus a throwaway
stub standing in for the unlanded entry — to show the row shape appends cleanly. It returned exit 0,
`rows 42`, `tier.A 39`, `status.mined 30`, W04 unchanged at S028/S029, i.e. exactly the §4 numbers.
Two details worth keeping:

- The first attempt appended the row after the file's trailing sections and drew
  `E12 S042 row outside Registry section` (exit 1). Placement, not row content, is what E12 polices.
- `--file <path>` re-roots E11 at the file's parent directory, dangling every `used-by`; an explicit
  lane directory (or `--root` + lane id) is required for a meaningful validate.

This section is corroboration only — the §4 live run supersedes it.

## 6. Transient mid-wave state, observed (not the round-end result)

Recorded because it shows the ordering dependency is real in this lane, not hypothetical. At
2026-10-25T17:24Z the S042 row had landed but `corpus/knowledge/japanese-domestic-disclosure-workflow.md`
had not, and the live census read:

```
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	E11	S041 missing used-by corpus/knowledge/japanese-domestic-disclosure-workflow.md
kasegi	E11	S042 missing used-by corpus/knowledge/japanese-domestic-disclosure-workflow.md
census_exit=1
```

Counters already read 42/39/30 at that moment; only exit was blocked. The entry landed at 14:26 local
(17:26Z) and the same command then returned the §4 output with `census_exit=0`. E11 resolves each
mined row's `used-by` against the lane directory (`[ ! -e "$dir/$path" ]`), so a registry row that
precedes its entry — and S041's newly widened `used-by` — both fail until that file exists. For any
future round: land the entry before or with the row, never after a census gate.

## 7. Compliance census block for `corpus/lessons/round-28.md`

Paste verbatim; every number below was observed in §4 at `corpus/SOURCES.md` sha256
`e59240f8e9842535e815f7d4575be7ea11a6a57a7bbaead43cbea92bd013945d`.

> Census at round end: exit 0, 42 rows (tier A 39 / B 1 / C 2; mined 30, queued 9, rejected 3), versus
> 41 rows at round start (A 38 / B 1 / C 2; mined 29, queued 9, rejected 3) — a delta of exactly one
> tier-A mined row (S042), with no error codes. The only warnings are the two pre-existing W04 rows
> (S028 colliding with S006, S029 with S024); the S042 URL was absent from the registry beforehand, so
> the round added no warning. A transient mid-wave state recorded E11 for S041 and S042 while the
> registry row preceded the F12 entry (exit 1, 17:24Z); the entry landed and the census cleared to
> exit 0 (17:26Z), so the ordering constraint is discharged at round end, not waived.

If `corpus/SOURCES.md` changes after this note, re-run it — do not carry these numbers forward
unchecked:

```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin
sha256sum corpus/SOURCES.md
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi; echo census_exit=$?
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin kasegi
```

## 8. What this note does not claim

- It does not claim the F12 entry's content quality, the manifest's quote assertions, the README
  frontier row, or the entry's recheck line — other seats own those. Only the registry's census
  consequences are in scope here, and only `tier`, `status`, `opened`, `recheck`, `used-by` and the URL
  were read for that purpose.
- The scratch tree of §5 is not evidence of the round-end gate; §4 is.
- No claim is made about lane-wide file stability after 17:27Z. The run is bound to the registry sha256
  above; §7 carries the re-run command.
