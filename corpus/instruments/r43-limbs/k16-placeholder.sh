#!/usr/bin/env bash
# ExecK16Placeholder.sh -- round-43 K16 limb: the placeholder-section promise check.
#
# Sourceable:   . ExecK16Placeholder.sh
# Call:         check_k16 <export-root>      -> prints one payload line, exit 0|1
#
# The instrument grades committed narrative bytes, never a working tree: it is
# handed an export root (the tree `git -C <lane> archive <ref> | tar -x` writes)
# and reads only files below it.
#
# Placeholder shape (RD42-4).  A scanned file is corpus/lessons/*.md, LOG.md,
# SCORECARD.md and SHONEN.md.  A *section* is a line matching `^## ` outside a
# fenced block; its body runs to the next `^# ` or `^## ` line outside a fence.
# A section *promises* when its opening stanza -- the first non-blank body lines
# up to the first blank line, fenced lines excluded -- carries one of five
# promise clauses:
#
#   schedule       `when the <subject> reports`  (subject: 1-60 chars, no
#                  `; : , .` quote, backtick, bracket or pipe -- a clause
#                  boundary or a quoted span means the text is describing a
#                  promise, not making one)
#   to-be-filled   `to be filled`
#   tbd            `TBD` as a whole token
#   pending-wave   `pending the <subject> wave` (same subject rule)
#   placeholder    `the|this section|subsection|entry|block is|remains|stays
#                  a|an placeholder|stub`
#
# Text inside backticked spans and double-quoted spans is stripped before the
# clause test: a quoted clause is evidence about a promise, never the promise.
# A line inside a fenced block is never a section heading and never a promise;
# promise vocabulary that sits there is counted as `fenced` and ignored.
#
# A promise is *resolved* when, later in the same file, a line outside a fenced
# block carries the literal `Correction (round 43)` and names the section
# heading (the heading text after `## ` as a raw substring -- backticks and
# `## ` prefixes are allowed and are not stripped).  Append-only: the promise
# line is never rewritten; the correction names it.
#
# Payload: sections=<n> scanned `## ` sections, promises=<p> sections whose
# opening stanza promises, fenced=<k> promise-vocabulary lines ignored inside
# fenced blocks, unresolved=<u> promising sections with no naming correction.
# closed=1 only when sections>0, promises>0 and unresolved=0: a tree with no
# section or no promise is not a pass (an erased promise must not close the
# check), and any unresolved promise keeps it open.
#
# Limit: only the opening stanza is graded, so a promise parked mid-section is
# invisible by design -- the shape is "the section announces that it will be
# filled later", and quoted or tabulated narrative cannot trip it.

check_k16() {
    local root="${1:-.}"
    K16_ROOT="$root" python3 - <<'K16_PY'
import glob
import os
import re
import sys

ROOT = os.environ.get("K16_ROOT", ".")
VERBOSE = os.environ.get("K16_VERBOSE", "") not in ("", "0")

# A promise clause is a schedule/absence claim, not any occurrence of its
# vocabulary.  The subject of a schedule clause carries no clause boundary and
# no quote opener, so a narrative echo that quotes the promise cannot match.
_SUBJ = r"[^;:,.\n`\"'()|]{1,60}?"
CLAUSES = (
    ("schedule", re.compile(r"\bwhen the " + _SUBJ + r"\breports\b", re.I)),
    ("to-be-filled", re.compile(r"\bto be filled\b", re.I)),
    ("tbd", re.compile(r"\bTBD\b")),
    ("pending-wave", re.compile(r"\bpending the " + _SUBJ + r"\bwave\b", re.I)),
    ("placeholder", re.compile(
        r"\b(?:this|the) (?:section|subsection|entry|block)\s+"
        r"(?:is|remains|stays)\s+(?:a |an )?(?:placeholder|stub)\b", re.I)),
)
CORRECTION = "Correction (round 43)"
FENCE_RX = re.compile(r"^(```+|~~~+)")
HEADING_RX = re.compile(r"^#{1,2} ")


def strip_quoted(line):
    """Drop backticked and double-quoted spans: quoted text is not a promise."""
    out = []
    i = 0
    n = len(line)
    while i < n:
        c = line[i]
        if c == "`":
            j = line.find("`", i + 1)
            if j >= 0:
                i = j + 1
                continue
            i += 1
            continue
        if c == '"':
            j = line.find('"', i + 1)
            if j >= 0:
                i = j + 1
                continue
            out.append(c)
            i += 1
            continue
        out.append(c)
        i += 1
    return "".join(out)


def clauses(line):
    """Names of the promise clauses the (unquoted) line carries."""
    return [name for name, rx in CLAUSES if rx.search(line)]


def scan_file(path):
    """Return (sections, fenced_promise_lines) for one file."""
    with open(path, encoding="utf-8", errors="replace") as fh:
        lines = fh.read().split("\n")
    sections = []
    fenced = 0
    fence = None
    section = None
    for number, line in enumerate(lines, 1):
        m = FENCE_RX.match(line.strip())
        if m:
            tok = m.group(1)[0]
            if fence is None:
                fence = tok
            elif fence == tok:
                fence = None
            continue
        if fence is not None:
            if clauses(strip_quoted(line)):
                fenced += 1
            continue
        if HEADING_RX.match(line):
            if section is not None:
                sections.append(section)
            section = {"heading": line, "line": number, "body": []}
            continue
        if section is not None:
            section["body"].append((number, line))
    if section is not None:
        sections.append(section)
    return lines, sections, fenced


def opening_stanza(body):
    stanza = []
    seen = False
    for number, line in body:
        if line.strip() == "":
            if seen:
                break
            continue
        seen = True
        stanza.append((number, line))
    return stanza


def resolved(lines, section):
    heading = section["heading"][3:].strip()
    for index in range(section["line"], len(lines)):
        line = lines[index]
        if CORRECTION in line and heading in line:
            # The naming line itself must not sit inside a fence.
            fence = None
            for prior in lines[:index]:
                m = FENCE_RX.match(prior.strip())
                if m:
                    tok = m.group(1)[0]
                    fence = tok if fence is None else (None if fence == tok else fence)
            if fence is None:
                return True
    return False


def main():
    files = sorted(glob.glob(os.path.join(ROOT, "corpus/lessons/*.md")))
    files += [os.path.join(ROOT, name) for name in ("LOG.md", "SCORECARD.md", "SHONEN.md")]
    if not os.path.isdir(ROOT):
        sys.stderr.write("K16 root-not-found root=%s\n" % ROOT)
        sys.stdout.write("payload=sections=0,promises=0,fenced=0,unresolved=0 closed=0\n")
        return 1
    sections = 0
    promises = 0
    fenced = 0
    unresolved = 0
    for path in files:
        if not os.path.isfile(path):
            continue
        lines, found, fenced_here = scan_file(path)
        fenced += fenced_here
        sections += len(found)
        for section in found:
            hit = [c for _n, l in opening_stanza(section["body"]) for c in clauses(strip_quoted(l))]
            if not hit:
                continue
            promises += 1
            if resolved(lines, section):
                continue
            unresolved += 1
            if VERBOSE:
                sys.stderr.write(
                    "K16 unresolved file=%s line=%d heading=%s clause=%s\n"
                    % (os.path.relpath(path, ROOT), section["line"],
                       section["heading"][3:].strip(), hit[0]))
    closed = 1 if (sections > 0 and promises > 0 and unresolved == 0) else 0
    sys.stdout.write(
        "payload=sections=%d,promises=%d,fenced=%d,unresolved=%d closed=%d\n"
        % (sections, promises, fenced, unresolved, closed))
    return 0 if closed else 1


sys.exit(main())
K16_PY
}
