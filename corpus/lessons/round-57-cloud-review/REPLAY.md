# Replaying this review

From the workspace root, with recovered lane repo present:

```sh
A=shokunin-training/audit/kasegi57-independent
L=shokunin-training/lanes/kasegi
mkdir -p "$A/export" "$A/base-export"
git -C "$L" archive 9b1028c00656d2693f4accc513e14c4c180a2f27 | tar -x -C "$A/export"
git -C "$L" archive eae1d614542e8d30d77e9f4e8b9dea6a11aad138 | tar -x -C "$A/base-export"
python3 "$A/run.py"
bash "$A/check.sh"
python3 "$A/integrity.py"
```

`candidate/` retains the three exact small inputs used by `run.py`; the final-tip byte rebind is `rebind.txt`. Frozen cases must not be regenerated: running build_cases.py again would overwrite their freeze clock. Export trees were removed after verification; commands above restore them from cited commits. Original receipts remain unchanged; replay outputs should use new filenames. Scripts use absolute host paths where the candidate's own instruments require the Git object store. Review receipts do not assert portability of old host-bound source checks.
