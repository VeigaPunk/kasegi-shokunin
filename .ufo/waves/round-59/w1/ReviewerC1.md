VERIFIED: every frozen C1 check reproduces at 472737847 (P1-P8 refused with markers=0, CTRL admitted derived=35, RESIDUAL-awk-write admitted markers=1 as named open, selftest 14/0, mutbat 2/2, ledger 35/35, red fixture stale, scope clean). Separately, the derive gate admits further write and execute classes outside the named residual list (section 4); none trips a C1 kill rule, but they contradict the SKILL.md registry text "writes nothing in the lane".

Seat: ReviewerC1 (round 59, wave w1, C1 derive gate). Lane HEAD = 472737847ff31d1255bf1a0745822a5e878e9622 (verified). Clone: git clone -q --shared, then checkout 472737847 detached in the scratch dir; toplevel asserted equal to the clone path.
Scratch: /fast/scratch/hyaku/kasegi-r59/ReviewerC1 (removed before yield; see section 6).

## 1. Instrument identity and the four mandated checks (in the clone root)

1a. `sha256sum corpus/instruments/figure-audit.py` (in clone, exit 0)
    32e1cddb2291a643622d6501960d25d795d9e12ba2319a9b3ff9cab2d4e83ff0  (MATCHES the frozen want)
    Same sha for the lane file (`sha256sum /home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/figure-audit.py`, exit 0).
    controls/freeze-digests-r59.txt:2 `candidate 32e1cddb2291a643622d6501960d25d795d9e12ba2319a9b3ff9cab2d4e83ff0` (matches).

1b. `python3 corpus/instruments/figure-audit.py --selftest > selftest.txt; tail -1`  exit 0
    selftest cases=14 failures=0   (want: cases=14 failures=0, exit 0)  PASS

1c. `python3 corpus/instruments/figure-audit-mutbat.py > mutbat.txt; tail -1`  exit 0
    mutbat killed=2/2 survivors=0 controls=pass   PASS

1d. `python3 corpus/instruments/figure-audit.py > audit.txt; tail -1`  exit 0
    FIGURE-AUDIT figures=35 ok=35 stale=0 exit=0   PASS

1e. `python3 corpus/instruments/figure-audit.py --ledger .ufo/waves/round-54/controls/red-d53-ledger.json | grep d53-1`  exit of the instrument 1
    FIG d53-1-trailer recorded=34 derived=33 want=34 stale   PASS (reads stale, exit 1)

## 2. Probe battery (committed runner, CLONE instrument, scratch root)

2a. `bash /home/vgpnk/Projects/shokunin/kasegi-shokunin/.ufo/waves/round-59/controls/c1-probe-run.sh /fast/scratch/hyaku/kasegi-r59/ReviewerC1/clone/corpus/instruments/figure-audit.py /fast/scratch/hyaku/kasegi-r59/ReviewerC1/probes`  runner exit 0
    instrument=.../clone/corpus/instruments/figure-audit.py sha256=32e1cddb2291a643
    probe=P1-semicolon       derive=cat g.txt; touch MARK-P1   exit=2 markers=0 :: FIGURE-AUDIT: UNAVAILABLE reason=derive-not-read-only
    probe=P2-andand          derive=cat g.txt && touch MARK-P2 exit=2 markers=0 :: reason=derive-not-read-only
    probe=P3-background      derive=cat g.txt & touch MARK-P3  exit=2 markers=0 :: reason=derive-not-read-only
    probe=P4-newline         derive=cat g.txt|touch MARK-P4    exit=2 markers=0 :: reason=derive-not-read-only
    probe=P5-cmdsubst        derive=cat g.txt $(touch MARK-P5) exit=2 markers=0 :: reason=derive-not-read-only
    probe=P6-pipe-tee        derive=cat g.txt | tee MARK-P6    exit=2 markers=0 :: reason=derive-not-read-only
    probe=P7-redirect        derive=cat g.txt > MARK-P7        exit=2 markers=0 :: reason=derive-not-read-only
    probe=P8-oror            derive=cat nosuch.txt || touch MARK-P8 exit=2 markers=0 :: reason=derive-not-read-only
    probe=CTRL-quoted-separator derive=cat g.txt | awk 'BEGIN{x=1;y=2} {print}' exit=0 markers=0 :: FIG CTRL-quoted-separator recorded=35 derived=35 ok
    probe=RESIDUAL-awk-write    derive=cat g.txt | awk 'BEGIN{print 1 > "MARK-RES"}{print}' exit=0 markers=1 :: FIG RESIDUAL-awk-write recorded=35 derived=35 ok
    Each P1-P8 line matches the frozen 'after' predicate (exit 2, markers 0, reason=derive-not-read-only). CTRL exit 0 derived=35. RESIDUAL exit 0 markers=1 (named open, unchanged).
2b. Rerun of the same runner (scratch probes-rerun), exit 0: identical probe lines.
2c. Parity: `git show 472737847ff31d1255bf1a0745822a5e878e9622:.ufo/waves/round-59/controls/c1-probes-lane-after-r59.txt | grep '^probe='  | cut -c1-120` vs my run, same cut: identical for all 10 lines.

## 3. Scope audit of the implementation commit

3a. `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin show --name-only --format= 472737847ff31d1255bf1a0745822a5e878e9622`  exit 0, 10 files:
    .ufo/waves/round-59/controls/c1-lane-after-r59.txt          (allowed: controls/*)
    .ufo/waves/round-59/controls/c1-probes-lane-after-r59.txt   (allowed: controls/*)
    .ufo/waves/round-59/controls/c2-lane-after-r59.txt          (allowed: controls/*)
    PROVINCE.md                                                  (allowed)
    SKILL.md                                                     (allowed)
    corpus/README.md                                             (allowed)
    corpus/SOURCES.md                                            (allowed)
    corpus/instruments/figure-audit.py                           (allowed)
    corpus/instruments/knowledge-expected.txt                    (allowed)
    corpus/knowledge/google-big-sleep-findings-tracker.md        (allowed)
    OUT-OF-SCOPE FILES: none.
    Stat: 10 files changed, 261 insertions(+), 4 deletions(-) (`git show --stat`).

## 4. Attacks on the derive gate: NEW classes (outside the recorded B1-B6 and RESIDUAL-awk-write)

Method: each derive run through the lane instrument (clone) with a fresh root and a one-figure ledger; receipts via the real gate, plus check_read_only() imported directly. Write effects checked by sha256 or marker files. Exit codes are the instrument's; these derives also end with derive-empty or other "stale" codes because they print nothing useful, but the write effect is what counts.

X1 git-show write flag (NEW). Root = git fixture (`git init -q`; toplevel asserted; one commit). Derive `git show --output=MARK-X1 HEAD`. exit 1 (derive-empty), markers=1, MARK-X1 size 275 bytes. Head `git show ` is allow-listed (figure-audit.py:48); `--output` is a diff-family option and writes the file.

X5 pipe sort -o (same family as recorded B6, confirmed in pipe-segment form). Derive `cat g.txt | sort -o MARK-X5 g.txt`. exit 1 (derive-empty), markers=1. Head `sort ` in the second segment is allow-listed.

X6 sed -n in-place (NEW). Derive `sed -n -i 's/35/36/' g.txt`. g.txt sha256 before 90d7ec0f0acef104 -> after e3b0c44298fc1c14 (zero bytes). exit 1. Head `sed -n ` (figure-audit.py:49) admits any flags after it, including -i.

X7 gawk in-place extension (NEW). Derive `awk -i inplace '{print "ZZ"}' g.txt`. g.txt before 90d7ec0f0acef104 -> after 607abb39475310a1; content "ZZ". exit 1. Head `awk ` admits gawk's -i inplace.

X8 python path traversal (NEW). Layout: $EX/x8/evil.py (outside the root; opens MARK-X8 in cwd, prints 35); root = $EX/x8/root with corpus/instruments/ created. Derive `python3 corpus/instruments/../../../evil.py`. Output: `FIG X8 recorded=35 derived=35 ok` / `FIGURE-AUDIT figures=1 ok=1 stale=0 exit=0`, exit 0, markers-in-root=1. The gate's segment_ok (figure-audit.py:131-135, prefix test `parts[1].startswith("corpus/instruments/")`) does not normalize `..`, so a script outside the root runs. (An earlier attempt with two `..` resolved to root/evil.py, exit 2; that was my probe error, superseded.)

X9 committed counter writes --out (NEW; capture-source.py is admitted as any committed corpus/instruments/*.py). Root = copy of corpus/; derive `python3 corpus/instruments/capture-source.py --id X9 --url file://<scratch>/x9-src.txt --out MARK-X9 --kind text`. exit 1 (derive-exit-1 from the instrument's own exit), markers=1, MARK-X9 11 bytes (payload written). Instrument source: capture-source.py:92 open(out,"wb").

X10 same instrument, network egress (NEW). Local server `python3 -m http.server 18477 --bind 127.0.0.1` (nohup, stopped by pkill). Direct run (not through the gate; identical admission, see 4f): `python3 corpus/instruments/capture-source.py --id X10 --url http://127.0.0.1:18477/ping.txt --out MARK-X10 --kind text` exit 0; output `X10 status=200 fetched_bytes=11 ...`; server log `"GET /ping.txt HTTP/1.1" 200`. capture-source.py:75 urlopen of an arbitrary URL. A derive therefore performs an arbitrary HTTP GET. Through the gate it is admitted (4f).

4f. check_read_only receipts (imported figure-audit.py, no execution):
    check_read_only('sed -n -i s/35/36/ g.txt') -> True
    check_read_only('awk -i inplace 1 g.txt') -> True
    check_read_only('python3 corpus/instruments/../../evil.py') -> True
    check_read_only('python3 corpus/instruments/capture-source.py --id X --url http://127.0.0.1:9/ --out MARK-X') -> True
    check_read_only('git show --output=MARK-X HEAD') -> True
    check_read_only('sort -o MARK-X g.txt') -> True
    check_read_only('grep -c 35 g.txt') -> True

Refused (receipts, not findings): X2 `cat "$(touch MARK-X2)"` exit 2 markers 0 (reason=derive-not-read-only); X3 `cat "\`touch MARK-X3\`"` exit 2 markers 0. The double-quote $( and backtick rule (split_segments, figure-audit.py:78-130, docstring at 78-84) holds.

Residual list update (text only; not a change to the frozen claims): the gate admits, in addition to the recorded residuals, (a) flag-level writes on allow-listed heads: `git show --output=`, `sed -n -i`, `awk -i inplace`, `sort -o` in a pipe segment (B6 family); (b) `..` traversal through the `python3 corpus/instruments/` head, executing a script outside the lane root (X8); (c) any committed corpus/instruments/*.py as a counter, including capture-source.py, which writes --out and performs an arbitrary HTTP GET (X9, X10). The SKILL.md registry row added by this commit (diff hunk @@ -1214,3 +1214,14 @@, the figure-audit.py row) states "reads committed bytes and its ledger; writes nothing in the lane"; X1, X5, X6, X7 and X9 falsify that sentence for the derive path. Suggested correction (text only, not made): "reads its ledger and runs read-only derives; the derive gate does not refuse flag-level writes or path traversal (see the round-59 residual list)."

Not tested here: a ledger-supplied derive that reaches the network through means other than capture-source.py; sort --compress-program execution (not triggered on small input; not probed).

## 5. Tooling
No tools installed or upgraded. Used the host's existing python3 (3.14.8), GNU bash, gawk 5.4.1, git, curl, and the python stdlib http.server (X10). pacman not run (host paused). Nothing written to ~/.local/bin or any PATH directory.

## 6. Hygiene
Writes: only this file (W/ReviewerC1.md) under the lane; all other writes under $S (scratch). No git add/commit/stash/checkout/reset against the lane (only show, rev-parse, clone --shared on the lane). No credential material read or written. Lane files, claims.json, ledger, SOURCES.md, README.md, PROVINCE.md and instruments were not modified (read-only).
Scratch removal: `rm -rf -- /fast/scratch/hyaku/kasegi-r59/ReviewerC1` run before yield; `test -e` on that path then printed "scratch removed" (no leftovers).
