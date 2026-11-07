#!/usr/bin/env python3
"""Round-86 C2 mutation probe: single-point mutants of c2/e2e-check.py scored
against the frozen pre-freeze controls (controls/c2-controls-r86.sh), plus one
routed killing control per survivor.

Writes only under $S (default /fast/scratch/hyaku/kasegi-r86/MutC2Counter).
Reads lane bytes read-only. No git/jj.

Kill criterion (same as round 85): a mutant is KILLED when at least one frozen
control changes its (rc, per-limb pass/FAIL) signature against the pristine
counter. A detail-only change (`short=2` -> `short=1` with E4 still FAIL) is
recorded as `detail_only`, not as a kill.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
S = os.environ.get("MUT_SCRATCH", "/fast/scratch/hyaku/kasegi-r86/MutC2Counter")
FROZEN = os.path.join(LANE, ".ufo/waves/round-86/c2/e2e-check.py")
FROZEN_SHA = "b4a97e095da1d869a0e8c0b82f758ba8d517ae2d10cf72e48e7fc4962578a834"
CONTROLS = os.path.join(LANE, ".ufo/waves/round-86/controls/c2-controls-r86.sh")
SNAPS = os.path.join(LANE, "corpus/source-snapshots")
R85PKG = os.path.join(LANE, "corpus/practice/curl-h1-1913733")
GATE = os.path.join(LANE, "corpus/instruments/claim-package-check.py")

PRICING = """## Pricing

price-program: ibb
price-payer: internet-bug-bounty
price-severity: medium
price-reward-at-disclosure: 2400 USD
price-platform-bounty-flag: true
price-original-report: 1913733
price-reward-current-policy: ended 2026-01-31
price-kev: not-listed catalogVersion 2026.10.23
price-cve: CVE-2023-28319

> I would like to especially highlight the awesome Internet Bug Bounty project, which has paid the bounties for us for many years.
> There is no longer a curl bug-bounty program. It officially stops on January 31, 2026.
> Bug bounty: 2400 USD
"""

HEAD = "# HackerOne 1997312 (IBB): CVE-2023-28319 payer record (retrospective practice package)"
RECORD = "Record: https://hackerone.com/reports/1997312"
ORIGINAL = "Original: https://hackerone.com/reports/1913733"


def sha(b):
    return hashlib.sha256(b).hexdigest()


def rd(p, mode="r"):
    with open(p, mode, **({} if "b" in mode else {"encoding": "utf-8"})) as fh:
        return fh.read()


def wr(p, data):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    mode = "wb" if isinstance(data, bytes) else "w"
    with open(p, mode, **({} if mode == "wb" else {"encoding": "utf-8"})) as fh:
        fh.write(data)


def run(argv, env=None, cwd=None):
    e = dict(os.environ)
    e.update(env or {})
    p = subprocess.run(argv, capture_output=True, text=True, env=e, cwd=cwd or LANE)
    return p.returncode, p.stdout, p.stderr


# ---------------------------------------------------------------- frozen controls


def write_driver(path):
    text = rd(CONTROLS)
    old_c = 'C="python3 -B $W/c2/e2e-check.py --lane $L"'
    new_c = 'C="python3 -B ${COUNTER:-$W/c2/e2e-check.py} --lane $L"'
    assert text.count(old_c) == 1
    text = text.replace(old_c, new_c)
    old_s = 'echo "counter_sha256=$(sha256sum $W/c2/e2e-check.py | cut -d\' \' -f1)'
    new_s = 'echo "counter_sha256=$(sha256sum ${COUNTER:-$W/c2/e2e-check.py} | cut -d\' \' -f1)'
    assert text.count(old_s) == 1
    text = text.replace(old_s, new_s)
    wr(path, text)


def parse(text):
    """[(control_name, rc, ((limb, verdict), ...))] in transcript order."""
    blocks, name, cur, rc = [], None, [], None
    for line in text.splitlines():
        if line.startswith("== control ") or line.startswith("== pricing control "):
            if name is not None:
                blocks.append((name, rc, tuple(cur)))
            name = line[3:].split(":")[0].strip()
            cur, rc = [], None
            continue
        if name is None:
            continue
        m = re.match(r"^LIMB (\S+) (pass|FAIL)\b", line)
        if m:
            cur.append((m.group(1), m.group(2)))
        elif line.startswith("rc="):
            rc = int(line[3:].strip())
    if name is not None:
        blocks.append((name, rc, tuple(cur)))
    return blocks


def sig(blocks):
    return tuple((n, rc, fs) for n, rc, fs in blocks)


def run_controls(counter, scratch, label):
    shutil.rmtree(scratch, ignore_errors=True)
    os.makedirs(scratch)
    rc, out, err = run(["bash", os.path.join(S, "drive.sh"), scratch],
                       env={"COUNTER": counter, "TMPDIR": S})
    text = out + err
    wr(os.path.join(S, "out", label + ".txt"), text)
    return text


def details(text):
    return {ln for ln in text.splitlines() if ln.startswith("LIMB ")}


# ---------------------------------------------------------------- mutants

MUTANTS = [
    # E0 subject
    ("e0_head_no_subject",
     'head_ok = first.startswith("# ") and SUBJECT in first and want["cve"] in first',
     'head_ok = first.startswith("# ") and want["cve"] in first'),
    ("e0_head_no_cve",
     'head_ok = first.startswith("# ") and SUBJECT in first and want["cve"] in first',
     'head_ok = first.startswith("# ") and SUBJECT in first'),
    ("e0_head_no_hash_prefix",
     'head_ok = first.startswith("# ") and SUBJECT in first and want["cve"] in first',
     'head_ok = SUBJECT in first and want["cve"] in first'),
    ("e0_url_always_true",
     'url_ok = ("https://hackerone.com/reports/%s" % SUBJECT) in text',
     'url_ok = True'),
    ("e0_no_stray_check",
     'stray = sorted(ids - allowed)',
     'stray = []'),
    # duplicate keys
    ("e3_no_dup_check",
     'ok = len(heads) == 1 and not dup and not bad',
     'ok = len(heads) == 1 and not bad'),
    ("e3_dup_never_detected",
     'if mm.group(1) in got:',
     'if False:'),
    # section count
    ("e3_sections_ge1",
     'ok = len(heads) == 1 and not dup and not bad',
     'ok = len(heads) >= 1 and not dup and not bad'),
    # quote length and pool
    ("e4_min_quote_10", 'MIN_QUOTE = 20', 'MIN_QUOTE = 10'),
    ("e4_min_quote_1", 'MIN_QUOTE = 20', 'MIN_QUOTE = 1'),
    ("e4_no_short_check",
     'ok4 = len(quotes) >= 3 and not short and not miss and bool(from_s123)',
     'ok4 = len(quotes) >= 3 and not miss and bool(from_s123)'),
    ("e4_no_s123_requirement",
     'ok4 = len(quotes) >= 3 and not short and not miss and bool(from_s123)',
     'ok4 = len(quotes) >= 3 and not short and not miss and True'),
    ("e4_s123_taken_from_s120",
     'from_s123 = [q for q in quotes if len(q) >= MIN_QUOTE and q in pool[3]]',
     'from_s123 = [q for q in quotes if len(q) >= MIN_QUOTE and q in pool[0]]'),
    # field derivations
    ("program_hardwired_curl",
     '        "program": handle,',
     '        "program": "curl",'),
    ("payer_drop_handle_conjunction",
     '"payer": "internet-bug-bounty" if handle == "ibb" and PAYER_LINE in s123 else None,',
     '"payer": "internet-bug-bounty" if PAYER_LINE in s123 else None,'),
    ("payer_drop_s123_conjunction",
     '"payer": "internet-bug-bounty" if handle == "ibb" and PAYER_LINE in s123 else None,',
     '"payer": "internet-bug-bounty" if handle == "ibb" else None,'),
    ("policy_drop_end_line",
     '"reward-current-policy": "ended 2026-01-31" if END_LINE in s123 and "There is no bug bounty" in s121 else None,',
     '"reward-current-policy": "ended 2026-01-31" if "There is no bug bounty" in s121 else None,'),
    ("policy_drop_s121_conjunction",
     '"reward-current-policy": "ended 2026-01-31" if END_LINE in s123 and "There is no bug bounty" in s121 else None,',
     '"reward-current-policy": "ended 2026-01-31" if END_LINE in s123 else None,'),
    ("severity_drop_s120_agreement",
     '"severity": s122["severity_rating"].lower() if sev and sev.group(1).lower() == s122["severity_rating"].lower() else None,',
     '"severity": s122["severity_rating"].lower(),'),
    ("flag_truthy_not_strict_true",
     '"platform-bounty-flag": "true" if s122["has_bounty?"] is True else "false",',
     '"platform-bounty-flag": "true" if s122["has_bounty?"] else "false",'),
    ("original_report_drop_s120_corroboration",
     'orig_id = orig.group(1) if orig and ("Original report: https://hackerone.com/reports/%s" % orig.group(1)) in s120 else None',
     'orig_id = orig.group(1) if orig else None'),
    ("reward_regex_digits_only",
     'bb = re.search(r"^Bug bounty: (.+?)\\s*$", s120, re.M)',
     'bb = re.search(r"^Bug bounty: (\\d+)", s120, re.M)'),
    ("kev_always_not_listed",
     '"kev": "not-listed" if kev.count(cve) == 0 else "listed",',
     '"kev": "not-listed" if kev.count(cve) >= 0 else "listed",'),
    ("kev_reverse_prefix",
     'if not g.startswith(w) or (w == "listed" and g.startswith("not-listed")):',
     'if g.startswith(w) or (w == "listed" and g.startswith("not-listed")):'),
    ("cve_lowercased",
     '"cve": cve,',
     '"cve": cve.lower(),'),
    # E2 binding
    ("e2_drop_manifest_digest",
     'if b == snap and h == rec[sid] and str(art.get("sha256", "")).lower() == h:',
     'if b == snap and str(art.get("sha256", "")).lower() == h:'),
    ("e2_drop_byte_equality",
     'if b == snap and h == rec[sid] and str(art.get("sha256", "")).lower() == h:',
     'if h == rec[sid] and str(art.get("sha256", "")).lower() == h:'),
    ("e2_drop_recorded_artifact_digest",
     'if b == snap and h == rec[sid] and str(art.get("sha256", "")).lower() == h:',
     'if b == snap and h == rec[sid]:'),
    ("e2_follow_symlinks",
     'if not os.path.isfile(ap) or os.path.islink(ap):',
     'if not os.path.isfile(ap):'),
    ("e2_found_subset",
     'limbs.append(("E2", found == {"S122", "S123"}, "bound=%s" % (",".join(sorted(found)) or "none")))',
     'limbs.append(("E2", found <= {"S122", "S123"}, "bound=%s" % (",".join(sorted(found)) or "none")))'),
    ("e2_require_third_source",
     'limbs.append(("E2", found == {"S122", "S123"}, "bound=%s" % (",".join(sorted(found)) or "none")))',
     'limbs.append(("E2", found == {"S122", "S123", "S120"}, "bound=%s" % (",".join(sorted(found)) or "none")))'),
    # r85-survivor classes re-probed at r86
    ("reward_case_insensitive",
     '        elif g != w:\n            bad.append(f)',
     '        elif g.lower() != w.lower():\n            bad.append(f)'),
    ("e1_drop_verdict_check",
     'ok = p.returncode == 0 and "verdict=WELL-FORMED" in p.stdout',
     'ok = "verdict=WELL-FORMED" in p.stdout'),
    ("e1_drop_rc_check",
     'ok = p.returncode == 0 and "verdict=WELL-FORMED" in p.stdout',
     'ok = p.returncode == 0'),
    ("e4_quotes_not_normalized",
     'quotes = [norm(ln[2:]) for ln in sec.split("\\n") if ln.startswith("> ")]',
     'quotes = [ln[2:].strip() for ln in sec.split("\\n") if ln.startswith("> ")]'),
    ("e4_pool_includes_kev",
     'pool = [norm(s) for s in snaps]',
     'pool = [norm(s) for s in snaps] + [norm(rd(os.path.join(lane, "corpus", "source-snapshots", "round-35", "S052.txt")))]'),
    ("severity_case_sensitive",
     'if g.lower() != w:',
     'if g != w:'),
    # E5 and overall
    ("e5_or_instead_of_and",
     'ok = not rel.startswith("..") and rel in log and rel in sh',
     'ok = not rel.startswith("..") and (rel in log or rel in sh)'),
    ("allok_skips_e1",
     'allok = all(ok for _, ok, _ in limbs)',
     'allok = all(ok for n, ok, _ in limbs if n != "E1")'),
]


def gen_mutants():
    base = rd(FROZEN)
    out = []
    os.makedirs(os.path.join(S, "mut"), exist_ok=True)
    for mid, old, new in MUTANTS:
        if base.count(old) != 1:
            raise SystemExit("mutant %s: anchor count=%d" % (mid, base.count(old)))
        text = base.replace(old, new)
        path = os.path.join(S, "mut", mid + ".py")
        wr(path, text)
        out.append((mid, path, sha(text.encode())))
    return out


# ---------------------------------------------------------------- scratch lane

GOOD_PRICING = PRICING


def report_text():
    return HEAD + "\n\n" + RECORD + "\n" + ORIGINAL + "\n\n" + GOOD_PRICING + "\n## Next\n"


def build_lane0(root):
    """A minimal faithful lane: committed snapshots, gate, LOG/SHONEN, golden pkg."""
    snap = os.path.join(root, "corpus", "source-snapshots")
    for rnd in ("round-86", "round-85", "round-35"):
        wr(os.path.join(snap, rnd, ".keep"), "")
        for name in sorted(os.listdir(os.path.join(SNAPS, rnd))):
            if name.endswith(".txt") or name == "manifest.json":
                wr(os.path.join(snap, rnd, name), rd(os.path.join(SNAPS, rnd, name), "rb"))
    wr(os.path.join(root, "corpus", "instruments", "claim-package-check.py"), rd(GATE, "rb"))
    pkg = os.path.join(root, "corpus", "practice", "pkg")
    build_golden(pkg, root)
    rel = "corpus/practice/pkg"
    wr(os.path.join(root, "LOG.md"), "# LOG\n\nround-86 probe lane\n\n" + rel + "\n")
    wr(os.path.join(root, "SHONEN.md"), "# SHONEN\n\nround-86 probe lane\n\n" + rel + "\n")
    return root


def build_golden(pkg, lane):
    shutil.rmtree(pkg, ignore_errors=True)
    shutil.copytree(R85PKG, pkg)
    for sid in ("S122", "S123"):
        wr(os.path.join(pkg, "evidence", sid + ".txt"),
           rd(os.path.join(lane, "corpus", "source-snapshots", "round-86", sid + ".txt"), "rb"))
    man = json.loads(rd(os.path.join(pkg, "evidence", "manifest.json")))
    head = man["expected_head_sha256"]
    arts = []
    for sid in ("S119", "S120", "S121", "S122", "S123"):
        b = rd(os.path.join(pkg, "evidence", sid + ".txt"), "rb")
        arts.append({"path": sid + ".txt", "sha256": sha(b), "bytes": len(b),
                     "polarity": "positive", "note": "probe copy of " + sid})
    man["sequence"] = 2
    man["artifacts"] = arts
    man["redactions"] = [{"artifact": a["path"], "path": a["path"],
                          "artifact_sha256": a["sha256"],
                          "scanned_artifact_sha256": a["sha256"],
                          "producer": "MutC2Counter", "verifier": "MutC2Probe",
                          "verifier_receipt": "scratch", "removed": [],
                          "note": "public capture; zero bytes removed"} for a in arts]
    man["expected_head_sha256"] = head
    mb = (json.dumps(man, indent=1) + "\n").encode()
    wr(os.path.join(pkg, "evidence", "manifest.json"), mb)
    st = json.loads(rd(os.path.join(pkg, "status.json")))
    st["manifest_sha256"] = sha(mb)
    wr(os.path.join(pkg, "status.json"), json.dumps(st, indent=1) + "\n")
    rep = rd(os.path.join(pkg, "report.md"))
    rep = re.sub(r"^# .*$", lambda m: HEAD, rep, count=1, flags=re.M)
    rep = re.sub(r"^## Pricing\s*$.*?(?=^## )", GOOD_PRICING + "\n", rep, count=1, flags=re.M | re.S)
    for sid in ("S122", "S123"):
        b = rd(os.path.join(pkg, "evidence", sid + ".txt"), "rb")
        line = "- evidence/%s.txt sha256 %s polarity: positive\n" % (sid, sha(b))
        if line not in rep:
            rep = rep.replace("\n## Pricing", line + "\n## Pricing", 1)
    rep = rep.replace("Package kind:", "Record: https://hackerone.com/reports/1997312\nOriginal: https://hackerone.com/reports/1913733\nPackage kind:", 1)
    wr(os.path.join(pkg, "report.md"), rep)


# ---------------------------------------------------------------- probes

FIELD_LINES = {
    "program": "price-program: ibb",
    "payer": "price-payer: internet-bug-bounty",
    "severity": "price-severity: medium",
    "reward-at-disclosure": "price-reward-at-disclosure: 2400 USD",
    "platform-bounty-flag": "price-platform-bounty-flag: true",
    "original-report": "price-original-report: 1913733",
    "reward-current-policy": "price-reward-current-policy: ended 2026-01-31",
    "kev": "price-kev: not-listed catalogVersion 2026.10.23",
    "cve": "price-cve: CVE-2023-28319",
}
DEFAULT_QUOTES = [
    "> I would like to especially highlight the awesome Internet Bug Bounty project, which has paid the bounties for us for many years.",
    "> There is no longer a curl bug-bounty program. It officially stops on January 31, 2026.",
    "> Bug bounty: 2400 USD",
]


def report_fields(over=None, quotes=None):
    fields = dict(FIELD_LINES)
    fields.update(over or {})
    body = ["## Pricing", ""] + [fields[k] for k in
                                 ("program", "payer", "severity", "reward-at-disclosure",
                                  "platform-bounty-flag", "original-report",
                                  "reward-current-policy", "kev", "cve")] + [""]
    body += (quotes if quotes is not None else DEFAULT_QUOTES)
    return HEAD + "\n\n" + RECORD + "\n" + ORIGINAL + "\n\n" + "\n".join(body) + "\n\n## Next\n"


def probe_cases():
    """(probe_id, mutant_id, kind, lane_edit, report_override, pkg_edit)

    kind 'pricing' runs --pricing-only on a standalone report; kind 'pkg' runs
    the full counter on lane/corpus/practice/pkg.
    """
    def drop_line(round_, sid, needle):
        def fn(lane):
            p = os.path.join(lane, "corpus", "source-snapshots", round_, sid + ".txt")
            text = rd(p)
            assert needle in text, (sid, needle)
            wr(p, text.replace(needle, "", 1))
        return fn

    def set_line(round_, sid, needle, repl):
        def fn(lane):
            p = os.path.join(lane, "corpus", "source-snapshots", round_, sid + ".txt")
            text = rd(p)
            assert needle in text, (sid, needle)
            wr(p, text.replace(needle, repl, 1))
        return fn

    def set_handle(lane):
        p = os.path.join(lane, "corpus", "source-snapshots", "round-86", "S122.txt")
        d = json.loads(rd(p))
        d["team"]["handle"] = "curl"
        wr(p, json.dumps(d, separators=(",", ":")))

    def flag_nonstrict(lane):
        """has_bounty? = 1: not `is True`, but truthy (JSON number)."""
        p = os.path.join(lane, "corpus", "source-snapshots", "round-86", "S122.txt")
        d = json.loads(rd(p))
        d["has_bounty?"] = 1
        wr(p, json.dumps(d, separators=(",", ":")))

    def kev_listed(lane):
        p = os.path.join(lane, "corpus", "source-snapshots", "round-35", "S052.txt")
        wr(p, rd(p) + '\n{"cveID": "CVE-2023-28319"}\n')

    def pkg_symlink(lane):
        pkg = os.path.join(lane, "corpus", "practice", "pkg")
        art = os.path.join(pkg, "evidence", "S122.txt")
        os.unlink(art)
        os.symlink(os.path.join(lane, "corpus", "source-snapshots", "round-86", "S122.txt"), art)

    def pkg_only_s122(lane):
        pkg = os.path.join(lane, "corpus", "practice", "pkg")
        os.unlink(os.path.join(pkg, "evidence", "S123.txt"))

    def pkg_lying_recorded(lane):
        pkg = os.path.join(lane, "corpus", "practice", "pkg")
        p = os.path.join(pkg, "evidence", "manifest.json")
        man = json.loads(rd(p))
        for art in man["artifacts"]:
            if art["path"] == "S122.txt":
                art["sha256"] = "f" * 64
        for rec in man["redactions"]:
            if rec["artifact"] == "S122.txt":
                rec["artifact_sha256"] = rec["scanned_artifact_sha256"] = "f" * 64
        wr(p, json.dumps(man, indent=1) + "\n")

    def lane_manifest_lie(lane):
        p = os.path.join(lane, "corpus", "source-snapshots", "round-86", "manifest.json")
        man = json.loads(rd(p))
        for src in man["sources"]:
            if src["id"] == "S122":
                src["sha256"] = "f" * 64
        wr(p, json.dumps(man, indent=1) + "\n")

    def pkg_other_bytes_lane_agrees(lane):
        pkg = os.path.join(lane, "corpus", "practice", "pkg")
        art = os.path.join(pkg, "evidence", "S122.txt")
        b = rd(art, "rb") + b"\n"
        wr(art, b)
        h = sha(b)
        p = os.path.join(pkg, "evidence", "manifest.json")
        man = json.loads(rd(p))
        for a in man["artifacts"]:
            if a["path"] == "S122.txt":
                a["sha256"] = h
                a["bytes"] = len(b)
        for rec in man["redactions"]:
            if rec["artifact"] == "S122.txt":
                rec["artifact_sha256"] = rec["scanned_artifact_sha256"] = h
        wr(p, json.dumps(man, indent=1) + "\n")
        lp = os.path.join(lane, "corpus", "source-snapshots", "round-86", "manifest.json")
        lm = json.loads(rd(lp))
        for src in lm["sources"]:
            if src["id"] == "S122":
                src["sha256"] = h
        wr(lp, json.dumps(lm, indent=1) + "\n")

    def log_without_shonen(lane):
        wr(os.path.join(lane, "SHONEN.md"), "# SHONEN\n\nno package named here\n")

    def no_gate(lane):
        os.unlink(os.path.join(lane, "corpus", "instruments", "claim-package-check.py"))

    def gate_stub(lane, body):
        wr(os.path.join(lane, "corpus", "instruments", "claim-package-check.py"),
           "#!/usr/bin/env python3\nimport sys\n" + body + "\n")

    def gate_rc0_defect(lane):
        gate_stub(lane, 'print("package=x rules=8 pass=0 fail=8 verdict=DEFECT exit=0")\nsys.exit(0)')

    def gate_rc3_wellformed(lane):
        gate_stub(lane, 'print("package=x rules=8 pass=8 fail=0 verdict=WELL-FORMED exit=3")\nsys.exit(3)')

    def short_quote_report():
        return report_fields(quotes=[DEFAULT_QUOTES[0], DEFAULT_QUOTES[1], "> Severity: Medium"])

    def no_cve_heading_report():
        return report_fields().replace("CVE-2023-28319", "CVE-2025-9086", 1)

    NO_PAYER_QUOTE = ["> It officially stops on January 31, 2026.",
                      "> There is no longer a curl bug-bounty program.",
                      "> Bug bounty: 2400 USD"]
    NO_END_QUOTE = ["> There is no longer a curl bug-bounty program.",
                    "> Bug bounty: 2400 USD",
                    "> There is no bug bounty and the curl project never offers rewards for reported vulnerabilities."]

    return [
        # survivor probes: each one must flip the pristine verdict for its mutant
        ("p_e0_head_no_cve", "e0_head_no_cve", "pricing", None, no_cve_heading_report, None),
        ("p_e0_url_missing", "e0_url_always_true", "pricing", None,
         lambda: report_fields().replace(RECORD + "\n", "", 1), None),
        ("p_e0_no_hash_prefix", "e0_head_no_hash_prefix", "pricing", None,
         lambda: report_fields().replace(HEAD, HEAD[2:], 1), None),
        ("p_e4_min10_16char_quote", "e4_min_quote_10", "pricing", None, short_quote_report, None),
        ("p_e4_min1_16char_quote", "e4_min_quote_1", "pricing", None, short_quote_report, None),
        ("p_payer_no_handle", "payer_drop_handle_conjunction", "pricing", set_handle,
         lambda: report_fields({"program": "price-program: curl"}), None),
        ("p_payer_no_s123", "payer_drop_s123_conjunction", "pricing",
         drop_line("round-86", "S123", "Internet Bug Bounty project, which has paid the bounties for us"),
         lambda: report_fields(quotes=NO_PAYER_QUOTE), None),
        ("p_policy_no_endline", "policy_drop_end_line", "pricing",
         drop_line("round-86", "S123", "It officially stops on January 31, 2026."),
         lambda: report_fields(quotes=NO_END_QUOTE), None),
        ("p_policy_no_s121", "policy_drop_s121_conjunction", "pricing",
         drop_line("round-85", "S121", "There is no bug bounty and"), None, None),
        ("p_severity_no_s120", "severity_drop_s120_agreement", "pricing",
         set_line("round-85", "S120", "Severity: Medium", "Severity: High"), None, None),
        ("p_flag_truthy", "flag_truthy_not_strict_true", "pricing", flag_nonstrict, None, None),
        ("p_original_no_corroboration", "original_report_drop_s120_corroboration", "pricing",
         drop_line("round-85", "S120", "Original report: https://hackerone.com/reports/1913733"),
         None, None),
        ("p_kev_always_not_listed", "kev_always_not_listed", "pricing", kev_listed, None, None),
        ("p_e2_lying_recorded_digest", "e2_drop_recorded_artifact_digest", "pkg", None, None,
         pkg_lying_recorded),
        ("p_e2_no_manifest_binding", "e2_drop_manifest_digest", "pkg", lane_manifest_lie, None, None),
        ("p_e2_drop_byte_equality", "e2_drop_byte_equality", "pkg", pkg_other_bytes_lane_agrees,
         None, None),
        ("p_e2_symlink_evidence", "e2_follow_symlinks", "pkg", pkg_symlink, None, None),
        ("p_e2_one_source", "e2_found_subset", "pkg", pkg_only_s122, None, None),
        ("p_e5_one_doc", "e5_or_instead_of_and", "pkg", log_without_shonen, None, None),
        ("p_allok_only_e1_fails", "allok_skips_e1", "pkg", no_gate, None, None),
        # over-strictness demonstration on the golden package
        ("p_e2_require_s120", "e2_require_third_source", "pkg", None, None, None),
        # r85-survivor classes at r86
        ("p_reward_case", "reward_case_insensitive", "pricing", None,
         lambda: report_fields({"reward-at-disclosure": "price-reward-at-disclosure: 2400 usd"}), None),
        ("p_severity_case", "severity_case_sensitive", "pricing", None,
         lambda: report_fields({"severity": "price-severity: Medium"}), None),
        ("p_e1_rc0_bad", "e1_drop_rc_check", "pkg", gate_rc0_defect, None, None),
        ("p_e1_rc3_good", "e1_drop_verdict_check", "pkg", gate_rc3_wellformed, None, None),
        ("p_e4_ws_quote", "e4_quotes_not_normalized", "pricing", None,
         lambda: report_fields(quotes=[DEFAULT_QUOTES[0], DEFAULT_QUOTES[1],
                                       "> There is no bug bounty  and the curl project never offers rewards for reported vulnerabilities."]), None),
        ("p_e4_kev_quote", "e4_pool_includes_kev", "pricing", None,
         lambda: report_fields(quotes=[DEFAULT_QUOTES[0], DEFAULT_QUOTES[1],
                                       '> "vendorProject": "Arista",']), None),
    ]


def run_probe(case, mutant_path):
    pid, mid, kind, lane_edit, rep_edit, pkg_edit = case
    root = os.path.join(S, "probes", pid)
    shutil.rmtree(root, ignore_errors=True)
    os.makedirs(root)
    lane = os.path.join(root, "lane")
    shutil.copytree(os.path.join(S, "lane0"), lane, symlinks=True)
    if lane_edit:
        lane_edit(lane)
    if pkg_edit:
        pkg_edit(lane)
    if kind == "pricing":
        report = os.path.join(root, "report.md")
        wr(report, rep_edit() if rep_edit else report_text())
        args = ["--lane", lane, "--pricing-only", report]
    else:
        args = ["--lane", lane, "--pkg", os.path.join(lane, "corpus", "practice", "pkg")]
    base = run([sys.executable, "-B", FROZEN] + args)[1]
    mut = run([sys.executable, "-B", mutant_path] + args)[1]
    wr(os.path.join(root, "pristine.txt"), base)
    wr(os.path.join(root, "mutant.txt"), mut)
    return pid, base, mut


def main():
    got = sha(rd(FROZEN, "rb"))
    if got != FROZEN_SHA:
        raise SystemExit("frozen counter sha drift: %s" % got)
    os.makedirs(os.path.join(S, "out"), exist_ok=True)
    write_driver(os.path.join(S, "drive.sh"))

    pristine_text = run_controls(FROZEN, os.path.join(S, "fx"), "controls-pristine")
    base_sig = sig(parse(pristine_text))
    base_details = details(pristine_text)

    mutants = gen_mutants()
    rows = []
    for mid, path, msha in mutants:
        text = run_controls(path, os.path.join(S, "fx"), "controls-" + mid)
        msig = sig(parse(text))
        changed = []
        for (n0, rc0, f0), (n1, rc1, f1) in zip(base_sig, msig):
            if (rc0, f0) != (rc1, f1):
                changed.append(n0)
        detail_changed = sorted(details(text) - base_details) if not changed else []
        rows.append({"mutant": mid, "sha256": msha, "verdict": "killed" if changed else "survived",
                     "killed_by": changed, "detail_only": detail_changed})

    build_lane0(os.path.join(S, "lane0"))
    probe_rows = []
    mutant_by_id = {m[0]: m[1] for m in mutants}
    for case in probe_cases():
        if case[1] not in mutant_by_id:
            continue
        pid, base, mut = run_probe(case, mutant_by_id[case[1]])
        bs = [(n, "pass" if ok else "FAIL") for n, ok, _ in []]  # unused
        b_sig = re.findall(r"^(LIMB \S+ (?:pass|FAIL)|E2E-RESULT \S+ limbs=\d+ rc=\d+)", base, re.M)
        m_sig = re.findall(r"^(LIMB \S+ (?:pass|FAIL)|E2E-RESULT \S+ limbs=\d+ rc=\d+)", mut, re.M)
        probe_rows.append({"probe": pid, "mutant": case[1],
                           "distinguishes": b_sig != m_sig,
                           "pristine": b_sig, "mutant_out": m_sig})

    result = {"frozen_sha256": FROZEN_SHA, "gate_sha256": sha(rd(GATE, "rb")),
              "n_mutants": len(rows),
              "killed": sum(1 for r in rows if r["verdict"] == "killed"),
              "survived": sum(1 for r in rows if r["verdict"] == "survived"),
              "mutants": rows, "probes": probe_rows,
              "pristine_signature": [[n, rc, list(f)] for n, rc, f in base_sig]}
    wr(os.path.join(S, "results.json"), json.dumps(result, indent=1))
    print(json.dumps({k: result[k] for k in ("n_mutants", "killed", "survived")}))
    for r in rows:
        print("%-36s %-8s %s %s" % (r["mutant"], r["verdict"],
                                    ",".join(r["killed_by"]) or "-",
                                    ("detail-only:" + ",".join(r["detail_only"])) if r["detail_only"] else ""))
    print("--- probes")
    for p in probe_rows:
        print("%-34s %-34s distinguishes=%s" % (p["probe"], p["mutant"], p["distinguishes"]))


if __name__ == "__main__":
    main()
