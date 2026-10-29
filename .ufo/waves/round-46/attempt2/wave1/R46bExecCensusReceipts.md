VERDICT: DRAFT-READY

# R46bExecCensusReceipts — round-46 (attempt 2), lane kasegi

Seat scope (single item): write the round's census pair (before + after run-book) and
the freeze pins receipt. Deliverable:

- `.ufo/waves/round-46/attempt2/wave1/R46bExecCensusReceipts.draft/census.sh` (draft, L1 integrates)
- `.ufo/waves/round-46/attempt2/wave1/R46bExecCensusReceipts.draft/freeze-pins.txt`
- `.ufo/waves/round-46/attempt2/wave1/R46bExecCensusReceipts.draft/sources-census-before.txt`
- `.ufo/waves/round-46/attempt2/wave1/R46bExecCensusReceipts.draft/sources-census-after-preview.txt`
- `.ufo/waves/round-46/attempt2/wave1/R46bExecCensusReceipts.draft/sources-census-after-preview.filemode.txt`

Nothing outside the draft directory was written. No git/jj mutation, no commit, no push.
The lane's committed counters, the frozen claims file and the shared controls directory were
read only.

---

## 1. The frozen before-receipt EXISTS — verified, and reproducible

The card's premise is that the before receipt is already at
`.ufo/waves/round-46/attempt2/controls/sources-census-before.txt`. It exists, so the
"create it NOW" branch was **not** needed; the script's `before` mode would create it only
if absent.

Command:
```
ls -la /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-46/attempt2/controls/
```
Output (relevant line):
```
-rw-r--r-- 1 vgpnk vgpnk  366 Oct 29 17:49 sources-census-before.txt
```

Its content, quoted in full:
```
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	W04	S072 duplicate url bughunters.google.com/about/rules/about-this-section across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
```

**It is reproducible from the live tree right now.** Command:
```
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
```
Output:
```
kasegi	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
kasegi	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
kasegi	W04	S072 duplicate url bughunters.google.com/about/rules/about-this-section across scopes
kasegi	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
EXIT=0
```
`diff -u <frozen receipt> <fresh run>` printed nothing → `IDENTICAL`.

**The same three warnings also hold at the frozen base export 04af9bc9**, so the before
value is not an artefact of the current tree. Command (base exported with
`git -C <lane> archive 04af9bc92229232ea5cce8b32bfe59dd969eb26d corpus | tar -x -C <scratch>`):
```
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin <scratch>/base
```
Output:
```
base	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
base	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
base	W04	S072 duplicate url bughunters.google.com/about/rules/about-this-section across scopes
base	ok	<scratch>/base/corpus/SOURCES.md
EXIT=0
```
(The lane label differs — `base` vs `kasegi` — only because the census derives the label
from the target directory's basename; the W04 set and the `ok` line are identical.)

The census script's own selftest passes on this host, so the tool producing these values is
itself sound:
```
TMPDIR=<scratch> bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh selftest
```
Output (tail):
```
killed	W04-scope-sensitive-mutant
killed	W04-does-not-fail-validation
killed	E04-rejected-pair-exemption-mutant
killed	E04-rejected-pair-exemption-exit-0
killed	out-not-truncated-before-target-resolution
killed	H1-no-table-cell-execution
killed	gawk-failure-is-error-not-ok
selftest ok
EXIT=0
```

---

## 2. Does the S074 row share a URL with an already-held row? **NO.**

This is the question the card asks me to answer and report.

**Answer: no held row carries the repository-security-advisories URL.** Therefore adding
S074 raises **no W04** and **no E04**, and the after-run's expected output is exactly the
three carried warnings plus the `ok` line — i.e. **byte-identical to the before receipt**.

Evidence, three independent ways:

**(a) The census's own normalization over the live registry.** The census's `url_of()`
strips the scheme, strips a `#fragment`, strips a trailing `/`, lowercases the host and
keeps the path verbatim. Applying that to every held row's URL:
```
grep -oiE 'https?://[^ |)]+' corpus/SOURCES.md | sed -E 's#^[A-Za-z]+://##; s#/$##' | tr 'A-Z' 'a-z' | grep -i advisor
```
Output:
```
github.com/advisories/ghsa-v676-f8gm-92r9
```
That is S068 — a *GitHub Advisory Database* entry, a different ground from GitHub Docs'
*repository security advisories* concept page, and a different URL. The S074 URL
`https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories`
is absent from the registry.

**(b) Fleet-wide.** The same sweep across every lane's `corpus/SOURCES.md`:
```
grep -hoiE 'https?://[^ |)]+' /home/vgpnk/Projects/shokunin/*-shokunin/corpus/SOURCES.md | ... | grep -i "advisor"
```
Output:
```
github.com/advisories/ghsa-v676-f8gm-92r9
github.com/systemd/systemd/security/advisories/ghsa-652q-wxr6-h5j6
```
Neither is the S074 URL. The census's fleet-wide `shared` mode also lists no shared
`docs.github.com` URL:
```
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh shared --root /home/vgpnk/Projects/shokunin | grep -i "docs.github.com"
```
Output: `(none shared)`.

**(c) The census `shared` mode over the whole fleet does not list the S074 URL as shared**,
and `grep -rln "repository-security-advisories" /home/vgpnk/Projects/shokunin/*-shokunin/corpus/SOURCES.md`
prints `(no lane SOURCES.md contains it)`. The URL appears only in
`corpus/source-snapshots/round-46-a2/manifest.json` (the capture manifest, not a registry row).

**A near-miss that must not be mistaken for a collision:** S073's URL is
`https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately`
— the *reporter-side* private-reporting flow (F28). S074's URL is
`.../concepts/vulnerability-reporting-and-management/repository-security-advisories` — the
*maintainer-side* advisory lifecycle (F29). Different URLs, different grounds. The census
compares full normalized URLs, not host-only, so these do not collide.

The script's `urlcheck` mode automates (a) and states the consequence:
```
bash census.sh urlcheck
```
Output:
```
urlcheck: registry=/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
urlcheck: S074 url=https://docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories
urlcheck: normalized=docs.github.com/en/code-security/concepts/vulnerability-reporting-and-management/repository-security-advisories
urlcheck: NO COLLISION — no held row other than S074 carries the S074 URL
urlcheck: consequence: adding S074 raises NO W04 and NO E04
EXIT=0
```

---

## 3. The after run-book (what the L1 runs at round end)

Same command as before:

```
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kasegi
```

**Expected: exit 0; the same three W04 warnings (S028, S029, S072); NO W04 S074; no
E-findings; an `ok` line for the lane.** The expected output is byte-identical to the
frozen before receipt, because S074's URL is unique (section 2).

The script's `after` mode is that run-book, made executable and self-checking:

```
bash census.sh after
```

It asserts, in order: exit status 0; the W04 set is exactly ⊆ {S028, S029, S072, S074};
none of the three carried warnings was dropped; no `E*` finding anywhere; an `ok` line is
present; and a **second invocation** — the one C2's own admission gate uses — agrees.

### 3a. Why the second invocation matters

The f29-gate's H7 check does **not** use the lane roster; it runs
`bash <census> validate --file <root>/corpus/SOURCES.md`. Read from
`corpus/instruments/r46-f29-gate.py` (`def h7`):
```python
p = subprocess.run(["bash", CENSUS, "validate", "--file", os.path.join(root, "corpus/SOURCES.md")],
                   capture_output=True, text=True, timeout=120)
ok_line = bool(re.search(r"^\S+\tok\t", p.stdout, re.M))
return p.returncode == 0 and ok_line, "census-rc=%d ok-line=%d" % (p.returncode, int(ok_line))
```
The `after` mode therefore cross-checks both invocations and fails if their W04 sets
disagree. Verified equal on the live tree:
```
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file corpus/SOURCES.md
```
Output:
```
file	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
file	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
file	W04	S072 duplicate url bughunters.google.com/about/rules/about-this-section across scopes
file	ok	/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/SOURCES.md
EXIT=0
```
Same three W04 rows as the lane-roster invocation.

---

## 4. Do-nothing / counterfactual discrimination

A passing check that cannot fail proves nothing. Each mode was exercised against
deliberately broken inputs in scratch. **No production file was touched**; the broken
registries were copies under `$HYAKU_SCRATCH/kasegi-r46/…`.

| scenario | what it simulates | observed |
|---|---|---|
| `after` on the live tree | the wave has not landed | exit 0; `W04 S074 ABSENT` |
| `after` on a synthetic tree with an S074 row carrying its own unique URL | the wave landed as expected | exit 0; `W04 S074 ABSENT`; three carried W04s intact |
| `after` on a tree where S074 shares **S073's URL** (different scope) | a URL collision | exit 0; **`W04 S074 PRESENT`** — the script names the collision |
| `after` on a tree where S074 shares **S073's URL and scope** | a full duplicate | **exit 1** — the census raises `E04`, the script reports `exit status UNEXPECTED (exit=1 — expected exit=0)` |
| `pins` at the freeze rev | the honest current state | exit 0; all six `[freeze=SAME]` |
| `pins` at the base rev | a wrong freeze rev | **exit 1** — `FAIL — a pinned artifact is absent at the freeze rev` |
| `pins` on a scratch fixture whose **selftests/battery** were mutated | the C1 wave landing | exit 0; three `freeze=DIFF kind=wave-surface` lines **reported, not failed** |
| `pins` on a scratch fixture whose **S074 capture** was mutated | a tamper | **exit 1** — `FAIL — a frozen-evidence pin differs from the freeze commit (tamper)` |
| `urlcheck` with S073's URL as the probe | a collision | exit 1; `COLLISION — row S073 already carries this URL` |
| `urlcheck` on the synthetic after-tree | S074 landed | exit 0; `self — row S074 carries this URL` then `NO COLLISION` |

The counterfactual census outputs, quoted:
```
counterfactual	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
counterfactual	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
counterfactual	W04	S072 duplicate url bughunters.google.com/about/rules/about-this-section across scopes
counterfactual	W04	S074 duplicate url docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately across scopes
counterfactual	ok	<scratch>/counterfactual/corpus/SOURCES.md
EXIT=0
```
```
counterfactual2	W04	S028 duplicate url docs.hackerone.com/en/articles/8494502-safe-harbor-overview-faq across scopes
counterfactual2	W04	S029 duplicate url eur-lex.europa.eu/eli/reg/2024/2847/oj/eng across scopes
counterfactual2	W04	S072 duplicate url bughunters.google.com/about/rules/about-this-section across scopes
counterfactual2	E04	S074 duplicate url docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately within scope GitHub's own statement of the reporter-side private-reporting flow only (who may report, the form's default fields, submission and the temporary private fork); not maintainer handling of a report, the GitHub Advisory Database or CVE assignment
EXIT=1
```

Final regression matrix (all re-runs by me, this turn):
```
before (live)                             exit=0  before: REPRODUCIBLE — fresh output is byte-identical to the frozen receipt
after  (live)                             exit=0  after: W04 S074 ABSENT … after: OK — exit 0, three carried W04 warnings, no E-findings
after  (synth after)                      exit=0  after: W04 S074 ABSENT … after: OK — exit 0, three carried W04 warnings, no E-findings
after  (cf shared-url)                    exit=0  after: W04 S074 PRESENT — S074 shares a URL with an already-held row … after: OK
after  (cf E04)                           exit=1
pins  (freeze rev ok)                     exit=0  pins: OK — all six artifacts present; frozen evidence unchanged at the freeze commit
pins  (base rev)                          exit=1  pins: FAIL — a pinned artifact is absent at the freeze rev
urlcheck (live)                           exit=0  urlcheck: NO COLLISION — no held row other than S074 carries the S074 URL
```

---

## 5. The freeze pins receipt

`bash census.sh pins` writes `freeze-pins.txt` — the sha256 of the six artifacts at the
**current tree**, each cross-checked against its blob at the freeze commit
`fe0f56b78b811dbb89bc7f2e17580d11b1b6ebd4` (read-only `git cat-file -e` / `git show`):

```
1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039  corpus/source-snapshots/round-46-a2/S074.txt  [freeze=SAME kind=frozen-evidence]
46e8077ac89edb0335711826ecb7abf3a1b7eefedc7108c3f6d936135481569f  corpus/source-snapshots/round-46-a2/manifest.json  [freeze=SAME kind=frozen-evidence]
a1091e246a51c1c1e710a18c6e8c9ba0cd4004069233a452ba446048de6fb8cd  corpus/instruments/r46-f29-gate.py  [freeze=SAME kind=frozen-evidence]
f7a7cdfa187ef6f2a074e9bda06af7d6163e43da69593b500b95c2c3a29e7fa8  corpus/instruments/r46-mutbat.py  [freeze=SAME kind=wave-surface]
8b17164aadbd9c6925b5edd4111e3174936388e60e81e09465df0f00c04ec770  corpus/instruments/r46-counters-selftest-c1.py  [freeze=SAME kind=wave-surface]
ff7104cfc891007160c6e474bf1f3b00a9e0b25e6ca9aed96559ea648c2b688f  corpus/instruments/r46-counters-selftest-c2.py  [freeze=SAME kind=wave-surface]
```

All six are byte-identical to the freeze commit **right now** (verified both by the script
and by a direct `git show fe0f56b…:<path> | sha256sum` loop, which printed `SAME` for all six).

**Independent cross-check against the freeze record's own declared hashes.**
`.ufo/waves/round-46/attempt2/freeze.txt` declares:
```
mutbat-sha256-v1 f7a7cdfa187ef6f2a074e9bda06af7d6163e43da69593b500b95c2c3a29e7fa8
f29-gate-sha256-v1 a1091e246a51c1c1e710a18c6e8c9ba0cd4004069233a452ba446048de6fb8cd
S074-sha256 1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039
manifest-a2-sha256 46e8077ac89edb0335711826ecb7abf3a1b7eefedc7108c3f6d936135481569f
```
All four match the computed values exactly. The freeze record's other two claims also
check out:
- `claims-sha256 ca73279f5464cf6395028c7e848b5d82bfec95794f03b7fd9b1a61cf000ca1d0` matches
  `sha256sum .ufo/waves/round-46/attempt2/claims.json` exactly.
- The freeze record states the attempt-1 selftests are byte-identical to base `04af9bc9`;
  `git show 04af9bc9:corpus/instruments/r46-counters-selftest-c1.py | sha256sum` printed
  `8b17164aadbd9c6925b5edd4111e3174936388e60e81e09465df0f00c04ec770` and the c2 selftest
  printed `ff7104cfc891007160c6e474bf1f3b00a9e0b25e6ca9aed96559ea648c2b688f` — the same
  values as the current tree, confirming the record's assertion.
- `source-recheck-sha256 fd2e01e88c8c45a949f48d67b3154ae87a95aeba0b6a9c42fbf64641b5b9c003`
  matches `sha256sum corpus/instruments/source-recheck.py` exactly.

### 5a. Why the receipt carries a `kind=` column

A single "is it identical to freeze?" check would be wrong at round end: the C1 work is
*supposed* to change the battery and the two selftests (the freeze record itself says
"the round's C1 work extends the selftests and the battery only"). So the receipt
classifies each pin:

- `kind=frozen-evidence` — the S074 capture, its manifest, and the F29 admission gate.
  These must **not** change; a DIFF is a **tamper** and the script fails.
- `kind=wave-surface` — `r46-mutbat.py` and the two counter selftests. The wave is
  **expected** to change these; a DIFF is the claimed work landing, so the script reports
  it and does not fail.

Both branches are exercised above (fixture with mutated selftests → exit 0 with three
reported DIFFs; fixture with mutated S074.txt → exit 1 "tamper").

---

## 6. Run-book summary — what the L1 must run at round end

```
bash .ufo/waves/round-46/attempt2/wave1/R46bExecCensusReceipts.draft/census.sh before
bash .ufo/waves/round-46/attempt2/wave1/R46bExecCensusReceipts.draft/census.sh pins
bash .ufo/waves/round-46/attempt2/wave1/R46bExecCensusReceipts.draft/census.sh urlcheck
bash .ufo/waves/round-46/attempt2/wave1/R46bExecCensusReceipts.draft/census.sh after
```

`after` is the round-end gate; it writes `sources-census-after.txt` (lane mode) and
`sources-census-after.filemode.txt` (the H7 `--file` mode) into `--out-dir`
(default: the shared controls directory) and exits non-zero on any expectation break.
`before` and `pins` write `sources-census-before.txt` and `freeze-pins.txt`.

---

---

## 7. Defects found and fixed in the draft script during this seat

The draft was exercised rather than merely written; three real defects surfaced and were
fixed before delivery.

1. **W04 id extraction was wrong.** The census packs `"<id> duplicate url <url> across
   scopes"` into **one** tab-separated field, so `awk -F'\t' '$2=="W04"{print $3}'`
   yields the whole sentence, not the id. The script then reported the three legitimate
   carried warnings as "UNEXPECTED W04 rows" and failed every clean tree. Fixed by
   splitting field 3 on whitespace (`split($3,a," "); print a[1]`), with a comment
   recording why.
2. **`urlcheck` normalized the URL wrongly and read the wrong columns.** It kept only the
   first path segment (`docs.github.com/en`), so every `docs.github.com` URL collapsed to
   the same key and S073's unrelated URL produced a false collision; and it read the
   `scope` column from the wrong pipe field. Fixed by reproducing the census's `url_of()`
   exactly (strip scheme, strip fragment, strip trailing slash, lowercase host, keep path
   verbatim) and by using the census's own field layout (`$2`=id, `$3`=source cell,
   `$6`=scope cell) via a single `awk` pass.
3. **`--help` was unreachable and an unused variable remained.** The mode was taken from
   `$1` before option parsing, so `census.sh --help` fell through to "unknown mode".
   Reworked so the mode is the first non-option argument and options may precede it;
   removed the dead `dropped_w04` local (`shellcheck` SC2034).

After the fixes the full regression matrix in section 4 was re-run end to end and every
mode behaves as documented.

---

## Limitations

1. **The after-run was not executed against the real landed tree.** No S074 row exists in
   `corpus/SOURCES.md` yet and `corpus/knowledge/github-repository-security-advisories.md`
   does not exist yet. The after-expectation is derived from (a) the census's own
   `url_of`/W04/E04 logic read in the source, (b) the live registry's URL inventory, and
   (c) synthetic trees in scratch that reproduce the shape of the real S074 row. When the
   wave lands, `after` must be re-run against the real tree; that re-run is the pass, not
   this prediction.
2. **The synthetic S074 row is a stand-in.** Its scope/teaches/anchor wording is invented
   for the census experiment. The census's W04/E04 verdict depends only on the URL and the
   scope cell, so the verdict transfers; but the row's *text* is not the L1's row and the
   E04 counterfactual in particular used S073's exact scope string, which the real S074
   row will not have.
3. **`used-by` / E11 was neutralised in the synthetic trees** by creating a placeholder
   `corpus/knowledge/github-repository-security-advisories.md`, so E11 could not mask the
   W04/E04 signal. On the real tree, the entry must exist for the mined row's `used-by`
   path to pass E11; that is C2's H6/H3 concern, not this seat's.
4. **The pins receipt pins the current tree, which is the pre-wave tree.** It proves the
   six artifacts are unmodified since the freeze *now*; it is not a claim that they will
   be unchanged after the wave (three of them are expected to change). The `kind=` column
   carries that distinction.
5. **Fleet-wide URL uniqueness was checked across `*/-shokunin/corpus/SOURCES.md` only.**
   A URL held in some other registry form (a non-`*-shokunin` directory, a shokuknow
   file) would not have been seen. The census's own `shared` mode over the fleet root
   agrees, and it reads the same `*-shokunin` registries, so the census's own verdict is
   unaffected.
6. **`shared` mode's `docs.github.com` result is fleet-wide but the W04 rule is
   per-lane.** Even if another lane held the S074 URL, the kasegi after-run would be
   unaffected; the fleet-wide sweep was run anyway to make the "no collision" statement
   stronger than strictly required.
7. **No live-target testing was performed** (this corpus is documentation only); the
   census reads local files only and made no network call.
8. **Tooling:** no package was installed or upgraded for this seat. `sha256sum`, `gawk`,
   `awk`, `sed`, `git` (read-only `log`/`show`/`cat-file`/`rev-parse`/`archive`/`status`/
   `diff`), `bash`, `python3` and `shellcheck` (0.11.0) were all already present on the
   host; per the host guard all pacman transactions are paused and none was attempted.
   `bash -n census.sh` → `SYNTAX OK`; `shellcheck -S warning census.sh` → clean (no
   output, exit 0).

---
