# R44Scribe5 — source Gate shape for a C2 admission + one reject (draft, report only)

Seat: `R44Scribe5` (scribe, leaf, no subagent dispatch). Lane `/home/vgpnk/Projects/shokunin/kasegi-shokunin`;
frozen base `5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a`; measured mid-wave (files changed under me — every value
below is re-measured on the bytes named). Scope: `claims.json` C2 admission surface only; C1 untouched.
Read-only: no lane file edited, no git/jj mutation, nothing installed (`python3 3.x`, `curl 8.23.0`, `gawk`,
`sha256sum` already present; pacman not invoked). Scratch `/home/vgpnk/Projects/shokunin/.scratch/kasegi-r44/R44Scribe5`
(untracked; deleted on exit). NOTE on scratch: `$HYAKU_SCRATCH` was unset, so fleet-root `.scratch/` was used per
the fleet's own convention; nothing tracked was touched.

## 0. Do-nothing discrimination (re-measured on frozen base 5ab3a60)

The frozen `controls/do-nothing.txt` claims `admitted=25 registry=68 knowledge=62`. The moved lane bytes now
print `admitted=26 registry=70 knowledge=63` — but **only under the control's own regex**, not under the
regex `claims.json` C2 froze. Re-measured 2026-10-28T19:2xZ at the current lane working tree:

```
$ grep -cE '^\| F[0-9]+ \| .* \| admitted \|' corpus/README.md      # control regex
26
$ grep -cE '^\| F[0-9]+ \| admitted \|' corpus/README.md            # claims.json's frozen C2 counter
0
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
70
$ find corpus/knowledge -maxdepth 1 -name '*.md' | wc -l
63
```

So the frozen C2 `counter` field (`grep -cE '^\| F[0-9]+ \| admitted \|' corpus/README.md`) prints **0 at the
moved state and 0 at base** — it can never observe the move. The *control's* regex is the correct one. A Gate
must name a counter whose before/after differ; the frozen claims counter does not. (Also flagged by sibling
seats; this is my own measurement, not their report.)

Append-only check on the moved tracked files:

```
$ git diff --numstat corpus/README.md corpus/SOURCES.md corpus/instruments/knowledge-expected.txt
19	0	corpus/README.md
5	0	corpus/SOURCES.md
1	0	corpus/instruments/knowledge-expected.txt
```

---

## 1. Draft — `### Gate` shape for a source admission (the C2 admit)

Field-level draft. The landed candidate is `S069` / `F26` / `corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md`;
each limb is tested against those bytes, not described in the abstract.

**Rule G1 — registry row shape (census-clean, 11 cells / NF=13, append-only).**
`| S0NN | <name — URL> | kind∈{docs,spec,dataset,paper,community} | tier∈{A,B,C} | scope | anchor | teaches | status∈{queued,mined,rejected} | opened=ISO-date ≤ today | recheck=<NNd|ISO date|symbolic> | used-by=<path|- > |`.
Measured on S069: `NF=13`, `docs`, `A`, `mined`, `opened=2026-10-28`, `recheck=180d`, `used-by` path exists on disk →
`./scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` prints `kasegi ok` exit 0
(two pre-existing W04 warnings S028/S029, unchanged from the do-nothing). Constraints the draft enforces:
E04/E11 (no dup URL+scope without `supersedes`, `used-by` must exist), E10 (`community` is never tier A).

**Rule G2 — URL binding (row URL = manifest `url`; capture may use `capture_url`).**
`capture-binding-check.py` rule B5 requires the record's `url` to be byte-identical to the single `https://`
token in the row's source cell, and E3 permits `capture_url`/`http.final_url` to differ from `url` only as a
legal redirect/capture endpoint. Measured: S069 row's source cell carries the human page
`https://bughunters.google.com/about/rules/google-friends/cloud-vulnerability-reward-program-rules`; the
manifest now records `url`= that human page, `capture_url`/`http.final_url` = the REST endpoint
`…/rest/v1/articles/about/rules/google-friends/…` → `records=58 bound=58 unbound=0`, exit 0. So the shape
`(url = documented page, capture_url = capture endpoint)` is the working one. **Earlier the manifest had
`url` = the API endpoint and no `capture_url`; the bind would fail — the current shape is required.**

**Rule G3 — the capture must be regenerable by a committed producer from a documented URL.**
A capture is auditable only if a third party can re-derive it. `capture-source.py --kind <kind> --url <u>`
prints `status fetched_bytes snapshot_bytes sha256 utc`; the manifest record's `sha256` must equal a rerun's
digest. Measured **against the landed candidate — it FAILS**:

```
$ curl -sS -o s069.live.txt '…/rest/v1/articles/…' ; wc -c s069.live.txt
48657                                        # served JSON, single line

$ python3 corpus/instruments/capture-source.py --id S069 \
    --url '…/rest/v1/articles/…' --out S069.repro.txt --kind text
S069 status=200 fetched_bytes=48657 snapshot_bytes=47136 sha256=7e2004ba… out=…/S069.repro.txt
   (1 line — collapse() treats the JSON as one line)

$ sha256sum corpus/source-snapshots/round-44/S069.txt .ufo/waves/round-44/source-recon/S069-body.txt
0932279c…   45681 B / 1132 lines   corpus/…/S069.txt
0932279c…   45681 B / 1132 lines   .ufo/…/S069-body.txt      ← capture is a copy of the UNCOMMITTED recon file
```

Neither `collapse(served JSON)` (47136 B / 1 line / `7e2004ba…`) nor `collapse(extracted body)` (44887 B /
961 lines / `260cfcd9…`) nor per-line-collapse-with-blanks (45058 B / 1132 lines / `7b155e3e…`) reproduces the
committed `0932279c…`. **No committed producer exists** (`grep -rn 'rest/v1/articles' corpus/ scripts/` over
`*.py`/`*.sh` = 0 hits; no `--field body`/`--json` option in `capture-source.py`). The manifest carries no
`extraction`/raw-bytes field and the row's anchor cell records no raw byte count. So the capture is bound
(G2) but not re-derivable — a third party cannot regenerate `0932279c…` with committed tooling.
**Draft rule: the manifest record must carry `extraction` (e.g. `{"type":"json-field","field":"body"}`) plus
`raw_bytes`, and the producer must be a committed instrument or committed script; otherwise the anchor cell
must record the raw fetch byte count and the exact pipeline.** This is the strongest concrete defect found
in the landed candidate.

**Rule G4 — pinned quotes are re-verifiable against the capture (and against a live open).**
`source-recheck.py --manifest …/round-44/manifest.json --source S069` verifies `sha256` and every `quotes[]`
entry: normalized text must occur in the capture; a non-unique quote must carry an `anchor` whose 4-line
window holds it. Measured on the landed manifest:

```
S069:sha256 OK
S069:Q1 OK normalized=markup-whitespace occurrences=1 anchor=61-ok
S069:Q2 OK normalized=markup-whitespace occurrences=1 anchor=62-ok
S069:Q3 OK normalized=markup-whitespace occurrences=1 anchor=70-ok
exit=0
```

and each pinned quote re-occurs in my own live fetch (normalized body, `occurrences=1`, live windows 59/60/69):
the source still says what was captured. Draft shape: every located quote cited by an entry or a frontier row
must be a `quotes[]` record (`{"id","anchor","quote"}`, ≤25 words); an `anchor` is required whenever the quote
is non-unique. The landed manifest does this for Q1–Q3.

**Rule G5 — the knowledge entry's `recheck:` line is a bare shell command, not a cadence-prefixed sentence.**
`frontier-recheck-count.py` runs `bash -c "<text after 'recheck:'>"` and requires it to be a
`source-recheck.py` invocation whose `--source` set equals the entry's declared `source:` ids, exit 0.
Measured **against the landed entry — it FAILED at my first measurement and passes now after a sibling fix**:

```
# at the earlier revision the line read:  recheck: 180d — cd … && python3 …source-recheck.py …
FAIL     F26  knowledge/google-cloud-vrp-customer-resource-boundary.md ids=S069 exit=127 problems=recheck-exit-127
entries=29 pass=28 exit=1

# after a sibling edit (mtime 2026-10-28T16:13:36Z) the line is:  … --source S069 # 180d
PASS     F26  knowledge/google-cloud-vrp-customer-resource-boundary.md ids=S069 exit=0
entries=29 pass=29 exit=0
```

`bash -c '180d — cd …'` exits 127 (`180d: command not found`); the cadence belongs as a `#`-comment or in the
registry row's `recheck` column, never as a line prefix. **Draft rule: `recheck:` = `cd <lane> && python3
corpus/instruments/source-recheck.py --manifest <m> --source <S###>` with `--source` = declared set in BOTH
directions (no dropped id, no undeclared id), exit 0.**

**Rule G6 — frontier row shape and entry grounding.**
`| F26 | <topic> | admitted | knowledge/<entry>.md | S0NN | <next> |` on one line, entry path bare or
backticked (the harness strips `` ` ``; the existing rows are bare, so bare is the convention). The entry must
declare `source: S0NN` and cite it. `ground:` is carried by 16 of 26 frontier entries (F01–F08 and F11 lack it,
as does F26's draft — optional, not a failure; recommend adding `ground: F26` for consistency with F21–F25).

**Rule G7 — quote discipline inside the entry body.**
The S067 lesson (round-43 §6 row 3) requires each quoted span to be verbatim ≤25 words and reproducible at its
locator. Measured on the landed entry — **one quote fails**:

```
entry line 9: “In principle, any Google Cloud product or web service that handles reasonably sensitive user
               data is intended to be in scope” (`S069.txt:9-11`)
capture L9  : In principle, any [Google Cloud](https://cloud.google.com/products?e=48754805)
              product or web service that handles reasonably sensitive user data is intended
              to be in scope.

normalize(entry-quote) in normalize(capture) = False   (occurrences over whole capture = 0)
```

The entry elides the `[Google Cloud](…)` link markup inside a quoted span, so the sentence is not verbatim —
and it is not pinned in the manifest, so `source-recheck` never sees it. The other quoted spans (the
`source:` line and the two `“…”` boundary sentences) verify. **Draft rule: every quoted span in the body is
either (a) a manifest `quotes[]` record, or (b) verbatim under `source-recheck.normalize`; markup inside a
quoted span must be shown (`[Google Cloud](url)`) or elided explicitly with `[…]`.**

**Rule G8 — the frozen counter must actually move.**
C2's `after` needs `26` admitted rows; the claims counter prints `0` (§0). The Gate's counting command must be
the one that changes: `grep -cE '^\| F[0-9]+ \| .* \| admitted \|' corpus/README.md`. A Gate that cites a
counter which returns the same value on before and after is a do-nothing gate.

**Rule G9 — record the reject with the admit (registry row + a logged candidate).**
See §2: every rejected row lands as an 11-cell row with `status=rejected`, `teaches` = `REJECTED: <ground>;
flip: <falsifiable condition>`, `used-by=—`, `opened`=today, `recheck` a cadence. The record must carry the
opened evidence (status + fetched bytes + what the capture would contain) so a later reader can re-open it.

**Gate block, ready to append** (the shape the integrator would land in `corpus/lessons/round-44.md`):

```
## Gate — C2 source admission + reject (round 44)

### Admitted — F26 / S069
- S069 | Google Cloud VRP rules | docs | A | scope… | anchor: API capture S069.txt, sha256 0932279c…,
  fetched 2026-10-28T18:53:38Z, quotes Q1–Q3 | mined | opened 2026-10-28 | recheck 180d |
  used-by corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md
  + conditions G1–G9 hold except: G3 capture not re-derivable (record extraction+raw_bytes or commit the
    producer); G7 one elided-markup quote at entry:9. Both must be fixed before this row is gate-clean.

### Rejected — S071 (candidate)
- URL https://bughunters.google.com/about/rules/google-friends/cloud-vulnerability-reward-program-rules
  | opened 2026-10-28T19:11:43Z | status 200 | fetched 3753 B | snapshot 62 B sha256 5ed0e397…
  REJECTED: JS shell, zero rule text in served bytes; capture cannot carry Q1–Q3.
  flip: HTML serves the operative rule text server-side, evidenced by a --kind html capture containing Q1.

### Seam check — row ↔ entry ↔ manifest ↔ live fetch
S069 row (source cell human URL) ⇄ manifest url (same) ⇄ capture_url (API) ⇄ S069.txt sha256 0932279c…
⇄ live body (same quotes, occurrences=1). Re-run: source-recheck exit 0; binding exit 0; census exit 0.
```

---

## 2. The one reject (opened, measured, drafted)

**Candidate reject — `S071` (proposed), the human/HTML form of the very same rules page.**

Opened by this seat after the S069 capture:

```
$ python3 corpus/instruments/capture-source.py --id REJ-A \
    --url 'https://bughunters.google.com/about/rules/google-friends/cloud-vulnerability-reward-program-rules' \
    --out REJ-A.txt --kind html
REJ-A status=200 fetched_bytes=3753 snapshot_bytes=62 sha256=5ed0e397dd5928bde2af555cdc26b0d959b4a231b3dd9c250831f47151ba96ac utc=2026-10-28T19:11:43Z

$ cat REJ-A.txt
Cloud Vulnerability Reward Program Rules | Google Bug Hunters        # one line — the <title> only
```

The served 3,753-byte HTML is a JS shell: no operative rule text, no Q1–Q3. Ground for rejection: **a source
row must carry a capture that contains its pinned quote; this URL cannot produce one.** It also *proves the
admitted row's URL choice*: had S069's source cell been the HTML URL, `url`/`capture_url` would both be the
shell and the capture would be 62 bytes — the admission would fail its own gate.

Proposed row (11 cells, census-clean shape):

```
| S071 | Google Bug Hunters HTML rules page — https://bughunters.google.com/about/rules/google-friends/cloud-vulnerability-reward-program-rules | docs | C | Whether the HTML rules page itself carries the operative Cloud VRP scope text absent the REST endpoint | opened 2026-10-28T19:11:43Z, status 200, 3753 B, <title> only | REJECTED: JS shell; served bytes contain no rule text and cannot carry Q1–Q3; flip: page server-renders the operative rules, evidenced by a --kind html capture containing 'The Google Cloud VRP scope is strictly limited to Google-owned infrastructure and services.' | rejected | 2026-10-28 | 180d | — |
```

This is a second reject beyond the lane's already-landed `S070` (the rules-directory shell). It is a different,
sharper case: same program, same publisher, *admissible URL class* — but wrong capture surface.

**Screened but not drafted (one line):** `https://cloud.google.com/security/vulnerability-reward-program` —
HTTP `200`, fetched 41,263 B, but the body is a 404 page (`snapshot_bytes=169 sha256 7a295f3f…`, text
`404. Page Not Found` / `The requested URL … was not found on this server`). A status-code-only screen admits
it; the gate's body-content check rejects it. Flip: the URL serves the programme page. Recorded here as a
second rejected candidate; a row is not drafted because the soft-404 makes it the weaker of the two cases.

---

## 3. Checks this seat ran (exact commands, real output)

| # | command | observed | limb |
|---|---|---|---|
| 1 | `grep -cE '^\| F[0-9]+ \| .* \| admitted \|' corpus/README.md` / frozen regex | 26 / 0 | G8 |
| 2 | `grep -cE '^\|[[:space:]]*S[0-9]{3,}\|' corpus/SOURCES.md`; `find corpus/knowledge -name '*.md' \| wc -l` | 70 / 63 | G8 |
| 3 | `git diff --numstat corpus/README.md corpus/SOURCES.md corpus/instruments/knowledge-expected.txt` | 19/0, 5/0, 1/0 — append-only | G1 |
| 4 | `python3 corpus/instruments/capture-binding-check.py --root .` | `records=58 bound=58 unbound=0`, `round-44 records=1 url_bound=1`, exit 0 | G2 |
| 5 | `python3 corpus/instruments/source-recheck.py --manifest corpus/source-snapshots/round-44/manifest.json --source S069` | `sha256 OK`, `Q1 anchor=61-ok`, `Q2 anchor=62-ok`, `Q3 anchor=70-ok`, exit 0 | G4 |
| 6 | `python3 corpus/instruments/frontier-recheck-count.py --root .` | `entries=29 pass=29 exit=0` now; at first run `entries=29 pass=28 exit=1` with `F26 … problems=recheck-exit-127` | G5 |
| 7 | `./scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi` | `kasegi ok`, exit 0 (W04 S028, W04 S029 unchanged) | G1 |
| 8 | `curl -sS '…/rest/v1/articles/…'` | `200`, 48,657 B | live open |
| 9 | `python3 corpus/instruments/capture-source.py --id S069 --url '…/rest/v1/articles/…' --kind text` | `fetched_bytes=48657 snapshot_bytes=47136 sha256=7e2004ba…` ≠ committed `0932279c…` | G3 |
| 10 | `sha256sum corpus/…/S069.txt .ufo/…/S069-body.txt` | both `0932279c…` (capture = uncommitted recon copy) | G3 |
| 11 | `python3 corpus/instruments/capture-source.py --id REJ-A --url '…/about/rules/…' --kind html` | `200`, `fetched 3753`, `snapshot 62`, `sha256=5ed0e397…` | reject |
| 12 | `python3 corpus/instruments/capture-source.py --id REJ-B --url 'https://cloud.google.com/security/vulnerability-reward-program' --kind html` | `200`, `fetched 41264`, `snapshot 169`, `sha256=7a295f3f…`; body `404. Page Not Found` | reject |
| 13 | instrument `normalize` vs entry line-9 quote | `False`, `occurrences=0` over capture | G7 |

No sibling seat's output was trusted without an independent re-measure: row cells were dumped from
`corpus/SOURCES.md` directly, the capture was re-hashed, and the reject URLs were fetched by this seat.

## 4. Findings summary

| severity | rule | finding | evidence |
|---|---|---|---|
| defect (must fix before gate-clean) | G3 | committed capture `0932279c…` is not re-derivable by committed tooling; source is a copy of uncommitted `source-recon/S069-body.txt`; no `extraction`/`raw_bytes` recorded | §1 G3 commands |
| defect (already fixed by a sibling) | G5 | `recheck: 180d — cd …` exited 127 → `entries=29 pass=28 exit=1`; line is now `… --source S069 # 180d` → `29/29` | §1 G5, two measurements + mtime |
| defect (minor) | G7 | entry quote at `S069.txt:9-11` elides `[Google Cloud](…)` link markup → not verbatim, not in manifest | §1 G7 |
| defect (frozen artifact) | G8 | `claims.json` C2 counter regex returns 0; cannot observe the move it claims to measure | §0 |
| cosmetic | G6 | `ground:` absent (26/63 entries carry it); F26 row uses backticked path where F01–F25 are bare | §1 G6 |
| pass | G1 | row shape, census exit 0, append-only, all enums valid | §1 G1 |
| pass | G2 | `url`/`capture_url`/`http.final_url` bind correctly after the manifest was corrected | §1 G2 |
| pass | G4 | Q1–Q3 reproduce in capture and in my own live fetch | §1 G4, §3 #8 |

## 5. Limitations

- The candidate admission was already landed by sibling seats when this draft was measured; the Gate shape is
  therefore a *post-landing* check, not a pre-admission gate. The two live defects (G3, G7) are mine to hand
  to the integrator, not to fix.
- The reject `S071` is a draft row, not a landed row: the row text is provided for L1 to integrate; the
  candidate's served bytes were measured live at 2026-10-28T19:11:43Z.
- The "non-author admit/reject spot-check" limb of the C2 after-state is a sibling's seat; not measured here.
- `source-recon/S069.txt`/`S069-body.txt` are untracked wave files — they are recon evidence, not committed
  capture provenance.
