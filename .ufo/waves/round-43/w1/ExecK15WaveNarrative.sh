#!/usr/bin/env bash
# ExecK15WaveNarrative.sh -- round-43 K15 limb: wave-dispatch narrative vs
# results evidence (the RD42-2 / RD42-3 class).
#
# Sourceable:  source ExecK15WaveNarrative.sh; check_k15 <export-dir>
# Executable:  bash ExecK15WaveNarrative.sh <export-dir>
#
# Rule (K15).  Every sentence in LOG.md or corpus/lessons/*.md that asserts a
# named `kasegi-r<NN>-<word>` wave was dispatched -- or gives a `round total`
# for such a wave -- must be backed in the same export by that wave's evidence,
# or be named never-true by a later `Correction (round 43)` line in the same
# file.  The round and the wave are parsed from the sentence itself (the named
# wave carries the round, the `wave N` label carries the wave), never from the
# record's file name or from a hard-coded round.
#
# Evidence chain, tried in order (first hit decides):
#   1. .ufo/waves/round-<NN>/wave<label>-results.json    label from `wave N`
#   2. .ufo/waves/round-<NN>/<named-wave>-results.json   name from the sentence
#   3. the wave's own seat-receipt corpus: .ufo/waves/round-<NN>/wave<label>/,
#      .ufo/waves/round-<NN>/w<label>/ or .ufo/waves/round-<NN>/<word>/ with
#      exactly the stated number of `*.md` seat receipts.  Rounds 23/25 predate
#      the aggregate artifact; their dispatch sentences are true and carry 36
#      and 32 seat receipts under falsify/ and wave2/.
#   A results artifact must parse as a JSON object with an integer `seats`
#   equal to len(results) and, when the key is present, `round` equal to <NN>.
#   Missing -> absent; empty, corrupt or contradictory -> mismatch.
#
# Supersession.  When the wave has no evidence, the sentence is retired only by
# a line in the same file whose stripped text starts with
# `Correction (round 43)` (optional `- `/`* `/`**` prefix), later than the
# sentence, carrying `never-true` or `not taken`, and naming the wave: either
# the named wave token, or `wave <label>` together with the round token
# (<NN> or r<NN>).  A present-but-wrong artifact is never retired by a
# correction: the counting rule grades the bytes.
#
# Not narrative (quoted evidence, skipped): Markdown table rows, fenced code
# blocks, headings, correction blocks (a correction and the rest of its block
# are never re-collected as assertions), and inline-code spans for the
# `dispatched` predicate (`wave1.ready.dispatched` is a file name, not an
# assertion).  A `round total` with no named wave in the sentence is out of
# scope by the rule, which binds totals "for such a wave" -- the sentence names
# none; it is neither graded nor counted.
#
# stdout: exactly one line
#   K15 payload=sentences=<n>,unbacked=<k>,superseded=<s>,mismatch=<m> closed=0|1
# stderr (only when red): one `K15 detail=<file>:<line> ...` line per red claim,
# naming the evidence path and why, so a transcript names every offending
# sentence without disturbing the graded stdout line.  K15_VERBOSE=1 also emits
# the per-claim supersession lines on an otherwise green run.
#
# Exit status: 0 closed, 1 open, 2 usage error (no export dir).  Read-only over
# the given export tree; no writes anywhere.

check_k15() {
    local export="${1:-${R43_EXPORT:-}}"
    if [ -z "$export" ] || [ ! -d "$export" ]; then
        printf 'K15 payload=sentences=0,unbacked=0,superseded=0,mismatch=0 closed=0\n' >&2
        printf 'K15 usage: check_k15 <export-dir>\n' >&2
        return 2
    fi
    python3 - "$export" <<'K15_PY'
import glob
import json
import os
import re
import sys

root = sys.argv[1]
VERBOSE = os.environ.get('K15_VERBOSE', '0') == '1'

FENCE = "```"
CORRECTION = re.compile(r'^Correction \(round (\d+)\)')
WAVE_LABEL = re.compile(r'\bwave[ -](\d{1,3})\b', re.I)
NAMED = re.compile(r'(?<![\w/.-])kasegi-r(\d{2,3})-([a-z0-9]+(?:-[a-z0-9]+)*)')
NAMED_TAIL = ('-results', '-dispatch', '-spec', '-ready', '-err')
DISPATCH = re.compile(r'(?<![.\w-])dispatched\b', re.I)
ROUND_TOTAL = re.compile(r'\bround\s+total\b', re.I)
SEATS = re.compile(r'\b(\d{1,4})\s+seats\b', re.I)
CODE_SPAN = re.compile(r'`[^`]*`')
SENTENCE_END = re.compile(r'(?<![0-9])[.!?](?=\s|$)')


def corpus_files(export):
    paths = [os.path.join(export, 'LOG.md')]
    paths += sorted(glob.glob(os.path.join(export, 'corpus', 'lessons', '*.md')))
    return [p for p in paths if os.path.isfile(p)]


def mask_code(text):
    """Blank out inline-code spans, preserving length and offsets."""
    return CODE_SPAN.sub(lambda m: ' ' * len(m.group(0)), text)


def collect(path):
    """Return (sentences, corrections) for one record file.

    sentences: {text, start_line, end_line, linemap, offset}
    corrections: [(line_no, text)]
    Table rows, fenced blocks, headings and correction blocks are quoted
    evidence and are never collected as assertions.
    """
    with open(path, encoding='utf-8', errors='replace') as fh:
        raw = fh.read().split('\n')
    sentences = []
    corrections = []
    para = []           # list of (line_no, text)
    in_fence = False
    in_correction = False

    def add_sentence(s, a, linemap):
        body = s.strip()
        if not body:
            return
        lo = a + (len(s) - len(s.lstrip()))
        hi = lo + len(body)
        if lo >= len(linemap):
            return
        sentences.append({'text': body, 'start_line': linemap[lo],
                          'end_line': linemap[min(hi - 1, len(linemap) - 1)],
                          'linemap': linemap, 'offset': lo})

    def flush():
        if not para:
            return
        segs = list(para)
        para.clear()
        text = ' '.join(s for _, s in segs)
        linemap = []
        for line_no, s in segs:
            linemap.extend([line_no] * len(s))
            linemap.append(line_no)          # the joining space
        pos = 0
        for m in SENTENCE_END.finditer(text):
            add_sentence(text[pos:m.end()], pos, linemap)
            pos = m.end()
        if pos < len(text):
            add_sentence(text[pos:], pos, linemap)

    def correction_body(stripped):
        """Drop an optional list marker or bold wrapper from the line head."""
        body = stripped
        changed = True
        while changed:
            changed = False
            for pre in ('- ', '* ', '+ '):
                if body.startswith(pre):
                    body = body[len(pre):].lstrip()
                    changed = True
            if body.startswith('**') and len(body) > 2:
                body = body[2:].lstrip()
                changed = True
        return body

    for number, line in enumerate(raw, 1):
        stripped = line.strip()
        if stripped.startswith(FENCE):
            in_fence = not in_fence
            flush()
            in_correction = False
            continue
        if in_fence:
            continue
        if in_correction:
            # a correction block is prose: it ends at a blank line, a heading or
            # a new list item, so a following LOG entry is never swallowed
            if stripped == '' or stripped.startswith('#') or stripped[:2] in ('- ', '* ', '+ '):
                in_correction = False
            else:
                continue
        body = correction_body(stripped)
        if CORRECTION.match(body):
            flush()
            corrections.append((number, body))
            in_correction = True
            continue
        if stripped == '' or stripped.startswith('#') or stripped.startswith('|'):
            flush()
            continue
        if stripped[:2] in ('- ', '* ', '+ ') and para:
            flush()
        para.append((number, stripped))
    flush()
    return sentences, corrections


def parse_named(text):
    out = []
    for m in NAMED.finditer(text):
        tail = text[m.end():]
        if tail.startswith('-') or tail.startswith('.json'):
            continue
        word = m.group(2)
        if any(word.endswith(s) for s in NAMED_TAIL):
            continue
        out.append({'pos': m.start(), 'round': int(m.group(1)),
                    'name': m.group(0), 'word': word})
    return out


def clause_bounds(text, pos):
    left = text.rfind(';', 0, pos)
    right = text.find(';', pos)
    return (0 if left < 0 else left + 1, len(text) if right < 0 else right)


def build_claims(sentence):
    text = sentence['text']
    masked = mask_code(text)
    names = parse_named(text)
    if not names:
        return []
    labels = [{'pos': m.start(), 'label': int(m.group(1))}
              for m in WAVE_LABEL.finditer(text)]
    dispatch = [m.start() for m in DISPATCH.finditer(masked)]
    round_total = bool(ROUND_TOTAL.search(masked))
    sentence_rounds = sorted({n['round'] for n in names})
    claims = []

    def nearest_name(pos, lo, hi):
        best = None
        for n in names:
            if not (lo <= n['pos'] <= hi):
                continue
            d = abs(n['pos'] - pos)
            if best is None or d < best[0]:
                best = (d, n)
        return best[1] if best else None

    def seats_after(pos, stop):
        m = SEATS.search(text, pos, stop)
        return (int(m.group(1)), m.start()) if m else (None, None)

    for idx, lab in enumerate(labels):
        lo, hi = clause_bounds(text, lab['pos'])
        local_dispatch = any(lo <= d < hi for d in dispatch)
        if not (local_dispatch or round_total):
            continue
        nxt = labels[idx + 1]['pos'] if idx + 1 < len(labels) else len(text)
        # A label invokes the named wave written after it and before the next
        # label ("wave 2 `kasegi-r42-falsify`"); a name before the label belongs
        # to an earlier wave and is never borrowed.
        name = nearest_name(lab['pos'], lab['pos'], min(nxt, len(text)))
        if name is not None and not (lab['pos'] <= name['pos'] <= min(nxt, hi)):
            name = None
        if name is None and len(sentence_rounds) != 1:
            continue
        stated, seat_pos = seats_after(lab['pos'], min(nxt, hi))
        claims.append({'round': name['round'] if name else sentence_rounds[0],
                       'label': lab['label'],
                       'name': name['name'] if name else None,
                       'word': name['word'] if name else None,
                       'stated': stated, 'pos': lab['pos'], 'seat_pos': seat_pos})

    # a named wave asserted without a `wave N` label
    for n in names:
        if any(c['name'] == n['name'] for c in claims):
            continue
        lo, hi = clause_bounds(text, n['pos'])
        if not any(lo <= d < hi for d in dispatch):
            continue
        stated, seat_pos = seats_after(n['pos'], hi)
        claims.append({'round': n['round'], 'label': None, 'name': n['name'],
                       'word': n['word'], 'stated': stated,
                       'pos': n['pos'], 'seat_pos': seat_pos})

    unique = []
    index = {}
    for c in claims:
        key = (c['round'], c['label'], c['name'])
        if key in index:
            have = unique[index[key]]
            if have['stated'] is None and c['stated'] is not None:
                have['stated'] = c['stated']
                have['pos'] = c['pos']
                have['seat_pos'] = c['seat_pos']
            continue
        index[key] = len(unique)
        unique.append(c)
    return unique


def read_artifact(path, want_round):
    try:
        with open(path, encoding='utf-8') as fh:
            data = json.load(fh)
    except (OSError, ValueError):
        return {'state': 'corrupt'}
    if not isinstance(data, dict):
        return {'state': 'corrupt'}
    if 'round' in data and data.get('round') != want_round:
        return {'state': 'wrong-round'}
    seats = data.get('seats')
    results = data.get('results')
    if not isinstance(seats, int) or not isinstance(results, list):
        return {'state': 'corrupt'}
    if seats != len(results):
        return {'state': 'inconsistent', 'seats': seats, 'results': len(results)}
    return {'state': 'ok', 'seats': seats}


def receipt_count(directory):
    if not os.path.isdir(directory):
        return None
    n = 0
    for entry in os.listdir(directory):
        if entry.endswith('.md') and os.path.isfile(os.path.join(directory, entry)):
            n += 1
    return n


def grade_claim(export, claim):
    round_dir = os.path.join(export, '.ufo', 'waves', 'round-%02d' % claim['round'])
    artifacts = []
    if claim['label'] is not None:
        artifacts.append(os.path.join(round_dir, 'wave%d-results.json' % claim['label']))
    if claim['name']:
        artifacts.append(os.path.join(round_dir, '%s-results.json' % claim['name']))
    present = [(p, read_artifact(p, claim['round']))
               for p in artifacts if os.path.isfile(p)]
    for path, info in present:
        if info['state'] == 'ok' and (claim['stated'] is None
                                      or info['seats'] == claim['stated']):
            return 'backed', path, info
    if present:
        return 'mismatch', present[0][0], present[0][1]

    dirs = []
    if claim['label'] is not None:
        dirs.append(os.path.join(round_dir, 'wave%d' % claim['label']))
        dirs.append(os.path.join(round_dir, 'w%d' % claim['label']))
    if claim['word']:
        dirs.append(os.path.join(round_dir, claim['word']))
    mismatched = None
    for directory in dirs:
        count = receipt_count(directory)
        if count is None or count == 0:
            continue
        if claim['stated'] is None or count == claim['stated']:
            return 'backed', directory, {'state': 'receipts', 'seats': count}
        mismatched = (directory, count)
    if mismatched is not None:
        return 'mismatch', mismatched[0], {'state': 'receipts', 'seats': mismatched[1]}
    return 'absent', None, {}


def superseded_by(corrections, claim, sentence_end):
    for line_no, text in corrections:
        if line_no <= sentence_end:
            continue
        if 'never-true' not in text and 'not taken' not in text:
            continue
        if claim['name'] and claim['name'] in text:
            return line_no
        if claim['label'] is not None:
            label = re.search(r'\bwave[ -]%d\b' % claim['label'], text, re.I)
            rnd = re.search(r'(?<![\w])(r)?0*%d(?![\d])' % claim['round'], text)
            if label and rnd:
                return line_no
    return None


def describe(claim):
    return claim['name'] or ('wave%s' % claim['label'])


def main():
    export = os.path.abspath(root)
    if not os.path.isfile(os.path.join(export, 'LOG.md')):
        sys.stderr.write('K15 detail=LOG.md absent reason=no-export-tree\n')
        print('K15 payload=sentences=0,unbacked=0,superseded=0,mismatch=0 closed=0')
        return 1

    sentences_total = 0
    unbacked = 0
    superseded = 0
    mismatch = 0

    for path in corpus_files(export):
        rel = os.path.relpath(path, export)
        sentences, corrections = collect(path)
        for sentence in sentences:
            claims = build_claims(sentence)
            if not claims:
                continue
            sentences_total += 1
            for claim in claims:
                verdict, where, info = grade_claim(export, claim)
                if verdict == 'backed':
                    continue
                anchor = claim['seat_pos'] if claim['seat_pos'] is not None else claim['pos']
                lm = sentence['linemap']
                idx = min(sentence['offset'] + anchor, len(lm) - 1)
                line = lm[idx] if lm else sentence['start_line']
                # A present-but-wrong artifact is never retired by prose.
                saved = (superseded_by(corrections, claim, sentence['end_line'])
                         if verdict == 'absent' else None)
                if saved is not None:
                    superseded += 1
                    if VERBOSE:
                        sys.stderr.write(
                            'K15 detail=%s:%d wave=%s round=%d superseded-by=%d\n'
                            % (rel, line, describe(claim), claim['round'], saved))
                    continue
                if verdict == 'mismatch':
                    mismatch += 1
                    if info.get('state') == 'inconsistent':
                        extra = 'seats=%s,results=%s' % (info['seats'], info['results'])
                    elif info.get('state') == 'wrong-round':
                        extra = 'artifact-round-mismatch'
                    elif info.get('state') == 'receipts':
                        extra = 'receipts=%s' % info.get('seats')
                    elif info.get('state') == 'ok':
                        extra = 'seats=%s' % info.get('seats')
                    else:
                        extra = info.get('state') or 'unknown'
                    sys.stderr.write(
                        'K15 detail=%s:%d wave=%s round=%d stated-seats=%s '
                        'mismatch=%s path=%s\n'
                        % (rel, line, describe(claim), claim['round'],
                           claim['stated'], extra,
                           os.path.relpath(where, export) if where else '-'))
                    continue
                unbacked += 1
                sys.stderr.write(
                    'K15 detail=%s:%d wave=%s round=%d stated-seats=%s '
                    'unbacked=no-evidence\n'
                    % (rel, line, describe(claim), claim['round'], claim['stated']))

    if sentences_total == 0:
        # A record with no qualifying narrative cannot show the rule holds.
        sys.stderr.write('K15 detail=. reason=no-qualifying-sentences\n')
        closed = 0
    elif unbacked == 0 and mismatch == 0:
        closed = 1
    else:
        closed = 0

    print('K15 payload=sentences=%d,unbacked=%d,superseded=%d,mismatch=%d closed=%d'
          % (sentences_total, unbacked, superseded, mismatch, closed))
    return 0 if closed == 1 else 1


sys.exit(main())
K15_PY
}

if [ "${BASH_SOURCE[0]:-$0}" = "$0" ]; then
    check_k15 "$@"
    exit $?
fi
