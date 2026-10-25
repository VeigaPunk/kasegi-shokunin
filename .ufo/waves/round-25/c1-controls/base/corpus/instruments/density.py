#!/usr/bin/env python3
"""kasegi r14 — runnable reimplementation of the r13 SKILL.md density census.

Usage: python3 density.py <SKILL.md> [--label LABEL]

Method (recorded in /tmp/kasegi-r13/scout-thin.md §1; cite rule lifted
verbatim from r13's own extractor /tmp/kasegi-r13/extract.py):
  * Segment the file into blocks at every line matching ^#{2,3} (a '## ' or
    '### ' heading starts a new block). Front matter before the first '## ' is
    not a block. The heading line belongs to its block.
  * nb      non-blank lines in the block (heading included, blanks excluded)
  * cites   occurrences of backticked `token`s that are "path-like"
  * tbl     markdown table DATA rows (leading '|', separator rows skipped)
            that are concrete: contain a digit or any backticked token
  * num     UNIQUE numeric tokens, excluding bare years (19xx/20xx), tokens
            letter-adjacent (AR14, H1, I8, K3, b1k, 3CX, 8x8 -> their digit
            fragments do not count), section-reference fragments (§A.2),
            markdown enumeration markers ("3. "), and date/time stamps
            (2026-09-05, T17:24:52Z -> neither the year nor 2-digit date
            parts count). Numbers are taken from prose and from backticked
            spans that are letter-free (`4002776` counts, `finding_count≥1`
            does not); comma-joined numbers are unified (7,224 -> 7224).
  * sig     UNIQUE ALL-CAPS signatures: pure A-Z parts (after '_' splitting)
            of length >= 5, scanned across prose AND non-path-like code
            spans (`RECEIPT EXISTS — DO NOT RESUBMIT` counts), but NOT
            inside path-like citations (those already count as cites, so
            `INGESTION.md`/`README.md` are never double-counted). State and
            table vocabulary is excluded via GENERIC_SIG below.
  * ev      cites + tbl + num + sig ;  dens = ev * 100 / nb
  * mean dens = unweighted mean over blocks (r13's 96.5 = 1737.6 / 18).

Path-like rule (extract.py:is_pathlike, plus one extension):
  strip surrounding ".,;:" punctuation, drop http(s)/xd://-style URLs, then a
  token counts when it (a) ENDS in a code/doc extension from EXT (anchored at
  end — `provenance.json.pin` therefore does NOT count), (b) ends with '/',
  (c) starts with '/' or '~/', (d) contains '/', '<', '{', '~' or '..',
  or (e) ends in a `:NN`/`:NN-MM` line anchor after (a) applied, e.g.
  `claim-check.mjs:169` (extension added r14; r13's extract2.py resolved
  file:line cites the same way).

GENERIC_SIG exclusion list (state/verdict/table vocabulary that appears as
boilerplate in every section, not as evidence):
  REVIEW, DONE, BLOCKED, PARKED, SCOPED, PLANNED, LEARNED, RETIRED, FAILED,
  SUBMITTED, VERIFIED, UNVERIFIED, UNKNOWN, WARNING, HOLD, PASS, FAIL, ONLY,
  TAGS, TERM, TERMS, SCOPE, REPORT

Deterministic: stdlib only, no randomness, no locale, fixed-format output.
"""
import re
import sys

TOKEN = re.compile(r"`([^`\n]+)`")
EXTS = re.compile(r"\.(mjs|md|json|jsonl|ya?ml|py|sh|txt|git|gitignore)$", re.I)
PATHY = re.compile(r"[/<{~]|\.\.")
LINEANCHOR = re.compile(r":\d+([–-]\d+)?$")
YEAR = re.compile(r"^(19|20)\d{2}$")
WORD = re.compile(r"[A-Za-z0-9_]+")
SEP_ROW = re.compile(r"\s*\|[\s:|-]+\|?\s*$")
# --- r14 locked exclusion rules (calibrated on the pre-r13 file, see report) ---
MARKER = re.compile(r"^\s*\d+[.)]\s+")           # markdown enumeration "1. "
DATETIME = re.compile(r"\d{4}-\d{2}-\d{2}(?:T[\d:.]+(?:Z|[+-]\d{2}:?\d{2})?)?|\d{2}:\d{2}(?::\d{2})?(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?")
COMMAJOIN = re.compile(r"(?<=\d),(?=\d)")          # 7,224 -> 7224
NUMTOKEN = re.compile(r"\d[\d.,%]*")

# Pure-uppercase parts (after '_' splitting) that never count as signatures.
GENERIC_SIG = {
    "REVIEW", "DONE", "BLOCKED", "PARKED", "SCOPED", "PLANNED", "LEARNED",
    "RETIRED", "FAILED", "SUBMITTED", "VERIFIED", "UNVERIFIED", "UNKNOWN",
    "WARNING", "HOLD", "PASS", "FAIL", "ONLY", "TAGS", "TERM", "TERMS",
    "SCOPE", "REPORT",
}


def is_pathlike(tok):
    """r13 extract.py rule + :line-anchor tolerance."""
    t = tok.strip().strip(".,;:")
    if not t or (" " in t and "/" not in t):
        return False
    if t.startswith("http") or t.startswith("xd://") or t.startswith("skill://"):
        return False
    if EXTS.search(t):
        return True
    if t.endswith("/"):
        return True
    if t.startswith("~/") or t.startswith("/"):
        return True
    if PATHY.search(t):
        return True
    if EXTS.search(LINEANCHOR.sub("", t)):
        return True
    return False


def split_blocks(lines):
    """Yield (title, lines) per ^#{2,3} heading; preamble dropped."""
    blocks = []
    cur, buf = None, []
    for ln in lines:
        m = re.match(r"^#{2,3} (.+?)\s*$", ln)
        if m:
            if cur is not None:
                blocks.append((cur, buf))
            cur, buf = m.group(1), [ln]
        elif cur is not None:
            buf.append(ln)
    if cur is not None:
        blocks.append((cur, buf))
    return blocks


def census_block(block_lines, debug=False):
    nb = cites = tbl = 0
    num_tokens, sig_tokens = set(), set()
    for raw in block_lines:
        line = raw.rstrip("\n")
        if not line.strip():
            continue
        nb += 1
        spans = TOKEN.findall(line)
        path_spans = [s for s in spans if is_pathlike(s)]
        cites += len(path_spans)
        work_sig = work_num = line
        for s in spans:
            tagged = "`" + s + "`"
            if s in path_spans:
                replacement = " "                          # cite: drop from text scans
            elif re.search(r"[A-Za-z]", s):
                replacement = f" {s} "                     # caps vocab stays visible to sig
            else:
                replacement = f" {s} "                     # pure-numeric span: visible to both
            work_sig = work_sig.replace(tagged, replacement)
            if not re.search(r"[A-Za-z]", s):
                work_num = work_num.replace(tagged, replacement)
            else:
                work_num = work_num.replace(tagged, " ")
        work = work_sig
        work_num = MARKER.sub(" ", work_num)
        work_num = DATETIME.sub(" ", work_num)
        work_num = COMMAJOIN.sub("", work_num)
        work = MARKER.sub(" ", work)
        work = DATETIME.sub(" ", work)
        work = COMMAJOIN.sub("", work)
        if re.match(r"\s*\|", line):
            if not SEP_ROW.match(line) and (re.search(r"\d", line) or "`" in line):
                tbl += 1
        for m in NUMTOKEN.finditer(work_num):
            tok = m.group(0).strip(".,").rstrip(".")
            pre = work_num[m.start() - 1] if m.start() > 0 else " "
            pre2 = work_num[m.start() - 2] if m.start() > 1 else " "
            post = work_num[m.end()] if m.end() < len(work_num) else " "
            if tok and not tok.startswith(".") and not pre.isalpha() and not post.isalpha() \
                    and not (pre == "." and pre2.isalpha()) \
                    and not YEAR.match(tok):
                num_tokens.add(tok)
        for w in WORD.findall(work):
            for part in w.split("_"):
                if re.fullmatch(r"[A-Z]{5,}", part) and part not in GENERIC_SIG:
                    sig_tokens.add(part)
    ev = cites + tbl + len(num_tokens) + len(sig_tokens)
    return {
        "lines": len(block_lines), "nb": nb, "cites": cites, "tbl": tbl,
        "num": len(num_tokens), "sig": len(sig_tokens), "ev": ev,
        "dens": ev * 100.0 / nb if nb else 0.0,
        "num_tokens": sorted(num_tokens), "sig_tokens": sorted(sig_tokens),
    }


def main(argv):
    if len(argv) < 2:
        print("usage: density.py <SKILL.md> [--label LABEL]", file=sys.stderr)
        return 2
    path = argv[1]
    label = argv[argv.index("--label") + 1] if "--label" in argv else path
    debug = "--debug" in argv
    with open(path, encoding="utf-8") as fh:
        lines = fh.readlines()
    blocks = split_blocks(lines)
    if debug:
        for i, (title, bl) in enumerate(blocks, 1):
            r = census_block(bl)
            print(f"## {i} {title}\n   num: {r['num_tokens']}\n   sig: {r['sig_tokens']}")
        return 0
    print(f"# Density census — {label} ({len(lines)} lines, {len(blocks)} blocks)")
    print("# ev = path-cites + concrete-tbl-rows + numerics + signatures; dens = ev*100/nb")
    print("# num: unique numeric tokens (no bare years, no letter-adjacent fragments, no")
    print("#      enumeration markers, no date/time stamps; letter-free code spans count);")
    print("# sig: unique ALL-CAPS parts >=5 chars incl. non-path-like code spans, minus")
    print("#      GENERIC_SIG (full rules: see density.py docstring)")
    print()
    print("| # | block | lines | nb | cites | tbl | num | sig | ev | dens |")
    print("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|")
    total_cites = 0
    dens_sum = 0.0
    for i, (title, bl) in enumerate(blocks, 1):
        r = census_block(bl)
        total_cites += r["cites"]
        dens_sum += r["dens"]
        print(f"| {i} | {title} | {r['lines']} | {r['nb']} | {r['cites']} | "
              f"{r['tbl']} | {r['num']} | {r['sig']} | {r['ev']} | {r['dens']:.1f} |")
    mean = dens_sum / len(blocks) if blocks else 0.0
    print(f"| | **mean dens** | | | | | | | | **{mean:.1f}** |")
    print()
    print(f"Total path-citation instances: {total_cites} across {len(blocks)} blocks.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
