# ReviewC2Scanner — round 92, w1 (attack/review seat)

Scope: the landed C2 capability extension, `github-token` in
`corpus/instruments/capture-secret-scan.py`, and the SCORECARD row that names it.

- base `0628fd247914555838a42c02ba5d4ac08b7e095d`, freeze `9e4f0d6830dcc9a30c6f524c48d074ec8979f040`,
  C2 landing `58c0c115342877ee556cae19928d69839b0b29f0` (`git diff-tree`: `SCORECARD.md`,
  `corpus/instruments/capture-secret-scan.py` — two paths, matching C2 P3).
- instrument sha256 at the landing `04666f67…af3a9e` = the frozen candidate sha; gate sha256
  `8b6f849…1cc8e6` = the frozen gate sha (receipts `boundary-probes-r92.txt`).
- `patterns()` returns **13** names at the landing; the last is `github-token`.
- `--selftest` on the landed bytes: `SELFTEST-RESULT pass cases=68`.
- Corroboration only (the counter's own seats judge the claim): `capability-check.py` at the
  landing, seed 1545880357, `LIMB K1–K8 pass`, `CAPABILITY-CHECK-RESULT pass rc=0`
  (`capability-check-r92.txt`).

Nothing below re-scores either claim; each item is a routed defect or qualifier against the
frozen predicates as landed.

---

## Findings by severity

### F1 (high) — six block quotes fail at the landing (four of them newly) and 75 citations in the four scanner-reading entries now point at different text

`quote-anchor-check.py` (round-91 instrument) over
`corpus/knowledge/{capture-intake-gate,cloud-signed-cookies-and-user-bound-sas,
cloud-signed-url-credentials-in-captured-evidence,presigned-url-credentials-in-captured-evidence}.md`:

| rev | result |
|---|---|
| `0628fd2` (base) | `checked=68 bad=2 cites=257 out_of_range=0` rc=1 |
| `58c0c11` (landing) | `checked=68 bad=6 cites=257 out_of_range=0` rc=1 |

Four quotes are **new** BAD at the landing, all in `capture-intake-gate.md`:
`:69` (cites `:94-95`), `:71` (`:95`), `:109` (`:81`), `:111` (`:85`). The two remaining BAD
quotes pre-date the landing (F1b below). The check only validates block quotes and range
containment, so it under-reports: a plain `` `capture-secret-scan.py:N` `` citation that now
points at unrelated text is invisible to it. I therefore rebuilt the base↔landing line map
from the diff (four hunks: `+15` after base line 81, `+7` after 140, `+2` after 273, `+15`
after 316; file 378 → 417 lines) and compared every scanner citation's cited text at the base
numbers with the text at the same numbers at the landing.

Result: **75 citation tokens** (path-qualified and bare `:N` continuations) now point at
different lines — `capture-intake-gate.md` 29, `cloud-signed-cookies-and-user-bound-sas.md` 24,
`cloud-signed-url-credentials-in-captured-evidence.md` 22,
`presigned-url-credentials-in-captured-evidence.md` 0. Each row carries the corrected landing
range in `ReviewC2Scanner-receipts/reanchor-r92.tsv` (75 data rows). 60 rows reproduce the base
text exactly (normalised) at the new range; the other 15 are containment-only: the 10
`Known limits:` rows whose new range must absorb the round-92 sentence (base `:81-87` →
`:95-102`, `:96-102` at the two sites whose prose says "round-91 text", `:95-98` for `:81-83`),
the two `patterns()`-block rows (`:164-173` → `:186-195`, whose last line gained
`+ GITHUB_PATTERNS`), the two docstring-extent rows (`:1-105` → `:1-120`; `:1-104` → `:1-119`,
the positional map — the docstring now closes at `:120` and the base token was likewise one line
short of base `:105`), and `capture-intake-gate.md:134`'s `:23-87` → `:23-102` (shapes-plus-limits
span). No row is unexplained.

Verification of the list: applying the 75 rows plus the two F1b quote fixes to scratch copies of
the four entries leaves **0 BAD** among the 7 block quotes that cite the scanner, and every
mapped range reproduces the base text (60 exact, 15 by containment) and the landing file has no
in-range violation.

### F1b (medium, pre-existing) — the two BAD quotes already present at base

- `presigned-url-credentials-in-captured-evidence.md:67` quotes "run it on every capture before
  the commit that first adds it" but cites `:18-19`; the quoted sentence spans **`:20-21`**
  (unchanged by C2; both ≤ 80).
- `presigned-url-credentials-in-captured-evidence.md:75` quotes "Rows for aws-sts-session-token
  are refused (a session token is never a false positive)" but cites `:37-38`, which is
  `azure-sas-signature` shape prose. At base the text is `:95-96`; at the landing it is
  **`:110-111`** — so C2 moves the correct anchor even though it did not create the defect.

Both fixes verified (`presigned:67 → 20-21 ok`, `presigned:75 → 110-111 ok`).

### F1c (high, routed at the L1) — two rows of the L1's own re-anchor list would falsify a historical citation

`.ufo/waves/round-92/l1/reanchor-r92.txt` (78 `CHANGE` rows plus hand dispositions) agrees with
`reanchor-r92.tsv` on 64 rows, including the two reverse-dispositions it records itself
(`cookies:49 :196-197`, the two presigned quotes) and the `intake-gate:109 :81 → :96` hand fix.
Two rows must be **dropped**, because both tokens cite the round-90 instrument
`bb4309fffbe9bf98153a2933af72c8f2c3f4b5b1`, not the current one:

- `reanchor-r92.txt` `CHANGE capture-secret-scan.py:100 -> :115` for
  `cloud-signed-cookies-and-user-bound-sas.md:86` — that sentence reads
  "…the round-90 window admitted two to six (`…:100` at `bb4309fff…`)"; at `bb4309`,
  `sed -n '100p'` is `_PARAM = …[A-Za-z]{2,6}=…`, which is exactly the claim. `:115` at the
  landing is the *widened* `{2,7}` line, a different revision's rule.
- the same `:100 -> :115` for `cloud-signed-cookies-and-user-bound-sas.md:96` — "previously
  `{2,6}` at `:100` of the base revision": same pinned line, same reason. `:115` would make the
  sentence say the previous window is the current one.

Two further deltas are precision, not defects, and my list differs deliberately:
`intake-gate:107` and `cloud-signed-url…:79` say "round-91 text", where I map `:81-87` to
`:96-102` (the round-91 limits) rather than the L1's `:95-102` (which keeps the round-92
fine-grained clause inside a range the prose labels round 91); and `cloud-signed-url…:65`
`:1-104` maps positionally to `:1-119` (L1 agrees; `:1-120` only if the closing `"""` is meant).

### F2 (medium) — `capture-intake-gate.md:105` now states the wrong shape count

The sentence "Round 91 added a fourth cloud shape, `cloudfront-signed-cookie-signature`
(`…:164-173` now returns twelve)" is read at the landing, where the same expression returns
**thirteen** (`patterns()` = the six gate shapes + two AWS + four cloud + `github-token`). The
citation reanchors to `:186-195`; the count in the prose is stale. Line `:246` says "eleven
shapes", which was already wrong at base (twelve) and is wrong at the landing for the same
reason. Both are routed content defects, not counter failures.

### F3 (low, citation precision) — "40 characters in all" cites the line that says the opposite

The new docstring clause reads "…36 base62 characters (30 random plus a 6-character checksum,
S137 lines 167, 173: 40 characters in all, S136 line 160, S137 line 174)". `S136:160` is the
note whose point is that the **stateless** form (`ghs_APPID_JWT`) may *not* be 40 characters
("If your application expects or relies on installation tokens being exactly 40 characters
long, it may not handle this new token format correctly"). The 40-character fact for the
prefixed classic form is `S137:153` ("old authentication token formats are hex-encoded 40
character strings") plus `S137:174` ("without changing the token length"). Behaviour is
unaffected; the citation should name `S137:153`, not `S136:160`.

### F4 (low, coverage) — the `_` boundary suppresses true positives and is not a named limit

`_GH_LB`/the right lookahead treat `_` as a word character, so a token written against an
underscore reads clean:

```
02-pre-underscore   key_ghp_<36 base62>            hits=0 rc=0
03-post-underscore  ghp_<36 base62>_x              hits=0 rc=0
01-plain-space      use ghp_<36 base62> as …       HIT  rc=1
```

`S137:162` establishes that `_` is *not* a Base64/Base62 character and is the prefix
separator, so an adjacent `_` cannot be part of a token body; the guard is therefore stricter
than the evidence and loses a real match. The claim's frozen statement says exactly what the
code does ("not preceded … by a letter, digit or `_`"), so this is a design gap, not a claim
failure — but the docstring's `Known limits` list does not name it.

### F5 (low) — the stateless branch has no right boundary

`ghs_<digits>_<seg>.<seg>.<seg>` carries no `(?![A-Za-z0-9_])`, so a longer dotted run hits on a
truncated three-segment prefix:

```
12-stateless-4-segments  ghs_<d>_<10>.<10>.<10>.<10>  HIT
15-appid-21-digits       ghs_<21 digits>_<10>.<10>.<10>  hits=0  (matches the stated 1-20)
14-stateless-9char-seg   ghs_<d>_<9>.<9>.<9>             hits=0  (matches the stated 10+)
```

Claim-consistent (form (b) imposes no boundary) and benign in practice, but asymmetric with the
classic branch.

### Qualifier — honest, not a defect

`unused_allow=19` is unchanged by the landing and no allowlist row binds `github-token`, so the
new shape reads clean by absence. The fine-grained `github_pat_` limit is correctly declared
and correctly absent from `patterns()`.

---

## Clause-by-clause: what the sources state vs what is inference

Read at `corpus/source-snapshots/round-92/S136.txt` (GitHub Docs) and `S137.txt` (GitHub Blog);
line text collected in `clauses-vs-sources-r92.txt`.

| docstring clause | verdict |
|---|---|
| five three-letter prefixes (`ghp_`, `gho_`, `ghu_`, `ghs_`, `ghr_`) | **STATED** — `S137:157-161` lists exactly these five; `S136:162-167` lists the same five plus `github_pat_` (11 letters), which the docstring correctly treats separately as the named limit. `S136:158` states that tokens "begin with a prefix". |
| "case-sensitive" | **INFERENCE** — both sources render the prefixes in lower case and neither says anything about case. Implementation is consistent (`gh-upper-prefix` → no hit). |
| 30 random characters over base62 | **STATED** — `S137:173`: `Math.log((a-z + A-Z + 0-9).length)/Math.log(2) * 30 = 178`. |
| 6-character checksum, Base62 | **STATED** — `S137:167`: "A 32 bit checksum in the last 6 digits of each token … encode the result with a Base62 implementation". |
| "exactly 36 base62 characters" | **INFERENCE** — arithmetic 30 + 6; neither snapshot writes "36". |
| "40 characters in all" | **INFERENCE from stated parts** — `S137:153` (old formats are 40 chars) + `S137:174` (length unchanged), 4 + 36 = 40; the cited `S136:160` says the stateless form may *not* be 40 (F3). |
| boundaries: not preceded/followed by letter, digit or `_`; JSON `\n` escape allowed | **INFERENCE** — neither source states a boundary rule; the `\n` exception is a lane convention mirroring the earlier shapes. See F4. |
| stateless form `ghs_<APPID>_<JWT>` | **LABEL STATED, SHAPE INFERRED** — `S136:160` gives only the placeholder `ghs_APPID_JWT`; reading it as `ghs_` + APPID + `_` + JWT (two underscores) is an inference — a plain reading could put `APPID_JWT` after one underscore. |
| "numeric app id" | **INFERENCE** — no source line describes the app-id format. |
| "three dot-separated base64url JWT segments of 10+ characters each" | **INFERENCE** — JWS compact serialization is general knowledge, not in S136/S137; the 10+ floor and the 1-20 digit app id are lane-chosen bounds. |
| placeholder `ghs_APPID_JWT` and a bare prefix are not hits | **DESIGN**, verified: selftest `gh-doc-placeholder`, `gh-bare-prefix`; probes `ghs_<alpha appid>_…` → hits=0, and a bare `ghp_` followed by prose → no hit. |
| known limit: fine-grained `github_pat_`, "neither opened source states their length or alphabet" | **CORRECT** — `S136:163` gives the prefix only; S137 predates fine-grained tokens. |

So of the four items asked: the **five prefixes** are stated; the **36-character bound** is an
inference (30 and 6 are stated); the **boundary rules** are an inference (and stricter than the
evidence, F4); the **stateless form** is a label from `S136:160` with an inferred decomposition
and inferred segment grammar.

---

## Drift tokens excluded after checking (no change)

| token | why |
|---|---|
| `capture-intake-gate.md:53` `:192-193` | continues `capture-source.py` (`REFUSED_RC` mapping), not the scanner |
| `capture-intake-gate.md:53` `:164-171` | continues `capture-source.py` (kept-file selftest), not the scanner |
| `capture-intake-gate.md:134` `:136-142` | continues `capture-source.py:115-123` in the same sentence |
| `cloud-signed-cookies…:49` `:196-197` | refers to `S134.txt` occurrence lines, not the scanner |
| `cloud-signed-cookies…:86` `:100` | explicitly pinned `at bb4309fff…` — correct at that rev |
| `cloud-signed-cookies…:96` `:100` | explicitly "of the base revision" — correct there |

---

## Residual risk and verification gaps

1. **Another seat already holds an uncommitted re-anchor of the same four entries**
   (`git status`: 4 modified, 48 insertions/48 deletions). I did not touch them. Its mappings
   agree with `reanchor-r92.tsv` on every site I checked, with two deliberate differences:
   it writes `:95-102` for `Known limits:` at the two sites whose prose says "round-91 text"
   (I recommend `:96-102` there, since `:95` now carries the round-92 fine-grained clause), and
   it leaves the prose references of paragraph (3) below untouched.
2. **Prose line references bypass the machine check.** In
   `presigned-url-credentials-in-captured-evidence.md` these are already stale at base and
   remain so: `:69` "instrument lines 77-82" and "line 77" (base 77-82 is CloudFront shape
   prose; the Output paragraph is base `99-104` = landing **`114-119`**, and "never prints a
   matched value" is base `99` = landing **`114`**), and `:77` "instrument lines 33-36" for the
   allowlist row format (base `90-93` = landing **`105-108`**). The bare "instrument lines
   25-31" / "lines 32-42" at `:13` are still correct (both ranges are above the insert).
3. **Count sentences are only partially maintained.** `capture-intake-gate.md:105` ("twelve")
   and `:246` ("eleven") are stale (F2); `cloud-signed-url…:69` ("the two round-88 cloud shapes
   and the round-89 CloudFront shape") and `:152` (`:23-66`, "the three cloud ones") already
   undercounted at round 91 and still exclude `github-token`; `:152`'s explicit citation
   `:23-66` is correct *as a range* (the new block lives at `:81-94`) but no longer describes
   the shape set.
4. **Gap in what I ran:** one `capability-check.py` pass at a printed seed (K1-K8 pass); I did
   not run seeds 9191 and 1 — those belong to the claim's own seats. `--selftest` and the
   probes ran against a scratch copy of the landed bytes plus the landed
   `claim-package-check.py` and `capture-secret-allow.tsv` beside it (my first standalone copy
   failed with `FileNotFoundError` until the gate was placed beside it — that dependency is by
   design, `gate_patterns()` imports the file relative to the instrument).
5. **CREDENTIAL HYGIENE:** no fixture bytes are in this directory. The probes were generated in
   scratch (`/fast/scratch/hyaku/kasegi-r92/ReviewC2Scanner`, deleted before yield) and the
   receipt records only `HIT`/`CAPTURE-SECRET-SCAN` lines with `path=<f>`; no token, plant, or
   snapshot copy is present. Scratch dir removed.

## Files written

- `.ufo/waves/round-92/w1/ReviewC2Scanner.md` (this file)
- `.ufo/waves/round-92/w1/ReviewC2Scanner-receipts/reanchor-r92.tsv` (75 rows: file:line, old token, new token, reason)
- `.ufo/waves/round-92/w1/ReviewC2Scanner-receipts/quote-anchor-r92.txt` (checker at both revs)
- `.ufo/waves/round-92/w1/ReviewC2Scanner-receipts/boundary-probes-r92.txt` (selftest, shape set, 15 probes)
- `.ufo/waves/round-92/w1/ReviewC2Scanner-receipts/clauses-vs-sources-r92.txt` (S136/S137 cited lines + the new docstring block)
- `.ufo/waves/round-92/w1/ReviewC2Scanner-receipts/capability-check-r92.txt` (K1-K8 at the landing)
