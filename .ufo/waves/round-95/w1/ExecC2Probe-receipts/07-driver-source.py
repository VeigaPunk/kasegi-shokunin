#!/usr/bin/env python3
"""ExecC2Probe: independent fixture-repo probe of the round-95 C2 scanner.

Builds a fresh throwaway git fixture repo (never the lane's fixtures), runs the
landed C2 instrument and the round-94 base instrument with --files, and diffs
observed (file, shape) sets against sets derived by hand from the frozen
statement. All token bytes are synthetic placeholders (aB3/xyz repeats), never
real credentials. v2: glpat length fixed to 20; dash-inside-tail reclassified
positive (variable-length tail absorbs '-'); 1001-char cap negatives added.
"""
import hashlib
import os
import re
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
RT = os.path.join(LANE, ".ufo/waves/round-95/w1/ExecC2Probe-receipts")
HERE = os.path.dirname(os.path.abspath(__file__))
INSTR_C2 = os.path.join(HERE, "instr-c2", "capture-secret-scan.py")
INSTR_R94 = os.path.join(HERE, "instr-r94", "capture-secret-scan.py")
NO_ALLOW = os.path.join(HERE, "no-allowlist.tsv")  # intentionally absent
C2_PIN = "66edd66143ec62f6e40c864817a97383916d7ff67e5ab384e130b65c44516707"

# ---- synthetic token bytes (deterministic, obviously fake) -----------------
GH76 = b"aB3" * 25 + b"a"          # exactly 76 alnum after ghr_
GH75 = b"aB3" * 25                 # 75: one below
GH77 = b"aB3" * 25 + b"aa"         # 77: one above
GH36 = b"aB3" * 12                 # classic PAT-length tail
SEG10 = b"x" * 10                  # minimum first/middle segment
MID10 = b"y" * 10
TAIL20 = b"z" * 20                 # minimum third segment
TAIL1000 = b"z" * 1000             # maximum third segment
TAIL1001 = b"z" * 1001             # one above the cap
SEG1001 = b"x" * 1001              # one above the first-segment cap
GL_PLAIN = b"glcbt-eyJ" + SEG10 + b".eyJ" + MID10 + b"." + TAIL20
GL_PREFIX20 = b"A1b2C3d4E5f6G7h8I9j0-" + GL_PLAIN   # max instance prefix
GL_PREFIX21_GLUED = b"ABCDEFGHIJKLMNOPQRSTU" + GL_PLAIN  # no dash: boundary kill
GL_GLSAT = b"glsat-eyJ" + SEG10 + b".eyJ" + MID10 + b"." + TAIL20
GL_GLIAMAT = b"gliamat-eyJ" + SEG10 + b".eyJ" + MID10 + b"." + TAIL20
GH_TOKEN36 = b"ghp_" + b"yZ7" * 12
GL_PAT20 = b"glpat-" + b"wK9" * 6 + b"qL"           # exactly 20
GENERIC_JWT = (b"eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJyOTVwcm9iIn0."
               b"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJ")

FIXTURES = {
    # -- positives for the two new shapes (expected C2 hits) ------------------
    "pos/ghr76-plain.txt": b"probe " + b"ghr_" + GH76 + b" ok\n",
    "relocated/dir-a/deep/nested/audit-2026-11.log": b"probe " + b"ghr_" + GH76 + b" ok\n",
    "pos/ghr76-json-joined.json": b'{"refresh_token":"' + b"ghr_" + GH76 + b'","issued":1730000000}\n',
    "pos/ghr76-escaped-u0020.json": b'{"v":"\\u0020' + b"ghr_" + GH76 + b'"}\n',
    "pos/ghr76-pct-escaped.txt": b"https://ci.example/artifacts?name=%41" + b"ghr_" + GH76 + b"\n",
    "pos/ghr76-entity.html": b'<meta name="x" content="&#x3B;' + b"ghr_" + GH76 + b'"/>\n',
    "pos/ghr76-line-start.txt": b"ghr_" + GH76 + b"\n",
    "pos/ghr76-trailing-quote.json": b'{"v":"' + b"ghr_" + GH76 + b'"}\n',
    "pos/multi-shape.json": (b'{"refresh_token":"' + b"ghr_" + GH76 + b'","session":"'
                             + GL_PLAIN + b'"}\n'),
    "pos/gl-jwt-glcbt-plain.txt": b"probe " + GL_PLAIN + b" ok\n",
    "pos/gl-jwt-glcbt-prefix20.txt": b"instance " + GL_PREFIX20 + b" audit\n",
    "pos/gl-jwt-glsat-escaped-n.json": b'{"log":"before\\n' + GL_GLSAT + b'"}\n',
    "pos/gl-jwt-gliamat.html": b"<code>" + GL_GLIAMAT + b"</code>\n",
    "relocated/b/other-name.md": b"redirect_uri=%2Facme-" + GL_PLAIN + b"&scope=read\n",
    "pos/url-query-jwt.txt": b"https://gitlab.example/oauth/callback?ticket=" + GL_PLAIN + b"&next=/dash\n",
    "pos/gl-jwt-gliamat-dashprefix.txt": b"probe acme-" + GL_GLIAMAT + b" ok\n",
    "pos/gl-jwt-prefix21-overflow.txt": b"probe " + b"ABCDEFGHIJKLMNOPQRSTU-" + GL_PLAIN + b"\n",
    "pos/gl-jwt-dash-inside-tail.txt": b"probe " + GL_PLAIN + b"-more ok\n",
    "pos/gl-jwt-tail-max1000.txt": b"probe glcbt-eyJ" + SEG10 + b".eyJ" + MID10 + b"." + TAIL1000 + b" ok\n",
    # -- negatives for the two new shapes -------------------------------------
    "neg/ghr75.txt": b"probe " + b"ghr_" + GH75 + b" ok\n",
    "neg/ghr77.txt": b"probe " + b"ghr_" + GH77 + b" ok\n",
    "neg/ghr36-classic.txt": b"probe " + b"ghr_" + GH36 + b" ok\n",
    "neg/ghr76-trailing-underscore.txt": b"probe " + b"ghr_" + GH76 + b"_ ok\n",
    "neg/ghr76-dash-inside.txt": b"probe " + b"ghr_" + b"x" * 38 + b"-" + b"y" * 37 + b" ok\n",
    "neg/ghr76-letter-prefixed.txt": b"probe x" + b"ghr_" + GH76 + b" ok\n",
    "neg/ghr76-underscore-prefixed.txt": b"probe _" + b"ghr_" + GH76 + b" ok\n",
    "neg/gl-jwt-glsat-mid-not-eyj.txt": b"probe " + b"glsat-eyJ" + SEG10 + b".ABCDEFGHIJ." + TAIL20 + b" ok\n",
    "neg/gl-jwt-head-not-eyj.txt": b"probe glsat-abcdefghij.eyJyyyyyyyyyy.zzzzzzzzzzzzzzzzzzzz ok\n",
    "neg/gl-jwt-tail19.txt": b"probe glcbt-eyJ" + SEG10 + b".eyJ" + MID10 + b"." + b"z" * 19 + b" ok\n",
    "neg/gl-jwt-seg9.txt": b"probe glcbt-eyJxxxxxxxxx.eyJ" + MID10 + b"." + TAIL20 + b" ok\n",
    "neg/gl-jwt-letter-before.txt": b"probe xglcbt-eyJ" + SEG10 + b".eyJ" + MID10 + b"." + TAIL20 + b" ok\n",
    "neg/gl-jwt-glued-prefix.txt": b"probe " + GL_PREFIX21_GLUED + b" ok\n",
    "neg/gl-jwt-tail-1001.txt": b"probe glcbt-eyJ" + SEG10 + b".eyJ" + MID10 + b"." + TAIL1001 + b" ok\n",
    "neg/gl-jwt-seg-1001.txt": b"probe glcbt-eyJ" + SEG1001 + b".eyJ" + MID10 + b"." + TAIL20 + b" ok\n",
    "neg/generic-jwt-url.txt": b"https://sso.example/cb?assertion=" + GENERIC_JWT + b"\n",
    "neg/gl-jwt-doc-placeholder.txt": b"docs say glcbt-eyJ<header>.<payload>.<signature> here\n",
    # -- old-shape regression (both instruments must agree) -------------------
    "relocated/c/vendor-notes/ghp36.txt": b"probe " + GH_TOKEN36 + b" ok\n",
    "reg/glpat20.txt": b"probe " + GL_PAT20 + b" ok\n",
}

EXPECTED_C2 = {
    "pos/ghr76-plain.txt": {"github-refresh-token"},
    "relocated/dir-a/deep/nested/audit-2026-11.log": {"github-refresh-token"},
    "pos/ghr76-json-joined.json": {"github-refresh-token"},
    "pos/ghr76-escaped-u0020.json": {"github-refresh-token"},
    "pos/ghr76-pct-escaped.txt": {"github-refresh-token"},
    "pos/ghr76-entity.html": {"github-refresh-token"},
    "pos/ghr76-line-start.txt": {"github-refresh-token"},
    "pos/ghr76-trailing-quote.json": {"github-refresh-token"},
    "pos/multi-shape.json": {"github-refresh-token", "gitlab-jwt-token"},
    "pos/gl-jwt-glcbt-plain.txt": {"gitlab-jwt-token"},
    "pos/gl-jwt-glcbt-prefix20.txt": {"gitlab-jwt-token"},
    "pos/gl-jwt-glsat-escaped-n.json": {"gitlab-jwt-token"},
    "pos/gl-jwt-gliamat.html": {"gitlab-jwt-token"},
    "relocated/b/other-name.md": {"gitlab-jwt-token"},
    "pos/url-query-jwt.txt": {"gitlab-jwt-token"},
    "pos/gl-jwt-gliamat-dashprefix.txt": {"gitlab-jwt-token"},
    "pos/gl-jwt-prefix21-overflow.txt": {"gitlab-jwt-token"},
    "pos/gl-jwt-dash-inside-tail.txt": {"gitlab-jwt-token"},
    "pos/gl-jwt-tail-max1000.txt": {"gitlab-jwt-token"},
    "neg/ghr36-classic.txt": {"github-token"},
    "relocated/c/vendor-notes/ghp36.txt": {"github-token"},
    "reg/glpat20.txt": {"gitlab-pat"},
}
NEW_SHAPES = {"github-refresh-token", "gitlab-jwt-token"}

EXPECTED_R94 = {p: (s - NEW_SHAPES) for p, s in EXPECTED_C2.items()}

HIT_RX = re.compile(r"^HIT shape=(\S+) path=(.*) line=(\d+)$")
SUM_RX = re.compile(r"^CAPTURE-SECRET-SCAN mode=(\S+) scanned=(\d+) hits=(\d+) "
                    r"files=(\d+) allowed=(\d+) unused_allow=(\d+) rc=(\d+)$")


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, **kw)


def run_scanner(instr, paths, cwd):
    proc = sh([sys.executable, "-B", instr, "--files", *paths, "--allow", NO_ALLOW],
              cwd=cwd)
    hits, summary = set(), None
    for line in proc.stdout.decode().splitlines():
        m = HIT_RX.match(line)
        if m:
            hits.add((m.group(2), m.group(1)))
            continue
        m = SUM_RX.match(line)
        if m:
            summary = m.groups()
    return proc, hits, summary


def main():
    os.makedirs(RT, exist_ok=True)
    rec = {}
    lines = []

    def note(s):
        lines.append(s)
        print(s, flush=True)

    # setup receipt ------------------------------------------------------------
    revs = {}
    for name, rev in [("base", "9ef0126cc60b7f62baafd04f3e52c45e2a8e2f10"),
                      ("landing", "38e7319f44a9fab2978b59ffd43faf207cf62b32")]:
        r = sh(["git", "-C", LANE, "rev-parse", rev])
        revs[name] = r.stdout.decode().strip()
    sha_c2 = hashlib.sha256(open(INSTR_C2, "rb").read()).hexdigest()
    sha_r94 = hashlib.sha256(open(INSTR_R94, "rb").read()).hexdigest()
    note("LANE base rev:      %s" % revs["base"])
    note("LANE landing rev:   %s" % revs["landing"])
    note("instrument sha256 C2  (landed): %s" % sha_c2)
    note("instrument sha256 R94 (base):   %s" % sha_r94)
    note("frozen C2 candidate pin:        %s" % C2_PIN)
    note("instrument==pin: %s" % (sha_c2 == C2_PIN))
    rec["00-setup"] = lines[:]

    # fixture repo ---------------------------------------------------------------
    D = tempfile.mkdtemp(prefix="exec2probe-fx-")
    sh(["git", "init", "-q", D])
    top = sh(["git", "-C", D, "rev-parse", "--show-toplevel"]).stdout.decode().strip()
    assert top == os.path.realpath(D), "fixture toplevel mismatch: %r != %r" % (top, D)
    note("fixture repo: %s (toplevel asserted)" % D)
    for rel, data in sorted(FIXTURES.items()):
        dst = os.path.join(D, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(dst, "wb") as fh:
            fh.write(data)

    TAGS = {
        "pos/ghr76-plain.txt": "ghr_+76, plain text",
        "relocated/dir-a/deep/nested/audit-2026-11.log": "ghr_+76, relocated dir+basename",
        "pos/ghr76-json-joined.json": "ghr_+76, JSON-joined (refresh_token key)",
        "pos/ghr76-escaped-u0020.json": "ghr_+76, \\u0020 escape left boundary",
        "pos/ghr76-pct-escaped.txt": "ghr_+76, %41 escape left boundary (forced path)",
        "pos/ghr76-entity.html": "ghr_+76, HTML entity context",
        "pos/ghr76-line-start.txt": "ghr_+76, start-of-input boundary",
        "pos/ghr76-trailing-quote.json": "ghr_+76, quote right boundary",
        "pos/multi-shape.json": "ghr_+76 + glcbt JWT in one file",
        "pos/gl-jwt-glcbt-plain.txt": "glcbt- no prefix",
        "pos/gl-jwt-glcbt-prefix20.txt": "glcbt- 20-char instance prefix (max)",
        "pos/gl-jwt-glsat-escaped-n.json": "glsat-, \\n escape left boundary",
        "pos/gl-jwt-gliamat.html": "gliamat-",
        "relocated/b/other-name.md": "glcbt- acme- prefix, %2F escape, relocated dir+basename",
        "pos/url-query-jwt.txt": "glcbt- JWT inside URL query (?ticket=)",
        "pos/gl-jwt-gliamat-dashprefix.txt": "acme-gliamat- (match begins at gliamat)",
        "pos/gl-jwt-prefix21-overflow.txt": "21-char label + -glcbt (match begins at glcbt)",
        "pos/gl-jwt-dash-inside-tail.txt": "dash inside tail absorbed (variable-length tail)",
        "pos/gl-jwt-tail-max1000.txt": "third segment exactly 1000 (cap inclusive)",
        "neg/ghr75.txt": "ghr_+75 (one below boundary)",
        "neg/ghr77.txt": "ghr_+77 (one above boundary)",
        "neg/ghr36-classic.txt": "ghr_+36 classic (old shape only)",
        "neg/ghr76-trailing-underscore.txt": "ghr_+76 then _ (lookahead kill)",
        "neg/ghr76-dash-inside.txt": "ghr_ tail broken by dash (fixed 76 window)",
        "neg/ghr76-letter-prefixed.txt": "letter before ghr_ (lookbehind kill)",
        "neg/ghr76-underscore-prefixed.txt": "underscore before ghr_ (lookbehind kill)",
        "neg/gl-jwt-glsat-mid-not-eyj.txt": "glsat- middle segment not eyJ",
        "neg/gl-jwt-head-not-eyj.txt": "glsat- first segment not starting eyJ",
        "neg/gl-jwt-tail19.txt": "third segment 19 chars (one below)",
        "neg/gl-jwt-seg9.txt": "first segment 9 chars (one below)",
        "neg/gl-jwt-letter-before.txt": "letter before glcbt-",
        "neg/gl-jwt-glued-prefix.txt": "21 alnum glued to glcbt- (no dash boundary)",
        "neg/gl-jwt-tail-1001.txt": "third segment 1001 chars (one above cap)",
        "neg/gl-jwt-seg-1001.txt": "first segment 1001 chars (one above cap)",
        "neg/generic-jwt-url.txt": "generic valid JWT in URL query (no provider prefix)",
        "neg/gl-jwt-doc-placeholder.txt": "glcbt-eyJ<header> doc placeholder",
        "relocated/c/vendor-notes/ghp36.txt": "ghp_+36 classic (old shape), relocated",
        "reg/glpat20.txt": "glpat-20 (old shape)",
    }
    man = ["fixture toplevel: %s" % D,
           "files: %d  (positives-new-shape: %d, negatives-new-shape: %d, old-shape regression: %d)"
           % (len(FIXTURES), 19, 17, 2),
           "expected C2 (file,shape) pairs: %d" % sum(len(v) for v in EXPECTED_C2.values()),
           "expected R94 (file,shape) pairs: %d" % sum(len(v) for v in EXPECTED_R94.values()),
           "note: contents are synthetic placeholders (aB3/x/y/z repeats); token values not printed"]
    for rel in sorted(FIXTURES):
        man.append("  %-52s %s" % (rel, TAGS[rel]))
    rec["01-fixture-manifest"] = man

    paths = sorted(FIXTURES)
    proc_c2, obs_c2, sum_c2 = run_scanner(INSTR_C2, paths, D)
    proc_r94, obs_r94, sum_r94 = run_scanner(INSTR_R94, paths, D)
    rec["02-scan-c2-files"] = proc_c2.stdout.decode().splitlines()
    rec["03-scan-r94-files"] = proc_r94.stdout.decode().splitlines()
    note("C2  scan rc=%s %s" % (proc_c2.returncode, sum_c2))
    note("R94 scan rc=%s %s" % (proc_r94.returncode, sum_r94))

    # selftests ----------------------------------------------------------------
    st_c2 = sh([sys.executable, "-B", INSTR_C2, "--selftest"])
    st_r94 = sh([sys.executable, "-B", INSTR_R94, "--selftest"])
    res_c2 = [l for l in st_c2.stdout.decode().splitlines() if l.startswith("SELFTEST-RESULT")]
    res_r94 = [l for l in st_r94.stdout.decode().splitlines() if l.startswith("SELFTEST-RESULT")]
    rec["04-selftest-c2"] = st_c2.stdout.decode().splitlines()
    rec["05-selftest-r94"] = st_r94.stdout.decode().splitlines()
    note("C2  selftest: %s (rc=%d)" % (res_c2, st_c2.returncode))
    note("R94 selftest: %s (rc=%d)" % (res_r94, st_r94.returncode))

    # diff ---------------------------------------------------------------------
    diff = []
    for label, obs, exp in [("C2/landed", obs_c2, EXPECTED_C2),
                            ("R94/base  ", obs_r94, EXPECTED_R94)]:
        # compare as (path, shape) tuples
        exp_pairs = {(p, s) for p, ss in exp.items() for s in ss}
        missing = sorted(exp_pairs - obs)
        extra = sorted(obs - exp_pairs)
        for p, s in missing:
            diff.append("MISSING  %s  (%s, %s)" % (label, p, s))
        for p, s in extra:
            diff.append("EXTRA    %s  (%s, %s)" % (label, p, s))
        note("%s observed=%d expected=%d missing=%d extra=%d"
             % (label, len(obs), len(exp_pairs), len(missing), len(extra)))

    # discrimination: new shapes fire on C2, never on R94; old shapes on both --
    disc = []
    new_c2 = {p for p, s in obs_c2 if s in NEW_SHAPES}
    new_r94 = {p for p, s in obs_r94 if s in NEW_SHAPES}
    for p, s in sorted(obs_c2):
        if s in NEW_SHAPES and (p, s) in obs_r94:
            disc.append("LEAK  new shape on R94: (%s, %s)" % (p, s))
    old_pairs = {("relocated/c/vendor-notes/ghp36.txt", "github-token"),
                 ("reg/glpat20.txt", "gitlab-pat"),
                 ("neg/ghr36-classic.txt", "github-token")}
    for pair in sorted(old_pairs):
        if pair not in obs_c2 or pair not in obs_r94:
            disc.append("OLD-SHAPE REGRESSION: %s not on both" % (pair,))
    for p, s in sorted(obs_r94 - old_pairs):
        disc.append("UNEXPECTED R94 hit: (%s, %s)" % (p, s))
    note("new-shape pairs on C2: %d files; on R94: %d" % (len(new_c2), len(new_r94)))
    note("discrimination findings: %s" % (disc or "none"))

    # summary consistency -------------------------------------------------------
    cons = []
    if sum_c2 and int(sum_c2[2]) != len(obs_c2):
        cons.append("C2 summary hits=%s != observed %d" % (sum_c2[2], len(obs_c2)))
    if sum_c2 and sum_c2[0] != "files":
        cons.append("C2 mode=%s" % sum_c2[0])
    if sum_r94 and int(sum_r94[2]) != len(obs_r94):
        cons.append("R94 summary hits=%s != observed %d" % (sum_r94[2], len(obs_r94)))
    st_ok = (st_c2.returncode == 0 and res_c2 == ["SELFTEST-RESULT pass cases=115"]
             and st_r94.returncode == 0 and res_r94 == ["SELFTEST-RESULT pass cases=101"])

    verdict_lines = []
    ok = (proc_c2.returncode == 1 and proc_r94.returncode == 1
          and not diff and not disc and not cons and st_ok and sha_c2 == C2_PIN)
    verdict_lines.append("sha_c2==pin: %s" % (sha_c2 == C2_PIN))
    verdict_lines.append("diff empty: %s (%d lines)" % (not diff, len(diff)))
    verdict_lines.append("discrimination clean: %s" % (not disc))
    verdict_lines.append("summary consistent: %s" % (not cons))
    verdict_lines.append("selftests: C2 cases=115 pass, R94 cases=101 pass: %s" % st_ok)
    verdict_lines.append("PROBE RESULT: %s" % ("PASS" if ok else "FAIL"))
    rec["06-diff-passfail"] = diff + disc + cons + [""] + verdict_lines
    note("")
    for l in verdict_lines:
        note(l)

    for name, body in sorted(rec.items()):
        with open(os.path.join(RT, name + ".txt"), "w") as fh:
            fh.write("\n".join(body) + "\n")
    # driver source receipt (reproducibility)
    with open(os.path.abspath(__file__), "rb") as fh:
        src = fh.read()
    with open(os.path.join(RT, "07-driver-source.py"), "wb") as fh:
        fh.write(src)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
