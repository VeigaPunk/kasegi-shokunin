#!/usr/bin/env python3
"""The claim-package gate: eight rules over the six-file claim-package contract.

The contract is corpus/knowledge/claim-package-contract.md (six files) with the
per-gate derivations in corpus/knowledge/claim-gates.md. The lost claimant tool
(~/Projects/bounties/ops/claim-check.mjs) was documentation-only for this lane;
this file is the executable gate for the subset the contract states, and nothing
more. Round 43 of kasegi-shokunin: the capability is acquired, not asserted.

Usage:
  python3 corpus/instruments/claim-package-check.py <package-dir>
  python3 corpus/instruments/claim-package-check.py <package-dir> --json
  python3 corpus/instruments/claim-package-check.py --selftest

Output (text mode), one line per rule in this order, then the verdict line:

  RULE R-FILES verdict=pass|fail detail=<short>
  RULE R-MANIFEST ...
  RULE R-REDACT ...
  RULE R-CUSTODIAN ...
  RULE R-PROVENANCE ...
  RULE R-STATUS ...
  RULE R-REPORT ...
  RULE R-NOSECRET ...
  package=<path> rules=8 pass=<k> fail=<m> verdict=WELL-FORMED|DEFECT exit=0|1

`--json` prints one JSON object with the same fields and the same exit status.

`detail=<short>` is comma-separated `key=value` tokens with no spaces: a reader
can split on `,` and `=`; the text never carries a matched secret value.

Exit status: 0 only when all eight rules pass; 1 when any rule fails; 2 on a
usage error, a missing/non-directory package argument, or `--selftest` without
an available selftest implementation. The verdict line's `exit=` token repeats
that status, so a transcript carries the code without an out-of-band note. A
missing package prints `package=<path> verdict=ERROR exit=2`.

Read confinement (the whole point of the gate): every path the gate opens is
built from the package root it was given. Artifact paths must be relative, carry
no `..` component, contain no symlink at any component, and resolve beneath the
package root; a path that escapes fails R-MANIFEST. The gate reads no file
outside the package directory, makes no network call and runs no git command.

Fail-closed (R30): a read error, a parse error, a missing file or an internal
exception is a FAIL for the rule that needed it, never a pass. A rule that cannot
inspect its input has not verified anything, so it reports `verdict=fail`.

Rule table (the exact predicate of each rule; the round-43 receipt carries the
same table with the contract sentence each rule enforces):

  R-FILES      six contract files present, regular, non-symlink, non-empty; the
               four JSON files parse as JSON objects.
  R-MANIFEST   schema_version == "evidence-manifest/v1"; numeric sequence;
               64-hex expected_head_sha256; every artifact path relative,
               inside evidence/, no symlink, bytes' sha256 equals the recorded
               digest; polarity in {positive,negative}; at least one positive.
  R-REDACT     redactions[] non-empty; exactly one receipt binds each artifact;
               artifact_sha256 == scanned_artifact_sha256 == the manifest digest;
               non-empty distinct producer/verifier identities.
  R-CUSTODIAN  non-empty chain; per decision non-empty action, 64-hex
               input/decision digests, non-empty matched_grant_id and
               scope_signal exactly "NO_SCOPE_OBJECTION"; head_sha256 equals the
               final decision digest and manifest.expected_head_sha256.
  R-PROVENANCE agents carry requested/resolved models per transition; commands
               carry exit codes; pin has remote + commit; policy_sha256 is
               64-hex; external_effects_performed == []; secrets attestation
               present and not negative.
  R-STATUS     manifest_sha256 recomputed over the manifest bytes; claim_review
               holds hard_gates, subchecks and a reviewer with requested/resolved
               model, boolean fallback and an identity distinct from every
               manifest producer/verifier; claimable true requires every gate and
               subcheck PASS and finding_count >= 1; claimable false names a
               blocker.
  R-REPORT     report.md carries the `Scope excerpt` heading, the literal
               `No submission performed`, an https URL, and every 64-hex token
               it cites occurs in the manifest.
  R-NOSECRET   no symlink in the package tree; no file over 5 MiB; no
               secret-shaped token (private-key header, op:// reference,
               bearer/authorization value, labelled credential, session cookie).
"""
import argparse
import hashlib
import json
import os
import re
import stat
import subprocess
import sys

_GATE_RULE_ORDER = (
    'R-FILES',
    'R-MANIFEST',
    'R-REDACT',
    'R-CUSTODIAN',
    'R-PROVENANCE',
    'R-STATUS',
    'R-REPORT',
    'R-NOSECRET',
)

SIX_FILES = (
    'report.md',
    'claim_checklist.md',
    'evidence/manifest.json',
    'custodian-receipts.json',
    'provenance.json',
    'status.json',
)
JSON_FILES = (
    'evidence/manifest.json',
    'custodian-receipts.json',
    'provenance.json',
    'status.json',
)

HEX64 = re.compile(r'^[0-9a-fA-F]{64}$')
HEX_ANY = re.compile(r'^(?:[0-9a-fA-F]{7,64})$')
HEX64_TOKEN = re.compile(r'(?<![0-9a-fA-F])[0-9a-fA-F]{64}(?![0-9a-fA-F])')
HTTPS_URL = re.compile(r'https://[^\s)\]<>"]+')
SCOPE_EXCERPT = re.compile(r'scope\s+excerpt', re.IGNORECASE)
NO_SUBMISSION = 'No submission performed'

HARD_GATE_KEYS = (
    'written_scope',
    'authorization',
    'evidence_integrity',
    'no_duplicate_or_prior_submission',
)
SUBCHECK_KEYS = ('no_secrets', 'operator_attribution')

MAX_SCAN_BYTES = 5 * 1024 * 1024

# Secret shapes: (name, bytes regex). A hit fails R-NOSECRET; the matched value
# is never printed, so a receipt cannot leak the thing it reported.
SECRET_PATTERNS = (
    ('private-key', re.compile(rb'-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----')),
    ('op-ref', re.compile(rb'op://[A-Za-z0-9_./-]{3,}')),
    ('bearer', re.compile(rb'(?i)\bbearer\s+[A-Za-z0-9_.\-]{16,}')),
    ('authorization', re.compile(rb'(?i)\bauthorization\b\\?["\']?\s*[:=]\s*\\?["\']?(?:bearer\s+)?[A-Za-z0-9_.+/=\-]{16,}')),
    ('credential', re.compile(rb'(?i)\b(?:api[_-]?key|secret|token|password)\b\\?["\']?\s*[:=]\s*\\?["\']?[A-Za-z0-9_\-]{16,}')),
    ('session-cookie', re.compile(rb'(?i)\bsession[_-]?cookie\b\\?["\']?\s*[:=]\s*\\?["\']?[^\s"\'\\]{16,}')),
)


class _GateFail(Exception):
    """A rule failed; str(exc) is the short detail token(s)."""


def _gate_token(value):
    """Render a failure token without spaces or newlines."""
    text = re.sub(r'[\s,=]+', '_', str(value)).strip('_')
    return text or 'unknown'


def inspect_path(root, rel):
    """Resolve a package-relative path, or return a short error token.

    Returns (absolute_path, None) when the path is a regular file that is
    lexically inside the package and whose real path is inside the package.
    Returns (None, token) for: empty, absolute, backslash, dotdot, missing,
    symlink, notdir, notfile, escape.
    """
    if not isinstance(rel, str) or not rel.strip():
        return None, 'empty'
    if os.path.isabs(rel) or rel.startswith('/') or rel.startswith('~'):
        return None, 'absolute'
    if '\\' in rel or '\x00' in rel:
        return None, 'backslash'
    parts = [part for part in rel.split('/') if part not in ('', '.')]
    if not parts:
        return None, 'empty'
    if '..' in parts:
        return None, 'dotdot'
    current = root
    for index, part in enumerate(parts):
        current = os.path.join(current, part)
        try:
            st = os.lstat(current)
        except OSError:
            return None, 'missing'
        if stat.S_ISLNK(st.st_mode):
            return None, 'symlink'
        if index < len(parts) - 1 and not stat.S_ISDIR(st.st_mode):
            return None, 'notdir'
    real = os.path.realpath(current)
    if real != root and not real.startswith(root + os.sep):
        return None, 'escape'
    try:
        st = os.lstat(real)
    except OSError:
        return None, 'missing'
    if not stat.S_ISREG(st.st_mode):
        return None, 'notfile'
    return real, None


class Package:
    """Read-only view of one package directory; all reads go through here."""

    def __init__(self, path):
        self.root = os.path.realpath(path)
        self._bytes = {}
        self._json = {}

    def read_bytes(self, rel):
        if rel in self._bytes:
            return self._bytes[rel]
        target, error = inspect_path(self.root, rel)
        if error:
            raise _GateFail(error)
        try:
            with open(target, 'rb') as handle:
                data = handle.read()
        except OSError:
            raise _GateFail('unreadable')
        self._bytes[rel] = data
        return data

    def read_json(self, rel):
        if rel in self._json:
            cached = self._json[rel]
            if isinstance(cached, _GateFail):
                raise cached
            return cached
        try:
            data = self.read_bytes(rel)
            value = json.loads(data.decode('utf-8'))
        except _GateFail as exc:
            self._json[rel] = exc
            raise
        except (UnicodeDecodeError, ValueError):
            exc = _GateFail('parse:' + rel.replace('/', '_'))
            self._json[rel] = exc
            raise exc
        self._json[rel] = value
        return value

    def manifest(self):
        value = self.read_json('evidence/manifest.json')
        if not isinstance(value, dict):
            raise _GateFail('manifest:not-object')
        return value


def _as_text(value):
    return value if isinstance(value, str) else ''


def _require_dict(parent, key, where):
    value = parent.get(key)
    if not isinstance(value, dict):
        raise _GateFail('missing:' + where + '.' + key)
    return value


def _require_list(parent, key, where):
    value = parent.get(key)
    if not isinstance(value, list):
        raise _GateFail('missing:' + where + '.' + key)
    return value


def _artifacts(manifest):
    artifacts = manifest.get('artifacts')
    if not isinstance(artifacts, list) or not artifacts:
        raise _GateFail('artifacts=none')
    for index, artifact in enumerate(artifacts):
        if not isinstance(artifact, dict):
            raise _GateFail('artifacts:not-object:' + str(index))
    return artifacts


# ---- R-FILES ----------------------------------------------------------------

def rule_files(pkg):
    """The six contract files present, regular, non-symlink, non-empty; JSON parses."""
    missing = []
    bad = []
    for rel in SIX_FILES:
        target, error = inspect_path(pkg.root, rel)
        if error in ('missing', 'notdir', 'escape', 'symlink', 'absolute', 'dotdot'):
            missing.append(rel)
            continue
        if error or os.path.getsize(target) == 0:
            bad.append(rel)
    for rel in JSON_FILES:
        try:
            value = pkg.read_json(rel)
        except _GateFail:
            if rel not in missing and rel not in bad:
                bad.append(rel)
            continue
        if not isinstance(value, dict) and rel not in missing and rel not in bad:
            bad.append(rel)
    if missing or bad:
        raise _GateFail('missing=%d,bad=%d' % (len(missing), len(bad)))
    return 'files=6,missing=0,bad=0'


# ---- R-MANIFEST -------------------------------------------------------------

def rule_manifest(pkg):
    """Manifest schema, per-artifact recomputed digest, polarity, path confinement."""
    manifest = pkg.manifest()
    if manifest.get('schema_version') != 'evidence-manifest/v1':
        raise _GateFail('schema=%s' % _gate_token(manifest.get('schema_version', 'absent')))
    sequence = manifest.get('sequence')
    if isinstance(sequence, bool) or not isinstance(sequence, (int, float)):
        raise _GateFail('sequence=not-number')
    head = manifest.get('expected_head_sha256')
    if not isinstance(head, str) or not HEX64.match(head):
        raise _GateFail('expected_head=bad')
    artifacts = _artifacts(manifest)
    positive = 0
    digest_bad = []
    escape = []
    polarity_bad = []
    seen = set()
    for artifact in artifacts:
        rel = artifact.get('path')
        recorded = artifact.get('sha256')
        if not isinstance(recorded, str) or not HEX64.match(recorded):
            digest_bad.append(str(artifact.get('path', '?')))
            continue
        if not isinstance(rel, str) or not rel:
            escape.append('?')
            continue
        if rel in seen:
            digest_bad.append(rel)
            continue
        seen.add(rel)
        if artifact.get('polarity') == 'positive':
            positive += 1
        elif artifact.get('polarity') != 'negative':
            polarity_bad.append(rel)
        target, error = inspect_path(pkg.root, 'evidence/' + rel)
        if error:
            escape.append(rel)
            continue
        try:
            with open(target, 'rb') as handle:
                actual = hashlib.sha256(handle.read()).hexdigest()
        except OSError:
            escape.append(rel)
            continue
        if actual != recorded.lower():
            digest_bad.append(rel)
    if escape:
        raise _GateFail('artifacts=%d,escape=%d' % (len(artifacts), len(escape)))
    if digest_bad:
        raise _GateFail('artifacts=%d,digest-bad=%d' % (len(artifacts), len(digest_bad)))
    if polarity_bad:
        raise _GateFail('artifacts=%d,polarity-bad=%d' % (len(artifacts), len(polarity_bad)))
    if positive < 1:
        raise _GateFail('artifacts=%d,positive=0' % len(artifacts))
    return 'artifacts=%d,positive=%d,digest-bad=0,escape=0' % (len(artifacts), positive)


# ---- R-REDACT ---------------------------------------------------------------

def rule_redact(pkg):
    """One same-digest redaction receipt per artifact, distinct producer/verifier."""
    manifest = pkg.manifest()
    artifacts = _artifacts(manifest)
    receipts = manifest.get('redactions')
    if not isinstance(receipts, list) or not receipts:
        raise _GateFail('redactions=empty')
    by_path = {}
    by_digest = {}
    for artifact in artifacts:
        path = artifact.get('path')
        digest = artifact.get('sha256')
        if isinstance(path, str):
            by_path[path] = artifact
            by_path['evidence/' + path] = artifact
        if isinstance(digest, str):
            by_digest.setdefault(digest.lower(), []).append(artifact)

    bound = {}
    extra = 0
    digest_mismatch = 0
    identity_bad = 0
    for receipt in receipts:
        if not isinstance(receipt, dict):
            extra += 1
            continue
        path = receipt.get('artifact')
        if not isinstance(path, str):
            path = receipt.get('path')
        artifact = by_path.get(path) if isinstance(path, str) else None
        if artifact is None:
            digest = receipt.get('artifact_sha256')
            candidates = by_digest.get(digest.lower(), []) if isinstance(digest, str) else []
            if len(candidates) == 1:
                artifact = candidates[0]
        if artifact is None:
            extra += 1
            continue
        key = artifact.get('path')
        if key in bound:
            extra += 1
            continue
        bound[key] = receipt
        recorded = artifact.get('sha256', '')
        first = receipt.get('artifact_sha256')
        second = receipt.get('scanned_artifact_sha256')
        if not (isinstance(first, str) and isinstance(second, str)
                and isinstance(recorded, str)
                and first.lower() == second.lower() == recorded.lower()):
            digest_mismatch += 1
        producer = receipt.get('producer')
        verifier = receipt.get('verifier')
        if (not isinstance(producer, str) or not producer.strip()
                or not isinstance(verifier, str) or not verifier.strip()
                or producer.strip().casefold() == verifier.strip().casefold()):
            identity_bad += 1
    missing = [artifact.get('path') for artifact in artifacts
               if artifact.get('path') not in bound]
    if missing:
        raise _GateFail('artifacts=%d,receipts=%d,missing=%d' % (len(artifacts), len(receipts), len(missing)))
    if extra:
        raise _GateFail('receipts=%d,unbound=%d' % (len(receipts), extra))
    if digest_mismatch:
        raise _GateFail('artifacts=%d,digest-mismatch=%d' % (len(artifacts), digest_mismatch))
    if identity_bad:
        raise _GateFail('receipts=%d,identity=%d' % (len(receipts), identity_bad))
    return 'artifacts=%d,receipts=%d,missing=0,digest-mismatch=0' % (len(artifacts), len(receipts))


# ---- R-CUSTODIAN ------------------------------------------------------------

def rule_custodian(pkg):
    """Decision chain shape, scope signal, grant id, head/manifest three-way bind."""
    manifest = pkg.manifest()
    head_expected = manifest.get('expected_head_sha256')
    document = pkg.read_json('custodian-receipts.json')
    if not isinstance(document, dict):
        raise _GateFail('receipts=not-object')
    chain = document.get('chain')
    if not isinstance(chain, list):
        chain = document.get('decisions')
    if not isinstance(chain, list) or not chain:
        raise _GateFail('chain=empty')
    grant_miss = 0
    signal_bad = 0
    digest_bad = 0
    for index, decision in enumerate(chain):
        if not isinstance(decision, dict):
            digest_bad += 1
            continue
        if not isinstance(decision.get('action'), str) or not decision['action'].strip():
            digest_bad += 1
        for key in ('input_sha256', 'decision_sha256'):
            value = decision.get(key)
            if not isinstance(value, str) or not HEX64.match(value):
                digest_bad += 1
        grant = decision.get('matched_grant_id')
        if not isinstance(grant, str) or not grant.strip():
            grant_miss += 1
        if decision.get('scope_signal') != 'NO_SCOPE_OBJECTION':
            signal_bad += 1
    final = chain[-1]
    final_digest = final.get('decision_sha256') if isinstance(final, dict) else None
    head = document.get('head_sha256')
    if (not isinstance(head, str) or not HEX64.match(head)
            or not isinstance(final_digest, str) or not HEX64.match(final_digest)
            or head.lower() != final_digest.lower()):
        raise _GateFail('chain=%d,head=mismatch' % len(chain))
    if not isinstance(head_expected, str) or not HEX64.match(head_expected):
        raise _GateFail('chain=%d,manifest-head=bad' % len(chain))
    if head.lower() != head_expected.lower():
        raise _GateFail('chain=%d,head-manifest=mismatch' % len(chain))
    if signal_bad:
        raise _GateFail('chain=%d,signal-bad=%d' % (len(chain), signal_bad))
    if grant_miss:
        raise _GateFail('chain=%d,grant-miss=%d' % (len(chain), grant_miss))
    if digest_bad:
        raise _GateFail('chain=%d,digest-bad=%d' % (len(chain), digest_bad))
    return 'chain=%d,grant-miss=0,signal-bad=0,head=bound' % len(chain)


# ---- R-PROVENANCE -----------------------------------------------------------

def rule_provenance(pkg):
    """Agents/models, commands/exit codes, pin, policy digest, no effects, attestation."""
    document = pkg.read_json('provenance.json')
    if not isinstance(document, dict):
        raise _GateFail('provenance=not-object')
    agents = document.get('agents')
    if not isinstance(agents, list) or not agents:
        raise _GateFail('agents=empty')
    agent_bad = 0
    for agent in agents:
        if not isinstance(agent, dict):
            agent_bad += 1
            continue
        for key in ('transition', 'requested_model', 'resolved_model'):
            value = agent.get(key)
            if not isinstance(value, str) or not value.strip():
                agent_bad += 1
                break
    commands = document.get('commands')
    if not isinstance(commands, list) or not commands:
        raise _GateFail('commands=empty')
    command_bad = 0
    for command in commands:
        if not isinstance(command, dict):
            command_bad += 1
            continue
        if not isinstance(command.get('command'), str) or not command['command'].strip():
            command_bad += 1
        code = command.get('exit_code')
        if isinstance(code, bool) or not isinstance(code, int):
            command_bad += 1
    pin = document.get('pin')
    if not isinstance(pin, dict):
        raise _GateFail('pin=absent')
    remote = pin.get('remote')
    commit = pin.get('commit')
    if not isinstance(remote, str) or not remote.strip():
        raise _GateFail('pin=remote')
    if not isinstance(commit, str) or not HEX_ANY.match(commit):
        raise _GateFail('pin=commit')
    policy = document.get('policy_sha256')
    if not isinstance(policy, str) or not HEX64.match(policy):
        raise _GateFail('policy_sha256=bad')
    effects = document.get('external_effects_performed')
    if not isinstance(effects, list) or effects:
        raise _GateFail('external_effects_performed=not-empty')
    attestation = document.get('secrets_attestation')
    if isinstance(attestation, str):
        if not attestation.strip():
            raise _GateFail('secrets_attestation=empty')
    elif isinstance(attestation, dict):
        if not attestation or attestation.get('no_secrets') is not True:
            raise _GateFail('secrets_attestation=not-affirmative')
    else:
        raise _GateFail('secrets_attestation=absent')
    if agent_bad:
        raise _GateFail('agents=%d,agents-bad=%d' % (len(agents), agent_bad))
    if command_bad:
        raise _GateFail('commands=%d,commands-bad=%d' % (len(commands), command_bad))
    return 'agents=%d,commands=%d,pin=ok,effects=none,secrets=ok' % (len(agents), len(commands))


# ---- R-STATUS ---------------------------------------------------------------

def _identities(manifest):
    """Every producer/verifier identity the manifest's redaction receipts name."""
    identities = set()
    receipts = manifest.get('redactions')
    if isinstance(receipts, list):
        for receipt in receipts:
            if not isinstance(receipt, dict):
                continue
            for key in ('producer', 'verifier'):
                value = receipt.get(key)
                if isinstance(value, str) and value.strip():
                    identities.add(value.strip().casefold())
    return identities


def _named_blocker(status):
    for key in ('blockers', 'residual_gates'):
        value = status.get(key)
        if isinstance(value, list) and any(isinstance(item, str) and item.strip() for item in value):
            return True
        if isinstance(value, str) and value.strip():
            return True
    for key in ('verdict', 'claimability_blocker', 'blocked_reason'):
        value = status.get(key)
        if isinstance(value, str) and value.strip():
            return True
    return False


def rule_status(pkg):
    """Manifest-byte binding, reviewer distinctness, claimable/blocker coherence."""
    manifest_bytes = pkg.read_bytes('evidence/manifest.json')
    manifest = pkg.manifest()
    status = pkg.read_json('status.json')
    if not isinstance(status, dict):
        raise _GateFail('status=not-object')
    recorded = status.get('manifest_sha256')
    actual = hashlib.sha256(manifest_bytes).hexdigest()
    if not isinstance(recorded, str) or not HEX64.match(recorded):
        raise _GateFail('manifest_sha256=bad')
    if recorded.lower() != actual:
        raise _GateFail('manifest_sha256=mismatch')
    review = _require_dict(status, 'claim_review', 'status')
    hard = _require_dict(review, 'hard_gates', 'claim_review')
    subchecks = _require_dict(review, 'subchecks', 'claim_review')
    reviewer = _require_dict(review, 'reviewer', 'claim_review')
    missing = [key for key in HARD_GATE_KEYS if key not in hard]
    missing += [key for key in SUBCHECK_KEYS if key not in subchecks]
    if missing:
        raise _GateFail('gates-missing=%d' % len(missing))
    identity = reviewer.get('identity')
    if not isinstance(identity, str) or not identity.strip():
        raise _GateFail('reviewer:identity')
    for key in ('requested_model', 'resolved_model'):
        value = reviewer.get(key)
        if not isinstance(value, str) or not value.strip():
            raise _GateFail('reviewer:' + key)
    if not isinstance(reviewer.get('fallback'), bool):
        raise _GateFail('reviewer:fallback')
    if identity.strip().casefold() in _identities(manifest):
        raise _GateFail('reviewer=not-distinct')
    claimable = status.get('claimable')
    if not isinstance(claimable, bool):
        raise _GateFail('claimable=not-bool')
    if claimable:
        failing = [key for key in HARD_GATE_KEYS if hard.get(key) != 'PASS']
        failing += [key for key in SUBCHECK_KEYS if subchecks.get(key) != 'PASS']
        if failing:
            raise _GateFail('claimable=true,gates-not-pass=%d' % len(failing))
        count = status.get('finding_count')
        if isinstance(count, bool) or not isinstance(count, int) or count < 1:
            raise _GateFail('claimable=true,finding_count=bad')
        return 'manifest=bound,reviewer=distinct,gates=6/6,claimable=true'
    if not _named_blocker(status):
        raise _GateFail('claimable=false,blocker=none')
    return 'manifest=bound,reviewer=distinct,gates=6/6,claimable=false,blocker=named'


# ---- R-REPORT ---------------------------------------------------------------

def rule_report(pkg):
    """Scope excerpt heading, no-submission literal, program URL, cited digests bound."""
    text = pkg.read_bytes('report.md').decode('utf-8', 'replace')
    manifest = pkg.manifest()
    artifacts = _artifacts(manifest)
    digests = {str(artifact.get('sha256', '')).lower() for artifact in artifacts}
    if not SCOPE_EXCERPT.search(text):
        raise _GateFail('scope-excerpt=absent')
    if NO_SUBMISSION not in text:
        raise _GateFail('marker=absent')
    if not HTTPS_URL.search(text):
        raise _GateFail('url=absent')
    cited = {token.lower() for token in HEX64_TOKEN.findall(text)}
    unbound = sorted(token for token in cited if token not in digests)
    if unbound:
        raise _GateFail('cited=%d,unbound=%d' % (len(cited), len(unbound)))
    return 'scope-excerpt=ok,marker=ok,url=ok,cited=%d,unbound=0' % len(cited)


# ---- R-NOSECRET -------------------------------------------------------------

def rule_nosecret(pkg):
    """Symlink ban, 5 MiB cap, secret-shaped-token scan; never prints a value."""
    symlinks = 0
    oversize = 0
    hits = 0
    first = ''
    first_pattern = ''
    for dirpath, dirnames, filenames in os.walk(pkg.root, followlinks=False):
        dirnames.sort()
        for name in sorted(dirnames):
            if os.path.islink(os.path.join(dirpath, name)):
                symlinks += 1
        for name in sorted(filenames):
            full = os.path.join(dirpath, name)
            try:
                st = os.lstat(full)
            except OSError:
                continue
            if stat.S_ISLNK(st.st_mode):
                symlinks += 1
                continue
            if not stat.S_ISREG(st.st_mode):
                continue
            if st.st_size > MAX_SCAN_BYTES:
                oversize += 1
                continue
            try:
                with open(full, 'rb') as handle:
                    data = handle.read()
            except OSError:
                raise _GateFail('unreadable:%s' % _gate_token(os.path.relpath(full, pkg.root)))
            rel = os.path.relpath(full, pkg.root)
            for pattern_name, pattern in SECRET_PATTERNS:
                if pattern.search(data):
                    if not first:
                        first = rel
                        first_pattern = pattern_name
                    hits += 1
                    break
    if symlinks:
        raise _GateFail('symlinks=%d' % symlinks)
    if oversize:
        raise _GateFail('oversize=%d' % oversize)
    if hits:
        raise _GateFail('hits=%d,first=%s,shape=%s' % (hits, _gate_token(first), first_pattern))
    return 'files-scanned=ok,symlinks=0,oversize=0,hits=0'


_GATE_RULE_IMPL = {
    'R-FILES': rule_files,
    'R-MANIFEST': rule_manifest,
    'R-REDACT': rule_redact,
    'R-CUSTODIAN': rule_custodian,
    'R-PROVENANCE': rule_provenance,
    'R-STATUS': rule_status,
    'R-REPORT': rule_report,
    'R-NOSECRET': rule_nosecret,
}


def run_rules(package_dir):
    """Evaluate the eight rules in order; returns the per-rule result list."""
    pkg = Package(package_dir)
    results = []
    for rule_id in _GATE_RULE_ORDER:
        try:
            detail = _GATE_RULE_IMPL[rule_id](pkg)
            verdict = 'pass'
        except _GateFail as exc:
            detail = str(exc) or 'failed'
            verdict = 'fail'
        except Exception as exc:  # fail closed: an internal error is not a pass
            detail = 'error:' + type(exc).__name__
            verdict = 'fail'
        results.append({'id': rule_id, 'verdict': verdict, 'detail': detail})
    return results


def evaluate(package_arg):
    """Return (results, exit_status, summary_verdict)."""
    if not os.path.isdir(package_arg):
        return None, 2, 'ERROR'
    results = run_rules(package_arg)
    failed = sum(1 for result in results if result['verdict'] != 'pass')
    return results, (0 if failed == 0 else 1), ('WELL-FORMED' if failed == 0 else 'DEFECT')


def emit(package_arg, results, status, verdict, as_json):
    if as_json:
        payload = {
            'package': package_arg,
            'rules': results,
            'rules_count': len(_GATE_RULE_ORDER),
            'pass': 0,
            'fail': 0,
            'verdict': verdict,
            'exit': status,
        }
        if results is not None:
            payload['pass'] = sum(1 for result in results if result['verdict'] == 'pass')
            payload['fail'] = sum(1 for result in results if result['verdict'] != 'pass')
        sys.stdout.write(json.dumps(payload, sort_keys=True) + '\n')
        return
    if results is None:
        sys.stdout.write('package=%s verdict=ERROR exit=2\n' % package_arg)
        return
    for result in results:
        sys.stdout.write('RULE %s verdict=%s detail=%s\n'
                         % (result['id'], result['verdict'], result['detail']))
    passed = sum(1 for result in results if result['verdict'] == 'pass')
    failed = sum(1 for result in results if result['verdict'] != 'pass')
    sys.stdout.write('package=%s rules=%d pass=%d fail=%d verdict=%s exit=%d\n'
                     % (package_arg, len(_GATE_RULE_ORDER), passed, failed, verdict, status))


def selftest_dispatch(rest):
    """Run the `--selftest` implementation that lives beside or inside this file.

    Preferred: a module-level `run_selftest(gate_path)` pasted into this file
    (ExecGateSelftest supplies it). Fallback: a standalone companion script
    `claim-package-selftest.py` in this file's directory (or $CLAIM_PACKAGE_SELFTEST).
    With neither available the call exits 2: an absent selftest is never green.
    """
    hook = globals().get('run_selftest')
    if callable(hook):
        return int(hook(os.path.abspath(__file__)))
    companion = os.environ.get('CLAIM_PACKAGE_SELFTEST') or os.path.join(
        os.path.dirname(os.path.realpath(__file__)), 'claim-package-selftest.py')
    if os.path.isfile(companion):
        return subprocess.call([sys.executable, companion] + list(rest))
    sys.stdout.write('selftest module=%s verdict=missing exit=2\n' % companion)
    return 2


def main(argv):
    if '--selftest' in argv:
        rest = [arg for arg in argv if arg != '--selftest']
        return selftest_dispatch(rest)
    parser = argparse.ArgumentParser(
        prog='claim-package-check.py',
        description='Gate the six-file claim-package contract with eight fail-closed rules.')
    parser.add_argument('package', nargs='?', help='package directory (contains report.md, ...)')
    parser.add_argument('--json', action='store_true', help='print one JSON object instead of text')
    args = parser.parse_args(argv)
    if not args.package:
        parser.error('a package directory is required')
    results, status, verdict = evaluate(args.package)
    emit(args.package, results, status, verdict, args.json)
    return status


# <!-- selftest-body-paste-anchor: paste run_selftest(...) ABOVE this guard -->
if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
