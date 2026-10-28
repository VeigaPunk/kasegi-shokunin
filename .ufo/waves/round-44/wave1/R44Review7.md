# R44Review7 — C1 defect 7: instrument registry pointer

## Finding

**Confirmed defect; safe remediation is a report-pointer retarget (not adding duplicate rows).** The exact C1 item is R43 verifier spot-check §6.7: the round-43 report's SHONEN bullet says both new instruments are registered in `corpus/instruments/README.md`, but that file has zero hits for `r43-closure.sh` / the claim-package gate; the correct registry home for instruments is the Gates & probes table in root `SKILL.md`, while the r43 suite's gate registration is separately noted in `corpus/README.md`.

Evidence:
- Frozen source `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/lessons/round-43-verifier-spotcheck.md:107` states the defect and suggested retarget-or-append remedy; `:30` records the original pointer claim and zero hits in the instruments README.
- `/home/vgpnk/Projects/shokunin/kasegi-shokunin/corpus/instruments/README.md:1-12` documents the instruments collection and lists the three original depth scripts, not the two R43 instruments. This README is descriptive documentation, not the instrument index/registry.
- The actual instrument registry is root `SKILL.md`'s **Gates & probes registry** table (R43 closure item) and the gate-registration note is `corpus/README.md`; the latter distinction is explicitly reported in spot-check `:30`.
- `corpus/lessons/round-43.md:144` calls the claim gate's landed pointer `corpus/instruments/claim-package-check.py` and names its knowledge entry, illustrating a valid code-location pointer, not proof of registry registration.

## Discriminate do-nothing

The round-44 frozen control (`.ufo/waves/round-44/controls/do-nothing.txt:2-7`) pins base `5ab3a60a5cb09e5880d11e8a1b96f9b29d368c7a`, counts eight routed defects and states none has an R44 correction at base. Therefore this pointer correction is **not fixed by do-nothing**. No claim is made here about the final R44 resolution or committed R44 changes.

## Safe remediation

Append the correction to the report/lesson as required by §6's append-only rule (`round-43-verifier-spotcheck.md:99`): replace the erroneous registry pointer with the actual `SKILL.md` Gates & probes registry location (and, if referring to the r43 closure suite's gate note, distinguish its `corpus/README.md` registration). Do not append duplicate registrations to `corpus/instruments/README.md` merely to preserve the inaccurate sentence. Do not rewrite historical report text in place.

## Limitations / verification

This is a read-only scope review. The requested first `controls/do-nothing.txt` path was absent; the actual frozen control is `.ufo/waves/round-44/controls/do-nothing.txt`, read before analysis. No LSP device/status was exposed in the available tool inventory, so no semantic references/definition/diagnostics were available; evidence is direct file content. No tools installed. No git/jj/index or production files changed. Scratch was not created, so nothing required cleanup.

## Report trailer

Relative to `/home/vgpnk/Projects/shokunin/kasegi-shokunin`: `.ufo/waves/round-44/wave1/R44Review7.md`
