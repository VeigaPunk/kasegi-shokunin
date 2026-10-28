#!/usr/bin/env bash
# ExecK17ClaimsBefore.sh — round-43 closure-suite limb K17 (family RD42-8:
# claims.json `before` literal vs the control receipt it cites).
#
# WHAT IT REPAIRS
#   The r42 suite was green at 13/13 while `.ufo/waves/round-42/claims.json`
#   C1 `before` read "the r41 suite at base prints `closed=10/12` exit=1" and the
#   control that cell cites (`.ufo/waves/round-42/c1-controls/do-nothing.txt`)
#   prints `closed=8/12 exit=1`.  No check in the thirteen compared a frozen
#   claim's quoted control value against the control receipt, so a record that
#   contradicted the run it describes stayed invisible.  K17 grades exactly that
#   binding for every committed round claims.json in the export.
#
# THE RULE (what is graded, and where a token may be backed)
#   Population: every `.ufo/waves/round-<NN>/claims.json` at depth two under
#   `.ufo/waves/` (fixture copies nested inside a round's wave dirs are not
#   round freezes and are not read).  For each claim, `before` and `after`
#   strings are walked recursively (a JSON string, list or object cell).
#
#   Token: `closed=<n>/<m>`, `failures=<k>` or `cases=<k>`, matched only as a
#   WHOLE token (r41/claims-erratum-2 E6): the value is the maximal digit run
#   with at most one `/` between digits, and the character before the key and
#   the character after the value must be absent or not a letter, digit, `_`,
#   `/` or `-`.  `closed=10/100` therefore extracts as `10/100` and never as
#   `10/12`; `closed=13/13x`, `closed=13/13/7` and `xclosed=13/13` are not
#   tokens at all.
#
#   `before` tokens are MEASUREMENTS and are graded.  A token is backed when it
#   appears as a whole token in one of the claim's cited control receipts:
#   `controls.c1`/`controls.c2` (any string value of the `controls` object) or a
#   receipt path named in the cell (a `.ufo/`, `corpus/` or `scripts/` path that
#   is not a record — see below).  A token NOT printed by a cited receipt is
#   still accepted when a committed `claims-erratum*.md` file in the SAME round
#   dir names it in a paragraph that also carries `superseded`: that is the
#   round-43 escape hatch for a frozen literal the round formally supersedes.
#   Anything else is `unbacked` and reds the check.  A claim that cites no
#   receipt at all (no `controls` value and no receipt path in the cell, as in
#   the round-23..39 freezes) has no control to be compared against: its tokens
#   are outside the population and are neither graded nor counted, because the
#   rule above is "the receipt the claim cites" and inventing one would grade a
#   claim against a document it never named.
#
#   `after` tokens are TARGETS, not measurements: an after cell states the
#   post-run state that the suite itself is measuring, and no historical round's
#   after cell is printed by a control receipt (round 27's `failures=0`, round
#   35's `closed=0/7`, round 36's `closed=9/9` are aspirations, not transcripts).
#   They are extracted and near-token-checked but never counted as backed or
#   unbacked.  This is the fixpoint rule the r42 J8 canonical mode established:
#   a round's own claim cannot be evidence for the run that grades it.
#
#   QUOTATIONS: a `before` token introduced by a quotation verb (`quote`,
#   `says`, `states`, `carries`, `reads`) from a RECORD — another claims.json,
#   a claims-erratum, a corpus/lessons or corpus/knowledge file, or any path
#   carrying `:LINE` — is that record's statement, not this claim's control
#   assertion, and is skipped (`quoted=`).  The record is graded when its own
#   claims.json is reached; the round-43 freeze quotes the round-42 defect
#   (`closed=10/12`) and `corpus/.../claims-erratum-4.md`'s unbacked
#   `closed=10/13` exactly this way, and grading those quotations as round-43
#   measurements would make the frozen C1 unsatisfiable.  A receipt verb
#   (`prints`, `outputs`, `tees`, `reports`) between the attribution and the
#   literal cancels the exemption, so "claims.json says X while its own control
#   prints Y" grades Y and does not excuse it.
#
#   NEAR-TOKENS: within one cell, two whole tokens of the same key related by
#   DIGIT DELETION (`10/12` vs `10/120`, `13/13` vs `1/13`) are a mangled twin
#   beside a truth token (the committed r41 I3 defeat shape).  The non-printed,
#   longer-digit twin is REJECTED: it is not counted in `tokens=` and it reds
#   the check; the payload names it (`rejected=closed=10/120`).
#
# PAYLOAD
#   payload=claims=<n>,tokens=<t>,verified=<v>,superseded=<s>,unbacked=<u>
#   plus `,quoted=<q>` when a record quotation was skipped, `,rejected=<tok>[+<tok>]`
#   when a near-token was rejected, and `,parse=<k>` when a claims.json failed
#   to parse.  t = v + s + u.  On the clean base and green trees the payload is
#   exactly the five frozen cells.
#   closed=1 iff claims>0, tokens>0, unbacked=0, no rejected near-token and no
#   parse error.  Detail lines go to STDERR (`K17 detail ...`) and carry the
#   mismatched token and the values the cited receipt prints; stdout carries
#   exactly one `K17 payload=... closed=0|1` line.
#
# SOURCING
#   Sourceable limb: sourcing defines functions and globals only, sets no shell
#   options and runs nothing.  Integration contract for the suite:
#       out=$(check_k17 "$EXPORT"); rc=$?     # one K17 line, rc 0 == closed
#       payload=$(k17_payload "$EXPORT")      # the payload cell only
#   Fixture/replay driver: k17_selftest WORK TREE  (builds trees under WORK
#   from TREE, grades the repaired tree positive and every mutant rejected).
#
# STANDALONE DRIVER (export mode only, like the suite)
#   bash ExecK17ClaimsBefore.sh --export-ref <hash> [--lane DIR] [--work DIR] [--selftest]
#   bash ExecK17ClaimsBefore.sh --tree DIR [--selftest]
#   A plain run (neither --export-ref nor --tree) refuses with exit 2.

K17_ROUND=43
K17_RECORDS_RX='claims\.json'

k17_py() {
  python3 - "$@" <<'K17_PY'
import json
import os
import re
import shutil
import sys

TOKEN_RX = re.compile(r"(closed|failures|cases)=(\d+)(?:/(\d+))?")
BOUND = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_/-")
PATH_RX = re.compile(r"(?:\.ufo/|corpus/|scripts/)[A-Za-z0-9_./-]+")
RECORD_RX = re.compile(r"\bclaims\.json\b")
QUOTE_RX = re.compile(r"\b(quote[sd]?|says|said|states|carries|reads)\b", re.I)
RCPT_VERB_RX = re.compile(r"\b(print(?:s|ed)?|outputs?|tees?|reports?|produced)\b", re.I)
ROUND_RX = re.compile(r"^round-(\d+)$")
ERRATA_RX = re.compile(r"^claims-erratum.*\.md$")
RECEIPT_DIRS = ("c1-controls", "c2-controls", "final-gates", "receipts")


def read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return ""


def norm_path(raw):
    p = raw.rstrip(".,;:!?)]}\"'")
    p = re.sub(r":\d+(-\d+)?$", "", p)
    return p


def under_root(root, rel):
    if not rel or rel.startswith("/"):
        return None
    full = os.path.normpath(os.path.join(root, rel))
    rootn = os.path.normpath(root)
    if full != rootn and not full.startswith(rootn + os.sep):
        return None
    return full


def is_record(rel):
    base = os.path.basename(rel)
    if base == "claims.json" or ERRATA_RX.match(base):
        return True
    return rel.startswith("corpus/lessons/") or rel.startswith("corpus/knowledge/")


def strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from strings(item)
    elif isinstance(value, dict):
        for key in sorted(value):
            yield from strings(value[key])


def token_value(m):
    return m.group(2) + ("/" + m.group(3) if m.group(3) else "")


def whole_tokens(text):
    out = []
    for m in TOKEN_RX.finditer(text):
        s, e = m.start(), m.end()
        if s > 0 and text[s - 1] in BOUND:
            continue
        if e < len(text) and text[e] in BOUND:
            continue
        out.append((s, m.group(1) + "=" + token_value(m), token_value(m), m.group(1)))
    return out


def present(text, needle):
    start = 0
    while True:
        idx = text.find(needle, start)
        if idx < 0:
            return False
        s, e = idx, idx + len(needle)
        if not (s > 0 and text[s - 1] in BOUND) and not (e < len(text) and text[e] in BOUND):
            return True
        start = idx + 1


def is_del(short, long):
    if short == long or len(short) >= len(long):
        return False
    i = 0
    for ch in long:
        if i < len(short) and short[i] == ch:
            i += 1
    return i == len(short)


def del_variant(a, b):
    fa, fb = a.split("/"), b.split("/")
    if a == b or len(fa) != len(fb):
        return False
    return any(is_del(x, y) or is_del(y, x) for x, y in zip(fa, fb))


def like_key_values(text, key):
    return [tok for _s, tok, _v, k in whole_tokens(text) if k == key]


def attribution(text, pos, receipts):
    """Return the record path a token is quoted from, or None."""
    window = text[max(0, pos - 240):pos]
    last, last_end = None, -1
    for m in PATH_RX.finditer(window):
        last, last_end = norm_path(m.group(0)), m.end()
    for m in RECORD_RX.finditer(window):
        if m.end() > last_end:
            last, last_end = "claims.json", m.end()
    if last is None or last in receipts or not is_record(last):
        return None
    segment = window[last_end:]
    if QUOTE_RX.search(segment) and not RCPT_VERB_RX.search(segment):
        return last
    return None


def superseded_by(round_dir, token):
    try:
        names = sorted(n for n in os.listdir(round_dir) if ERRATA_RX.match(n))
    except OSError:
        return None
    for name in names:
        text = read(os.path.join(round_dir, name))
        for para in re.split(r"\n[ \t]*\n", text):
            if present(para, token) and re.search(r"supersed", para, re.I):
                return name
    return None


def grade(tree):
    waves = os.path.join(tree, ".ufo", "waves")
    claims_files = []
    try:
        entries = sorted(os.listdir(waves))
    except OSError:
        entries = []
    for entry in entries:
        if not ROUND_RX.match(entry):
            continue
        path = os.path.join(waves, entry, "claims.json")
        if os.path.isfile(path):
            claims_files.append((entry, path))

    detail = []
    n_claims = 0
    n_tokens = n_verified = n_superseded = n_unbacked = n_quoted = 0
    rejected = []
    parse_errors = 0

    for entry, path in claims_files:
        n_claims += 1
        round_dir = os.path.dirname(path)
        try:
            doc = json.loads(read(path))
        except (ValueError, TypeError):
            parse_errors += 1
            detail.append("K17 detail round=%s result=parse-error" % entry)
            continue
        claims = doc.get("claims") if isinstance(doc, dict) else None
        if not isinstance(claims, list):
            continue
        controls = doc.get("controls") if isinstance(doc, dict) else None
        control_list = list(strings(controls)) if isinstance(controls, (str, list, dict)) else []
        for claim in claims:
            if not isinstance(claim, dict):
                continue
            cid = claim.get("id", "?")
            cells = []
            for field in ("before", "after"):
                if field in claim:
                    for cell in strings(claim[field]):
                        cells.append((field, cell))
            receipts = []
            for raw in control_list:
                rel = norm_path(raw.strip())
                if rel:
                    receipts.append(rel)
            for _f, cell in cells:
                for m in PATH_RX.finditer(cell):
                    rel = norm_path(m.group(0))
                    if rel and not is_record(rel):
                        receipts.append(rel)
            receipts = sorted(set(receipts))
            receipt_text = {}
            for rel in receipts:
                full = under_root(tree, rel)
                if full and os.path.isfile(full):
                    receipt_text[rel] = read(full)

            for field, cell in cells:
                toks = whole_tokens(cell)
                near = set()
                vals = [(i, tok, val, key) for i, (pos, tok, val, key) in enumerate(toks)]
                for a in range(len(vals)):
                    for b in range(a + 1, len(vals)):
                        ia, ta, va, ka = vals[a]
                        ib, tb, vb, kb = vals[b]
                        if ka != kb or not del_variant(va, vb):
                            continue
                        pa = ta.split("=", 1)[1]
                        pb = tb.split("=", 1)[1]
                        printed_a = any(present(t, ta) for t in receipt_text.values())
                        printed_b = any(present(t, tb) for t in receipt_text.values())
                        if printed_a and not printed_b:
                            near.add(ib)
                        elif printed_b and not printed_a:
                            near.add(ia)
                        else:
                            long_idx = ia if len(pa) >= len(pb) else ib
                            near.add(long_idx)
                for idx, (pos, tok, val, key) in enumerate(toks):
                    if idx in near:
                        if tok not in rejected:
                            rejected.append(tok)
                        detail.append(
                            "K17 detail round=%s claim=%s field=%s token=%s result=rejected near-token"
                            % (entry, cid, field, tok))
                        continue
                    if field == "after":
                        continue
                    if not receipts:
                        continue
                    record = attribution(cell, pos, receipts)
                    if record is not None:
                        n_quoted += 1
                        detail.append(
                            "K17 detail round=%s claim=%s field=%s token=%s record=%s result=quoted"
                            % (entry, cid, field, tok, record))
                        continue
                    n_tokens += 1
                    hit = [rel for rel in receipts
                           if rel in receipt_text and present(receipt_text[rel], tok)]
                    if hit:
                        n_verified += 1
                        continue
                    erratum = superseded_by(round_dir, tok)
                    if erratum:
                        n_superseded += 1
                        detail.append(
                            "K17 detail round=%s claim=%s field=%s token=%s by=%s result=superseded"
                            % (entry, cid, field, tok, erratum))
                        continue
                    n_unbacked += 1
                    printed = []
                    for rel in receipts:
                        if rel in receipt_text:
                            for tokv in like_key_values(receipt_text[rel], key):
                                if tokv not in printed:
                                    printed.append(tokv)
                    own = [t for _s, t, _v, k in whole_tokens(cell) if k == key and t != tok]
                    printlist = printed + [t for t in own if t not in printed]
                    detail.append(
                        "K17 detail round=%s claim=%s field=%s token=%s cited=%s control-prints=%s result=unbacked"
                        % (entry, cid, field, tok, "|".join(receipts) or "none",
                           "+".join(printlist) or "none"))

    payload = "claims=%d,tokens=%d,verified=%d,superseded=%d,unbacked=%d" % (
        n_claims, n_tokens, n_verified, n_superseded, n_unbacked)
    if n_quoted:
        payload += ",quoted=%d" % n_quoted
    if rejected:
        payload += ",rejected=" + "+".join(rejected)
    if parse_errors:
        payload += ",parse=%d" % parse_errors
    ok = (n_claims > 0 and n_tokens > 0 and n_unbacked == 0
          and not rejected and parse_errors == 0)
    return payload, ok, detail


# ---------------------------------------------------------------------------
# fixture/replay driver
# ---------------------------------------------------------------------------

def minimal_tree(src, dst):
    waves = os.path.join(src, ".ufo", "waves")
    os.makedirs(os.path.join(dst, ".ufo", "waves"), exist_ok=True)
    for entry in sorted(os.listdir(waves)):
        if not ROUND_RX.match(entry):
            continue
        sdir = os.path.join(waves, entry)
        ddir = os.path.join(dst, ".ufo", "waves", entry)
        os.makedirs(ddir, exist_ok=True)
        for name in sorted(os.listdir(sdir)):
            spath = os.path.join(sdir, name)
            if name == "claims.json" or ERRATA_RX.match(name):
                shutil.copy2(spath, os.path.join(ddir, name))
            elif name in RECEIPT_DIRS and os.path.isdir(spath):
                shutil.copytree(spath, os.path.join(ddir, name), dirs_exist_ok=True)


def subst(path, old, new):
    """Replace exactly one occurrence; return True on success."""
    text = read(path)
    if text.count(old) != 1:
        return False
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text.replace(old, new))
    return True


def selftest(work, tree):
    base = os.path.join(work, "k17-base")
    shutil.rmtree(base, ignore_errors=True)
    minimal_tree(tree, base)
    r42 = os.path.join(base, ".ufo", "waves", "round-42")
    claims = os.path.join(r42, "claims.json")
    erratum = os.path.join(r42, "claims-erratum-1.md")
    erratum_text = ("# round-42 claims erratum (K17 fixture)\n\n"
                    "`closed=10/12` in the frozen C1 before cell is superseded by the "
                    "control's `closed=8/12`.\n")

    cases = []

    def variant(name, mutate):
        dst = os.path.join(work, "k17-" + name)
        shutil.rmtree(dst, ignore_errors=True)
        shutil.copytree(base, dst)
        built = mutate(dst)
        if built is False:
            cases.append((name + "(mutation-failed)", "n/a", None))
            return
        payload, ok, _d = grade(dst)
        cases.append((name, payload, ok))

    def repaired(dst):
        with open(os.path.join(dst, ".ufo/waves/round-42/claims-erratum-1.md"),
                  "w", encoding="utf-8") as fh:
            fh.write(erratum_text)

    def claims_of(dst):
        return os.path.join(dst, ".ufo/waves/round-42/claims.json")

    def no_superseded(dst):
        with open(os.path.join(dst, ".ufo/waves/round-42/claims-erratum-1.md"),
                  "w", encoding="utf-8") as fh:
            fh.write("`closed=10/12` is restated here without the disposal word.\n")

    def near_token(dst):
        repaired(dst)
        return subst(claims_of(dst), "closed=10/12",
                     "closed=10/12 (mangled twin closed=10/120)")

    def fabricated(dst):
        repaired(dst)
        return subst(claims_of(dst), "closed=10/12",
                     "closed=10/12 (the control prints closed=9/12)")

    def citation_missing(dst):
        repaired(dst)
        os.remove(os.path.join(dst, ".ufo/waves/round-42/c1-controls/do-nothing.txt"))

    variant("committed-defect", lambda dst: None)
    variant("repaired", repaired)
    variant("erratum-without-superseded", no_superseded)
    variant("near-token", near_token)
    variant("fabricated-value", fabricated)
    variant("citation-missing", citation_missing)

    failures = 0
    for name, payload, ok in cases:
        expected = {"repaired": True}.get(name, False)
        good = (ok is not None and ok == expected)
        if not good:
            failures += 1
        print("K17 replay %s expected=%s observed=%s payload=%s verdict=%s"
              % (name, "accept" if expected else "reject",
                 "build-failed" if ok is None else ("accept" if ok else "reject"),
                 payload, "pass" if good else "fail"))
    print("K17 selftest cases=%d failures=%d" % (len(cases), failures))
    return 0 if failures == 0 else 1


def main(argv):
    mode = argv[1] if len(argv) > 1 else ""
    if mode in ("line", "payload"):
        tree = argv[2] if len(argv) > 2 else ""
        if not tree or not os.path.isdir(os.path.join(tree, ".ufo", "waves")):
            print("K17 payload=claims=0,tokens=0,verified=0,superseded=0,unbacked=0,parse=1 closed=0")
            return 1
        payload, ok, detail = grade(tree)
        for line in detail:
            sys.stderr.write(line + "\n")
        if mode == "payload":
            print(payload)
        else:
            print("K17 payload=%s closed=%d" % (payload, 1 if ok else 0))
        return 0 if ok else 1
    if mode == "selftest":
        return selftest(argv[2], argv[3])
    sys.stderr.write("k17: unknown mode %s\n" % mode)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
K17_PY
}

# check_k17 TREE — prints exactly one `K17 payload=... closed=0|1` line to stdout
# (detail evidence goes to stderr) and returns 0 only when closed.
check_k17() {
  local tree=${1:-}
  if [ -z "$tree" ]; then
    printf 'K17 payload=claims=0,tokens=0,verified=0,superseded=0,unbacked=0 closed=0\n'
    return 1
  fi
  k17_py line "$tree"
}

# k17_payload TREE — the payload cell only (suite convenience).
k17_payload() {
  local tree=${1:-}
  [ -n "$tree" ] || { printf 'claims=0,tokens=0,verified=0,superseded=0,unbacked=0\n'; return 1; }
  k17_py payload "$tree"
}

# k17_selftest WORK TREE — build the fixture trees under WORK from TREE and
# grade them: the repaired tree must accept, every mutant must reject.
k17_selftest() {
  local work=${1:-} tree=${2:-}
  if [ -z "$work" ] || [ -z "$tree" ]; then
    printf 'k17_selftest: usage: k17_selftest WORK TREE\n' >&2
    return 2
  fi
  mkdir -p -- "$work" || return 2
  k17_py selftest "$work" "$tree"
}

k17_lane_from_script() {
  local d
  d=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" 2>/dev/null && pwd -P) || return 1
  while [ "$d" != "/" ]; do
    if [ -f "$d/SCORECARD.md" ] && [ -d "$d/corpus" ]; then printf '%s\n' "$d"; return 0; fi
    d=$(dirname -- "$d")
  done
  return 1
}

if [ "${BASH_SOURCE[0]}" = "$0" ]; then
  K17_TREE=''
  K17_REF=''
  K17_LANE=''
  K17_WORK=''
  K17_SELFTEST=0
  while [ $# -gt 0 ]; do
    case $1 in
      --tree)       K17_TREE=$2; shift 2 ;;
      --export-ref) K17_REF=$2; shift 2 ;;
      --lane)       K17_LANE=$2; shift 2 ;;
      --work)       K17_WORK=$2; shift 2 ;;
      --selftest)   K17_SELFTEST=1; shift ;;
      -h|--help)    sed -n '2,/^K17_ROUND=/p' "${BASH_SOURCE[0]}" | sed -e '$d' -e 's/^# \{0,1\}//'; exit 0 ;;
      *) printf 'ExecK17ClaimsBefore: unknown argument: %s\n' "$1" >&2; exit 2 ;;
    esac
  done
  if [ -z "$K17_TREE" ] && [ -z "$K17_REF" ]; then
    printf 'ExecK17ClaimsBefore: refusing to run against the live worktree: this limb is export-mode only.\n' >&2
    printf 'ExecK17ClaimsBefore: pass --export-ref <hash> (or --tree <exported dir>).\n' >&2
    exit 2
  fi
  [ -n "$K17_LANE" ] || K17_LANE=$(k17_lane_from_script) || K17_LANE=/home/vgpnk/Projects/shokunin/kasegi-shokunin
  if [ -z "$K17_WORK" ]; then
    K17_WORK=$(mktemp -d "${TMPDIR:-/tmp}/k17-work.XXXXXXXX") || exit 2
  fi
  mkdir -p -- "$K17_WORK" || exit 2
  if [ -n "$K17_REF" ]; then
    rm -rf -- "$K17_WORK/export"
    mkdir -p -- "$K17_WORK/export" || exit 2
    if ! git -C "$K17_LANE" archive --format=tar "$K17_REF" 2>/dev/null | tar -xf - -C "$K17_WORK/export"; then
      printf 'ExecK17ClaimsBefore: export failed for ref %s (ref-not-found or unreadable lane)\n' "$K17_REF" >&2
      exit 1
    fi
    K17_TREE="$K17_WORK/export"
  fi
  if [ ! -d "$K17_TREE/.ufo/waves" ]; then
    printf 'ExecK17ClaimsBefore: %s has no .ufo/waves (not a lane tree)\n' "$K17_TREE" >&2
    exit 2
  fi
  check_k17 "$K17_TREE"; rc=$?
  if [ "$K17_SELFTEST" -eq 1 ]; then
    k17_selftest "$K17_WORK/selftest" "$K17_TREE" || rc=1
  fi
  exit "$rc"
fi
