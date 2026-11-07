# ScribeEntry — round-87 attempt 1, knowledge-entry candidate (one v1 wave of 12 seats; this is one leaf seat)

Scope: draft a candidate knowledge entry for `corpus/knowledge/` (the L1 integrates it), plus the
two SOURCES `used-by` change texts. No lane file was edited, no commit was made, no counter for C1
or C2 was run.

## Measured state (as of this seat's last command, 2026-11-06)

| fact | value |
|---|---|
| base | `cd1f568a6be2656b5f5dc479eb90ef99b91131b5` |
| freeze | `afb13a88e6fbc8e2f8a0c11f9cfbfde77e907e69` |
| C1 landing | `d87b1b55a51d78411438e962a9abbebdd17930cd` |
| C2 landing / current HEAD | `132e16c588a2424c06b5ca15ea01fce1ee9a396d` |
| working tree | `M corpus/SOURCES.md` (uncommitted; S124/S125 flipped `queued`→`mined`, `used-by` `—`→`corpus/instruments/capture-secret-scan.py`) |
| capture digests | S122 `08cab370e7f153d051719bfe098cb140d0d68e9da99e27caacfa0b4228a72eb5`; S124 `88d4f703cef1b9d1cead11053dd9f02692bd4629a7110e42caecc74a2fc2f1cb`; S125 `65c99351e731b743f18243e93613da7e05b4030d5fe2060a6cc484a320de55fe` — each equals its manifest record |

## Deliverables

| file | sha256 | what |
|---|---|---|
| `.ufo/waves/round-87/w1/ScribeEntry-candidate/presigned-url-credentials-in-captured-evidence.md` | `1ced45b2afb57852d567ffeb33d170ebeaba8783b9c76dbc68817f3d25a7c48c` | the candidate entry, 135 lines, H1 + `source:` / `verified-at:` / `recheck:` then `## Attribution`, Claims 1–6, `## How a researcher uses this`, `## Falsifiable rule and checks` (FC-1…FC-6), `## Rejected over-generalizations` (7), `## Honest limit` (7) |
| `.ufo/waves/round-87/w1/ScribeEntry-candidate/sources-used-by-draft.md` | `1e938b888736dd6cbbc7f15224a7ec86bde59380f37593c43e9524e91ddd7a15` | exact old→new `used-by` (and, if deferred, `status`) cell text for `corpus/SOURCES.md:136` (S124) and `:137` (S125), the rule-2 lesson log line, the post-edit census commands, the order dependency, and the out-of-scope S122 third cell |
| `.ufo/waves/round-87/w1/ScribeEntry-receipts/entry-checks.txt` | `11153bb14e57f7fbd283785db527511bfafc919c2a7b58a710a203106b619f98` | every command this seat ran with its terminal output (180 lines); digests and counts only, no mined value |

## Behavior (what the entry says, and on what)

1. **Claim 1** — a disclosed bounty record can carry presigned avatar URLs at three levels. S122 is
   one 5,361-byte line, 51 top-level keys, 6 `profile_picture_urls` strings of which exactly 2 are
   signed (the two 211-character team sizes), both `attachments` arrays empty, `X-Amz-` count 0
   after redaction. Anchored on the redaction tool's own sentence
   (`.ufo/waves/round-86/l1/redact-presigned.py:5-6`) and the manifest's `redaction.removed` field.
2. **Claim 2** — `X-Amz-Security-Token` holds the session token of a temporary credential, in the
   header or the query string (`corpus/source-snapshots/round-87/S124.txt:81-85`), and placement is
   not fixed (`:86-89`).
3. **Claim 3** — the prefix table classifies the identifier, not the secret: `AKIA`/`Access key` at
   `corpus/source-snapshots/round-87/S125.txt:318-319`, `ASIA`/`Temporary (AWS STS) access key` at
   `:330-331`, and the combination sentence at `:332-333`; 12 prefix codes in the table.
4. **Claim 4** — the documented example key id (`corpus/source-snapshots/round-87/S124.txt:409`, and
   at `:385`, `:395`, `:422`) is the one exact string the scanner exempts (`ALLOWED_VALUES`,
   instrument line 63), not an allowlist row.
5. **Claim 5** — expiry bounds use, not publication: `X-Amz-Date` 2026-11-07T00:58:29Z plus
   `X-Amz-Expires` 3600 s (`corpus/lessons/round-86.md:61`) gives 01:58:29Z, while the commit was
   pushed inside that window; history keeps the pre-redaction bytes (`ceb01841…`, 9,131 bytes) and
   the lesson states no force-push (`:63`).
6. **Claim 6** — the operating rule: `--files` scan before the first commit
   (`corpus/instruments/capture-secret-scan.py:18-19`, output/exit contract at `:41-46`), redact the
   query string while keeping scheme/host/path, keep `redaction.pre_redaction_sha256` beside the
   post-redaction `sha256`, and note that an `aws-sts-session-token` allowlist row is refused
   (`:37-38`) while an unused row is reported only (`:44-45`).

## Gates — what this seat measured, and what it did not

| gate | status | measurement |
|---|---|---|
| Q1 three header lines | hold | `source:` names S124 and S125 with URLs, both anchors and both capture digests; `verified-at:` carries the three digests and the two recheck runs; `recheck:` is one line |
| Q2 tier-A support | hold | S124, S125, S122 are tier A in `corpus/SOURCES.md` (rows at `:136`, `:137`, `:134`) |
| Q3 ≤25-word verbatim quotes with location | hold | 12 blockquotes, longest 24 words; each anchored (`FC-1`, `FC-3`) |
| Q4 attribution | hold | AWS's statements labelled as AWS's; HackerOne record labelled as HackerOne's; redaction and scanner labelled as lane work |
| Q5 falsifiable rule + rejected over-generalization | hold | `## Falsifiable rule and checks` (3 falsifiers) + 7 rejected over-generalizations, each with a source or a measurement |
| Q6 documentation only, no credential material | hold | no token value, no private URL, no vault reference; the only key id is `AKIAIOSFODNN7EXAMPLE`; `capture-secret-scan.py --files` on the entry reads `hits=0 rc=0` |
| Q7 executable recheck | hold | `bash -n` rc 0; run from `/tmp` it exits 0 and prints the S124/S125 quote lines and the S122 redaction line |
| Q8 declared normalization | hold | each quote is a substring of the capture after whitespace collapse across a line break (S124 84-85, S125 304-305, 332-333); `source-recheck.py` confirms `occurrences=1` and `anchor=N-ok` |
| Q9 binding (stem=id, exactly-once, occurrence count printed) | hold | the recheck prints `occurrences=1` per quote; the manifest's own anchors are the entry's anchors |
| Q10 one executable `recheck:` with a `cd` prefix | hold | single line, `bash -n` 0, foreign-cwd rc 0, human note after `#` |
| R12 recheck ids vs header ids | hold | `--source S124` and `--source S125` cover the two ids on the `source:` line, and the named manifest lists both; S122's manifest is named in the body line that cites it |
| R33/R120 recheck census form | hold by construction | prefix-present, foreign-cwd rc 0, fail-closed on a missing manifest or capture (`source-recheck.py` exits 2) |
| R135 absence rule | hold | the entry makes no "finds nothing"-style rule; its falsifiers are positive measurements |
| R6 (existing line numbers) | not applicable | the candidate is a new file; no cited file was edited by this seat |

Not run by this seat, deliberately: the C1 `knowledge-meter.py` (a clone of the landing commit is
the C1 seat's instrument), the C2 `capability-check.py`, any mutation battery, and any package gate.
No build, lint, or test run was required for a Markdown draft; the entry's own commands are the
checks the L1 can replay.

## Touched surfaces

Written, all inside this seat's output dir: the three files in the table above. Read-only
everywhere else: `corpus/SOURCES.md`, `corpus/knowledge/*`, `corpus/lessons/round-86*.md`,
`corpus/instruments/*` (imports only via `python3 -B`), `corpus/source-snapshots/round-86|87/*`,
`SCORECARD.md`, `.ufo/waves/round-87/{claims.json,landing.json,c1/*,c2/*,controls/*}`,
`.ufo/waves/round-86/l1/redact-presigned.py`.

No git or jj write. No fixture repository was created (no credential fixture was needed: every
measurement reads pinned lane bytes, and `--selftest` exercises the scanner's own fake token).
Scratch `/fast/scratch/hyaku/kasegi-r87/ScribeEntry` was created with `TMPDIR` passed explicitly
and is removed on exit.

## Out of scope (not done, by design)

- No edit to `corpus/SOURCES.md`, `corpus/knowledge/`, `SCORECARD.md`, `LOG.md`, `SHONEN.md` or any
  instrument; the `used-by` draft is text for the L1 to apply.
- No C1/C2 counter run, no claim re-scoring, no judgement of the frozen predicates.
- No live network fetch: every quotation comes from the pinned captures; the two round-87 URLs are
  recorded from the manifest, not re-opened.
- The S122 `used-by` cell is not drafted as a required change (see F5).

## Findings (routed; each with its re-runnable command)

**F1 — the tip is not quiescent while this entry is being drafted.**
`git status --porcelain -- corpus/SOURCES.md` prints ` M corpus/SOURCES.md` at `132e16c`. If the
round closed now, R110's quiescence gate fails on that row edit, and the in-place change is not yet
logged old→new anywhere.
```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && git status --porcelain && git log --oneline -1
```

**F2 — the entry must not be read as part of the C1 census.** C1's target `678/1719` is measured on
a clone of `d87b1b55`, and M3 requires the same file set and per-file line counts; adding
`corpus/knowledge/presigned-url-credentials-in-captured-evidence.md` changes the population. Using
the lane's own `resolve.collect`/`resolve.classify` (not the frozen counter) I reproduce the
documented +1 and the post-admission shift: tree **679/1719** → with the entry admitted
**704/1754** (35 new distinct tokens, 10 of them GONE — command invocations and printed outputs,
the same shape the landed scope already carries 1,040 of; reproduction in
`ScribeEntry-receipts/entry-checks.txt` § `meter-reproduction`). So: integrate after C1 is read, and
never cite a post-entry meter reading as the C1 predicate.
```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && for r in cd1f568a afb13a88 d87b1b55 132e16c; do printf '%s %s\n' "$r" "$(git ls-tree -r --name-only $r corpus/knowledge | grep -c '\.md$')"; done
```

**F3 — the SOURCES edit must be logged, and the cell appended rather than replaced.** The working
tree already sets `used-by: corpus/instruments/capture-secret-scan.py`; the entry's cell change is
an append (`, corpus/knowledge/presigned-url-credentials-in-captured-evidence.md`) and rule 2 wants
the old→new line in the round lesson. Exact text in `ScribeEntry-candidate/sources-used-by-draft.md`.
```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && git diff -- corpus/SOURCES.md | grep -E '^[+-]\| S12[45] ' | cut -c1-200
```

**F4 — order dependency on the registry census.** `status: mined` requires its `used-by` paths to
exist; a `used-by` naming the entry before the entry file exists makes the census below print
`missing: corpus/knowledge/presigned-url-credentials-in-captured-evidence.md`.
```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {s=$9; gsub(/[[:space:]]/,"",s); if (s=="mined") {n=split($12, a, /[,;]/); for (j=1;j<=n;j++) {p=a[j]; gsub(/^[[:space:]]+|[[:space:]]+$/,"",p); if (p!="" && p!="—") print p}}}' corpus/SOURCES.md | while read -r p; do [ -e "$p" ] || echo "missing: $p"; done
```

**F5 — S122's `used-by` is a third cell the ticket did not assign.** The entry's Claim 1 cites
`corpus/source-snapshots/round-86/S122.txt:1`, so under the same rule S122's cell should gain the
entry path (drafted as an optional line in the used-by file). Left as an L1 decision so the two-row
scope stays as assigned.

**F6 — the entry's own citation tokens are new.** It introduces 15 distinct
`corpus/source-snapshots/…` tokens plus path citations to `corpus/instruments/*`, `corpus/lessons/*`,
`SCORECARD.md` and `.ufo/waves/round-86/l1/redact-presigned.py` (all classify INTERNAL — 0 GONE
paths). A future tranche reading the knowledge scope sees a larger token set than r87's 1,719; that
is expected growth, not a regression, but it must not be compared against the r87 target.
```sh
cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && grep -oE 'corpus/source-snapshots/[A-Za-z0-9/._-]+\.txt(:[0-9]+(-[0-9]+)?)?' .ufo/waves/round-87/w1/ScribeEntry-candidate/presigned-url-credentials-in-captured-evidence.md | sort -u | wc -l
```

**F7 — two quotes are lane own-work, not captured source.** The redaction tool's sentence and the
round-86 lesson's clauses are cited by file and line but are not `S###` sources; if the lane's
admission rule ever requires every blockquote to resolve to a capture, these two would need the
`own-work` label made explicit in `source:`. Recorded, not repaired.

## Artifact paths

- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-87/w1/ScribeEntry.md` (this report)
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-87/w1/ScribeEntry-candidate/presigned-url-credentials-in-captured-evidence.md`
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-87/w1/ScribeEntry-candidate/sources-used-by-draft.md`
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-87/w1/ScribeEntry-receipts/entry-checks.txt`

Tooling: none installed or upgraded (no pacman, no uv, no npx); the lane's own `python3 -B` and coreutils
were sufficient.
