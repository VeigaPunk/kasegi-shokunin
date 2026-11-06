# MutCounter — r83 C1 counter new-limb mutation probe

Round 83, attempt 1, seat `MutCounter` (leaf; one probe). Frozen counter
`.ufo/waves/round-83/c1/mutbat.py` sha256 `2f7c49d44bb1f21e8286d1a8b54d4c57bccc0be990fd7946a57813db0d81cb7d`
(617 lines); frozen candidate `.ufo/waves/round-83/c1/recheck-cwd-census.py` sha256
`343b21e46d4107fd81456840b7547b514283541bbe6fc2fface1da1adece08c9`; frozen table
`.ufo/waves/round-83/c1/mutant-table.json` sha256 `5b1d99f59cede6cffa36d554ce7e8256bf1eba1cb84a9591bfbb9f7f386b6f44`
(67 rows; one row, G4, carries `extra`). Scratch `/fast/scratch/hyaku/kasegi-r83/MutCounter`
(deleted at yield). The lane tree was never written.

## Method

Thirteen single mutants, one per round-83 limb: mutant run-dir prefix, decoy run-dir prefix,
keyed D1, keyed D2, D3 skipped, D3 no-op, D3 candidate filter, D3 selection, `extra` applied,
`extra` uniqueness, `validate_rows` extra shape, `DECOY` output line, `decoy_ok` in the exit
predicate. Each is a unique-substring replacement asserted to occur exactly once in the frozen
bytes; unified diffs are in the receipts. Detector for every run, pristine and mutated:

```
TMPDIR=$S python3 -B <mutant> --selftest --work $S/work/<id>
```

`KILLED` = `mutbat selftest FAIL` and/or rc != 0; `SURVIVED` = rc 0 with `mutbat selftest ok`.
Baseline (pristine copy, sha `2f7c49d4…`, byte-identical to the lane file by `cmp -s`): rc 0,
`mutbat selftest ok … r83_forgeries={'count': (True, False), 'hashwl': (True, False),
'path': (True, False)} bad_tables=[True, True, True, True]`. Restoration: the lane counter was
never opened for writing; after all runs `cmp -s $S/base/mutbat.py
.ufo/waves/round-83/c1/mutbat.py` printed identical and both sha256 values stayed `2f7c49d4…`;
the pristine detector was re-run on those bytes (rc 0). For the two `extra` mutants the same
67-row battery was also run over the frozen candidate bytes with the frozen table
(`--expect-cases 27`), because only that run can decide P3.

## Mutant table

| # | new limb mutated | exact diff (frozen -> mutant) | rc | verdict | detector evidence |
|---|---|---|---|---|---|
| M01 | constant mutant run dir | `prefix=("mutbat-%s-" % row["id"]) if legacy else "mutbat-t-"` -> `prefix="mutbat-%s-" % row["id"]` | 1 | **KILLED** | `r83_forgeries path=(True, True)` (path forgery accepted; the `killed=0` assertion also fails) |
| M02 | constant decoy run dir | `prefix="mutbat-t-" if nonce is not None else "mutbat-decoy-"` -> `prefix=("mutbat-%s-" % (d3_id or "decoy")) if nonce is not None else "mutbat-decoy-"` | 0 | SURVIVED | `mutbat selftest ok`, `path=(True, False)` |
| M03 | keyed D1 nonce | `[d + "_mutbat_k = %r\n" % nonce for d in decoys]` -> `[d1, d2 + "_mutbat_k = %r\n" % nonce]` | 0 | SURVIVED | `mutbat selftest ok`, `hashwl=(True, False)` |
| M04 | keyed D2 nonce | same expression -> `[d1 + "_mutbat_k = %r\n" % nonce, d2]` | 0 | SURVIVED | `mutbat selftest ok`, `hashwl=(True, False)` |
| M05 | D3 limb | `d3_id, d3 = single_decoy(…)` / `if d3 is None: return False, decoys, None` / `decoys.append(d3)` -> `d3_id = None` | 1 | **KILLED** | `count=(True, True)` |
| M06 | D3 insertion | `return rid, src[:pos] + "  # mutbat-%s" % nonce + src[pos:]` -> `return rid, src` | 1 | **KILLED** | `count=(True, True)` |
| M07 | D3 candidate filter | `{n for n in range(1, len(lines) + 1) if n not in inside and lines[n - 1].strip() and not lines[n - 1].endswith("\\")}` -> `set(range(1, len(lines) + 1))` | 0 | SURVIVED | `mutbat selftest ok` |
| M08 | D3 selection | `cands[int(nonce, 16) % len(cands)]` -> `cands[0]` | 0 | SURVIVED | `mutbat selftest ok` |
| M09 | `extra` application | remove `for anchor, repl in row.get("extra", []): … out = out.replace(anchor, repl, 1)` | 0 | SURVIVED | `mutbat selftest ok`; **P3 FALSE** (below) |
| M10 | `extra` uniqueness | remove `if out.count(anchor) != 1: return None` from the extra loop | 0 | SURVIVED | `mutbat selftest ok`; P3 exact (below) |
| M11 | `validate_rows` extra shape | remove `extra = row.get("extra", [])` … `return "row %s has a malformed extra"` | 1 | **KILLED** | `bad_tables=[True, True, True, False]` |
| M12 | `DECOY` output line | remove `lines.append("DECOY keyed=%s nonce=%s d3_row=%s" …)` | 0 | SURVIVED | `mutbat selftest ok` |
| M13 | `ok` predicate | `… and tally["neutral_ok"] == n_neutral and decoy_ok and hidden >= 1)` -> drop `decoy_ok and` | 1 | **KILLED** | `selfdiff_forgery_exit=True`, `count=(True, True)`, `hashwl=(True, True)` |

Tally: 13 mutants — 5 KILLED, 8 SURVIVED.

Observed 67-row runs over the frozen candidate (P3 command shape, random nonce):

```
M09-extra-ignored:                     G4 SURVIVED rc=0
  killed=63 survived=1 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3 decoy=ok decoy_hidden=63/64  (battery rc=1)
M10-extra-notderived-check-dropped:    G4 KILLED rc=1 failed_cases=main-verbose
  killed=64 survived=0 miskilled=0 dirty=0 notderived=0 neutral_ok=3/3 decoy=ok decoy_hidden=63/64  (battery rc=0)
  target_sha256=343b21e4…67-row run identical to the frozen P3 line
```

## Survivors: frozen-predicate impact and the cheapest killing assertion

| # | Would a frozen C1 predicate become false if the mutant were the landed counter? | Cheapest `--selftest` assertion that kills it |
|---|---|---|
| M02 | No. The candidate is path-blind (`__file__` is read only for its own bytes, line 777), so P3's summary is unchanged (`decoy=ok`, `decoy_hidden=63/64`); under P4 F9 still exits 1 with `killed=0` (mutant dirs stay constant; a row-id decoy dir only changes why the decoy breaks). | Add a toy forgery that reports one missing anchor only when its run dir starts with `mutbat-t-`; under pristine D3's constant dir it fails and the battery rejects it (`killed=0`), under M02 D3's row-id dir makes it pass while mutant dirs still fail, so the battery accepts it and the existing `not new[0]` / `killed=0` r83 assertions FAIL. |
| M03 | No (inference from the two keyed decoys): F10 still finds D2 keyed, so P4 keeps `rc=1 decoy=broken`; P3 is unchanged because the candidate passes decoys either way. | In `selftest`, call `run_decoy(toy, rows=good, nonce="00000000000000a1")` and assert both `decoys[0]` and `decoys[1]` end with `_mutbat_k = '00000000000000a1'\n`. |
| M04 | No, symmetric to M03: D1 keyed still breaks F10. | Same assertion — both returned D1 and D2 tails must carry the nonce. |
| M07 | No. The filter is irrelevant on the frozen table: the eligible candidate set is identical with and without it (39 rows, same order; `d3-candidates-static.txt`), and no anchor's first newline ends inside a string token, so every nonce picks the same row and P3/P4 are unchanged (inference, statically checked). | Unit assertion: `single_decoy('DOC = """alpha\nbeta"""\n', [row_ending_on_line_1], nonce) == (None, None)` — an anchor whose first newline ends inside a string token must be ineligible. |
| M08 | No. D3 still hides exactly one eligible anchor, so `decoy_hidden`, `decoy=ok`, F11's one-missing-anchor failure and P3 are unchanged (inference; cands[0] = K-M1, whose anchor occurs once in the forged source); only the diagnostic `d3_row=` differs. | In `selftest`, assert the returned id is the nonce index: with `good2` and nonce `00000000000000a1` (index 1) assert `single_decoy(toy, good2, "00000000000000a1")[0] == "T2-B"` (M08 returns `"T2-A"`). |
| M09 | **Yes — P3** (observed). G4's `extra` flips `main()`'s default verbose (candidate line 778) and is what makes the `main-verbose` case fail; with extras ignored only G4's weakened `main-default` limb remains and passes. The 67-row candidate run printed `killed=63 survived=1`, rc 1, instead of the pinned `killed=64 survived=0`, rc 0. P1/P2/P4-P8 are unaffected, and the counter's own selftest still says ok. | Assert `apply_row(TOY, {"id":"T-EXTRA","anchor":"def untested(x):\n","replacement":"def untested(x):\n","class":"assertion","kill_cases":["a"],"extra":[["    return (x > 0)\n","    return True\n"]]}) == TOY.replace("    return (x > 0)\n", "    return True\n", 1)` — an identity primary with a behaviour-bearing extra must yield the extra-applied bytes (or add one battery row whose extra alone flips a kill case). |
| M10 | No (observed). G4's extra anchor `    root, lane, verbose = ".", DEFAULT_LANE, False\n` occurs exactly once after the primary replacement, so the removed uniqueness branch changes no row; the 67-row candidate run reproduced the frozen P3 line byte-for-byte (`killed=64 survived=0 … decoy=ok decoy_hidden=63/64`, rc 0). | Assert `apply_row("a\nb\na\n", {"id":"T-DUP","anchor":"b\n","replacement":"b\n","class":"assertion","kill_cases":["a"],"extra":[["a\n","c\n"]]}) is None` — an extra anchor occurring twice must be NOT-DERIVED. |
| M12 | No. No predicate or selftest assertion reads the `DECOY` line: P3 reads the `MUTBAT` summary, P6 the `mutbat selftest` line, and the P4 driver parses only `MUTANT`/`MUTBAT` lines. | After the first `battery(...)` in `selftest`, assert `any(l.startswith("DECOY keyed=yes nonce=") and " d3_row=" in l for l in lines)` and that the line is second-to-last. |

## Findings (coverage, not contract changes)

1. **M09 is the real gap: the `extra` limb is unexercised by the counter's selftest, and only
   the frozen table catches it.** The selftest's tables contain no row with a well-formed
   `extra`; `bad_tables` only checks a malformed shape via `validate_rows`. A landed M09 would
   falsify P3 at landing (`killed=63 survived=1`, rc 1) while P1/P2/P4-P8 stay true — C1 still
   fails, but the counter gives a false green.
2. **M10: the extra-uniqueness branch is unexercised.** No selftest row has an `extra` anchor
   absent or duplicated after the primary replacement; the frozen table happens not to need the
   branch (G4's extra anchor is unique), so P3 is blind to its removal too.
3. **Keying is pinned as a conjunction, not per decoy (M03/M04).** Either single keying drop is
   invisible because the other keyed decoy still breaks F10; only dropping both would be caught
   (`hashwl=(True, True)`). P4's F10 expectation therefore holds for either single drop.
4. **D3's candidate policy is not observed (M07/M08).** The `comment_lines` filter is dead code
   on the current bytes (identical 39-candidate list with and without it; no anchor ends inside
   a string), and nonce-indexed selection is unobserved because any one eligible anchor suffices
   for the count/hashwl forgeries.
5. **The constant decoy prefix is not observed (M02).** Restoring a row-id leak in decoy
   directory names leaves the selftest green and P3/P4 unchanged; the path forgery is still
   rejected under r83 by `killed=0`.
6. **The `DECOY` diagnostic line is unobserved (M12).** Removing it keeps the selftest and all
   P1-P8 true; it is the only receipt exposing `keyed=`, the nonce and `d3_row`, so its removal
   reduces auditability without a behavioral signal.
7. **Byte pin is the only guard for seven of eight survivors.** The counter sha is not one of
   P1-P8; C1's kill rule ("frozen counter bytes differ between freeze and landing") is what
   rejects M02/M03/M04/M07/M08/M10/M12 if landed. Survival here is a selftest-coverage statement,
   not licence to relax the pin.

## Receipts

Under `.ufo/waves/round-83/w1/MutCounter-receipts/`: `base.txt` (pristine selftest, rc 0),
`rcs.txt`, `summary.json`, `frozen-hashes.txt`, one `M<nn>-*.txt` selftest output and one
`M<nn>-*.diff` unified diff per mutant, `d3-candidates-static.txt` (static D3 candidate
comparison on the frozen bytes), and `cand-M09-extra-ignored.txt` /
`cand-M10-extra-notderived-check-dropped.txt` (the 67-row battery over the frozen candidate for
the two `extra` mutants). No tool was installed or upgraded.
