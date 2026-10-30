#!/usr/bin/env python3
"""r47-routed-defects.py — round-47 C1 counter over committed lane evidence.

WHAT IT MEASURES
    The four lane-repo routed defects D5-D8 of the round-46 non-author closure
    (`corpus/lessons/round-46-verifier-spotcheck.md` §7 items D1-D4 are report-side
    and are graded in the round-47 report, not here; §8 items D5-D8 are lane bytes):

    D5  unlanded drafting scaffold inside `corpus/SOURCES.md` — L1 instruction prose
        and ```markdown fences at :113-:123 and :177-:185 with the F29 Search-log
        bullet and both S074 Registry-changes bullets trapped inside the fences,
        never landed as section bullets (fix: land the three bullets in their real
        sections, delete prose and fences, append a correction to the round-46
        lesson's misleading status sentence) — limbs L1, L2, L3.
    D6  three false sentences still standing in the admitted F29 entry
        `corpus/knowledge/github-repository-security-advisories.md` ("all 42 lines
        are body prose" / "the whole capture is that body" at :11 and :89 — the
        capture carries page chrome; "in the order the page states it" at :16 — the
        page states the CVE request before the fix-version material; "the three
        cases at S074.txt:40, :41 and :42" at :111-:112 — :40 forbids
        publish-without-fix, only :41-:42 permit it) — limbs L4, L5, L6, L7 (L7 =
        the lesson erratum naming the dropped seat findings).
    D7  the pinned attempt-2 capture is not reproducible by any committed
        instrument (fix chosen: re-capture with the committed `capture-source.py
        --kind html`, register it as a superseding row S076 per CORPUS rule 2, and
        re-anchor the entry's citations to the new capture) — limbs L8, L9.
    D8  reject (c)'s id reservation silently voided and two pointer/precision gaps
        (fix: `## Leads (unopened)` bullet for the repository-advisories REST API
        page; round-47 lesson notes resolving the ZDI reservation via this round's
        admission and correcting the S068 n=1 precedent wording) — limbs L10, L11.

    Each limb is `fixed` only when the substantive evidence is present in the tree
    under `--root`; the counter is READ-ONLY over the tree it grades: it never
    writes into `--root`, never runs git, and never mutates the lane. Content
    binding per QUALITY R48: absence checks pin the exact false phrases, presence
    checks pin tokens the defect text itself names, and L8/L9 verify the manifest
    sha and that every re-anchored span locates in the committed capture.

    Line-number note (QUALITY R6 exception, recorded): landing the D5 bullets in
    their real sections moves `corpus/SOURCES.md` line numbers below :90; the
    round-47 lesson records the shift and names the files whose SOURCES.md line
    anchors moved. The F29 entry keeps its own line count (same-line corrections),
    so entry-line anchors stay valid.

USAGE
    python3 corpus/instruments/r47-routed-defects.py --root TREE [--baseline EXPORT] [--work DIR]
OUTPUT
    one `limb L<n> fixed=0|1 read=<token>` line each, then
    `routed-defects total=11 fixed=<k> unresolved=<m> exit=0|1`
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

SELF = os.path.realpath(__file__)
INSTRUMENTS = os.path.dirname(SELF)
LANE_CD = "/home/vgpnk/Projects/shokunin/kasegi-shokunin"
ENTRY = "corpus/knowledge/github-repository-security-advisories.md"
SOURCES = "corpus/SOURCES.md"
MAN_REL = "corpus/source-snapshots/round-47/manifest.json"
SNAP76_REL = "corpus/source-snapshots/round-47/S076.txt"
MAN_SHA = "6168521b5f5555fd06f2a63c1dc0e8543cd89f8146f79f684daf586f32f35e9b"
LESSON46 = "corpus/lessons/round-46.md"
LESSON47 = "corpus/lessons/round-47.md"

SCAFFOLD_PHRASES = [
    "The `## Search log` bullet to append",
    "Append inside `## Search log`",
    "`## Registry changes` bullets to append",
    "Append at the end of the `## Registry changes` section",
]
FALSE_PHRASES = [
    "all 42 lines are body prose",
    "the whole capture is that body",
    "in the order the page states it",
    "three cases",
]


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def norm(s: str) -> str:
    s = s.replace("\u201c", '"').replace("\u201d", '"').replace("\u2018", "'").replace("\u2019", "'")
    s = s.replace("**", "").replace("*", "").replace("`", "")
    return re.sub(r"\s+", " ", s).strip()


def live_lines(text: str) -> list[str]:
    out = []
    fence = False
    for ln in text.splitlines():
        st = ln.strip()
        if st.startswith("```") or st.startswith("~~~"):
            fence = not fence
            continue
        if fence or not st:
            continue
        clean = re.sub(r"<!--.*?-->", " ", ln)
        clean = clean.strip()
        if not clean or clean.startswith("<!--"):
            continue
        out.append(clean)
    return out


def txt(root: str, rel: str) -> str | None:
    p = os.path.join(root, rel)
    try:
        return open(p, encoding="utf-8", errors="replace").read()
    except OSError:
        return None


def section(text: str, heading: str) -> str:
    """The rendered (fence-skipping) body of a `## <heading>` section."""
    lines = text.splitlines()
    out, inside, fence = [], False, False
    for ln in lines:
        st = ln.strip()
        if st.startswith("```") or st.startswith("~~~"):
            fence = not fence
            continue
        if fence:
            continue
        if re.match(r"^##\s+", ln):
            inside = ln.strip().startswith("## " + heading)
            continue
        if inside:
            out.append(ln)
    return "\n".join(out)


def body_range(root: str) -> tuple[int, int] | None:
    try:
        man = json.load(open(os.path.join(root, MAN_REL), encoding="utf-8"))
        rec = [x for x in man["sources"] if x.get("id") == "S076"]
        if len(rec) != 1:
            return None
        lo, hi = rec[0]["body_lines"]
        return int(lo), int(hi)
    except Exception:
        return None


def l1(root: str) -> tuple[bool, str]:
    t = txt(root, SOURCES) or ""
    hits = [p for p in SCAFFOLD_PHRASES if p in t]
    return not hits, ("scaffold-phrases=%d" % len(hits)) if hits else "scaffold-phrases=0"


def l2(root: str) -> tuple[bool, str]:
    raw = txt(root, SOURCES) or ""
    fences = len(re.findall(r"^\s*```", raw, re.M))
    bad = []
    if fences:
        bad.append("fence-markers=%d" % fences)
    search = section(raw, "Search log")
    if not re.search(r"^- Repository security advisory lifecycle sweep \(round 46 attempt 2, frontier F29\); question:", search, re.M):
        bad.append("search-log-bullet-absent")
    reg = section(raw, "Registry changes")
    if not re.search(r"^- S074 row added: new row", reg, re.M):
        bad.append("s074-row-bullet-absent")
    if not re.search(r"^- Capture directory note: `corpus/source-snapshots/round-46-a2/` exists beside", reg, re.M):
        bad.append("capture-note-bullet-absent")
    return not bad, ("bad=" + ",".join(bad)) if bad else "bullets-landed fences=0"


def l3(root: str) -> tuple[bool, str]:
    t = txt(root, LESSON46) or ""
    m = re.search(r"^## Corrections \(round 47\)\s*$", t, re.M)
    if not m:
        return False, "corrections-section-absent"
    tail = t[m.start():]
    ok = ("SOURCES.md" in tail) and ("fence" in tail) and ("Search log" in tail or "Registry changes" in tail)
    return ok, "corrections-section-present content=%d" % int(ok)


def entry_text(root: str) -> str | None:
    return txt(root, ENTRY)


def l4(root: str) -> tuple[bool, str]:
    t = entry_text(root)
    if t is None:
        return False, "entry-absent"
    bad = [p for p in FALSE_PHRASES[:2] if p in t]
    if bad:
        return False, "false-phrases=%d" % len(bad)
    if not re.search(r"\bchrome\b", t):
        return False, "chrome-note-absent"
    return True, "prose-claims-corrected chrome=present"


def l5(root: str) -> tuple[bool, str]:
    t = entry_text(root)
    if t is None:
        return False, "entry-absent"
    if FALSE_PHRASES[2] in t:
        return False, "order-phrase-still-present"
    if "CVE request before the fix-version" not in t:
        return False, "corrected-order-sentence-absent"
    return True, "order-claim-corrected"


def l6(root: str) -> tuple[bool, str]:
    t = entry_text(root)
    if t is None:
        return False, "entry-absent"
    if re.search(r"three cases[^.]*let a maintainer publish", t):
        return False, "three-cases-still-present"
    if "two cases" not in t:
        return False, "two-cases-absent"
    if "wait to disclose the issue when the fix is ready" not in t:
        return False, "forbidding-case-quote-absent"
    return True, "fix-version-cases-corrected"


def l7(root: str) -> tuple[bool, str]:
    for rel in (LESSON47, LESSON46):
        t = txt(root, rel) or ""
        if "R46bW2RevEntryClaims" in t and "R46bConnPatterns" in t and re.search(r"dropped|not carried|erratum", t, re.I):
            return True, "dropped-findings-named in=%s" % rel
    return False, "dropped-findings-unnamed"


def l8(root: str) -> tuple[bool, str]:
    raw = txt(root, SOURCES) or ""
    hits = [ln for ln in live_lines(raw) if re.match(r"^ {0,3}\|\s*S076\s*\|", ln)]
    if len(hits) != 1:
        return False, "row-S076=absent-or-duplicated hits=%d" % len(hits)
    c = [x.strip() for x in hits[0].strip().strip("|").split("|")]
    if len(c) != 11:
        return False, "row-S076-cells=%d" % len(c)
    bad = []
    if not c[6].startswith("supersedes S074"):
        bad.append("teaches-not-supersedes")
    if c[2] != "docs":
        bad.append("kind")
    if c[3] != "A":
        bad.append("tier")
    if c[7] != "mined":
        bad.append("status")
    if c[8] != "2026-10-30":
        bad.append("opened")
    if "github-repository-security-advisories.md" not in c[10]:
        bad.append("used-by")
    if "round-47/S076.txt" not in c[5] or "9bd8ab57dac9cc605355c60831f51e02b92f5e34990aa99a49566d207e6bbb38" not in c[5]:
        bad.append("anchor-sha-or-path")
    if not re.search(r"(?:lines?|L)\s*558\s*[-\u2013]\s*L?600", c[5]):
        bad.append("anchor-locator")
    man = os.path.join(root, MAN_REL)
    if not os.path.isfile(man) or sha(open(man, "rb").read()) != MAN_SHA:
        bad.append("manifest-not-pinned")
    else:
        p2 = subprocess.run([sys.executable, "-I", os.path.join(INSTRUMENTS, "source-recheck.py"),
                             "--manifest", man, "--source", "S076"], capture_output=True, text=True, timeout=120)
        if p2.returncode != 0 or "S076:sha256 OK" not in p2.stdout:
            bad.append("source-recheck-rc=%d" % p2.returncode)
    return not bad, ("row-S076=ok" if not bad else "bad=" + ",".join(bad))


def l9(root: str) -> tuple[bool, str]:
    t = entry_text(root)
    if t is None:
        return False, "entry-absent"
    old = t.count("S074.txt:")
    if old:
        return False, "old-citations=%d" % old
    rng = body_range(root)
    if rng is None:
        return False, "manifest-body-lines-unreadable"
    snap = (txt(root, SNAP76_REL) or "").splitlines()
    cite = r"\s*\(`?S076\.txt:(\d+)(?:-(\d+))?`?"
    curly = "\u201c([^\u201d]+)\u201d"
    spans = re.findall(curly + cite, t) + re.findall('"([^"]+)"' + cite, t, re.S)
    quoted = re.findall(curly, t) + [q for q in re.findall('"([^"]+)"', t, re.S) if len(q.split()) >= 4]
    passed, failed = 0, 0
    for q, a, b in spans:
        a = int(a)
        b = int(b) if b else a
        window = norm(" ".join(snap[max(a - 1, 0):b]))
        nq = norm(q)
        if len(nq.split()) <= 25 and nq and rng[0] <= a <= b <= rng[1] and b - a <= 11 and nq in window:
            passed += 1
        else:
            failed += 1
    uncited = len(quoted) - len(spans)
    ok = failed == 0 and uncited <= 0 and passed >= 20
    return ok, "spans=%d located=%d failed=%d uncited=%d" % (len(spans), passed, failed, max(uncited, 0))


def l10(root: str) -> tuple[bool, str]:
    raw = txt(root, SOURCES) or ""
    leads = section(raw, "Leads (unopened)")
    if not leads.strip():
        return False, "leads-section-absent"
    hit = [ln for ln in leads.splitlines() if ln.lstrip().startswith("- ")
           and "docs.github.com/en/rest/security-advisories" in ln]
    if not hit:
        return False, "rest-api-lead-bullet-absent"
    return True, "rest-api-lead-bullet-present"


def l11(root: str) -> tuple[bool, str]:
    t = txt(root, LESSON47) or ""
    if not t:
        return False, "round-47-lesson-absent"
    a = "ZDI" in t and "reservation" in t
    b = "S068" in t and "one GHSA advisory entry" in t
    return a and b, "zdi-reservation=%d s068-precision=%d" % (int(a), int(b))


LIMBS = [("L1", l1), ("L2", l2), ("L3", l3), ("L4", l4), ("L5", l5), ("L6", l6),
         ("L7", l7), ("L8", l8), ("L9", l9), ("L10", l10), ("L11", l11)]

DEFECT_OF = {"L1": "D5", "L2": "D5", "L3": "D5", "L4": "D6", "L5": "D6", "L6": "D6",
             "L7": "D6", "L8": "D7", "L9": "D7", "L10": "D8", "L11": "D8"}


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", required=True)
    ap.add_argument("--baseline", default=None, help="unused; kept for freeze-check compatibility")
    ap.add_argument("--work", default=None)
    a = ap.parse_args(argv)
    if not os.path.isdir(a.root):
        print("routed-defects total=11 fixed=0 unresolved=11 exit=1 (root-missing)")
        return 1
    fixed = 0
    for name, fn in LIMBS:
        try:
            ok, read = fn(a.root)
        except Exception as exc:  # a limb that raises is red, never green
            ok, read = False, "limb-error=%s" % type(exc).__name__
        print("limb %s (%s) fixed=%d read=%s" % (name, DEFECT_OF[name], int(bool(ok)), read))
        fixed += int(bool(ok))
    total = len(LIMBS)
    print("routed-defects total=%d fixed=%d unresolved=%d exit=%d" % (total, fixed, total - fixed, 0 if fixed == total else 1))
    return 0 if fixed == total else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
