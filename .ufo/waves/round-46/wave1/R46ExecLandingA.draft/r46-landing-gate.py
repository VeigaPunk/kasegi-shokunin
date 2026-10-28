#!/usr/bin/env python3
"""r46-landing-gate.py -- quiescence + report/commit-ordering gate (round 46, draft).

Closes two routed items with one read-only instrument:
  * corpus/lessons/round-45-verifier-spotcheck.md section 6 item 1 -- the round-45
    report commit a1f7761 was authored 19:30:06 -0300, before the lane commit
    2998baa (19:36:30 -0300) that the report cites as final;
  * considerthese/2026-10-26.md proposal 3 -- a quiescence gate before `complete`
    (`git status --porcelain` empty + the placeholder grep of
    corpus/instruments/r35-defect-closure.sh check_d1).

Modes
  --pre-report  --lane DIR --branch B --round N [--jj-lane PATH]
  --post-report --lane DIR --branch B --report PATH --fleet DIR [--remote-tip H]
  --selftest [--work DIR]

Reads only: it runs `git status/rev-parse/ls-remote/cat-file/merge-base/log/show`
and `jj-lane.sh state` (documented "pure git, read-only; no jj calls"). The
selftest is the only writer, and only inside a scratch fixture it creates and
removes itself (every fixture git call names -C <fixture> and asserts
`git rev-parse --show-toplevel` equals that fixture first).

Output: one `check <id> pass=0|1 read=<token>` line per check, then last
`landing-gate mode=<m> checks=<n> fail=<k> exit=0|1`. Selftest prints
`selftest cases=<N> failures=<F>` last. Exit 0 all pass, 1 any fail, 2 usage.

Check ids
  pre : tree-clean, jj-state, remote-tip, placeholder-{scorecard,log,shonen,lesson}
  post: shonen-heading, report-committed, cited-hashes, and per cited 40-hex hash
        (suffix -<first 8 hex>): resolves, ancestor, final-tip (only when the
        sentence says final lane hash/commit/tip), date-order-committer,
        date-order-author.

Deliberate points (see the Report):
  * date-order-committer is the card rule (cited committer time <= committer time
    of the fleet commit `git log -1 -- <report>`). It does NOT reproduce the
    round-45 defect (a1f7761 committer 19:37:42 > 2998baa 19:36:31): the 19:30:06
    the spot-check quotes is the AUTHOR time. date-order-author therefore checks
    cited committer time <= author time of that same fleet commit, which is the
    ordering a report written after the landing satisfies and a report written
    before it cannot.
  * placeholder tokens are the two spellings of r35 check_d1 (`filled by the L1`,
    `<LANE_HASH>`). SCORECARD.md and the lesson are scanned raw (as D1 does);
    LOG.md and SHONEN.md are scanned with inline `code spans` removed because they
    legitimately describe the tokens in prose (LOG.md:1616,1632,1655,1665,
    SHONEN.md:157 print the tokens inside backticks).
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

JJ_LANE_DEFAULT = "/home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh"
# r35-defect-closure.sh check_d1 spellings, kept split so this file never matches itself.
PH_TOKEN = "filled by the " + "L1"
LH_TOKEN = "<LANE" + "_HASH>"

HASH_RE = re.compile(r"(?<![0-9A-Fa-f])[0-9a-f]{40}(?![0-9A-Fa-f])")
KEY_RE = re.compile(r"\blanded\b|\bfinal lane hash\b|\blane commit\b", re.I)
FINAL_RE = re.compile(r"\bfinal (?:lane )?(?:hash|commit|tip)\b|\bfinal landed\b", re.I)
HEADING_RE = re.compile(r"^#{1,6}\s")
LANDED_HEADING_RE = re.compile(r"^#{1,6}\s.*\blanded\b", re.I)
SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z`*\[(])")


def git(d, *args):
    """Read-only git call; returns (rc, stdout)."""
    p = subprocess.run(["git", "-C", d, *args], capture_output=True, text=True)
    return p.returncode, p.stdout.strip()


def res(cid, ok, read):
    return (cid, 1 if ok else 0, read)


# --------------------------------------------------------------------- pre-report
def strip_code_spans(line):
    return re.sub(r"`[^`]*`", "", line)


def count_tokens(path, strip):
    ph = lh = 0
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            s = strip_code_spans(line) if strip else line
            ph += s.count(PH_TOKEN)
            lh += s.count(LH_TOKEN)
    return ph, lh


def run_pre(lane, branch, rnd, jj_lane):
    out = []
    rc, por = git(lane, "status", "--porcelain")
    n = len(por.splitlines()) if rc == 0 and por else 0
    out.append(res("tree-clean", rc == 0 and n == 0, f"porcelain-lines={n}" if rc == 0 else f"git-status-rc={rc}"))

    p = subprocess.run(["bash", jj_lane, "state", lane], capture_output=True, text=True)
    m = re.search(r"\bahead=(\d+) behind=\d+ head=\S+ tracked=(\d+) untracked=(\d+)", p.stdout)
    if p.returncode == 0 and m:
        a, t, u = (int(x) for x in m.groups())
        out.append(res("jj-state", a == 0 and t == 0 and u == 0, f"ahead={a},tracked={t},untracked={u}"))
    else:
        out.append(res("jj-state", False, f"jj-lane-state-rc={p.returncode}"))

    rc1, remote = git(lane, "ls-remote", "origin", f"refs/heads/{branch}")
    rtip = remote.split()[0] if rc1 == 0 and remote else ""
    rc2, ltip = git(lane, "rev-parse", branch)
    ok = bool(rtip) and rc2 == 0 and rtip == ltip
    out.append(res("remote-tip", ok, f"remote={rtip[:12] or 'none'},local={ltip[:12] or 'none'}"))

    files = [
        ("scorecard", "SCORECARD.md", False),
        ("log", "LOG.md", True),
        ("shonen", "SHONEN.md", True),
        ("lesson", f"corpus/lessons/round-{rnd}.md", False),
    ]
    for tag, rel, strip in files:
        path = os.path.join(lane, rel)
        if not os.path.isfile(path):
            out.append(res(f"placeholder-{tag}", False, f"missing={rel}"))
            continue
        ph, lh = count_tokens(path, strip)
        out.append(res(f"placeholder-{tag}", ph == 0 and lh == 0, f"{rel}:placeholders={ph},lane-hash-markers={lh}"))
    return out


# -------------------------------------------------------------------- post-report
def cited_hashes(text):
    """Ordered {hash: final_flag} from landed / final lane hash / lane commit sentences
    and from every line of a `Landed ...` section."""
    found = {}
    in_landed = False
    for line in text.splitlines():
        if HEADING_RE.match(line):
            in_landed = bool(LANDED_HEADING_RE.match(line))
            continue
        sentences = [line] if line.lstrip().startswith("|") else SPLIT_RE.split(line)
        for s in sentences:
            hs = HASH_RE.findall(s)
            if not hs or not (in_landed or KEY_RE.search(s)):
                continue
            for h in hs:
                found[h] = found.get(h, False) or bool(FINAL_RE.search(s))
    return found


def run_post(lane, branch, report, fleet, remote_tip_override=None):
    out = []
    path = report if os.path.isabs(report) else (
        os.path.join(fleet, report) if os.path.exists(os.path.join(fleet, report)) else os.path.abspath(report))
    try:
        text = open(path, encoding="utf-8", errors="replace").read()
    except OSError as e:
        return [res("report-readable", False, f"unreadable={e.__class__.__name__}")]
    rel = os.path.relpath(os.path.realpath(path), os.path.realpath(fleet))

    n_shonen = len(re.findall(r"(?m)^## SHONEN", text))
    out.append(res("shonen-heading", n_shonen == 1, f"count={n_shonen}"))

    rc, line = git(fleet, "log", "-1", "--format=%H %ct %cI %at %aI", "--", rel)
    f = line.split() if rc == 0 else []
    if len(f) == 5:
        fh, fct, fci, fat, fai = f
        fct, fat = int(fct), int(fat)
        out.append(res("report-committed", True, f"fleet={fh[:12]},committer={fci},author={fai}"))
    else:
        fct = fat = None
        out.append(res("report-committed", False, "report-not-in-fleet-history"))

    cited = cited_hashes(text)
    out.append(res("cited-hashes", len(cited) >= 1, f"count={len(cited)}"))

    if remote_tip_override:
        rtip, rsrc = remote_tip_override, "override"
    else:
        rc1, remote = git(lane, "ls-remote", "origin", f"refs/heads/{branch}")
        rtip, rsrc = (remote.split()[0] if rc1 == 0 and remote else ""), "ls-remote"

    for h, final in cited.items():
        k = h[:8]
        rcv, _ = git(lane, "cat-file", "-e", f"{h}^{{commit}}")
        resolved = rcv == 0
        out.append(res(f"resolves-{k}", resolved, "commit" if resolved else "unresolvable"))
        if not resolved:
            out.append(res(f"ancestor-{k}", False, "skipped-unresolved"))
            if final:
                out.append(res(f"final-tip-{k}", False, "skipped-unresolved"))
            out.append(res(f"date-order-committer-{k}", False, "skipped-unresolved"))
            out.append(res(f"date-order-author-{k}", False, "skipped-unresolved"))
            continue
        rca, _ = git(lane, "merge-base", "--is-ancestor", h, branch)
        out.append(res(f"ancestor-{k}", rca == 0, f"is-ancestor-of-{branch}={'yes' if rca == 0 else 'no'}"))
        if final:
            out.append(res(f"final-tip-{k}", bool(rtip) and rtip == h, f"{rsrc}={rtip[:12] or 'none'},cited={h[:12]}"))
        _, cts = git(lane, "log", "-1", "--format=%ct %cI", h)
        cct, cci = cts.split()
        cct = int(cct)
        if fct is None:
            out.append(res(f"date-order-committer-{k}", False, "skipped-no-report-commit"))
            out.append(res(f"date-order-author-{k}", False, "skipped-no-report-commit"))
            continue
        out.append(res(f"date-order-committer-{k}", cct <= fct, f"cited={cci},report-committer={fci}"))
        out.append(res(f"date-order-author-{k}", cct <= fat, f"cited={cci},report-author={fai}"))
    return out


def emit(mode, results):
    for cid, ok, read in results:
        print(f"check {cid} pass={ok} read={read}")
    fail = sum(1 for _, ok, _ in results if not ok)
    code = 1 if fail else 0
    print(f"landing-gate mode={mode} checks={len(results)} fail={fail} exit={code}")
    return code


# ---------------------------------------------------------------------- selftest
T0 = 1767225600  # 2026-01-01T00:00:00Z


class Fx:
    """Scratch fixture: bare origin + lane clone + fleet repo. Mutates only itself."""

    def __init__(self, scratch, name):
        self.base = tempfile.mkdtemp(prefix=name + ".", dir=scratch)
        self.tmp = self.base
        self.origin = os.path.join(self.base, "origin.git")
        self.lane = os.path.join(self.base, "lane")
        self.fleet = os.path.join(self.base, "fleet")
        for d in (self.origin, self.lane, self.fleet):
            os.mkdir(d)
        self.g(self.origin, "init", "-q", "--bare", "-b", "master", guard=False)
        self.g(self.lane, "init", "-q", "-b", "master", guard=False)
        self.g(self.lane, "remote", "add", "origin", self.origin)
        self.g(self.lane, "config", "lane.branch", "master")
        self.g(self.fleet, "init", "-q", "-b", "master", guard=False)
        self.put(self.lane, "SCORECARD.md", "# SCORECARD\n")
        self.put(self.lane, "LOG.md", "# LOG\n")
        self.put(self.lane, "SHONEN.md", "# SHONEN\n")
        self.put(self.lane, "corpus/lessons/round-46.md", "# lesson\n")
        self.commit(self.lane, "base", T0, T0, push=False)
        self.base_hash = self.head(self.lane)
        self.put(self.lane, "corpus/knowledge/x.md", "x\n")
        self.commit(self.lane, "landed", T0 + 60, T0 + 60, push=True)
        self.tip = self.head(self.lane)

    def g(self, d, *args, guard=True, date=None):
        d = os.path.realpath(d)
        env = dict(os.environ, TMPDIR=self.tmp, GIT_CONFIG_GLOBAL="/dev/null", GIT_CONFIG_SYSTEM="/dev/null",
                   GIT_AUTHOR_NAME="fx", GIT_AUTHOR_EMAIL="fx@example.invalid",
                   GIT_COMMITTER_NAME="fx", GIT_COMMITTER_EMAIL="fx@example.invalid")
        if date:
            env["GIT_AUTHOR_DATE"] = f"{date[0]} +0000"
            env["GIT_COMMITTER_DATE"] = f"{date[1]} +0000"
        if guard:
            top = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"], capture_output=True,
                                 text=True, env=env).stdout.strip()
            if os.path.realpath(top) != d:
                raise RuntimeError(f"fixture guard: toplevel {top!r} != {d!r}")
        p = subprocess.run(["git", "-C", d, *args], capture_output=True, text=True, env=env)
        if p.returncode != 0:
            raise RuntimeError(f"fixture git {args} rc={p.returncode}: {p.stderr}")
        return p.stdout.strip()

    def put(self, d, rel, text, append=False):
        p = os.path.join(d, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "a" if append else "w", encoding="utf-8") as fh:
            fh.write(text)

    def commit(self, d, msg, at, ct, push=False, paths=None):
        self.g(d, "add", "-A" if paths is None else "--", *([] if paths is None else paths))
        self.g(d, "commit", "-q", "-m", msg, date=(at, ct))
        if push:
            self.g(d, "push", "-q", "origin", "master")

    def head(self, d):
        return self.g(d, "rev-parse", "HEAD")

    def report(self, text, at, ct):
        self.put(self.fleet, ".ufo/reports/round-46/kasegi.md", text)
        self.commit(self.fleet, "report", at, ct)


def report_text(cited_line, shonen=1, extra=""):
    t = f"# Report\n\n{cited_line}\n\n{extra}"
    t += "".join("## SHONEN\n\n- [~] box\n\n" for _ in range(shonen))
    return t


def selftest(work):
    base_scratch = work or os.path.join(os.environ.get("HYAKU_SCRATCH", "/fast/scratch/hyaku"),
                                        "kasegi-r46", "R46ExecLandingA")
    os.makedirs(base_scratch, exist_ok=True)
    root = tempfile.mkdtemp(prefix="landing-selftest.", dir=base_scratch)
    cases = []  # (name, mode, expected-failing-normalised-ids, results)
    norm = lambda cid: re.sub(r"-[0-9a-f]{8}$", "", cid)
    try:
        def pre(name, fx, expect, rnd=46):
            r = run_pre(fx.lane, "master", rnd, JJ_LANE_DEFAULT)
            cases.append((name, "pre", sorted(set(expect)), r))

        def post(name, fx, expect, tip=None):
            r = run_post(fx.lane, "master", ".ufo/reports/round-46/kasegi.md", fx.fleet, tip)
            cases.append((name, "post", sorted(set(expect)), r))

        good = lambda fx: report_text(f"Final lane hash `{fx.tip}` (landed, remote-verified).",
                                      extra=f"Round base `{'b' * 40}`.\n\n")

        # ---- pre-report
        fx = Fx(root, "pre-clean"); pre("pre-clean-positive", fx, [])
        fx = Fx(root, "pre-dirty"); fx.put(fx.lane, "SCORECARD.md", "edit\n", append=True)
        pre("pre-dirty-tree", fx, ["tree-clean", "jj-state"])
        fx = Fx(root, "pre-untracked"); fx.put(fx.lane, "stray.txt", "x\n")
        pre("pre-untracked-file", fx, ["tree-clean", "jj-state"])
        fx = Fx(root, "pre-ahead"); fx.put(fx.lane, "a.md", "a\n"); fx.commit(fx.lane, "local", T0 + 90, T0 + 90)
        pre("pre-ahead-of-remote", fx, ["jj-state", "remote-tip"])
        fx = Fx(root, "pre-ph"); fx.put(fx.lane, "SCORECARD.md", f"**Final lane commit: {PH_TOKEN} in the closing commit.**\n", append=True)
        fx.commit(fx.lane, "ph", T0 + 90, T0 + 90, push=True); pre("pre-placeholder-scorecard", fx, ["placeholder-scorecard"])
        fx = Fx(root, "pre-lh"); fx.put(fx.lane, "corpus/lessons/round-46.md", f"Final: {LH_TOKEN}\n", append=True)
        fx.commit(fx.lane, "lh", T0 + 90, T0 + 90, push=True); pre("pre-lane-hash-marker-lesson", fx, ["placeholder-lesson"])
        fx = Fx(root, "pre-logprose"); fx.put(fx.lane, "LOG.md", f"prose: the `{LH_TOKEN}` marker and `{PH_TOKEN}` were cleared\n", append=True)
        fx.commit(fx.lane, "prose", T0 + 90, T0 + 90, push=True); pre("pre-backticked-token-in-LOG-is-prose", fx, [])
        fx = Fx(root, "pre-logbare"); fx.put(fx.lane, "LOG.md", f"landed hash: {LH_TOKEN}\n", append=True)
        fx.commit(fx.lane, "bare", T0 + 90, T0 + 90, push=True); pre("pre-bare-token-in-LOG", fx, ["placeholder-log"])
        fx = Fx(root, "pre-scbt"); fx.put(fx.lane, "SCORECARD.md", f"`{LH_TOKEN}`\n", append=True)
        fx.commit(fx.lane, "bt", T0 + 90, T0 + 90, push=True); pre("pre-backticked-token-in-SCORECARD-still-fails", fx, ["placeholder-scorecard"])
        fx = Fx(root, "pre-nolesson"); pre("pre-wrong-round-lesson-missing", fx, ["placeholder-lesson"], rnd=99)

        # ---- post-report
        fx = Fx(root, "post-clean"); fx.report(good(fx), T0 + 600, T0 + 600); post("post-clean-positive", fx, [])
        fx = Fx(root, "post-unres")
        fx.report(report_text(f"Lane commit `{'a' * 40}` landed. Final lane hash `{fx.tip}` (landed)."), T0 + 600, T0 + 600)
        post("post-unresolvable-hash", fx, ["resolves", "ancestor", "date-order-committer", "date-order-author"])
        fx = Fx(root, "post-side")
        fx.g(fx.lane, "checkout", "-q", "-b", "side"); fx.put(fx.lane, "s.md", "s\n"); fx.commit(fx.lane, "side", T0 + 30, T0 + 30)
        side = fx.head(fx.lane); fx.g(fx.lane, "checkout", "-q", "master")
        fx.report(report_text(f"Lane commit `{side}` landed. Final lane hash `{fx.tip}` (landed)."), T0 + 600, T0 + 600)
        post("post-non-ancestor-hash", fx, ["ancestor"])
        fx = Fx(root, "post-inv"); fx.report(good(fx), T0 + 10, T0 + 10)
        post("post-date-inversion-committer-and-author", fx, ["date-order-committer", "date-order-author"])
        fx = Fx(root, "post-auth"); fx.report(good(fx), T0 + 10, T0 + 600)
        post("post-round45-shape-author-before-cited-committer-after", fx, ["date-order-author"])
        fx = Fx(root, "post-2sh"); fx.report(report_text(f"Final lane hash `{fx.tip}` (landed).", shonen=2), T0 + 600, T0 + 600)
        post("post-two-SHONEN-headings", fx, ["shonen-heading"])
        fx = Fx(root, "post-nohash"); fx.report(report_text("Landed the work; no hash cited."), T0 + 600, T0 + 600)
        post("post-no-cited-hash", fx, ["cited-hashes"])
        fx = Fx(root, "post-notfinal"); fx.report(report_text(f"Final lane hash `{fx.base_hash}` (landed)."), T0 + 600, T0 + 600)
        post("post-final-hash-not-remote-tip", fx, ["final-tip"])
        fx = Fx(root, "post-uncommitted"); fx.put(fx.fleet, ".ufo/reports/round-46/kasegi.md", good(fx))
        post("post-report-not-committed", fx, ["report-committed", "date-order-committer", "date-order-author"])
        fx = Fx(root, "post-tipov"); fx.report(report_text(f"Final lane hash `{fx.base_hash}` (landed)."), T0 + 600, T0 + 600)
        post("post-replay-override-matches", fx, [], tip=fx.base_hash)

        failures = 0
        for name, mode, expect, r in cases:
            got = sorted({norm(cid) for cid, ok, _ in r if not ok})
            ok = got == expect
            failures += 0 if ok else 1
            print(f"selftest case={name} mode={mode} checks={len(r)} expect_fail={','.join(expect) or '-'} "
                  f"got_fail={','.join(got) or '-'} ok={1 if ok else 0}")
        n = len(cases)
        # do-nothing controls: a gate that passes everything / fails everything must disagree with the suite
        always_pass = sum(1 for _, _, e, _ in cases if not e)
        always_fail = sum(1 for _, _, e, _ in cases if e)
        print(f"selftest control=always-pass agrees={always_pass}/{n} control=always-fail agrees={always_fail}/{n}")
        if always_pass == n or always_fail == n:
            failures += 1
        print(f"selftest cases={n} failures={failures}")
        return 0 if failures == 0 else 1
    finally:
        shutil.rmtree(root, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser(add_help=True)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--pre-report", action="store_true")
    g.add_argument("--post-report", action="store_true")
    g.add_argument("--selftest", action="store_true")
    ap.add_argument("--lane")
    ap.add_argument("--branch")
    ap.add_argument("--round", type=int)
    ap.add_argument("--report")
    ap.add_argument("--fleet")
    ap.add_argument("--jj-lane", default=JJ_LANE_DEFAULT)
    ap.add_argument("--remote-tip", help="historical replay only: compare final-hash sentences to this hash instead of ls-remote")
    ap.add_argument("--work")
    a = ap.parse_args()
    if a.selftest:
        return selftest(a.work)
    if a.pre_report:
        if not (a.lane and a.branch and a.round is not None):
            print("usage: --pre-report --lane DIR --branch B --round N", file=sys.stderr)
            return 2
        return emit("pre-report", run_pre(a.lane, a.branch, a.round, a.jj_lane))
    if not (a.lane and a.branch and a.report and a.fleet):
        print("usage: --post-report --lane DIR --branch B --report PATH --fleet DIR", file=sys.stderr)
        return 2
    return emit("post-report", run_post(a.lane, a.branch, a.report, a.fleet, a.remote_tip))


if __name__ == "__main__":
    sys.exit(main())
