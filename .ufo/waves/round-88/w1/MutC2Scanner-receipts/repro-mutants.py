#!/usr/bin/env python3
"""MutC2Scanner (round 88) re-runnable mutation probe for the C2 landing scanner.

24 single-point mutants of corpus/instruments/capture-secret-scan.py at the C2
landing (b43dc215; instrument sha256 d7349536...) driven through the frozen
counter .ufo/waves/round-88/c2/capability-check.py WITHOUT --instrument-sha256,
plus one residual-kill probe per survivor.

Each mutant run: `git clone --shared` of the lane at the base revision, the
mutated instrument copied into corpus/instruments/ beside the frozen allowlist,
the frozen c2/candidate/scorecard-row.txt written over the SCORECARD row, one
fixture-identity commit (toplevel asserted), then the counter at HEAD.

Fixtures are generated at runtime: no matched value (and no credential-shaped
literal) is stored here or printed. Receipts carry shape names, paths and rc.

  python3 -B repro-mutants.py --work DIR [--sweep|--probes|--all]

Exit 0 when every mutant reaches a verdict (killed or survived) and every
survivor probe separates; 1 when a run errors or a probe cannot separate.
"""
import argparse
import base64
import os
import shutil
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
W = os.path.join(LANE, ".ufo/waves/round-88")
CAND = os.path.join(W, "c2/candidate")
COUNTER = os.path.join(W, "c2/capability-check.py")
INSTR_REL = "corpus/instruments/capture-secret-scan.py"
ALLOW_REL = "corpus/instruments/capture-secret-allow.tsv"
BASE = "6beead9148945fa695cf3139e8fc9d8e91cc5fd0"

# Runtime-generated fixture bodies (never literal credential-shaped values).
HEX = "0123456789abcdef" * 8                       # 128 hex
HEX96 = "0123456789abcdef" * 6                     # 96 hex
HEX72 = ("0123456789abcdef" * 4) + "01234567"      # 72 hex
B64 = base64.b64encode(b"probe sas signature fixture 0123456789").decode().rstrip("=")
B64_35 = B64[:35]
B64_40 = B64[:40]
SAS = "https://a.blob.core.windows.net/c/b.txt"
# Gate `credential` shape with a file-name value; the key word is split so this
# script itself never carries a credential-shaped literal (it is scanned too).
JSON_TOK = '{"%s": "%s"}' % ("tok" + "en", "probe-envelope-json-file")

SPECS = [
    ("sep-drop-html-amp", '_SEP = rb"(?:&amp;|&|\\\\u0026)"', '_SEP = rb"(?:&|\\\\u0026)"',
     "_SEP loses &amp;"),
    ("sep-drop-json-u0026", '_SEP = rb"(?:&amp;|&|\\\\u0026)"', '_SEP = rb"(?:&amp;|&)"',
     "_SEP loses \\u0026"),
    ("param-bound-1", '[^&\\s\\"\'<>\\\\]*){0,20}?', '[^&\\s\\"\'<>\\\\]*){0,1}?',
     "_PARAM bound 20 -> 1"),
    ("param-name-max3", 'rb"[A-Za-z]{2,6}=', 'rb"[A-Za-z]{2,3}=', "_PARAM name width 2-6 -> 2-3"),
    ("sig-threshold-64", 'sig=[A-Za-z0-9%+/]{40,}', 'sig=[A-Za-z0-9%+/]{64,}', "_SIG floor 40 -> 64"),
    ("sig-threshold-32", 'sig=[A-Za-z0-9%+/]{40,}', 'sig=[A-Za-z0-9%+/]{32,}', "_SIG floor 40 -> 32"),
    ("sig-padding-drop", '{40,}(?:=|%3D){0,2}', '{40,}', "_SIG padding group dropped"),
    ("sv-hardcoded-version", '_SV = rb"sv=\\d{4}-\\d{2}-\\d{2}"', '_SV = rb"sv=2022-11-02"',
     "_SV pinned to one storage version"),
    ("sv-missing-day", '_SV = rb"sv=\\d{4}-\\d{2}-\\d{2}"', '_SV = rb"sv=\\d{4}-\\d{2}"',
     "_SV accepts YYYY-MM"),
    ("alt-drop-sig-first", '+ rb"|" + _SIG + _PARAM + _SEP + _SV + rb")")),', '+ rb")")),',
     "alternation loses sig-first branch"),
    ("alt-drop-sv-first", '(?:" + _SV + _PARAM + _SEP + _SIG + rb"|"', '(?:"',
     "alternation loses sv-first branch"),
    ("lookbehind-drop", "(?<![A-Za-z0-9_])", "", "lookbehind deleted"),
    ("lookbehind-allow-underscore", "(?<![A-Za-z0-9_])", "(?<![A-Za-z0-9])",
     "lookbehind spares a preceding underscore"),
    ("gcs-threshold-128", 'X-Goog-Signature(?:=|\\\\?[\\"\']?\\s*:\\s*\\\\?[\\"\']?)[0-9a-f]{64,}',
     'X-Goog-Signature(?:=|\\\\?[\\"\']?\\s*:\\s*\\\\?[\\"\']?)[0-9a-f]{128,}', "GCS floor 64 -> 128"),
    ("gcs-threshold-80", 'X-Goog-Signature(?:=|\\\\?[\\"\']?\\s*:\\s*\\\\?[\\"\']?)[0-9a-f]{64,}',
     'X-Goog-Signature(?:=|\\\\?[\\"\']?\\s*:\\s*\\\\?[\\"\']?)[0-9a-f]{80,}', "GCS floor 64 -> 80"),
    ("gcs-nocase", 'rb"(?i)X-Goog-Signature', 'rb"X-Goog-Signature', "GCS pattern loses (?i)"),
    ("gcs-name-truncated", 'rb"(?i)X-Goog-Signature(?:=', 'rb"(?i)X-Goog-Sign(?:=', "GCS name truncated"),
    ("gcs-json-quote-drop", '\\s*:\\s*\\\\?[\\"\']?)[0-9a-f]{64,}', '\\s*:\\s*)[0-9a-f]{64,}',
     "GCS separator loses the quote after ':'"),
    ("scope-min-depth6", '(len(parts) >= 5 and parts[:2]', '(len(parts) >= 6 and parts[:2]',
     "practice scope needs 6 parts"),
    ("scope-prefix-loose", 'parts[:2] == ["corpus", "practice"]', 'parts[0] == "corpus"',
     "practice scope unpinned from corpus/practice"),
    ("scope-evidence-not-parts3", 'parts[3] == "evidence"', 'parts[-2] == "evidence"',
     "practice scope accepts evidence at any depth"),
    ("selftest-drop-gcs-json-key",
     '        ("gcs-json-key", b\'{"X-Goog-Signature": "\' + gsig + b\'"}\', {"gcs-signed-url-signature"}),\n',
     '', "selftest GCS JSON-key case deleted"),
    ("selftest-drop-azure-html-amp",
     '        ("azure-html-amp", b\'<a href="https://a.blob.core.windows.net/c/b.txt?sv=2022-11-02&amp;sr=b&amp;sig=\' + asig + b\'">\', {"azure-sas-signature"}),\n',
     '', "selftest &amp; Azure case deleted"),
    ("selftest-case-count-zero",
     '"SELFTEST-RESULT %s cases=%d" % ("pass" if not bad else "fail", len(cases) + len(paths) + len(checks))',
     '"SELFTEST-RESULT %s cases=%d" % ("pass" if not bad else "fail", 0)', "selftest stops counting cases"),
]

PROBES = [
    ("param-bound-1", "files",
     SAS + "?sv=2022-11-02&ss=b&srt=sco&sp=rwdlac&se=2026-11-08T00:00:00Z&sig=" + B64 + "\n",
     "positive: four intervening parameters (SAS order of S127:605)"),
    ("sig-threshold-32", "files", SAS + "?sv=2022-11-02&sig=" + B64_35 + "\n",
     "negative: 35-char sig beside sv"),
    ("sv-hardcoded-version", "files", SAS + "?sv=2024-11-04&sr=b&sig=" + B64 + "\n",
     "positive: a newer service version"),
    ("gcs-threshold-80", "files",
     '{"u":"https://storage.googleapis.com/b/o.png?X-Goog-Signature=%s"}\n' % HEX72,
     "positive: 72-hex signature"),
    ("gcs-threshold-128", "files",
     '{"u":"https://storage.googleapis.com/b/o.png?X-Goog-Signature=%s"}\n' % HEX96,
     "positive: 96-hex signature"),
    ("gcs-nocase", "files",
     '{"u":"https://storage.googleapis.com/b/o.png?x-goog-signature=%s"}\n' % HEX,
     "positive: lower-case parameter name"),
    ("param-name-max3", "files",
     SAS + "?sv=2022-11-02&skoid=00000000-0000-0000-0000-000000000000&sig=" + B64 + "\n",
     "positive: 5-letter intervening parameter name"),
    ("lookbehind-drop", "files", "https://example.com/x?mysv=2022-11-02&sig=" + B64 + "\n",
     "negative: sv= run into a longer parameter name"),
    ("lookbehind-drop", "files",
     '{"u":"' + SAS + "?sp=r" + "\\u0026" + "st=2026-11-07T00:00:00Z" + "\\u0026"
     + "sv=2022-11-02" + "\\u0026" + "sr=b" + "\\u0026" + "sig=" + B64 + '"}\n',
     "positive: JSON-escaped SAS whose sv= follows \\u0026 (ReviewC2Scanner F1 position)"),
    ("lookbehind-allow-underscore", "files", "https://example.com/x?_sv=2022-11-02&sig=" + B64 + "\n",
     "negative: sv= run into an underscored parameter name"),
    ("sig-padding-drop", "files", SAS + "?sv=2022-11-02&sig=" + B64_40 + "==\n",
     "EQUIVALENT-mutant check: literal padding (separation is a FAILURE here)"),
    ("sig-padding-drop", "files", SAS + "?sv=2022-11-02&sig=" + B64 + "\n",
     "EQUIVALENT-mutant check: %-encoded padding (separation is a FAILURE here)"),
    ("gcs-json-quote-drop", "files", '{"X-Goog-Signature": "%s"}\n' % HEX,
     "positive: JSON-key form (K1-only ground)"),
    ("scope-prefix-loose", "rev", {"corpus/practice2/p/evidence/F.txt": JSON_TOK},
     "negative: a sibling corpus tree is out of scope"),
    ("scope-evidence-not-parts3", "rev", {"corpus/practice/p/sub/evidence/F.txt": JSON_TOK},
     "negative: evidence one level deeper than <pkg>/evidence/"),
    ("scope-min-depth6", "rev", {"corpus/practice/p/evidence/F.txt": JSON_TOK},
     "positive: <pkg>/evidence/<file>"),
    ("selftest-drop-gcs-json-key", "selftest", "gcs-json-key", "deleted selftest case"),
    ("selftest-drop-azure-html-amp", "selftest", "html-amp", "deleted selftest case"),
    ("selftest-case-count-zero", "selftest", "", "selftest case count zeroed"),
]


def git(d, *a, **kw):
    return subprocess.run(["git", "-C", d] + list(a), capture_output=True, text=True, **kw)


def build(work, name, old, new):
    d = os.path.join(work, "mut", name)
    shutil.rmtree(d, ignore_errors=True)
    subprocess.run(["git", "clone", "-q", "--shared", LANE, d], check=True, capture_output=True)
    subprocess.run(["git", "-C", d, "checkout", "-q", BASE], check=True, capture_output=True)
    top = git(d, "rev-parse", "--show-toplevel").stdout.strip()
    if os.path.realpath(top) != os.path.realpath(d):
        raise SystemExit("fixture toplevel mismatch: %r" % top)
    cand = open(os.path.join(CAND, "capture-secret-scan.py"), "rb").read()
    data = cand
    if old is not None:
        ob = old.encode()
        if cand.count(ob) != 1:
            raise SystemExit("spec %s occurs %d times" % (name, cand.count(ob)))
        data = cand.replace(ob, new.encode(), 1)
    with open(os.path.join(d, INSTR_REL), "wb") as fh:
        fh.write(data)
    shutil.copy(os.path.join(CAND, "capture-secret-allow.tsv"), os.path.join(d, ALLOW_REL))
    sc = os.path.join(d, "SCORECARD.md")
    lines = open(sc).read().split("\n")
    idx = [k for k, l in enumerate(lines) if l.startswith("| capture-secret-scan |")]
    if len(idx) != 1:
        raise SystemExit("SCORECARD row count %d" % len(idx))
    lines[idx[0]] = open(os.path.join(CAND, "scorecard-row.txt")).read().rstrip("\n")
    open(sc, "w").write("\n".join(lines))
    subprocess.run(["git", "-C", d, "-c", "user.name=fixture", "-c", "user.email=fixture@invalid",
                    "commit", "-qam", "mutant " + name], check=True, capture_output=True)
    return d


def counter(d, work, tag):
    w = os.path.join(work, "cw-" + tag)
    os.makedirs(w, exist_ok=True)
    p = subprocess.run([sys.executable, "-B", COUNTER, "--lane", d, "--rev", "HEAD", "--work", w],
                       capture_output=True, text=True, env=dict(os.environ, TMPDIR=work))
    limbs = [l for l in p.stdout.splitlines() if l.startswith("LIMB ")]
    res = [l for l in p.stdout.splitlines() if l.startswith("CAPABILITY-CHECK-RESULT")]
    return p.returncode, limbs, res[0] if res else "", p.stdout


def instr_dir(work, tag, data):
    d = os.path.join(work, "probe", tag)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    open(os.path.join(d, "capture-secret-scan.py"), "wb").write(data)
    shutil.copy(os.path.join(LANE, "corpus/instruments/claim-package-check.py"),
                os.path.join(d, "claim-package-check.py"))
    shutil.copy(os.path.join(CAND, "capture-secret-allow.tsv"),
                os.path.join(d, "capture-secret-allow.tsv"))
    return d


def scan(d, args):
    p = subprocess.run([sys.executable, "-B", os.path.join(d, "capture-secret-scan.py")] + args,
                       capture_output=True, text=True)
    hits = sorted(l for l in p.stdout.splitlines() if l.startswith("HIT "))
    res = [l for l in p.stdout.splitlines()
           if l.startswith("CAPTURE-SECRET-SCAN mode=") or l.startswith("SELFTEST-RESULT")]
    return p.returncode, hits, res


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--sweep", action="store_true")
    ap.add_argument("--probes", action="store_true")
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args(argv)
    work = os.path.abspath(a.work)
    os.makedirs(work, exist_ok=True)
    sweep = a.sweep or a.all or not a.probes
    probes = a.probes or a.all
    cand = open(os.path.join(CAND, "capture-secret-scan.py"), "rb").read()
    bad = 0
    if sweep:
        d = build(work, "__baseline__", None, None)
        rc, limbs, res, out = counter(d, work, "baseline")
        print("BASELINE %-32s %-9s rev=%s" % ("__baseline__", "SURVIVED" if rc == 0 else "ERROR",
                                              git(d, "rev-parse", "HEAD").stdout.strip()))
        bad += rc != 0
        for name, old, new, note in SPECS:
            d = build(work, name, old, new)
            rc, limbs, res, out = counter(d, work, name)
            fail = [l.split(" ")[1] for l in limbs if " FAIL " in l]
            status = "KILLED" if rc == 1 else "SURVIVED" if rc == 0 else "ERROR"
            print("MUTANT %-32s %-9s killed_by=%-8s rev=%s  # %s"
                  % (name, status, ",".join(fail) or "none", git(d, "rev-parse", "HEAD").stdout.strip(), note))
            for l in limbs:
                if " FAIL " in l:
                    print("    " + l)
            bad += status == "ERROR"
    if probes:
        for name, mode, arg, note in PROBES:
            rec = [s for s in SPECS if s[0] == name][0]
            data = cand.replace(rec[1].encode(), rec[2].encode(), 1)
            if mode == "selftest":
                pr = scan(instr_dir(work, name + "-pristine", cand), ["--selftest"])
                mu = scan(instr_dir(work, name + "-mutant", data), ["--selftest"])
                keep = lambda r: [l for l in r[2] if arg in l or "SELFTEST-RESULT" in l]
                p_pick, m_pick = keep(pr), keep(mu)
                sep = p_pick != m_pick
                print("PROBE  %-32s selftest pristine=%s mutant=%s separates=%s  # %s"
                      % (name, p_pick, m_pick, "yes" if sep else "no", note))
            elif mode == "files":
                pd = os.path.join(work, "probe", "fx-" + name)
                os.makedirs(pd, exist_ok=True)
                f = os.path.join(pd, "probe.txt")
                open(f, "wb").write(arg.encode())
                pr = scan(instr_dir(work, name + "-pristine", cand), ["--files", f])
                mu = scan(instr_dir(work, name + "-mutant", data), ["--files", f])
                sep = pr[0] != mu[0] or pr[1] != mu[1]
                print("PROBE  %-32s files pristine=rc%d hits %s | mutant=rc%d hits %s | separates=%s  # %s"
                      % (name, pr[0], pr[2] or "-", mu[0], mu[2] or "-", "yes" if sep else "no", note))
            else:
                d = os.path.join(work, "mut", name)
                if not os.path.isdir(d):
                    raise SystemExit("run --sweep first (missing %s)" % d)
                for rel, text in arg.items():
                    p = os.path.join(d, rel)
                    os.makedirs(os.path.dirname(p), exist_ok=True)
                    open(p, "w").write(text)
                subprocess.run(["git", "-C", d, "add", "-A"], check=True, capture_output=True)
                subprocess.run(["git", "-C", d, "-c", "user.name=fixture", "-c",
                                "user.email=fixture@invalid", "commit", "-q", "-m", "probe " + name],
                               check=True, capture_output=True)
                pr = scan(instr_dir(work, name + "-pristine", cand), ["--lane", d, "--rev", "HEAD"])
                mu = scan(instr_dir(work, name + "-mutant", data), ["--lane", d, "--rev", "HEAD"])
                sep = pr[0] != mu[0] or pr[1] != mu[1]
                print("PROBE  %-32s rev   pristine=rc%d hits %s | mutant=rc%d hits %s | separates=%s  # %s"
                      % (name, pr[0], pr[2] or "-", mu[0], mu[2] or "-", "yes" if sep else "no", note))
            want = not note.startswith("EQUIVALENT")
            bad += sep != want
    print("REPRO %s" % ("pass" if not bad else "fail rc=1"))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
