#!/usr/bin/env python3
"""r46-landing-gate.py -- quiescence + landing-order gate for a kasegi round (stdlib, reads only).

Closes two routed items:
  * round-45 verifier spot-check section 6 item 1 (`corpus/lessons/round-45-verifier-spotcheck.md`):
    the report commit a1f7761 (author 19:30:06) names, as final, the lane commit 2998baa
    (19:36:31) that did not yet exist when the report was written;
  * `considerthese/2026-10-26.md` proposal 3: a quiescence gate before `complete`
    (`git status --porcelain` empty + the placeholder grep of
    `corpus/instruments/r35-defect-closure.sh` D1).

Modes (exactly one):
  --pre-report  --lane DIR --branch master --round N [--jj-lane PATH]
      tree-clean     `git status --porcelain` of DIR is empty
      jj-state       `jj-lane.sh state DIR` reports ahead=0 tracked=0 untracked=0
      remote-tip     `git ls-remote origin refs/heads/<branch>` == `git rev-parse <branch>`
      placeholders   0 `filled by the L1` / `<LANE_HASH>` tokens in SCORECARD.md LOG.md
                     SHONEN.md corpus/lessons/round-<N>.md (SCORECARD.md strict, exactly the
                     D1 grep; the other three ignore a token that sits inside an inline
                     backtick span, because LOG.md/SHONEN.md quote the old spellings)
  --post-report --lane DIR --branch master --report PATH --fleet DIR [--tip REV]
      report-readable  the report file exists (PATH is relative to the fleet when not absolute)
      cited-hashes     the report cites >=1 40-hex hash in a lane-commit sentence (a sentence
                       containing `landed`, `final lane hash` or `lane commit`, or a table cell
                       under a `Commit`/`Hash` column header)
      resolves         every cited hash is a commit in the lane
      ancestor         every cited hash is an ancestor of <branch>
      final-is-tip     >=1 cited sentence says `final`, and each such hash == the
                       `ls-remote origin refs/heads/<branch>` tip (or --tip REV for a replay)
      date-order       every cited hash's committer time <= committer time of the fleet commit
                       that ADDS the report (`git log --diff-filter=A` in the fleet)
      date-order-author  every cited hash's committer time <= AUTHOR time of that same fleet
                       commit.  The committer time can be moved later by an amend/rebase/jj
                       rewrite; the author time is when the report text was written, and it is
                       the clock the round-45 defect inverted.
      shonen-heading   exactly one line matches `^## SHONEN`
  --selftest [--work DIR]   fixture lane + fleet; prints `selftest cases=N failures=F`

The last stdout line of a gate run is
  landing-gate mode=<m> checks=<n> fail=<k> exit=0|1
preceded by one `check <id> pass=0|1 read=<token>` line each.  Git is only ever called
through git(), which allows read-only subcommands; fixture construction (selftest only,
fixture directories only) goes through fx().
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

JJ_LANE_DEFAULT = "/home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh"
SCRATCH_DEFAULT = os.path.join(os.environ.get("HYAKU_SCRATCH", "/fast/scratch/hyaku"),
                               "kasegi-r46", "R46ExecLandingB")
READ_ONLY_GIT = {"status", "rev-parse", "ls-remote", "log", "merge-base", "cat-file", "show", "rev-list"}
# Spelled so this file never matches its own placeholder grep (same trick as r35 D1).
PLACEHOLDERS = ("filled by the " + "L1", "<LANE" + "_HASH>")
HEX40 = re.compile(r"(?<![0-9a-fA-F])[0-9a-f]{40}(?![0-9a-fA-F])")
TRIGGER = re.compile(r"landed|final lane hash|lane commit", re.I)
FINAL = re.compile(r"\bfinal\b", re.I)
COLHDR = re.compile(r"commit|hash", re.I)
SENT_SPLIT = re.compile(r"(?<=[.;!?])\s+")
TABLE_SEP = re.compile(r"^\|[\s:|-]+\|?$")


def tok(s):
    return re.sub(r"\s+", "_", str(s))


def git(repo, *args, timeout=60):
    """Read-only git. Anything outside READ_ONLY_GIT is a bug in this file, not a result."""
    if not args or args[0] not in READ_ONLY_GIT:
        raise RuntimeError("landing-gate: refusing non-read-only git subcommand %r" % (args[:1],))
    env = dict(os.environ, GIT_TERMINAL_PROMPT="0", LC_ALL="C")
    try:
        p = subprocess.run(["git", "--no-optional-locks", "-C", repo, *args], capture_output=True,
                           text=True, timeout=timeout, env=env)
    except (subprocess.TimeoutExpired, OSError) as e:
        return 99, "", str(e)
    return p.returncode, p.stdout, p.stderr


def ls_remote_tip(lane, branch):
    rc, out, _ = git(lane, "ls-remote", "origin", "refs/heads/" + branch)
    if rc != 0:
        return None
    for ln in out.splitlines():
        f = ln.split()
        if len(f) == 2 and f[1] == "refs/heads/" + branch and HEX40.fullmatch(f[0]):
            return f[0]
    return None


def short(h):
    return (h or "none")[:12]


# --------------------------------------------------------------------------- pre-report
def count_placeholders(text, strict):
    n = 0
    for line in text.splitlines():
        if not strict:
            line = re.sub(r"`[^`\n]*`", "", line)
        n += sum(line.count(p) for p in PLACEHOLDERS)
    return n


def pre_report(lane, branch, rnd, jj_lane):
    checks = []
    rc, out, _ = git(lane, "status", "--porcelain")
    n = len([x for x in out.splitlines() if x.strip()])
    checks.append(("tree-clean", rc == 0 and n == 0, "porcelain-lines=%d" % n if rc == 0 else "git-status-rc=%d" % rc))

    try:
        p = subprocess.run(["bash", jj_lane, "state", lane], capture_output=True, text=True, timeout=60)
        m = re.search(r"\bahead=(\d+)\b.*\btracked=(\d+)\b.*\buntracked=(\d+)\b", p.stdout)
        if p.returncode == 0 and m:
            a, t, u = (int(x) for x in m.groups())
            checks.append(("jj-state", a == 0 and t == 0 and u == 0, "ahead=%d,tracked=%d,untracked=%d" % (a, t, u)))
        else:
            checks.append(("jj-state", False, "jj-lane-rc=%d,unparsed" % p.returncode))
    except (subprocess.TimeoutExpired, OSError) as e:
        checks.append(("jj-state", False, "jj-lane-error=" + tok(type(e).__name__)))

    remote = ls_remote_tip(lane, branch)
    rc, out, _ = git(lane, "rev-parse", "--verify", "-q", "refs/heads/" + branch)
    local = out.strip() if rc == 0 else None
    checks.append(("remote-tip", bool(remote) and remote == local, "remote=%s,local=%s" % (short(remote), short(local))))

    reads, ok = [], True
    for rel, strict in (("SCORECARD.md", True), ("LOG.md", False), ("SHONEN.md", False),
                        ("corpus/lessons/round-%s.md" % rnd, False)):
        try:
            with open(os.path.join(lane, rel), encoding="utf-8", errors="replace") as fh:
                c = count_placeholders(fh.read(), strict)
        except OSError:
            reads.append("%s=missing" % rel)
            ok = False
            continue
        reads.append("%s=%d" % (rel, c))
        ok = ok and c == 0
    checks.append(("placeholders", ok, ",".join(reads)))
    return checks


# --------------------------------------------------------------------------- post-report
def report_blocks(text):
    """Yield ('p', paragraph) and ('row', (header_cells, cells)) blocks of a markdown report."""
    out, cur, hdr = [], [], None
    lines = text.splitlines()

    def flush():
        if cur:
            out.append(("p", " ".join(cur)))
            cur.clear()

    for i, raw in enumerate(lines):
        s = raw.strip()
        if not s:
            flush()
            continue
        if s.startswith("|"):
            flush()
            if TABLE_SEP.match(s):
                continue
            cells = [c.strip() for c in s.strip("|").split("|")]
            nxt = lines[i + 1].strip() if i + 1 < len(lines) else ""
            if TABLE_SEP.match(nxt):
                hdr = cells
                continue
            out.append(("row", (hdr or [], cells)))
            continue
        hdr = None
        if re.match(r"^(#{1,6}\s|[-*+]\s|\d+[.)]\s)", s):
            flush()
        cur.append(s)
    flush()
    return out


def cited_hashes(text):
    """{hash: is_final} for every 40-hex hash in a lane-commit sentence / Commit-column cell."""
    cites = {}

    def add(h, fin):
        cites[h] = cites.get(h, False) or fin

    for kind, payload in report_blocks(text):
        if kind == "p":
            for sent in SENT_SPLIT.split(payload):
                if TRIGGER.search(sent):
                    for h in HEX40.findall(sent):
                        add(h, bool(FINAL.search(sent)))
        else:
            hdr, cells = payload
            for i, c in enumerate(cells):
                if TRIGGER.search(c) or (i < len(hdr) and COLHDR.search(hdr[i])):
                    for h in HEX40.findall(c):
                        add(h, bool(FINAL.search(c)))
    return cites


def post_report(lane, branch, report, fleet, tip_override=None):
    checks = []
    path = report if os.path.isabs(report) else os.path.join(fleet, report)
    rel = os.path.relpath(os.path.realpath(path), os.path.realpath(fleet))
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            text = fh.read()
        checks.append(("report-readable", True, "bytes=%d" % len(text.encode("utf-8"))))
    except OSError:
        text = ""
        checks.append(("report-readable", False, "missing=" + tok(rel)))

    cites = cited_hashes(text)
    checks.append(("cited-hashes", len(cites) >= 1, "n=%d,final=%d" % (len(cites), sum(cites.values()))))
    none = "no-cited-hashes"

    resolved = {}
    for h in cites:
        rc, _, _ = git(lane, "cat-file", "-e", h + "^{commit}")
        resolved[h] = rc == 0
    bad = [short(h) for h in cites if not resolved[h]]
    checks.append(("resolves", bool(cites) and not bad, "unresolved=%s" % (",".join(bad) or "0") if cites else none))

    bad = []
    for h in cites:
        rc, _, _ = git(lane, "merge-base", "--is-ancestor", h, "refs/heads/" + branch)
        if not (resolved[h] and rc == 0):
            bad.append(short(h))
    checks.append(("ancestor", bool(cites) and not bad, "non-ancestor=%s" % (",".join(bad) or "0") if cites else none))

    finals = [h for h, f in cites.items() if f]
    if tip_override:
        rc, out, _ = git(lane, "rev-parse", "--verify", "-q", tip_override + "^{commit}")
        tip, src = (out.strip() if rc == 0 else None), "override"
    else:
        tip, src = ls_remote_tip(lane, branch), "ls-remote"
    bad = [short(h) for h in finals if h != tip]
    checks.append(("final-is-tip", bool(finals) and tip is not None and not bad,
                   ("final-not-tip=%s,tip=%s(%s)" % (",".join(bad) or "0", short(tip), src)) if finals
                   else ("final-sentences=0" if cites else none)))

    rc, out, _ = git(fleet, "log", "--diff-filter=A", "--format=%ct %cI %at %aI", "--", rel)
    rows = [ln.split() for ln in out.splitlines() if ln.strip()]
    add = rows[-1] if rc == 0 and rows and len(rows[-1]) == 4 else None
    if not add:
        for cid in ("date-order", "date-order-author"):
            checks.append((cid, False, "report-not-added-in-fleet=" + tok(rel)))
    else:
        rct, rci, rat, rai = int(add[0]), add[1], int(add[2]), add[3]
        worst, worst_ct, worst_ci, unreadable = None, -1, "", []
        for h in cites:
            rc, out, _ = git(lane, "log", "-1", "--format=%ct %cI", h)
            f = out.split()
            if rc != 0 or len(f) != 2:
                unreadable.append(short(h))
                continue
            if int(f[0]) > worst_ct:
                worst, worst_ct, worst_ci = h, int(f[0]), f[1]
        for cid, lim, lim_iso, lab in (("date-order", rct, rci, "report-commit-committer"),
                                       ("date-order-author", rat, rai, "report-commit-author")):
            if not cites:
                checks.append((cid, False, none))
                continue
            ok = not unreadable and worst_ct <= lim
            checks.append((cid, ok, "latest-cited=%s@%s,%s=%s%s" % (
                short(worst), worst_ci or "none", lab, lim_iso,
                ",unreadable=" + ",".join(unreadable) if unreadable else "")))

    n = len(re.findall(r"(?m)^## SHONEN", text))
    checks.append(("shonen-heading", n == 1, "count=%d" % n))
    return checks


# --------------------------------------------------------------------------- output
def emit(mode, checks):
    for cid, ok, rd in checks:
        print("check %s pass=%d read=%s" % (cid, 1 if ok else 0, tok(rd)))
    fail = sum(1 for c in checks if not c[1])
    code = 1 if fail else 0
    print("landing-gate mode=%s checks=%d fail=%d exit=%d" % (mode, len(checks), fail, code))
    return code


# --------------------------------------------------------------------------- selftest fixtures
T0 = 1_700_000_000


def fx(repo, *args, at=None):
    """Mutating git on a FIXTURE only; asserts the toplevel is the fixture dir first."""
    top = subprocess.run(["git", "-C", repo, "rev-parse", "--show-toplevel"], capture_output=True, text=True)
    if top.returncode != 0 or os.path.realpath(top.stdout.strip()) != os.path.realpath(repo):
        raise RuntimeError("fixture toplevel mismatch for %s: %r" % (repo, top.stdout))
    env = dict(os.environ)
    if at:
        env["GIT_AUTHOR_DATE"] = "%d +0000" % at[0]
        env["GIT_COMMITTER_DATE"] = "%d +0000" % at[1]
    p = subprocess.run(["git", "-c", "user.name=fx", "-c", "user.email=fx@example.invalid",
                        "-c", "commit.gpgsign=false", "-C", repo, *args],
                       capture_output=True, text=True, env=env)
    if p.returncode != 0:
        raise RuntimeError("fixture git %s failed: %s" % (args, p.stderr))
    return p.stdout.strip()


def fx_init(path, bare=False):
    os.makedirs(path)
    subprocess.run(["git", "init", "-q", "-b", "master"] + (["--bare"] if bare else []) + [path],
                   check=True, capture_output=True)
    if not bare:
        fx(path, "status", "--porcelain")


def put(repo, rel, text, append=False):
    p = os.path.join(repo, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "a" if append else "w", encoding="utf-8") as fh:
        fh.write(text)


def lane_commit(ctx, at, note, push=True):
    put(ctx["lane"], "LOG.md", note + "\n", append=True)
    fx(ctx["lane"], "add", "-A")
    fx(ctx["lane"], "commit", "-q", "-m", note, at=(at, at))
    if push:
        fx(ctx["lane"], "push", "-q", "origin", "master")
    return fx(ctx["lane"], "rev-parse", "HEAD")


def make_ctx(work):
    root = tempfile.mkdtemp(dir=work)
    ctx = {"root": root, "origin": os.path.join(root, "origin.git"),
           "lane": os.path.join(root, "lane"), "fleet": os.path.join(root, "fleet")}
    fx_init(ctx["origin"], bare=True)
    fx_init(ctx["lane"])
    for rel in ("SCORECARD.md", "LOG.md", "SHONEN.md", "corpus/lessons/round-46.md"):
        put(ctx["lane"], rel, "# %s\nclean text\n" % rel)
    fx(ctx["lane"], "add", "-A")
    fx(ctx["lane"], "commit", "-q", "-m", "base", at=(T0, T0))
    ctx["c1"] = fx(ctx["lane"], "rev-parse", "HEAD")
    fx(ctx["lane"], "remote", "add", "origin", ctx["origin"])
    fx(ctx["lane"], "push", "-q", "origin", "master")
    ctx["c2"] = lane_commit(ctx, T0 + 100, "final landing")
    fx_init(ctx["fleet"])
    ctx["rel"] = ".ufo/reports/round-46/kasegi.md"
    return ctx


def report_text(final, landed=(), shonen=1, table=(), extra=""):
    t = ["# Round 46 report", "", "Lane repo, branch `master`, final lane hash `%s` (`git ls-remote` prints it)." % final, ""]
    for h in landed:
        t += ["Lane commit `%s` landed earlier." % h, ""]
    if table:
        t += ["| Change | Commit |", "|---|---|"] + ["| row | `%s` |" % h for h in table] + [""]
    t += [extra, ""] if extra else []
    t += ["## SHONEN", "- [~] box"] * shonen
    return "\n".join(t) + "\n"


def commit_report(ctx, text, author=None, committer=None, commit=True):
    put(ctx["fleet"], ctx["rel"], text)
    if commit:
        fx(ctx["fleet"], "add", "-A")
        a, c = author or T0 + 200, committer or T0 + 210
        fx(ctx["fleet"], "commit", "-q", "-m", "report", at=(a, c))


def new_clone_push(ctx, at):
    other = os.path.join(ctx["root"], "other")
    subprocess.run(["git", "clone", "-q", ctx["origin"], other], check=True, capture_output=True)
    put(other, "LOG.md", "other writer\n", append=True)
    fx(other, "add", "-A")
    fx(other, "commit", "-q", "-m", "other", at=(at, at))
    fx(other, "push", "-q", "origin", "master")


def side_commit(ctx):
    fx(ctx["lane"], "checkout", "-q", "-b", "side", ctx["c1"])
    put(ctx["lane"], "side.txt", "side\n")
    fx(ctx["lane"], "add", "-A")
    fx(ctx["lane"], "commit", "-q", "-m", "side", at=(T0 + 50, T0 + 50))
    h = fx(ctx["lane"], "rev-parse", "HEAD")
    fx(ctx["lane"], "checkout", "-q", "master")
    return h


def pre_case(setup, expect):
    def run(ctx, jj):
        setup(ctx)
        return pre_report(ctx["lane"], "master", "46", jj), set(expect)
    return run


def post_case(setup, expect, tip=None):
    def run(ctx, jj):
        setup(ctx)
        t = tip(ctx) if tip else None
        return post_report(ctx["lane"], "master", ctx["rel"], ctx["fleet"], t), set(expect)
    return run


def commit_all(ctx, msg, push=True):
    fx(ctx["lane"], "add", "-A")
    fx(ctx["lane"], "commit", "-q", "-m", msg, at=(T0 + 150, T0 + 150))
    if push:
        fx(ctx["lane"], "push", "-q", "origin", "master")


def s_clean(ctx):
    pass


def s_dirty(ctx):
    put(ctx["lane"], "LOG.md", "uncommitted edit\n", append=True)


def s_untracked(ctx):
    put(ctx["lane"], "stray.txt", "x\n")


def s_ahead(ctx):
    lane_commit(ctx, T0 + 150, "unpushed", push=False)


def s_ph_score(ctx):
    put(ctx["lane"], "SCORECARD.md", "**Final lane commit: %s in the closing commit.**\n" % PLACEHOLDERS[0], append=True)
    commit_all(ctx, "ph")


def s_ph_log_bare(ctx):
    put(ctx["lane"], "LOG.md", "Final lane commit: %s\n" % PLACEHOLDERS[1], append=True)
    commit_all(ctx, "ph")


def s_ph_lesson(ctx):
    put(ctx["lane"], "corpus/lessons/round-46.md", "hash %s\n" % PLACEHOLDERS[1], append=True)
    commit_all(ctx, "ph")


def s_quote_log(ctx):
    put(ctx["lane"], "LOG.md", "the round-33 spelling was `%s` and `%s`\n" % PLACEHOLDERS, append=True)
    commit_all(ctx, "quote")


def s_quote_score(ctx):
    put(ctx["lane"], "SCORECARD.md", "quoted `%s` here\n" % PLACEHOLDERS[1], append=True)
    commit_all(ctx, "quote")


def s_lesson_missing(ctx):
    fx(ctx["lane"], "rm", "-q", "corpus/lessons/round-46.md")
    commit_all(ctx, "rm")


def s_remote_moved(ctx):
    new_clone_push(ctx, T0 + 160)


def s_nolane(ctx):
    ctx["lane"] = os.path.join(ctx["root"], "does-not-exist")


def s_post_clean(ctx):
    commit_report(ctx, report_text(ctx["c2"], [ctx["c1"]]))


def s_post_nohash(ctx):
    commit_report(ctx, "# Report\n\nNothing landed here.\n\n## SHONEN\n- [~] box\n")


def s_post_unresolvable(ctx):
    commit_report(ctx, report_text(ctx["c2"], ["b" * 40]))


def s_post_nonancestor(ctx):
    commit_report(ctx, report_text(ctx["c2"], [side_commit(ctx)]))


def s_post_table_nonancestor(ctx):
    commit_report(ctx, report_text(ctx["c2"], table=[side_commit(ctx)]))


def s_post_date_inversion(ctx):
    c3 = lane_commit(ctx, T0 + 500, "late lane commit")
    commit_report(ctx, report_text(c3), author=T0 + 200, committer=T0 + 210)


def s_post_author_inversion(ctx):  # the round-45 shape: committer time moved later by a rewrite
    commit_report(ctx, report_text(ctx["c2"]), author=T0 + 90, committer=T0 + 210)


def s_post_two_shonen(ctx):
    commit_report(ctx, report_text(ctx["c2"], shonen=2))


def s_post_zero_shonen(ctx):
    commit_report(ctx, report_text(ctx["c2"], shonen=0))


def s_post_final_not_tip(ctx):
    commit_report(ctx, report_text(ctx["c1"]))


def s_post_no_final(ctx):
    commit_report(ctx, "# Report\n\nLane commit `%s` landed.\n\n## SHONEN\n- [~] box\n" % ctx["c2"])


def s_post_untracked_report(ctx):
    commit_report(ctx, report_text(ctx["c2"]), commit=False)


def s_post_tip_moved(ctx):
    commit_report(ctx, report_text(ctx["c2"]))
    lane_commit(ctx, T0 + 300, "moved on after the report")


def s_post_missing_report(ctx):
    pass


ALL_POST = {"report-readable", "cited-hashes", "resolves", "ancestor", "final-is-tip",
            "date-order", "date-order-author", "shonen-heading"}

CASES = [
    ("pre-clean-positive", pre_case(s_clean, [])),
    ("pre-dirty-tracked-file", pre_case(s_dirty, ["tree-clean", "jj-state"])),
    ("pre-untracked-file", pre_case(s_untracked, ["tree-clean", "jj-state"])),
    ("pre-ahead-of-remote", pre_case(s_ahead, ["jj-state", "remote-tip"])),
    ("pre-remote-moved-by-other-writer", pre_case(s_remote_moved, ["remote-tip"])),
    ("pre-placeholder-filled-by-L1-scorecard", pre_case(s_ph_score, ["placeholders"])),
    ("pre-placeholder-lane-hash-log-bare", pre_case(s_ph_log_bare, ["placeholders"])),
    ("pre-placeholder-lane-hash-lesson", pre_case(s_ph_lesson, ["placeholders"])),
    ("pre-backticked-quote-in-log-exempt", pre_case(s_quote_log, [])),
    ("pre-backticked-quote-in-scorecard-strict", pre_case(s_quote_score, ["placeholders"])),
    ("pre-round-lesson-missing", pre_case(s_lesson_missing, ["placeholders"])),
    ("pre-do-nothing-control-no-lane", pre_case(s_nolane, ["tree-clean", "jj-state", "remote-tip", "placeholders"])),
    ("post-clean-positive", post_case(s_post_clean, [])),
    ("post-report-with-no-cited-hash", post_case(s_post_nohash, ["cited-hashes", "resolves", "ancestor", "final-is-tip",
                                                                  "date-order", "date-order-author"])),
    ("post-unresolvable-hash", post_case(s_post_unresolvable, ["resolves", "ancestor", "date-order", "date-order-author"])),
    ("post-non-ancestor-hash", post_case(s_post_nonancestor, ["ancestor"])),
    ("post-table-commit-column-non-ancestor", post_case(s_post_table_nonancestor, ["ancestor"])),
    ("post-date-inversion-committer-and-author", post_case(s_post_date_inversion, ["date-order", "date-order-author"])),
    ("post-date-inversion-author-only-round45-shape", post_case(s_post_author_inversion, ["date-order-author"])),
    ("post-two-shonen-headings", post_case(s_post_two_shonen, ["shonen-heading"])),
    ("post-zero-shonen-headings", post_case(s_post_zero_shonen, ["shonen-heading"])),
    ("post-final-hash-not-tip", post_case(s_post_final_not_tip, ["final-is-tip"])),
    ("post-no-final-sentence-fails-closed", post_case(s_post_no_final, ["final-is-tip"])),
    ("post-report-untracked-in-fleet", post_case(s_post_untracked_report, ["date-order", "date-order-author"])),
    ("post-tip-moved-after-report-live-tip", post_case(s_post_tip_moved, ["final-is-tip"])),
    ("post-tip-moved-after-report-replay-override", post_case(s_post_tip_moved, [], tip=lambda c: c["c2"])),
    ("post-do-nothing-control-missing-report", post_case(s_post_missing_report, ALL_POST)),
]


def selftest(work, jj):
    work = work or SCRATCH_DEFAULT
    os.makedirs(work, exist_ok=True)
    fails = 0
    mine = tempfile.mkdtemp(dir=work)
    os.environ.update(GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_NOSYSTEM="1", TMPDIR=mine)
    try:
        # read-only guard: the gate's git() must refuse a mutating subcommand
        try:
            git(mine, "commit", "-m", "x")
            guard = False
        except RuntimeError:
            guard = True
        print("selftest case=readonly-guard-refuses-commit expect=refuse got=%s verdict=%s"
              % ("refuse" if guard else "ran", "pass" if guard else "fail"))
        fails += 0 if guard else 1
        n = 1
        for name, fn in CASES:
            n += 1
            ctx = make_ctx(mine)
            try:
                checks, expect = fn(ctx, jj)
            except Exception as e:  # a fixture bug is a failure, never a skip
                print("selftest case=%s verdict=fail error=%s" % (name, tok(e)))
                fails += 1
                continue
            got = {c[0] for c in checks if not c[1]}
            ok = got == expect
            fails += 0 if ok else 1
            print("selftest case=%s expect=%s got=%s verdict=%s"
                  % (name, ",".join(sorted(expect)) or "-", ",".join(sorted(got)) or "-", "pass" if ok else "fail"))
        # CLI end-to-end: last-line format and exit codes on a positive and a failing fixture
        for name, setup, want_exit, want_fail in (("cli-positive", s_post_clean, 0, 0),
                                                   ("cli-two-shonen", s_post_two_shonen, 1, 1)):
            n += 1
            ctx = make_ctx(mine)
            setup(ctx)
            p = subprocess.run([sys.executable, os.path.abspath(__file__), "--post-report", "--lane", ctx["lane"],
                                "--branch", "master", "--report", ctx["rel"], "--fleet", ctx["fleet"]],
                               capture_output=True, text=True)
            last = p.stdout.rstrip("\n").split("\n")[-1]
            ok = (p.returncode == want_exit
                  and last == "landing-gate mode=post-report checks=8 fail=%d exit=%d" % (want_fail, want_exit))
            fails += 0 if ok else 1
            print("selftest case=%s exit=%d last=%s verdict=%s" % (name, p.returncode, tok(last), "pass" if ok else "fail"))
        print("selftest cases=%d failures=%d" % (n, fails))
    finally:
        shutil.rmtree(mine, ignore_errors=True)
    return 1 if fails else 0


# --------------------------------------------------------------------------- main
def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--pre-report", action="store_true")
    g.add_argument("--post-report", action="store_true")
    g.add_argument("--selftest", action="store_true")
    ap.add_argument("--lane")
    ap.add_argument("--branch", default="master")
    ap.add_argument("--round")
    ap.add_argument("--report")
    ap.add_argument("--fleet")
    ap.add_argument("--tip", help="replay only: treat REV as the remote tip for final-is-tip")
    ap.add_argument("--jj-lane", default=JJ_LANE_DEFAULT)
    ap.add_argument("--work")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest(a.work, a.jj_lane)
    if a.pre_report:
        if not (a.lane and a.round):
            ap.error("--pre-report needs --lane and --round")
        return emit("pre-report", pre_report(a.lane, a.branch, a.round, a.jj_lane))
    if not (a.lane and a.report and a.fleet):
        ap.error("--post-report needs --lane, --report and --fleet")
    return emit("post-report", post_report(a.lane, a.branch, a.report, a.fleet, a.tip))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
