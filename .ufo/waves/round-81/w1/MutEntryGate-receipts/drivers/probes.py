#!/usr/bin/env python3
"""Negative probes (base gate must FAIL) and positive probes (base must PASS), built from
the frozen S115 manifest. These are the cases B8's --selftest lacks."""
import json
import os
import subprocess
import sys

S = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
MAN = os.path.join(LANE, "corpus/source-snapshots/round-81/manifest.json")
GATE = os.path.join(S, "gate.py")
OUT = os.path.join(S, "probes")
os.makedirs(OUT, exist_ok=True)
man = json.load(open(MAN, encoding="utf-8"))
src = man["sources"][0]
qs = [(q["quote"], q["anchor"]) for q in src["quotes"]]
Q = {i: qs[i - 1][0] for i in range(1, 7)}
A = {i: qs[i - 1][1] for i in range(1, 7)}
recheck = ("recheck: cd %s && python3 corpus/instruments/source-recheck.py --manifest "
           "corpus/source-snapshots/round-81/manifest.json --source S115" % LANE)


def head(source_line="source: S115 — u", verified=True, rc=True, recheck_line=None):
    h = "# probe\n\n" + source_line + "\n"
    if verified:
        h += "verified-at: 2026-11-06\n"
    if rc:
        h += (recheck_line or recheck) + "\n"
    return h + "\n"


def claim(n, body, dash=" \u2014"):
    return "## Claim %s%s c\n\n%s\n" % (n, dash, body)


def span(t, n):
    return '"%s" (S115.txt:%d)' % (t, n)


MK = "Falsifiable rule: x\n\nRejected over-generalization\n\n"
ALL = lambda: "".join(claim(i, "%s\n\n%s" % (span(Q[i], A[i]), MK)) for i in range(1, 7))

NEG = {}
POS = {}
NEG["p_dump_unsectioned"] = head() + "\n".join(span(Q[i], A[i]) for i in range(1, 7)) + "\n"
NEG["p_norule"] = head() + "".join(claim(i, "%s\n\nRejected over-generalization\n" % span(Q[i], A[i]))
                                   for i in range(1, 7))
NEG["p_pins_outside_claims"] = head() + "## Attribution\n\n" + "\n".join(
    span(Q[i], A[i]) for i in range(1, 7)) + "\n\n" + "".join(
    claim(i, "%s\n\n%s" % (span("the", 36), MK)) for i in range(1, 7))
NEG["p_header_no_recheck"] = head(rc=False) + ALL()
NEG["p_header_other_sid"] = head(source_line="source: S114 — u") + ALL()
NEG["p_header_no_verified"] = head(verified=False) + ALL()
NEG["p_header_late"] = ("# probe\n\n" + "filler line\n" * 9 + "source: S115 — u\n"
                        "verified-at: 2026-11-06\n" + recheck + "\n\n" + ALL())
NEG["p_header_dash_missing"] = head(source_line="source: S115 u") + ALL()
NEG["p_header_verified_inline"] = ("# probe\n\nsource: S115 — u\n" + recheck +
                                   "\nsee also verified-at: 2026-11-06 in the log\n\n" + ALL())
NEG["p_header_recheck_suffix"] = head(recheck_line=recheck + " # extra trailing words") + ALL()
NEG["p_claim_unnumbered"] = head() + "".join(
    claim("-", "%s\n\n%s" % (span(Q[i], A[i]), MK)) for i in range(1, 7))
NEG["p_empty_span_claims"] = head() + claim(1, "\n".join(span(Q[i], A[i]) for i in range(1, 7))
                                            + "\n\n" + MK) + "".join(
    claim(i, '"" (S115.txt:36)\n\n' + MK) for i in range(2, 7))
NEG["p_five_claims"] = head() + claim(1, "\n".join(span(Q[i], A[i]) for i in range(1, 7))
                                      + "\n\n" + MK) + "".join(
    claim(i, "%s\n\n%s" % (span(Q[i], A[i]), MK)) for i in range(2, 6))
NEG["p_seven_claims"] = head() + ALL() + claim(7, "%s\n\n%s" % (span(Q[1], A[1]), MK))
NEG["p_rule_no_colon"] = head() + "".join(
    claim(i, "%s\n\nFalsifiable rule x\n\nRejected over-generalization\n\n" % span(Q[i], A[i]))
    for i in range(1, 7))
NEG["p_rule_midline"] = head() + "".join(
    claim(i, "%s\n\nSee Falsifiable rule: x\n\nRejected over-generalization\n\n" % span(Q[i], A[i]))
    for i in range(1, 7))
NEG["p_rejected_midline"] = head() + "".join(
    claim(i, "%s\n\nFalsifiable rule: x\n\nWe discussed Rejected over-generalization here.\n\n"
          % span(Q[i], A[i])) for i in range(1, 7))
NEG["p_span_casefold"] = head() + "".join(
    claim(i, "%s\n\n%s" % (span(Q[i].lower(), A[i]), MK)) for i in range(1, 7))

word26 = " ".join(man["sources"][0] and open(os.path.join(os.path.dirname(MAN), src["path"]),
                                              encoding="utf-8").read().split("\n")[31].split()[:26])
assert Q[2] in word26
NEG["p_overlong_pin"] = head() + claim(1, "%s\n\n%s" % (span(word26, 32), MK)) + "".join(
    claim(i, "%s\n\n%s" % (span(Q[i], A[i]), MK)) for i in (1, 3, 4, 5, 6))
NEG["p_pin_fragment_claims"] = head() + "".join(
    claim(i, "%s\n\n%s" % (span(" ".join(Q[i].split()[:3]), A[i]), MK)) for i in range(1, 7))
NEG["p_span_case_variant_extra"] = head() + claim(1, "\n".join(
    span(Q[i], A[i]) for i in range(1, 7)) + "\n\n" + MK) + "".join(
    claim(i, "%s\n\n%s" % (span(Q[i][0].lower() + Q[i][1:], A[i]), MK)) for i in range(2, 7))
POS["p_two_spans_on_line"] = head() + "".join(
    claim(i, "%s %s\n\n%s" % (span(Q[i], A[i]), span("the", 36), MK)) for i in range(1, 7))
NEG["p_span_padded"] = head() + "".join(
    claim(i, '%s\n\n%s' % (span(" " + Q[i] + " ", A[i]), MK)) for i in range(1, 7))

POS["p_claim_no_dash"] = head() + "".join(
    claim(i, "%s\n\n%s" % (span(Q[i], A[i]), MK), dash="") for i in range(1, 7))
POS["p_claim_zero_pad"] = head() + "".join(
    claim(i, "%s\n\n%s" % (span(Q[i], A[i]), MK)) for i in range(1, 7))


def run(name, text, expect_pass, bucket):
    p = os.path.join(OUT, name + ".md")
    open(p, "w", encoding="utf-8").write(text)
    r = subprocess.run([sys.executable, GATE, "--entry", p, "--manifest", MAN,
                        "--source", "S115", "--lane", LANE],
                       capture_output=True, text=True, env={**os.environ, "TMPDIR": S})
    o = (r.stdout or "").strip().split("\n")
    ok = (r.returncode == 0)
    tag = "OK " if ok == expect_pass else "BAD"
    print("%-30s %-4s expect=%-4s rc=%d %s | %s" % (name, tag, "pass" if expect_pass else "fail",
                                                    r.returncode, o[-1] if o else "",
                                                    o[0] if o else ""))
    return {"name": name, "bucket": bucket, "rc": r.returncode,
            "verdict": o[-1] if o else "", "line": o[0] if o else "",
            "expect": "pass" if expect_pass else "fail", "ok": ok == expect_pass}


rows = [run(n, t, False, "neg") for n, t in NEG.items()]
rows += [run(n, t, True, "pos") for n, t in POS.items()]
json.dump(rows, open(os.path.join(S, "probes.json"), "w"), indent=1)
bad = [r for r in rows if not r["ok"]]
print("SUMMARY neg=%d pos=%d unexpected=%d %s" % (
    len(NEG), len(POS), len(bad), [b["name"] for b in bad]))
