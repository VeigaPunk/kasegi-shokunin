# ScribeReadmeF16 receipt — round 33, C2/F16 README appends

- Seat: `ScribeReadmeF16` (leaf). Round 33, wave 1. Lane base `690b69dae23ab9f4ccf056ba2d619cadc2abb3c4`; claims-freeze commit `6e55c8d58a3e63efe11c0df47068bfc479bfc8e0`; lane HEAD when measured `a6a502351bb90c8cd6d9b8f45f55109b7848e0d1`.
- Answering model: `opencode-go/deepseek-v4.1-flash` (config route table decides; no model passed by hand).
- Write scope exercised: `corpus/README.md` (append only) + this receipt. No other path written. No git/jj mutation (read-only `git status` / `git diff` / `git rev-parse` only). No network fetch. No tool installed or upgraded; no pacman transaction.
- Scratch: none needed — no fixture, clone or temp tree was created; nothing under `$HYAKU_SCRATCH` or `/tmp` was written by this seat.

## 1. Dependency receipt waited for, then read

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && WD=.ufo/waves/round-33/wave1 && for i in $(seq 1 30); do if [ -s "$WD/ExecEntryF16.md" ]; then echo "GOT ExecEntryF16.md after ~$((i*20))s size=$(wc -c <"$WD/ExecEntryF16.md")"; exit 0; fi; sleep 20; done; …
GOT ExecEntryF16.md after ~140s size=16732
```

The entry itself was read only after it was final. Digest moved while three reviewers' findings
were applied (`8d209995…` → `eebd5ea5…`), so the earlier 278-line read is labelled
**PRE-STATE** and not used for wording:

```
$ sha256sum corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md
eebd5ea572b3359f012e9c7ef9975969ffcbd3e5b06e31d40ac56a6a7d15910b  corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md
$ wc -l -c corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md
  305 24318 corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md
```
(an earlier read of mine saw 278 lines / 21970 B / `8d209995ec5af1129fab2238cb92dbba2fd68700dbeabd5c05d921f50669d08c` — superseded, not cited as evidence)

Header lines of the final entry (`:1-6`): H1 `# Chinese crowdsourced-testing platform scope and
reward rules (CNVD 众测, 360SRC)`; `source: S049 — https://zc.cnvd.org.cn/news/helpList — …`;
`source: S050 — https://security.360.cn/Reward/rules — 360SRC 外部漏洞处理和评分标准 V2.0 (2023.03.01)…`;
`verified-at: 2026-10-26`; `ground: F16`.

What the appended wording is tied to (read at `:169-196`, `:242-305`):
- `## Honest limit` — neither document is an authorization; "In scope for 360SRC" cannot be derived from S050 alone because the enumerating list is the separate `https://security.360.cn/Product/product` page named at S050.txt:71 and not captured.
- `## What this adds beyond F13 and F15` — the CNVD 众测 manual publishes no per-severity payout (enterprise rating + project rules), and 360SRC publishes a coefficient formula over business tier and grade.
- `## Scope and limits` — `verified-at` is not the capture instant; the recheck line verifies pin + 14 quotes, not upstream liveness.

## 2. Pre-append state (measured before the edit)

```
$ cd /home/vgpnk/Projects/shokunin/kasegi-shokunin && sha256sum corpus/README.md
d9865b2e126c626559de9704d9e8d636b6f4ce7eba2a3a74e6f32d92b2146f98  corpus/README.md
$ wc -c -l corpus/README.md
  316 31530 corpus/README.md
$ git status --porcelain corpus/README.md      # empty: clean at HEAD
$ git rev-parse HEAD
a6a502351bb90c8cd6d9b8f45f55109b7848e0d1
$ awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md
15
```

## 3. Append (R6: every existing line keeps its number)

Appended a `## Round-33 admission — coverage map row and Frontier F16 (appended 2026-10-26)`
section at the end of the file (now lines 318-342), mirroring the round-31 F15 section's shape:
R6 preamble, one coverage-map row, one frontier row, one `[r33 amendment]` paragraph. Verbatim:

```
## Round-33 admission — coverage map row and Frontier F16 (appended 2026-10-26)

The coverage map above is not edited in place (R6): the round-33 entry
`knowledge/chinese-crowdsourced-testing-scope-and-rewards.md` (Frontier F16, sources S049 + S050;
source basis: the CNVD 众测 platform's 使用手册 at https://zc.cnvd.org.cn/news/helpList and
360SRC's 外部漏洞处理和评分标准 V2.0 at https://security.360.cn/Reward/rules, both captured
2026-10-25 under `corpus/source-snapshots/round-32/`) is recorded here as an appended amendment so
every existing line keeps its number. The coverage-map row is appended here rather than inserted
into the map, and the F16 frontier row is listed here on the same table shape as the frontier
above.

| Area | Entry | Source basis |
|---|---|---|
| Chinese crowdsourced-testing platform scope and reward rules (round 33) | knowledge/chinese-crowdsourced-testing-scope-and-rewards.md | S049, S050 — public primary, opened 2026-10-26 |

| id | topic | status | entry | sources | next |
|---|---|---|---|---|---|
| F16 | Chinese crowdsourced-testing platform scope and reward rules (CNVD 众测, 360SRC) | admitted | knowledge/chinese-crowdsourced-testing-scope-and-rewards.md | S049, S050 | Read a reward only from the platform that prints it — CNVD 众测 publishes no per-severity money table, since the enterprise's rating and the project's rules set the payout (S049.txt:419), while 360SRC pays its business-coefficient formula over base 安全币 (S050.txt:112, 129) — and read neither as scope or authorization: 360SRC's enumerating asset list is a separate page S050 names but this capture does not contain (S050.txt:71), and CNVD 众测 intake is the customer's per-project authorization, not the submission page's target list (S049.txt:211-214). |

[r33 amendment, appended 2026-10-26] The parenthetical above records the round-26 frontier state
and each later amendment paragraph states its own round; those are retained as history, not
rewritten (R9): at round 33 the frontier stands at **16/16 admitted** — F01-F08 at round 23, F09
at round 24, F10 at round 25, F11 at round 26, F12 at round 28, F13 at round 29, F14 at round 30,
F15 at round 31, F16 at round 33. The 0/18 sentence is untouched: the lost-domain denominator
still holds 0 of 18 surfaces present, and the frontier count stays outside it.
```

Both table cells carry no `|`; the frontier row is one physical line; its `entry` cell is the
bare path `knowledge/…md` (no backticks) and its sources cell is exactly `S049, S050`, the entry's
header id pair.

## 4. Verification — post-append, measured

```
$ awk -F'|' '$2 ~ /^ *F[0-9]+ / && $4 ~ /^ *admitted *$/ {n++} END{print n+0}' corpus/README.md
16
```
```
$ git diff --numstat corpus/README.md
26	0	corpus/README.md
$ git diff --stat corpus/README.md
 corpus/README.md | 26 ++++++++++++++++++++++++++
 1 file changed, 26 insertions(+)
$ git diff -U0 corpus/README.md | grep '^@@'
@@ -316,0 +317,26 @@ frontier count stays outside it.
$ git diff -U0 corpus/README.md | grep -c '^-[^-]'
0
$ git diff -U0 corpus/README.md | grep -c '^-'
1          # the single `--- a/corpus/README.md` header line, not a deletion
$ git diff -U0 corpus/README.md | grep -c '^+[^+]'
21         # 21 non-blank added lines + 5 blank added lines = the 26 in numstat
```
So the diff is **additions only** — one hunk `@@ -316,0 +317,26 @@`, zero deleted lines.

R6 head-bytes identity: the first 31530 B of the post-append file hash to the pre-append
whole-file digest, i.e. every earlier line keeps its byte offset and number:

```
$ head -c 31530 corpus/README.md | sha256sum
d9865b2e126c626559de9704d9e8d636b6f4ce7eba2a3a74e6f32d92b2146f98  -
pre-append whole-file sha256: d9865b2e126c626559de9704d9e8d636b6f4ce7eba2a3a74e6f32d92b2146f98
$ sha256sum corpus/README.md ; wc -l -c corpus/README.md
3779e77f07a2d76119a074f598389d35353e01a4651cec8c75201c770f754932  corpus/README.md
  342 33902 corpus/README.md
$ git status --porcelain corpus/README.md
 M corpus/README.md
```

### 4a. Harness binding (this seat's read-only run, not the C2 gate)

`corpus/instruments/frontier-recheck-count.py` matches the row with
`^\|\s*(F\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*`?([^|`]+?)`?\s*\|` (instrument `:45`), reads
`root/corpus/README.md` (`:55`) and resolves the entry cell against `root/corpus/<cell>` (`:76`).
Run from the lane root on the current lane bytes:

```
$ grep -c '^| F16 ' corpus/README.md
1
$ python3 corpus/instruments/frontier-recheck-count.py
…
PASS     F16  knowledge/chinese-crowdsourced-testing-scope-and-rewards.md ids=S049,S050      exit=0
entries=19 pass=19 exit=0
harness_exit=0
```

Label: this is **my own read-only run**, taken while other seats may still be landing
`corpus/SOURCES.md` rows and manifests, so it is non-comparative (M30-3) and is not the round's C2
gate — `ExecHarnessC2` re-runs it on quiescent bytes. The F16 line is what my append is
responsible for: without the row the same instrument reported `entries=18 pass=18` (ExecEntryF16's
PRE-STATE, `.ufo/waves/round-33/wave1/ExecEntryF16.md` §5), and the entry is unchanged since that
seat's final digest `eebd5ea5…`.

## 5. Bounds, risks, blockers

- Writes: `corpus/README.md` and this receipt only. Nothing under `.ufo/state/`,
  `MANIFEST.json`, `templates/`, `scripts/`, the fleet root or `/home/vgpnk/Projects/shokuknow`
  was written; claims.json, the controls dirs, the report, `LOG.md`, `SOURCES.md`, `SCORECARD.md`
  and the instruments were not touched.
- No git/jj mutation of any kind; no `add`/`commit`/`stash`/`checkout`/`reset`/`jj` subcommand.
  The L1 commits through the lane helper.
- No live target was contacted; no fetch was made (the two source URLs are quoted from the entry's
  `source:` lines and the round-32 captures). No credential material is reproduced here or in the
  appended text (Q6); the CNVD 众测 credential-bearing lines (`S049.txt:202-205`, `:398-406`) are
  not quoted, and my appended prose quotes no capture line at all.
- Frontier-row `next` cell quote discipline: it carries four short located citations
  (`S049.txt:419`, `S050.txt:112, 129`, `S050.txt:71`, `S049.txt:211-214`) and no quoted sentence
  longer than 25 words — the cell paraphrases and cites the entry, which owns the verbatim quotes.
- Known limit of this seat's evidence: the `16` count is the README's admitted-row tally, not a
  judgement that F16's sources are tier-A — that is ExecRegistryAppend's rows. **Pre-state at the
  time of my first measurement** (labelled, not comparable to the after column):
  `grep -nE '^\| S0?4[89] |^\| S050 ' corpus/SOURCES.md` matched only line 54, the `S048` row.
  **Re-run on the bytes as they stand now** (`corpus/SOURCES.md` modified in the worktree by that
  seat, not by me):

  ```
  $ grep -nE '^\| S0?4[89] |^\| S050 ' corpus/SOURCES.md | cut -c1-160
  54:| S048 | Microsoft Security Vulnerability Research (MSVR) — … | docs | A | …
  55:| S049 | 网络安全众测平台帮助 - CNVD — https://zc.cnvd.org.cn/news/helpList | docs | A | CNVD's own help-page statements …
  56:| S050 | 360SRC 外部漏洞处理和评分标准 V2.0 — https://security.360.cn/Reward/rules | docs | A | 360SRC's own handling and scoring standard: its …
  $ grep -c "chinese-crowdsourced-testing-scope-and-rewards" corpus/SOURCES.md
  4
  ```
  Both rows are tier `A` and name the F16 entry as used-by, so the coverage-map row's
  `S049, S050 — public primary` label matches the registry as it now stands. The rows' own
  correctness (anchors, cadence, census) is ExecRegistryAppend's and ExecCensusDry's evidence, not
  mine; I did not edit `corpus/SOURCES.md`.
- Nothing here is a gate run: the lane census, `capture-binding-check.py`, `recheck-audit.py`,
  `knowledge-expected.txt` and the post-integration harness are the parent's checks, and the
  `entries=19 pass=19` figure above must be re-taken on quiescent bytes.
