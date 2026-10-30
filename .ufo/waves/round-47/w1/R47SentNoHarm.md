# R47SentNoHarm — frozen no-harm baseline
**Axes:** depth:verifiability; coverage. **Disposition:** baseline captured; no protected working-tree drift observed. This is not a C1/C2 closure verdict.
Frozen commit `308a2cb2dc7bdce233461cc1ac49dd88e51c6193`; base `fc8e0af27fbfa13220cd245700e9cb7e5e94dfc8`. Timestamp `2026-10-30T11:49:53.158995+00:00`. Paths below are relative to the lane repo. Hashes are SHA-256 of exact bytes, not Git object IDs.
## Evidence and method
Executed read-only `git -C /home/vgpnk/Projects/shokunin/kasegi-shokunin ls-tree -r --name-only 308a2cb2dc7bdce233461cc1ac49dd88e51c6193`, then one `git cat-file --batch` request per `FREEZE:path`, and Python `hashlib.sha256(bytes).hexdigest()`. Compared the resulting immutable-object bytes with each live file. Printed output: `immutable_files=964 r46_artifacts=898 knowledge=65 rows=73 total_bytes_hashed=9150116 drift=[] symlinks=[]`. All 968 distinct sampled files matched freeze bytes. No Git mutation, counter execution, package installation, background job, network request, or sibling-lane access.
Protected historical scope: All freeze-tracked .ufo/waves/round-46/**; corpus/source-snapshots/round-46/** and round-46-a2/**; corpus/instruments/r46* including descendants; corpus/lessons/*round-46*.md. No other tracked path matches round[-_]?46 or r46[-_.]. Untracked historical files are outside this frozen-object inventory; no recursive sweep of untracked historical fixture trees was performed.
`bash /home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` printed `/fast/scratch/hyaku use%=54% free=375.2G`, `/tmp use%=25% free=96.7G`, `/var/tmp use%=41% free=532.8G`. Scratch was empty except this seat-created directory and is removed before return.
## Integration rules and limitations
- Immutable files must retain the listed bytes; missing files, changed mode/symlink substitutions, or unexpected replacements require rejection/review. Digests cover contents, not ownership or permission bits.
- Append-only files must have size >= recorded bytes and SHA-256 of exactly their first N bytes equal the listed digest. Hashing the entire post-append file would incorrectly reject legitimate append-only additions.
- SOURCES rows S001–S073 are individually byte-pinned including newline; locate each ID exactly once, then compare its whole row. This is stricter than cell-value stability (format-only changes also flag). S074 may flip; S075/S076 may be added. Do not freeze the entire SOURCES file: D5 must remove scaffold at SOURCES.md:113–123 and :177–185 and land its existing bullets; D8 may append notes outside protected rows.
- SKILL.md has multiple historical registry sections, not one contiguous exemption. Protected non-registry ranges are below. Preserve these baseline ranges in order even when registry edits shift line/byte offsets; offsets refer only to freeze. Whole-file and every existing registry-block digest are also retained for a narrow diff review; a mismatch in an excluded historical block is NOT blanket approval. Prefer only the required round-47 registry addition. Never dynamically exempt arbitrary new headings in a changed file.
- Exactly 65 existing knowledge files are immutable; the existing `github-repository-security-advisories.md` is intentionally excluded for D6/D7. F30 is new and therefore absent from freeze. Existing filename removals must not be hidden by merely recounting 67 entries.
- Frozen r46 artifacts include their manifests/captures, counters/equivalence receipts, lessons and all 877 tracked wave records. SOURCES.md:184 explicitly requires the original r46 manifest to remain byte-identical; its baseline digest is included below. Do not rewrite historical false claims while correcting current entry/registry prose.
- Point-in-time baseline only: no integrated-tree measurement was run. C1/C2 semantic correctness, completeness of new content, and live-source provenance are outside this assigned surface. Disclosed battery gaps remain C1 16 survivors and C2 18 survivors (claims.json mechanical_limits); no zero-survivor claim.
## Bounded discrimination controls
In-memory controls only, operating on frozen bytes; no fixture/production mutation. Printed results: `{"append_prefix_accepted": true, "changed_byte_whole_rejected": true, "changed_source_row_rejected": true, "do_nothing_prefix": true, "do_nothing_whole": true, "edited_prefix_rejected": true}`. Do-nothing control = unchanged frozen objects: accepted by no-harm checks. One-byte immutable edit and one-byte prefix edit: rejected; pure LOG append: accepted; source-row edit: rejected. These controls validate hash/prefix discrimination, not round progress: a do-nothing tree still fails the frozen C1/C2 acceptance targets (claims.json expect_before/freeze_tree_reading; not rerun here).
## Findings
**Informational — no observed protected-content drift.** Exploit/failure path: an integration can satisfy claim counters while silently editing old entries, history, or append-only prefixes. Evidence: 964 immutable files plus two prefix checks, 73 row checks and three SKILL ranges below provide an independent no-harm surface. Impact: without this comparison, historical provenance or unrelated research could change unnoticed. Smallest remediation: apply these comparisons to the integrated revision independently of C1/C2; investigate every mismatch, retaining the explicitly allowed edits only. No production remediation performed.
**Review caution — exemption expansion.** Defining SKILL exemptions from candidate headings alone could hide protected content under a newly inserted registry heading. This is a verification-design risk, not an observed exploit. Smallest remediation: keep the frozen protected spans as the contract and review registry-only diff hunks; do not infer permission from artifact prose.
## Append-only prefixes

| path | original lines | prefix bytes | sha256 |
|---|---:|---:|---|
| `LOG.md` | 2031 | 208735 | `8cc0e801600cb9e1c93b50beeaf842b966190deb1498b1c2618d6dbed237d3b3` |
| `corpus/README.md` | 693 | 69877 | `c676de83071a9fd6ef35cdc9fa7b8af31b5a60181fd453d96ba8f186e022e60f` |

## SKILL protected ranges

Full file informational digest: `b4dde6544298c11291fb0c6510036435a760dd0f4f0f8a05d3b3fc1e74b18db2` (134409 bytes).

| baseline lines | baseline start byte (0-based) | bytes | sha256 |
|---|---:|---:|---|
| 1–976 | 0 | 73748 | `ffce4754c733d78536bc639e42a9f57c04b6f8009c0534bf0eb784c1eda411a8` |
| 986–1036 | 75004 | 9077 | `f4356a981f3a37aff44a1acf67011118950b08eaf041e0c6302d125cce9334dd` |
| 1045–1049 | 85252 | 507 | `b2eb43a8abbb464770ee9240b48e530e6bb602b2e9fb99a06a41f0de10f25f30` |

### Registry blocks (diff-review receipts, not blanket edit permission)

| baseline lines | sha256 |
|---|---|
| 977–985 | `501eedcc320e7242ec42ebd5e19c23fb0d75bb10dc1db22848c84c60d8fb1665` |
| 1037–1044 | `ba546f115f1aabcdf78d4bfa2d044ce9acf288606fd71ff8b9159b4865317803` |
| 1050–1059 | `d8221bb015a9b059aefa7aaeaea6f1d2c102645ce03f0a2e7c17e438497dd54a` |
| 1060–1072 | `e92ed844dd57857cfcc9788e342fe7614cff8199eecacaa21da37ad306ea543c` |
| 1073–1093 | `aa497b26cb9bded262a845b48d9559d9770ad8989decd11e8bb3d65e981a2343` |
| 1094–1106 | `6c3fe489557433e04655bbc9b16f6a8dd6b443ea92fa640fd6afcec8054d7100` |
| 1107–1117 | `e639fa011053184fd3566841632a5225a717bc0a0403c8f62bd49df1ba768ff1` |
| 1118–1123 | `e1cbb8bbfd1382adeb1b8701329c20d5607f9dda280fc7cbd801932ecdc03344` |
| 1124–1129 | `0af1f77b5cb79ca4b0fcc73efca05fcb361cc18a7318dae8a5265ed01c983aae` |
| 1130–1135 | `a2eb0d60209d09912161b2cfa4adddfb6e841f40f1b9e41ffa33844a9c760f08` |
| 1136–1145 | `f97531321e91e81ccc59d0820489fa88aa565a396fb5dcf4dbfea8fa921f2e48` |
| 1146–1156 | `1f67ff4f42e39ed57a02bff46739406201f1349618f9ed9e21bc2f6f6e7e0df1` |
| 1157–1166 | `a16aaa76f2ef1ddc5c5bdb52d674b4d81d4170cf14d3f251a31a1cc4ea1a5704` |
| 1167–1173 | `5c02e916da5353c99d88b95986f0a52fdc2a1997389776626b24c7fdb4be6836` |

## SOURCES immutable registry rows

Whole-file informational hash (expected to change): `e3bdefcfaad97e093a2950af37e62430635f130d9ea2d43fb1585db988077a6c`. S074 at baseline line 80 is deliberately not in the protected set.

| id | baseline line | row bytes | sha256 (includes LF) |
|---|---:|---:|---|
| S001 | 7 | 407 | `dc51e82826cf8b180aa9d0e999c5ddaba94d0111fe9d59d6ea291b3ed47280d5` |
| S002 | 8 | 435 | `4c8f495429072a98b32dce9d0dea254435b860a6d5330f4fc1db557b62bc7e95` |
| S003 | 9 | 677 | `837ca2eda920d1cc8c2a0ca1a1f0289a410744f3bc996ca6eee1f7e432f2c531` |
| S004 | 10 | 542 | `a80ae72dcca22274707e3bc2538b90e4b2d09a84c0e7e96aa93ca9a48c0ff32a` |
| S005 | 11 | 503 | `82382abf30d18ea3c8d3521e7d118457c5f945882b4efec8261292bd141e86bc` |
| S006 | 12 | 528 | `510011e619ac00393b1b38ca92dcb45cf9e2d3c3220c8d88317a556ce17c8fb1` |
| S007 | 13 | 480 | `13d278c9b1386a0de0c41a26d42b045d0d87f6ac3d4c10651e00f29cea04a8ea` |
| S008 | 14 | 513 | `72a814133f6f22fd37ed058b2702c0700d00df6604407601d6f6164af0652ac9` |
| S009 | 15 | 545 | `d0c5f6a6b1e2f9dfaa2bd151cb68d9ed99be6b4ac4cda9386cee172f5a053869` |
| S010 | 16 | 479 | `0fdb4af4b25b4b16d3dc90eb76d16e35afc5dca2057449945590ebd89f4356f9` |
| S011 | 17 | 546 | `f235711274aac80031a8ca0edc1e224f7832479cfff0e23048ac4e1bc78442f0` |
| S012 | 18 | 472 | `ca7121bf6d739144e224538dc2b5ee3c76fcf1c3a97933bdba84f75238158490` |
| S013 | 19 | 527 | `c8ef475410499e909b9ee37cee4fc7edc7694da094bf630cf044064cb1c76f00` |
| S014 | 20 | 457 | `a89f047a6f81a4bdd37d2e1cb6fecbe7c120d37ceb00fac373a47b2325acbbbe` |
| S015 | 21 | 488 | `9a6f7a8cfeb81a37ab3323f6db185b4dc176ae1443a8a96c1854391c3b6f6f7d` |
| S016 | 22 | 554 | `31e325424525d70416d73f58ff5a5adbed132801ad5e1302f3dcd064693878cb` |
| S017 | 23 | 434 | `b2070a59705bb187fcfa8f463625d696911c32e2b54cd7204e02a28dec6c5d7c` |
| S018 | 24 | 571 | `46f62c29566349db50ed323e1335e6b33eda66ffd4ec07b891108ebfbc571a89` |
| S019 | 25 | 497 | `e78d280f6ab81dadd6eceb91eaa48554e4385ef85e6261403f587f8376dc4b0a` |
| S020 | 26 | 560 | `f810a3e27e738a59e2fdf6bdb6bd4439c1870e52f556d4dc342000aae281458c` |
| S021 | 27 | 552 | `1bf5e60ea4841eefe69b74e0306d8655cd2e0856209ad66e998e455a5c383d15` |
| S022 | 28 | 631 | `a25c7a2010af420bb6379d72afb06493ce784712e1654ed1f51e07a2829e0329` |
| S023 | 29 | 535 | `76d0d1e4cd480a87ba91d4bbeeed840ce60a481ea15984845ccbf7355006d2db` |
| S024 | 30 | 799 | `4e3d41e94881126b0d2a5757acebc6700e467036b9d3657a06389df036e47f06` |
| S025 | 31 | 547 | `0872cbcf3c9d54a14ec31dd8bb18fd9214e2c667a4a47af83000a11d0e60a06f` |
| S026 | 32 | 552 | `75fe806d115b4d3030326c445dcccd1bc3c02932df4e89fd9d4295d479ef026f` |
| S027 | 33 | 470 | `29b03e4a592e692f551f7b2459774dbd606e247d4622abaf3fc8a5037a9c2452` |
| S028 | 34 | 618 | `e3e6c28e139fe2819474bf71862a4c61ec9141e2fff3deb326c4aa24fd0b2944` |
| S029 | 35 | 602 | `7e8544de6bd013ac1798c1f5325a1de3c643bd82806583361498c36557f27c70` |
| S030 | 36 | 602 | `d81f79c35379efd0298159a7e11f7ae23fe83319f85aca59d3bcf11d7b85e887` |
| S031 | 37 | 568 | `3695ec19f0055f0de1264e9c4274b275b94f4a2463f14df2072c757509301704` |
| S032 | 38 | 795 | `de268ec0ea8f9f2a038086c9f7c832ef7ddf51748e9f91af2d4359dcc24cc793` |
| S033 | 39 | 760 | `100d7121c5266a78cfb59e47d5096ad0063357c381bb067d2850c236a2bc047a` |
| S034 | 40 | 732 | `e4082e1d8b1684f4ea71f568d9fb37dbf540d53b613cb62f2916eb98efc1b518` |
| S035 | 41 | 804 | `b4af653a90f57fd993f916695ae9399c082cbc54df36479d7b630123385181c4` |
| S036 | 42 | 992 | `2c39c3f5931f6e78c83f63df4af83b1a58b6f620a8505927ac1be2ce9248718f` |
| S037 | 43 | 1134 | `3d3f64988d18658289903ae48b8193f093bef1ac2acd1491961de3656f7263b8` |
| S038 | 44 | 952 | `11e43ba462db1e5bb2a4c19d1acecd44aef7d3a68efea00f102df86ced049709` |
| S039 | 45 | 1157 | `cd7b069cee5645dc52c5a3bfbb9752a311ca7ade04f736c9661fbe3592b1239a` |
| S040 | 46 | 1048 | `cb24fa63eea3a67bc2211d48ed252905b4fb5315d9cf6a25fb795323e0c3624e` |
| S041 | 47 | 1362 | `9c35930c3b057c5f3267920274b67102cb18e1d8535f06b8816143cf3f67867f` |
| S042 | 48 | 921 | `33d62d4e169e3a64befcb3226419bd1545550f06ec7168464344e46c3bc0c1b9` |
| S043 | 49 | 752 | `e376db945080489fbbadec4e7491b1d5db19723eab948a648823154cf4bc682f` |
| S044 | 50 | 789 | `020ace80001373446c98e9d7e17d45cbc8bca350db562a003146ea9086b85494` |
| S045 | 51 | 713 | `a3d6eee51f17018a41b4ca1cd4606fb3ab87612f0443bca40cc634ace0e94e15` |
| S046 | 52 | 705 | `316898e02b8301c2da4dc465d209e024c692e3efbc7f84499f75d61dc78f1476` |
| S047 | 53 | 501 | `77c78d5739c214fa5d53544c1afcaf4dbb57402d4cd43584f28b0fd02fd55c5b` |
| S048 | 54 | 916 | `0f2d9cb61c8743577476906fb6ea2a9285082931e5ff811dac98d0f26f83de7a` |
| S049 | 55 | 1145 | `dde2d9b9c96f9174b36695e6c7feebb73b06104ef0a69ebbaf26947f0c0cd88a` |
| S050 | 56 | 1380 | `a593b27331a3b8adc96f9e0be0dbb02b3b925f12bb02fce2dd0ef4e207fd20fa` |
| S051 | 57 | 1517 | `daecce25f3d79d6bce3a1fcfc06b4b4f1991b48620c5e0a4a37c529ab1fa618f` |
| S052 | 58 | 1598 | `ba69e0a05d7f437e684cc7714592cadb898bf35e874ddc4188ee17632bb3bc66` |
| S053 | 59 | 895 | `35c530afed9b9e8ef005223c31bba97b96af5f1d74c67fe4978a7d5bc02d6f32` |
| S054 | 60 | 866 | `83020b30ca32fd49c2a1cd85864792d01004a594b59ad2f13fb83e1e6f734f03` |
| S055 | 61 | 1713 | `901309af744b32383f3c8fe4c8023a960201baa65028600f0b9c31da59ff96cc` |
| S057 | 62 | 948 | `176762ea6a22ecffcd28e926ae026044bbbf59c40c530cf53a00c741e5d3c8d9` |
| S056 | 63 | 1281 | `e3b789f2f7c249c82a71b498ef498cdf8afa43407a3eae59895ad0da86a69ceb` |
| S058 | 64 | 1202 | `57f1ab24f58bc512301226d7fe8e8e48ca4bd759474db249c90d6909ea3f87bb` |
| S059 | 65 | 1044 | `faf60f0194690c91a6db77d8c6523e4f71034e886426619059ff3b0b80d5cb47` |
| S060 | 66 | 1673 | `5a9303e1ecc1cf9ec04ee011a5ed840dc7cab60c87f2bad8f0780ec9328b021a` |
| S061 | 67 | 1871 | `fe87b070962fc33b8a835cb545bbf901a7c90e7fbf729e71b44c6f399cf5aa9c` |
| S062 | 68 | 1605 | `0dbf7cbc2c7034a309f165e48c3b4b8c47b08d992f4a5f75b364e42d19cb874e` |
| S063 | 69 | 1425 | `e3de5d8076b9039a21513430052af8beab7e897ded4ad2cfc85bfcc7df94e5cc` |
| S064 | 70 | 1600 | `ce648c4ffcd26f7763ca644f129a9b3b4e16d8185b66bf4789e294fda605a0e2` |
| S065 | 71 | 1642 | `79c8447167d3da144b96994a93a1bc728def93f34b050da2e33cdadb41f38cbe` |
| S066 | 72 | 1839 | `147812a090269d7074273d3a4ae91c2501e2ff740a2ecf78523cff6bbb36d75e` |
| S067 | 73 | 1370 | `4e15544bd80759514bdd4d19127a36db118645a7b49de892372480cba42377b6` |
| S068 | 74 | 1892 | `c1ca669f6a030233f63173820c9fdc8eb072d15609fa6bb9492b36bdc009d6ce` |
| S069 | 75 | 1011 | `cae11aa0f74e8d4aee71bcbf20c5f3894c68c03e890acd45e2212fd021b1aba6` |
| S070 | 76 | 667 | `e2484f1f47c32eda15c35d1c3b39069a7a18c12c7c62e381125cbfbda35cd7ae` |
| S071 | 77 | 1493 | `49d5189cb4727e989e109772757a87b3d1e4ae114952b3f8844da9d48a6f0b78` |
| S072 | 78 | 1662 | `0610e2840931691c203b60df25c907efa7bb189ddd2002ef1f4f9c31ae9ce650` |
| S073 | 79 | 1300 | `8953ba3d78a105160c090e99b18272de123faac136ba89431fa8c2e86631b085` |

## Immutable whole-file inventory

964 files: PROVINCE.md + 65 knowledge entries + 898 r46 artifacts. Each line is `sha256  bytes  relative-path`.

```text
64783a90db8b4c550ca41026056ca045c2639aa7cd178e1e51f54a018551df70  168  .ufo/waves/round-46/a2w1.ready
9b693ed4fdc61ca29466318787151c94e64108d57e90a8291d4e05a1b3d71ecc  2651  .ufo/waves/round-46/a2w1.ready.dispatched
3890eb92cd119c44c53ea4ecc4a9abe2985c1f4b1c73849ee5d49e2d9d81f2c7  99860  .ufo/waves/round-46/a2w2-results.json
07caba64d7359a82f40de591444b7747a9cdd38fad65c4b69b82a7013b51249b  168  .ufo/waves/round-46/a2w2.ready
57cef3ba3d61d65386933addfb248e3fcf74c0b9218716bc7a9a62989b9a2b2e  1351  .ufo/waves/round-46/a2w2.ready.dispatched
458e3494eefc005b50df6a13425f1dece9890d1b660d7bf516a6ff04d801cbfa  449419  .ufo/waves/round-46/attempt2/a2w1-results.json
badbd8bc6bb04114a84a078c3010fd8962a4fdfeb2c3d9af3100e6b1139d1719  220  .ufo/waves/round-46/attempt2/assimilation/collisions
ee73e6562e11f9a98028e9ac5d761a3f9a5498a2a177939f71f3022de56d05ff  370  .ufo/waves/round-46/attempt2/assimilation/reg-ids
550a0129a446ae9bf0c6da3d86574b308dcadc7f4f4a2a03f704b9716948019f  470  .ufo/waves/round-46/attempt2/assimilation/staged-ids
364fac11e06fe9f1c688418c8d7f9d589eed62ace69e15ea7f2b13bba09c3626  49443  .ufo/waves/round-46/attempt2/build-wave1-spec.py
6e38b4055711c0a3406821924b6e91effec04a7b1e7b31a23534de45e246b73b  16949  .ufo/waves/round-46/attempt2/build-wave2-spec.py
ca73279f5464cf6395028c7e848b5d82bfec95794f03b7fd9b1a61cf000ca1d0  9912  .ufo/waves/round-46/attempt2/claims.json
2e95d4d4b6cf372a8464803bf82c7ae79d1612dc8060b5a9c18798cfbcbc07c2  7916  .ufo/waves/round-46/attempt2/controls/f29-defects.py
52ea96939c62a71943838ca883d7914dd598f3e7eeb061266975ece7ccb26275  9210  .ufo/waves/round-46/attempt2/controls/f29-fixture.py
0c5cff17ec697017a13a8b44de7c44587677f394e86676c455d9cc20602940ec  371  .ufo/waves/round-46/attempt2/controls/f29-gate-at-base.txt
f792ce11a514c904c2fd61e7cb885a107d6770e0259637e19b157a14cb94607d  5744  .ufo/waves/round-46/attempt2/controls/f29-r50-receipt.txt
ab4ace44ee801c0b9babf55780680bd39735f98a2c42f549a3f0e11e13139aea  2249  .ufo/waves/round-46/attempt2/controls/final-battery-c1.txt
5742697c6feef12d082ab983d7206841c8a0af95eddf3d1c461f9efa6ec8477b  3583  .ufo/waves/round-46/attempt2/controls/final-battery-c2f29.txt
466f690c2ecffcea2a5c4912c98f8a324226d7d132e71f49996d38786f733bab  607  .ufo/waves/round-46/attempt2/controls/final-battery-rerun.txt
298981e0e8f0238880640fa598c21271133ff9f920302fb97e4dcc1de1f77695  902  .ufo/waves/round-46/attempt2/controls/final-battery-summary.txt
dec981a5724d5822f83eaf7e1fb532df27f45f441f705c9f9515f17cbd783c05  374  .ufo/waves/round-46/attempt2/controls/final-battery.txt
62dea07f5171a9a8594ee13cd263c653bdad5e7fe0ef64790baeeb51d2cdef26  4217  .ufo/waves/round-46/attempt2/controls/final-measure.sh
9dbd4212b03184dc50b72a1321bdd4a0848182e09121f2347cd269cdc1bd8b18  63906  .ufo/waves/round-46/attempt2/controls/final-measure.txt
13c21fcd9e04c76b769013e56cb8db4f6546c52b2a436c08376b9f3459efb1fd  3424  .ufo/waves/round-46/attempt2/controls/mutbat-before.txt
e3bdaf2d1de46e434accc5a8867c8e945eca95a3677821d3c9a51efaef0c6fe3  294  .ufo/waves/round-46/attempt2/controls/selftest-baselines.txt
28ce995f12a6064472830039d3c6f16ee505923d7d453aa281ee9dff6d47a1f3  366  .ufo/waves/round-46/attempt2/controls/sources-census-after.txt
28ce995f12a6064472830039d3c6f16ee505923d7d453aa281ee9dff6d47a1f3  366  .ufo/waves/round-46/attempt2/controls/sources-census-before.txt
6b18734ac983a21717f63aa48d0e6e14a00fb98396a1b00ac20fee06b4a4fe6e  7040  .ufo/waves/round-46/attempt2/counter-errata.md
942353eff61f53f7e5fdfd058d94ba54874a10a23232a34509b7119262b96cd0  715  .ufo/waves/round-46/attempt2/digest-wave.py
4b887bff3fa962f9786494bce70eb4e9c7ed83230cc6b0dc0314fbed170473ed  1466  .ufo/waves/round-46/attempt2/freeze.txt
1e169823392ed6bc5ccf11a09d52599d29e7535283f4d3eab642f1c4405cfda5  216768  .ufo/waves/round-46/attempt2/wave1-dispatch.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1-dispatch.stderr.txt
dc037a615cdd6a8632a41e1fb4a2d986e727de626bc0bf91d6296d5484888168  87294  .ufo/waves/round-46/attempt2/wave1-spec.json
611d9f8d2034e5e001e80d31bc61640aad1abdf89136aef4ccd1f51493594013  23326  .ufo/waves/round-46/attempt2/wave1/R46bConnPatterns.md
2c80dbf2187fcdfbc70478f139c315f74e2b732d07092b977f47cdef51c8c3ff  4313  .ufo/waves/round-46/attempt2/wave1/R46bCritCalibration.md
7d7e79e5aadb7576756e8de6e61017b43f2bf77a7927c82b216741b2ffe5549f  6594  .ufo/waves/round-46/attempt2/wave1/R46bCritFreeze.md
e6476d094b09397d1c425edd9cdce7287d8a10e6dacf4032fff7bde1e18c5e70  5868  .ufo/waves/round-46/attempt2/wave1/R46bCritKillC1.md
dc264a54c687609da9348b8e83fafe30ee3c74c740f0ae32c395796a10f890d8  8471  .ufo/waves/round-46/attempt2/wave1/R46bCritKillC2.md
1b95ce5b2e93607175cc59f34a6721e8db4565e1812242e7b359d8de16873f36  4944  .ufo/waves/round-46/attempt2/wave1/R46bCritNovelty.md
115f1b082de7d9fa1acac01921cc6c7f56b161d67a7636d6a49e38fb7ae663c2  15047  .ufo/waves/round-46/attempt2/wave1/R46bExecCensusReceipts.draft/census.sh
d8a1a3e9d8836b27f1be1f698438cb7912761690d9d9581d905714c98edcf553  1695  .ufo/waves/round-46/attempt2/wave1/R46bExecCensusReceipts.draft/freeze-pins.txt
451d3636d709f7798a07ed96f7fdb7a765884b618fc3cb8008dab6290c69f2b8  358  .ufo/waves/round-46/attempt2/wave1/R46bExecCensusReceipts.draft/sources-census-after-preview.filemode.txt
28ce995f12a6064472830039d3c6f16ee505923d7d453aa281ee9dff6d47a1f3  366  .ufo/waves/round-46/attempt2/wave1/R46bExecCensusReceipts.draft/sources-census-after-preview.txt
28ce995f12a6064472830039d3c6f16ee505923d7d453aa281ee9dff6d47a1f3  366  .ufo/waves/round-46/attempt2/wave1/R46bExecCensusReceipts.draft/sources-census-before.txt
a074f9d1573aed88cb28b10f33761f99161247d873c6b5a6b53e7f12a40be6ae  22036  .ufo/waves/round-46/attempt2/wave1/R46bExecCensusReceipts.md
4d9c15a0169af44374e288191f067c6429152796152d2ac21fd1981122b26ddd  16499  .ufo/waves/round-46/attempt2/wave1/R46bExecControls.draft/freeze-controls.txt
d60771c44b5a3eede5afabd54a4112af4de2797b5ce5b7113a681a7217ad0365  103  .ufo/waves/round-46/attempt2/wave1/R46bExecControls.draft/run-controls.log
89c5777ebe7d82bb544ace5e6e02c63ee8d68e0440d07a2176a42365b997b3ed  15466  .ufo/waves/round-46/attempt2/wave1/R46bExecControls.draft/run-controls.sh
426b08d32ce3553999e1b848f34cae8df4aaef0574b77e7780102421b05df6fb  17939  .ufo/waves/round-46/attempt2/wave1/R46bExecControls.md
6c8550efc39f710599212bbffeaa90b6bc7dee76a40181a1f9cfa4e928b9e84d  2540  .ufo/waves/round-46/attempt2/wave1/R46bExecFixtureHarness.draft/control-donothing-counter-out.txt
98bbeb89bf9ac2210688c5c62006dc453c06376895e041fa23b190e4efeae294  6252  .ufo/waves/round-46/attempt2/wave1/R46bExecFixtureHarness.draft/control-mutated-receipt-out.txt
a61d0f09db37b882df5edb048ab6626ca3a87dbafc429d075f9ae3b825be4d27  32836  .ufo/waves/round-46/attempt2/wave1/R46bExecFixtureHarness.draft/f29-fixtures.py
03ab6b8f44e07315c27a68bfce6aa5dadae4c83b35c6e480560590bf938a5a4e  6252  .ufo/waves/round-46/attempt2/wave1/R46bExecFixtureHarness.draft/selftest-out-freeze-export.txt
09c59cb08289333ce63c3fdd2a01599f5da43fb2bd292f52a4a44b0512b111fc  6252  .ufo/waves/round-46/attempt2/wave1/R46bExecFixtureHarness.draft/selftest-out-strict-receipt.txt
03ab6b8f44e07315c27a68bfce6aa5dadae4c83b35c6e480560590bf938a5a4e  6252  .ufo/waves/round-46/attempt2/wave1/R46bExecFixtureHarness.draft/selftest-out.txt
1f84c6557fab96acaaae0e0256150dc8b0a23e358826aebdd71733b30e9484d9  15083  .ufo/waves/round-46/attempt2/wave1/R46bExecFixtureHarness.md
7d6d604d056136127bd2738199b544526d4d2bd32936708f79696cb239837dbb  21116  .ufo/waves/round-46/attempt2/wave1/R46bExecGatePinAmend.draft/r46-c2-gate.py
37a723c0952af8523f17e79e949e2e3670783dc126dc1f35047d653b9c73814a  51765  .ufo/waves/round-46/attempt2/wave1/R46bExecGatePinAmend.draft/r46-counters-selftest-c2.py
bf1682955b7f322bfe459db53d153bf780438324ee4d6ce93b6ab064403d13ba  538  .ufo/waves/round-46/attempt2/wave1/R46bExecGatePinAmend.draft/receipts/gate-v12-grown-ledger.txt
614416400de0c14e6ebffc48e1c8fb1dea00a71ed77095c95f8c26305609ced7  538  .ufo/waves/round-46/attempt2/wave1/R46bExecGatePinAmend.draft/receipts/gate-v12-live.txt
bf1682955b7f322bfe459db53d153bf780438324ee4d6ce93b6ab064403d13ba  538  .ufo/waves/round-46/attempt2/wave1/R46bExecGatePinAmend.draft/receipts/gate-v12-shrunk-ledger.txt
28334a0976e610c9bf2d02288f1d66836c3f6a17e153ae4494b0dff05d6c7039  479  .ufo/waves/round-46/attempt2/wave1/R46bExecGatePinAmend.draft/receipts/gate-v13-66-entries-29-rows.txt
8daddd854e29e74c7687b7cbcec19e520a5f4c75d0402189401e5263d51762ff  538  .ufo/waves/round-46/attempt2/wave1/R46bExecGatePinAmend.draft/receipts/gate-v13-66-entries.txt
614416400de0c14e6ebffc48e1c8fb1dea00a71ed77095c95f8c26305609ced7  538  .ufo/waves/round-46/attempt2/wave1/R46bExecGatePinAmend.draft/receipts/gate-v13-grown-ledger.txt
614416400de0c14e6ebffc48e1c8fb1dea00a71ed77095c95f8c26305609ced7  538  .ufo/waves/round-46/attempt2/wave1/R46bExecGatePinAmend.draft/receipts/gate-v13-live.txt
1b8ed305dcbf9dd7527ba440c7d6f0653fa9fb144d5ea65e28887f47290186ab  509  .ufo/waves/round-46/attempt2/wave1/R46bExecGatePinAmend.draft/receipts/gate-v13-shrunk-ledger.txt
b806696c513f238975b6030c4437b5101f4dc9fa9af42a95c6ef535111cf1e46  10774  .ufo/waves/round-46/attempt2/wave1/R46bExecGatePinAmend.draft/receipts/selftest-baseline-v12-counter-v12.txt
31c336ec9bc2f9b56cef9120cc82775619b306128dfc44f65c44e01b9bcf5288  16529  .ufo/waves/round-46/attempt2/wave1/R46bExecGatePinAmend.draft/receipts/selftest-donothing-control.txt
2da59c113996715374698c2c031f09862ff939101a363b1e7b328faff58cdb05  10766  .ufo/waves/round-46/attempt2/wave1/R46bExecGatePinAmend.draft/receipts/selftest-v12-counter-v13.txt
54f21c1f8d7d0f8e863b6b89e7c8944ec4b5434617ffcdbfad39976b57f8566e  10730  .ufo/waves/round-46/attempt2/wave1/R46bExecGatePinAmend.draft/receipts/selftest-v13.txt
96e48e19e69264e58fce3bf7a4ec4d996235a8e24c3f4d16c0329de0d354c9e1  17233  .ufo/waves/round-46/attempt2/wave1/R46bExecGatePinAmend.md
0133f616dc6572362d0218f38f7dd0766fa09483591bf5751ea59877a73001ae  10146  .ufo/waves/round-46/attempt2/wave1/R46bExecLedgerDraft.draft/ledger-append.md
ea18df46a3f15e97e15a21a5292df112b796ddef5c6ac378d5bd07b5f524a9c7  643  .ufo/waves/round-46/attempt2/wave1/R46bExecLedgerDraft.draft/receipts/c2-gate-append65.txt
ec3c7b4e1cebad0909637e3d193397e172963aa74e3fa679afa10cedd611b022  629  .ufo/waves/round-46/attempt2/wave1/R46bExecLedgerDraft.draft/receipts/c2-gate-base65.txt
377931d58d4fca1c3f8fc76fb82f3155811ad3eb79dc197457025c2f8261dc77  595  .ufo/waves/round-46/attempt2/wave1/R46bExecLedgerDraft.draft/receipts/c2-gate-v13-append65.txt
8efc56276485b9a9fa7b19eb2389eeb0a07401e605ee46cfb8c84b0b656355ea  606  .ufo/waves/round-46/attempt2/wave1/R46bExecLedgerDraft.draft/receipts/c2-gate-v13-append66.txt
541792d036567e718b8db61b92ac761f90824f47dc5eac091c48c5ba00f76562  578  .ufo/waves/round-46/attempt2/wave1/R46bExecLedgerDraft.draft/receipts/c2-gate-v13-base65.txt
6ba566b8808958738b69d2841ab837bcf00ee2368f0822aca32e027fcefa05f6  589  .ufo/waves/round-46/attempt2/wave1/R46bExecLedgerDraft.draft/receipts/c2-gate-v13-base66.txt
7fd9dc72089dfed8890e4c079eb53a2f7d8f3276c3aa70e74ab4da21b6680cad  382  .ufo/waves/round-46/attempt2/wave1/R46bExecLedgerDraft.draft/receipts/census-append.txt
77cf5d1e6a374617653cd0e0247012de38a2dbc097b403fc877e3cc3019e1879  380  .ufo/waves/round-46/attempt2/wave1/R46bExecLedgerDraft.draft/receipts/census-base.txt
9e3bf6e1fc2502768aa0320c475740c8c9e57d97541aa7c94b50f26ef638e6b8  657  .ufo/waves/round-46/attempt2/wave1/R46bExecLedgerDraft.draft/receipts/f29-gate-append.txt
e47483147846eff88cd9f59f9193d03398df4172326470f072e9e77d87ad47e0  666  .ufo/waves/round-46/attempt2/wave1/R46bExecLedgerDraft.draft/receipts/f29-gate-base.txt
691362b98f349f29887fedd51b9b5aa7a7a4fc91786fd15a580d384928ca9a1c  628  .ufo/waves/round-46/attempt2/wave1/R46bExecLedgerDraft.draft/receipts/f29-gate-shrink.txt
21a5f46047e45a638a0f70edc62580a487f3c0060e53cdc8a8a2d723998808f3  522  .ufo/waves/round-46/attempt2/wave1/R46bExecLedgerDraft.draft/receipts/selftest-c2-append65.txt
02c996ff176b787503c2692b6fdaf6afd2b794db0c9e485a1505881bf0182baf  397  .ufo/waves/round-46/attempt2/wave1/R46bExecLedgerDraft.draft/receipts/selftest-c2-base65.txt
48522ea858fa0b9185ea96275b00d6d22ce82a3aadc68384600c16661a880672  894  .ufo/waves/round-46/attempt2/wave1/R46bExecLedgerDraft.draft/receipts/selftests-instruments.txt
110dd727876666bc2db9fd55a589a16128087099196a52f116ac9a24f2c57c10  18995  .ufo/waves/round-46/attempt2/wave1/R46bExecLedgerDraft.md
c9e6c0705a386ec4ac5103a2b7863afdc6ce30d538a7163f1d9bb47d1c2e3366  26313  .ufo/waves/round-46/attempt2/wave1/R46bExecMutbatF29.draft/r46-mutbat.py
252acc7ba2c3d5b15fabedcf2d3a8536fcfc0c00473f9ebc2a7fd825889db4ab  1689  .ufo/waves/round-46/attempt2/wave1/R46bExecMutbatF29.draft/receipts/f29-run1.txt
252acc7ba2c3d5b15fabedcf2d3a8536fcfc0c00473f9ebc2a7fd825889db4ab  1689  .ufo/waves/round-46/attempt2/wave1/R46bExecMutbatF29.draft/receipts/f29-run2.txt
252acc7ba2c3d5b15fabedcf2d3a8536fcfc0c00473f9ebc2a7fd825889db4ab  1689  .ufo/waves/round-46/attempt2/wave1/R46bExecMutbatF29.draft/receipts/f29-run3-sepwork.txt
1bad562d8ea53599e18b0e2ad17ae29fa718e660e280361e58ff80d2d71158fd  2396  .ufo/waves/round-46/attempt2/wave1/R46bExecMutbatF29.draft/receipts/verify.py
e6aec2f0560557b9732f4f2067aa96650cc2b75f03109d0590bfdf0f6867f6a1  9729  .ufo/waves/round-46/attempt2/wave1/R46bExecMutbatF29.md
3f684a0a5bb6d45016af3962332162067bc1f305d29d310f1f29090b115a9a9f  56913  .ufo/waves/round-46/attempt2/wave1/R46bExecNoharm.draft/noharm-control-do-nothing.txt
8a1f4939a72d206978d8e8ac278eaab41f099984ab8656cc33655ec3d780c1c8  56990  .ufo/waves/round-46/attempt2/wave1/R46bExecNoharm.draft/noharm-live.txt
89ac2028e20dde53378f046161b8950d3c39d136ab29017fb4e26af54fb21fe5  2294  .ufo/waves/round-46/attempt2/wave1/R46bExecNoharm.draft/noharm-replay-attempt1-base-inputs.txt
675b566498a490ded244a19bb2721a5e23bd664ac4366d1a3c3916cb7ce5d776  6632  .ufo/waves/round-46/attempt2/wave1/R46bExecNoharm.draft/noharm.sh
7140cef9dd2e1b782bcbcc7863496fc2a4dc632dee5df5010767d218160098b7  17185  .ufo/waves/round-46/attempt2/wave1/R46bExecNoharm.md
54f21c1f8d7d0f8e863b6b89e7c8944ec4b5434617ffcdbfad39976b57f8566e  10730  .ufo/waves/round-46/attempt2/wave1/R46bExecPlain.draft/logs/base-lane-c2-selftest-G7a-mutant.txt
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bExecPlain.draft/logs/base-run.err
abc42cac8c798c7d34b6203abf797edf09a604a1724024dd0e7943cbf996891a  697  .ufo/waves/round-46/attempt2/wave1/R46bExecPlain.draft/logs/base-run.txt
94939ef57502d88903ab05aa7991a6d73a3e8519b1a970c4bb9ac129be181895  351  .ufo/waves/round-46/attempt2/wave1/R46bExecPlain.draft/logs/base/LASTLINE.txt
93b8ff10828fe78dabd685a86e3b3ac4f0d1ff75145f6393e8915bda1a202dc0  1692  .ufo/waves/round-46/attempt2/wave1/R46bExecPlain.draft/logs/base/bat-c1.log
f0460f56a6a31116a81ea94c472f6e25e3ac124f349356c028b380c347abeca6  83  .ufo/waves/round-46/attempt2/wave1/R46bExecPlain.draft/logs/base/bat-c1.out
571e247f092b2a51a6acb47a0d835d67f3fd0715a5bc4205086045a056b6875f  1722  .ufo/waves/round-46/attempt2/wave1/R46bExecPlain.draft/logs/base/bat-c2.log
abc0c46cd543cf6fef190cc2f4260121ea8d8822cd972a59f2bc8a095c1a1f6c  83  .ufo/waves/round-46/attempt2/wave1/R46bExecPlain.draft/logs/base/bat-c2.out
e462cf2fd90ed1d337c94916e8b24de0633e61fa621a3d3e5d095c1a44df1a65  85229  .ufo/waves/round-46/attempt2/wave1/R46bExecPlain.draft/logs/junk-c2-selftest-v.txt
ad3e908c9369bcd903473ebd72eb31dfd597bfdbeba17fc1828484f243e2cf64  1712  .ufo/waves/round-46/attempt2/wave1/R46bExecPlain.draft/logs/junk-mutbat-c2.txt
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bExecPlain.draft/logs/junk-run.err
e702b235c50ff6bbfde16738854357e10adbf11858eeabfb37158cb669918255  493  .ufo/waves/round-46/attempt2/wave1/R46bExecPlain.draft/logs/junk-run.txt
f084108719b941bb89f457333bba9ec7fd50182894a4e4a8b69696cff3030a7a  147  .ufo/waves/round-46/attempt2/wave1/R46bExecPlain.draft/logs/junk/LASTLINE.txt
52117363a97243fd2b6f02bfeeabff088424495e0b230a5f7c8fcb644baf2bd7  610  .ufo/waves/round-46/attempt2/wave1/R46bExecPlain.draft/logs/live-instrument-sha-after.txt
4b1e0fe6feca6bd60c2ab7e72b662222f9aa0a583282a1f5d7aa4d3a1e6124b9  610  .ufo/waves/round-46/attempt2/wave1/R46bExecPlain.draft/logs/live-instrument-sha-before.txt
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bExecPlain.draft/logs/live-run.err
ddbeabc7aaf028e9f62f7a5b910b8073f59f6cb369fb61dde51bf51b31c4e562  697  .ufo/waves/round-46/attempt2/wave1/R46bExecPlain.draft/logs/live-run.txt
437be666fffaad0861a7f8d0b559a76d72e0181edd9b06ede5e5a033b0022fd4  351  .ufo/waves/round-46/attempt2/wave1/R46bExecPlain.draft/logs/live/LASTLINE.txt
f2f586d149a25cf0cd07585bf8dc7d17b0be733f4a12f82d17614d74de31cbf9  1684  .ufo/waves/round-46/attempt2/wave1/R46bExecPlain.draft/logs/live/bat-c1.log
efae922d6a05c53b373b59ef407a4fa79d8f7f28ed53a9f14f45ad5e6de6533d  83  .ufo/waves/round-46/attempt2/wave1/R46bExecPlain.draft/logs/live/bat-c1.out
571e247f092b2a51a6acb47a0d835d67f3fd0715a5bc4205086045a056b6875f  1722  .ufo/waves/round-46/attempt2/wave1/R46bExecPlain.draft/logs/live/bat-c2.log
abc0c46cd543cf6fef190cc2f4260121ea8d8822cd972a59f2bc8a095c1a1f6c  83  .ufo/waves/round-46/attempt2/wave1/R46bExecPlain.draft/logs/live/bat-c2.out
3d169bbabef302d99aaac64f0f6eb1ef28f8175a2d38215b1abc938411f0c1a8  8990  .ufo/waves/round-46/attempt2/wave1/R46bExecPlain.draft/plain-measure2.sh
16f4eaa7a65d6d12aada45cc211e59c79823761de490f89afd74af75e9df0efd  21496  .ufo/waves/round-46/attempt2/wave1/R46bExecPlain.md
03079421b07639baabfc942ef4a022c9a8798ff8bc81f029d4b73c6a8b54e2fd  46486  .ufo/waves/round-46/attempt2/wave1/R46bExecSelftestC1.draft/r46-counters-selftest-c1.py
e0915bf564d442ec157ddbcfeecbede6bd6f053396317540a88d5968276d9289  9714  .ufo/waves/round-46/attempt2/wave1/R46bExecSelftestC1.draft/receipts/01-before-committed-selftest.txt
f04c77036a13a90f6b331b7f14b3b8316c4b241792247d1d840c1546c676d527  10588  .ufo/waves/round-46/attempt2/wave1/R46bExecSelftestC1.draft/receipts/02-after-extended-selftest.txt
ad3ace02e97a5d37dc95b5d88a6f108f179ba7ace385ff36151620137144d7f6  11575  .ufo/waves/round-46/attempt2/wave1/R46bExecSelftestC1.draft/receipts/03-mutant-M06-L3-home-dropped.txt
51b7fd715ec047b7f3bd6dfea355cc180ad751ea605f9a76d7a77a0b41086300  11040  .ufo/waves/round-46/attempt2/wave1/R46bExecSelftestC1.draft/receipts/03-mutant-M07-L3-home-no-abs.txt
8b4b79b46509b91e941b65a06290adbaf6e2b505feeb27f90b67c8786ebba03a  11971  .ufo/waves/round-46/attempt2/wave1/R46bExecSelftestC1.draft/receipts/03-mutant-M13-L6-control-dropped.txt
50b26e49ba28ac5d78868f552f42dad4070dd4969b5accfb28354df95cbcae85  11202  .ufo/waves/round-46/attempt2/wave1/R46bExecSelftestC1.draft/receipts/03-mutant-M18-anchor-dirs-wide.txt
c942c2c8059dc422fd4e419d948d0c698a2c1f5fc7075630d14962008c78c017  11103  .ufo/waves/round-46/attempt2/wave1/R46bExecSelftestC1.draft/receipts/03-mutant-M19-L2-eq-relaxed.txt
bae94e8427a758d2fdf6914800aba41025f977a5eef31aa0451420f5cfad9f01  11113  .ufo/waves/round-46/attempt2/wave1/R46bExecSelftestC1.draft/receipts/03-mutant-M20-syntax-ignored.txt
5706f5cef868fd1cf9b8faf21ea978dcc474d34fef96172937c1ca29b209a5f4  682  .ufo/waves/round-46/attempt2/wave1/R46bExecSelftestC1.draft/receipts/04-m14-equivalence.txt
98e95b37130f73369c79481cbd50a5e1a5a7b0ed47e25573f91d7d561f673dd9  3292  .ufo/waves/round-46/attempt2/wave1/R46bExecSelftestC1.draft/receipts/m14-equivalence-differential.py
33d81843c281d24eb5a89323bd6d802a60d9702bc5cb499b13e1c02852614a65  1722  .ufo/waves/round-46/attempt2/wave1/R46bExecSelftestC1.draft/receipts/make_mutant.py
a1e9d65050065e5b04fd66e94e127c010b719bbac2e179608b3ffb3c565c80d5  16264  .ufo/waves/round-46/attempt2/wave1/R46bExecSelftestC1.md
8039d6cf81bbe3f35aa15e51adf0cb76582a41efb493e5f92959caf7ebb0b1a6  3560  .ufo/waves/round-46/attempt2/wave1/R46bExecSelftestC2.draft/equivalence-probe.txt
b7a4df2fe46ffd54a0f67be77a84b83d716c776ecf195013dc5d0785870e10a7  1482  .ufo/waves/round-46/attempt2/wave1/R46bExecSelftestC2.draft/per-mutant-verification.txt
0457a1926d766d73297aa07b2997a4fd79037bed5201501e1310de3cd869c281  63172  .ufo/waves/round-46/attempt2/wave1/R46bExecSelftestC2.draft/r46-counters-selftest-c2.py
c99de21556b1d785b0af910f8e07fc7e48fa910f91c2fd4e3bdb38730ff95396  11519  .ufo/waves/round-46/attempt2/wave1/R46bExecSelftestC2.draft/selftest-baseline-147.txt
32b9fd569b0392421bd20e408f305321bb6fac8086e6c76afd8ed4bf4fa7467a  10493  .ufo/waves/round-46/attempt2/wave1/R46bExecSelftestC2.md
fbc4a11a5aca16b061a5ba0dcc8ec73f9452b1feea82361d4dd116a4449a2894  4195  .ufo/waves/round-46/attempt2/wave1/R46bExecSelftestF29.draft/r46-selftest-f29-mutprobe.py
ed7bb74bd9126009473d3db7bc714d66b7b1fc73941d8bf2e1be04702978fd24  7859  .ufo/waves/round-46/attempt2/wave1/R46bExecSelftestF29.draft/r46-selftest-f29-mutprobe.txt
23b528a40e1d982820d360aea3cd12166a8b6ac07226e7567fd5abaa16f4435d  46547  .ufo/waves/round-46/attempt2/wave1/R46bExecSelftestF29.draft/r46-selftest-f29.py
a4f5afa94d781d3907613aec7a0af61174896c8c0b0aa16702053df3772d4f63  18437  .ufo/waves/round-46/attempt2/wave1/R46bExecSelftestF29.md
b6367a053c2060a71d522eab82922be05829a4fb570487c63a066d06dae80474  11089  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/contract_check.py
2146d160607c4fda4c187e36d8254e07cfe22aa224e53c396811c0cbfcda84ea  14589  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/mutate_battery.py
ca026bcd18de32497543f972a20810e9fd62eb14839ef10d3ae03189e5ad6917  3374  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B01-S1.txt
56e22f5b10d0f75e7a9d00d95d6ad521a0e77efbe1399de45bb442938246d3fe  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B01-S1.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B01-S1.txt.err
ca026bcd18de32497543f972a20810e9fd62eb14839ef10d3ae03189e5ad6917  3374  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B01-S2.txt
b5cb64feb53efb34ed873ec592775405071b2b07964a1c4bb88718ca6d9db0c3  358  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B01-S2.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B01-S2.txt.err
d4e1f4be7ec92a1e008650e82360002088f7eda69a39e1e180da7bc223f331d4  1206  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B01-S3.txt
d902da9dd18c6a990e55f58d381a29b55f82fb40f803bcabf43f88789a72627d  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B01-S3.txt.cmd
0785bfec35ace1c98256d69fd859f0133327ff5a22f2d5c4decbfb3ec7b65a53  93  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B01-S3.txt.err
aefe79e92847b040d8829362bdf485b991c7998f3f15379c9688d45f1304bdf6  1751  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B01-S4.txt
3fe92f1593cf1de11309927887cdbdf10272a083fbdb4342be2ba89ceb310345  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B01-S4.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B01-S4.txt.err
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B01-S5.txt
4c42da32db2580801831e498e987b4e2ade4e04d8309d1ca38afb702d1219d85  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B01-S5.txt.cmd
30a2f9afcf67fda7a4780d732cf6d5894a078f13ec97eadccd9a27ae8366b8f0  1396  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B01-S5.txt.err
ab1faf5914e9394fe12f7b6ce0372705f0bf700b4c3b0655e65f2d4d197c85ce  3375  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B01-S6.txt
b66c6b4ca95286f8166fe64d76a9a80590edbacfc74dbd98be6348e35d42cc10  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B01-S6.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B01-S6.txt.err
510e31f3f293574c946366282e1f5251a531bff7b6add4dee5c60f898f1db97a  3414  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B02-S1.txt
6896bc6595e81326550166d52f00e5ed1df3e7fb741ec90bf3cfd65af1bdb83c  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B02-S1.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B02-S1.txt.err
13907fc6f354e7065719ae5726604e8f9e3c04cf907cedbb2e71e2bbf3a3b9c2  3416  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B02-S2.txt
beab669a496ffa3d7e5fc2ca8cbcc8dd4028104f89556041fd4e982a775cba3e  358  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B02-S2.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B02-S2.txt.err
0eda66951bffacf461707e5d192e84ef35895f42a41effd4e70a214e5c2895c3  1214  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B02-S3.txt
ef57bff2f19aa4565237ad540b475dadf8f026f09a507e322b4073c49b78412c  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B02-S3.txt.cmd
0785bfec35ace1c98256d69fd859f0133327ff5a22f2d5c4decbfb3ec7b65a53  93  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B02-S3.txt.err
a8ae4e0b335033d6d97600a8d7c078e3e5ed6635765325c773b0e2b4d7f70121  1777  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B02-S4.txt
27d9379be5acabfca56e68ad06596faefd8fa1d14c7d809ea65bf99764dfb50b  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B02-S4.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B02-S4.txt.err
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B02-S5.txt
6772c504f6bb23c4279b65ac908df884223321262729710623c69409a4516efd  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B02-S5.txt.cmd
2911e01c217a8653869c0b7f9319202c9852a31020cd5f33c45ba09be41aba2c  1396  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B02-S5.txt.err
584db0753889d145684d51a01bff47621875aed9807b9a490b3160d5aa0669a1  3439  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B02-S6.txt
ebe90af8f7cd246823bd145125602eba0b1beab55b7fe7c333043166167e1f9b  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B02-S6.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B02-S6.txt.err
82cbecb0d94025006969584159c08af23244d7ff886fa03f43499201013ad8b0  3414  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B03-S1.txt
a6c0af84af0a8d527b8ce8e4a5c3cfac61ea3ddc2d7246fea61954907f01611c  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B03-S1.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B03-S1.txt.err
eb4d5a69c14e89213398354a2d523adb032ca8626a877884d202e9db63019c38  3412  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B03-S2.txt
2a9cf2f0c67eea9422254b2c5b9f99f1db8078bb3fd6e30f470bffb79c76d5ec  358  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B03-S2.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B03-S2.txt.err
0eda66951bffacf461707e5d192e84ef35895f42a41effd4e70a214e5c2895c3  1214  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B03-S3.txt
ef8d670d5122411b897a4c376e490d3b5c18fb42ac247b4f54d6983b420db257  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B03-S3.txt.cmd
0785bfec35ace1c98256d69fd859f0133327ff5a22f2d5c4decbfb3ec7b65a53  93  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B03-S3.txt.err
e1326f1d1e067dbec212891e8765c5d36ca158f7db6e243a1736acb48812544c  1777  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B03-S4.txt
eb14588b5add801d6cca5c2df49c2b7d30622104fdb217be631cc425a5dfd3c5  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B03-S4.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B03-S4.txt.err
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B03-S5.txt
4caf4def0815816fb8350614583c502246cf542ebb76e2ba7cd76924282faa5f  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B03-S5.txt.cmd
379f2750447eddad4db75b5d1f6efaf04efefca3e98fffccad76acd61036cab4  1396  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B03-S5.txt.err
8032226a7fbcea7a007cef6d47371f1a95f9a1d63aa72624b1e1603a280efc31  3439  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B03-S6.txt
5604222527803fa234d94192ba0eaac5072e4b55754a47ec8813d022d3b51706  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B03-S6.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B03-S6.txt.err
82cbecb0d94025006969584159c08af23244d7ff886fa03f43499201013ad8b0  3414  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B04-S1.txt
ff310a2458ba8b2c4b5bcf69c70bbfb54f51f88f35c42476d478da22a57b99b8  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B04-S1.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B04-S1.txt.err
06978a5583767fe56d39937e94b9277197527fbb6cbd627bad66ab944c84a647  3418  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B04-S2.txt
062cbd918f6421e30341bdd49c275858c298444c795087cb648623c730f67bf5  358  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B04-S2.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B04-S2.txt.err
0eda66951bffacf461707e5d192e84ef35895f42a41effd4e70a214e5c2895c3  1214  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B04-S3.txt
61018f5d1649ab6a40890358da23685e244711b4d925a03d9276dd085c2bb5fb  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B04-S3.txt.cmd
0785bfec35ace1c98256d69fd859f0133327ff5a22f2d5c4decbfb3ec7b65a53  93  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B04-S3.txt.err
e1326f1d1e067dbec212891e8765c5d36ca158f7db6e243a1736acb48812544c  1777  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B04-S4.txt
222cff27429dd2da0a973b001adba03bfbee2ee357f9fc99b21b716c132d1723  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B04-S4.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B04-S4.txt.err
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B04-S5.txt
1360283ba2728b613dff5ff904165e92a9779b77460c7d43903bb68303f678f6  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B04-S5.txt.cmd
c770abf2c11e1a442d729963e00f3e26eb06374102e224ac571739a6fcc2b82a  1396  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B04-S5.txt.err
8032226a7fbcea7a007cef6d47371f1a95f9a1d63aa72624b1e1603a280efc31  3439  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B04-S6.txt
342996d5ed3c0fae877da6a4d43dcc9cd8db0b297be38833a5eaf8ad381b2065  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B04-S6.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B04-S6.txt.err
82cbecb0d94025006969584159c08af23244d7ff886fa03f43499201013ad8b0  3414  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B05-S1.txt
98d813cf4c2d826fa55f1f1c026338992959c9628d4bb608da66bf7b2e0b7287  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B05-S1.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B05-S1.txt.err
4d665e296c1d9d3fae289646e3d7971281cd5b4833d8ba6ebcacd61b2c2f6e36  3416  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B05-S2.txt
d9488d3e2caaa50e706b4afd67e0e8ce1abd81ace994dabb358e3dfe8010e0b9  358  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B05-S2.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B05-S2.txt.err
0eda66951bffacf461707e5d192e84ef35895f42a41effd4e70a214e5c2895c3  1214  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B05-S3.txt
5a1b509636c5a5ec5ada4dcb72a416ee435f128cd5a00e31dbf6c259fd34355e  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B05-S3.txt.cmd
0785bfec35ace1c98256d69fd859f0133327ff5a22f2d5c4decbfb3ec7b65a53  93  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B05-S3.txt.err
e1326f1d1e067dbec212891e8765c5d36ca158f7db6e243a1736acb48812544c  1777  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B05-S4.txt
d635df42e145c602b8ad06adbdb4087851af77b3af834e7b2047d9a8253063a8  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B05-S4.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B05-S4.txt.err
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B05-S5.txt
91c44987fc3a82222ad17d9ccd2c58b59095a292b99fc983f07fa89c0d3347d9  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B05-S5.txt.cmd
dd099270f0f9d5c6a70ca2689209acc29fed15e116b9cb56acc10a9f3594a0ea  1396  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B05-S5.txt.err
8032226a7fbcea7a007cef6d47371f1a95f9a1d63aa72624b1e1603a280efc31  3439  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B05-S6.txt
bbe367016d176a247b14f520177917b5dda0cdc2c33c3c862c2763bc2063ccfd  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B05-S6.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B05-S6.txt.err
0c15ce114b8f1f7214c511fa0ffb8b51e8dc78f79ff424dc0d37c4081d2dc0ea  3254  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B06-S1.txt
ca993e0810900a51805503d5675886e0e0061f7f9ae0fafbc58f2090e87a494d  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B06-S1.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B06-S1.txt.err
059755cb429d80d4d151b043e10bae1a365d401d4c8638a3b069a14ffccceed6  3256  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B06-S2.txt
d4c44494e47511cce0047cf401970e449c31d1879f133bf2b99fd5315fceeda8  358  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B06-S2.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B06-S2.txt.err
0eda66951bffacf461707e5d192e84ef35895f42a41effd4e70a214e5c2895c3  1214  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B06-S3.txt
6640a7d9af4211aa546fcf165231ac95500debad7fc19e2f667a94bbeb6d9ee7  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B06-S3.txt.cmd
0785bfec35ace1c98256d69fd859f0133327ff5a22f2d5c4decbfb3ec7b65a53  93  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B06-S3.txt.err
f3cb15cd4f8275627d4310d7648622eca7213ece2c80ae72c38860b5a4a1923b  1698  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B06-S4.txt
88dc1adc68e13af6a1a8f9eeb836f6961e243f2e2bd6ac4755aab261b036cf40  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B06-S4.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B06-S4.txt.err
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B06-S5.txt
05d9b3a44402b2569776dd4395ea0f7192477678eb82bc64fdf50962b635abc7  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B06-S5.txt.cmd
23eea258f0fc4b29e4b2eecf76921339d350aceff7843e72d40b0e34fb455c4f  1396  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B06-S5.txt.err
1029839be6c08d410bd53caa017794ef3dd445fceb67127885ab4ea40a85cb0c  3279  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B06-S6.txt
1d0f8be420420943595a17dd3f588500739bb7c2f68e52513da8f7b2866b3546  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B06-S6.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B06-S6.txt.err
82cbecb0d94025006969584159c08af23244d7ff886fa03f43499201013ad8b0  3414  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B07-S1.txt
754d85061401038b7b7856cecd094cc7988d9c783ef04a484c76ac2ab353214c  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B07-S1.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B07-S1.txt.err
4d665e296c1d9d3fae289646e3d7971281cd5b4833d8ba6ebcacd61b2c2f6e36  3416  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B07-S2.txt
89e38ee0f2f40ace3719163e030df00286198495068ebf8fbdd229b3568c39eb  358  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B07-S2.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B07-S2.txt.err
e3fe7f005c41e7f5ee090f50f8c8883babb578eb438c163a22678b0c843d8ef2  3416  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B07-S3.txt
1e35a46de2bcbdf0bb4ce710396d69ae93e2ba42e54256052c9cf9366178025d  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B07-S3.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B07-S3.txt.err
e1326f1d1e067dbec212891e8765c5d36ca158f7db6e243a1736acb48812544c  1777  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B07-S4.txt
cb86d3908744a110ecbea447fc5cda67cd336459e8a10ff532c4b8133a3ec7a2  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B07-S4.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B07-S4.txt.err
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B07-S5.txt
d31b6ee2017ca8c9a6b1bf9322646197dfaaaf5c65f5007ec67e8dd4dcb488c9  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B07-S5.txt.cmd
34db17d0bc96f380bbb6d96b97a2452e131f4a36dd70de3413401c54fee3af9d  1396  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B07-S5.txt.err
8032226a7fbcea7a007cef6d47371f1a95f9a1d63aa72624b1e1603a280efc31  3439  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B07-S6.txt
9f5d834d2f077b79d352d7a04269a5e66561d96532465532c0b1995a11dd723f  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B07-S6.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B07-S6.txt.err
82cbecb0d94025006969584159c08af23244d7ff886fa03f43499201013ad8b0  3414  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B08-S1.txt
7894b66d869c4105625de2737dbad2f568b101cf19d4796dda31a77fa1098130  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B08-S1.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B08-S1.txt.err
4d665e296c1d9d3fae289646e3d7971281cd5b4833d8ba6ebcacd61b2c2f6e36  3416  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B08-S2.txt
d84b19379eaf0b1b9d99e3522b05ac8c10fe4ac7f6f8c26cc608418e8b7b1b1f  358  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B08-S2.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B08-S2.txt.err
0eda66951bffacf461707e5d192e84ef35895f42a41effd4e70a214e5c2895c3  1214  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B08-S3.txt
d7be82c3bd11ed748318b7e5458bd4de2c78413cdfcad96695b6b762eaac3867  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B08-S3.txt.cmd
0785bfec35ace1c98256d69fd859f0133327ff5a22f2d5c4decbfb3ec7b65a53  93  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B08-S3.txt.err
25ebd093f7ff85838a850d40d36c6b45ce7025f70f248d08566deb0691cd0429  3458  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B08-S4.txt
e07fbf0b1ae6267e21db5785b2e42b389b66134306c12ea646eb0f3272247b05  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B08-S4.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B08-S4.txt.err
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B08-S5.txt
100f9f571cc23f03a45745ae19159f0248bc09706a9ac31f622da5e8a0dc986a  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B08-S5.txt.cmd
91e29fc99853b6c83e57a1bb961702402ba8697795b3febf785dfa80cfdf0aa7  1396  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B08-S5.txt.err
8032226a7fbcea7a007cef6d47371f1a95f9a1d63aa72624b1e1603a280efc31  3439  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B08-S6.txt
3b4f66ea698e2dd4227267e0148dd10988ae68ba1d58e8df52d1e39e0ec6151c  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B08-S6.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B08-S6.txt.err
ca04f1d0782e1c34d96f5cf7565b5dc699b973118c086ad8a5470309e3481d10  3413  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B09-S1.txt
c14dbe90d09326a83e7994fe0c6d63df3d1d0f4eb5c1adf23cbea7734a29db40  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B09-S1.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B09-S1.txt.err
548b4996d7245b516b167de66f7a679a3e0d620cda25350e1e651b20f502113d  3415  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B09-S2.txt
6679d1a6214c9d2d6e463462c6d266a98504136d4dc29f73b3dea1d6140f5547  358  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B09-S2.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B09-S2.txt.err
0eda66951bffacf461707e5d192e84ef35895f42a41effd4e70a214e5c2895c3  1214  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B09-S3.txt
9d49f6b2e7df3ab16f50e9c5a2d5d6038f93dfb3e7f15b646d3f11c71775098b  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B09-S3.txt.cmd
0785bfec35ace1c98256d69fd859f0133327ff5a22f2d5c4decbfb3ec7b65a53  93  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B09-S3.txt.err
75ab8ed725aac0b0c52f6663b2619b5825ce16f6f3cd6bf92d84f54215be30cf  1776  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B09-S4.txt
143209b6daec878b2ba7d9fe45279722de5ce0b9efeaaa5a3fc5981b7d25718d  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B09-S4.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B09-S4.txt.err
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B09-S5.txt
6cdac59095cd5891b20025d37768d4951d79fe38d5bac40d36e34eff9ce2b8b4  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B09-S5.txt.cmd
5f223fb6bea2cedf2abb9ce04302eedb3b248eaad8ce068a01ab7b0f7491ec9d  1396  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B09-S5.txt.err
2b37141f4336e3272739b34580e7724cd328cf515b49c4ed542db4427df8888a  3437  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B09-S6.txt
b9de1fa6a61792f2e604892595f94fef69e1c0f38fedaddb056c5c146b716c0c  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B09-S6.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B09-S6.txt.err
a81179ef700b98beffba7a4b02c7508c9ccba76dd87bae57f7373dbf71a1a2d0  3374  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B10-S1.txt
39dd0dbc731656ca67268b41b04af30d66c0e65cf8895f46aba10934ee752861  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B10-S1.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B10-S1.txt.err
bb6bf2c0fabbcd06c2a60bdc7a5cf78dd132f13ce08fe3389417ef85b2f32bf9  3378  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B10-S2.txt
16b490701774e7cd18eb55f9042066a2d64be3dbdfd69f1313702faeae2d22d0  358  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B10-S2.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B10-S2.txt.err
d4e1f4be7ec92a1e008650e82360002088f7eda69a39e1e180da7bc223f331d4  1206  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B10-S3.txt
eb384ff0253386681ea1bdc19ded2a9957daf4830aa008b57210a51b9d5ef032  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B10-S3.txt.cmd
0785bfec35ace1c98256d69fd859f0133327ff5a22f2d5c4decbfb3ec7b65a53  93  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B10-S3.txt.err
290ca7fab6b4681c0d72884b342a41ecfd9c5e65326202d220e3cef1af5286b5  1751  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B10-S4.txt
e361f6a8e5acb7d1e40c0661991ed591a45ef651e0bff053595d0be4255c7fa2  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B10-S4.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B10-S4.txt.err
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B10-S5.txt
534243885a682f2617e97d75ea838284091c17a6c5216fa39b3f1a48c05a1291  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B10-S5.txt.cmd
16befdae4817f2ff0cee0dd483a650a96f0d4582758b891f3a9bb7fa4c09e25b  1396  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B10-S5.txt.err
9fa0d992c7adc151ec814ac891b5ae0bb67711a66239a111bea043c3d5031bef  3373  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B10-S6.txt
db37efac6b72c221a2cc57ec51c79ecd4c7736f2d7cb517178658f2e42b164c8  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B10-S6.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B10-S6.txt.err
82cbecb0d94025006969584159c08af23244d7ff886fa03f43499201013ad8b0  3414  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B11-S1.txt
9b4849765edfd7f50d47a3f45984f74e3b4de5377c9426ec9aed8e7cbf46539e  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B11-S1.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B11-S1.txt.err
4d665e296c1d9d3fae289646e3d7971281cd5b4833d8ba6ebcacd61b2c2f6e36  3416  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B11-S2.txt
6761bac20337b5475b70d3282fd4fa680710da8a6681de44e309e52edaa071a6  358  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B11-S2.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B11-S2.txt.err
0eda66951bffacf461707e5d192e84ef35895f42a41effd4e70a214e5c2895c3  1214  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B11-S3.txt
5494ce1422cf16705fdb92ecaa1035994fa363c5221701ce73ecf3353a6a3733  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B11-S3.txt.cmd
0785bfec35ace1c98256d69fd859f0133327ff5a22f2d5c4decbfb3ec7b65a53  93  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B11-S3.txt.err
e1326f1d1e067dbec212891e8765c5d36ca158f7db6e243a1736acb48812544c  1777  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B11-S4.txt
5b81f16efe0ce764e07c1d9a1449d0b838cfbb9f0c2503bf4f83168cb4600fa8  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B11-S4.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B11-S4.txt.err
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B11-S5.txt
dd3babac9ad8a5fac01a84ce3aab24356f1ba1fa87c0c0e504f6c9e9e30cd155  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B11-S5.txt.cmd
390b18f7db7ac878858a02b2dedf8fe8b9af72d4bd549cdb0daea9872864db4f  1396  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B11-S5.txt.err
8032226a7fbcea7a007cef6d47371f1a95f9a1d63aa72624b1e1603a280efc31  3439  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B11-S6.txt
91fe7338a35b3f79f08c718a0fe4c940c8cb81ebf3dd0ef49877fcf4629351f9  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B11-S6.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B11-S6.txt.err
c6702724b7ea23371c5efd642ec9428963b47d4476e4e229a42aea2987371a37  3414  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B12-S1.txt
4024f9aa2e4cc2664ceaa6ecaa947fcb63ae0db3944c257877876335554c3a83  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B12-S1.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B12-S1.txt.err
09a3f24df0d9dc1ab23dbb5527a6d44451dfbb0cc52903807be5cbfd9343d4d2  3416  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B12-S2.txt
3a06e5d3a35d9e726d6e2f26c58ada95fce5bc7cf7087413a089ce801f4e3aac  358  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B12-S2.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B12-S2.txt.err
0eda66951bffacf461707e5d192e84ef35895f42a41effd4e70a214e5c2895c3  1214  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B12-S3.txt
577aa713a4010250147428140834550afea1b2cdf619898e0bb396085b98ae29  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B12-S3.txt.cmd
0785bfec35ace1c98256d69fd859f0133327ff5a22f2d5c4decbfb3ec7b65a53  93  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B12-S3.txt.err
557530c14ecc0a62bcd17a289359f0ec2e5f9b052ac34aaa94ce303207690d45  1777  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B12-S4.txt
7c44440e4b62d120ce796da7ee6a921e7a806ebd33238d9d096815e61c3626ea  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B12-S4.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B12-S4.txt.err
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B12-S5.txt
53991bff882a8d77ecdf68276d4bbdfbc3a65536d46ea134cd8a8e94e332fdb5  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B12-S5.txt.cmd
f1e28c1d9b693f7bff39fddc33266278b3f07d8536bbaa44cfe0e980cc69a636  1396  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B12-S5.txt.err
97227383bf9597e63d2cab7de2942b231f28d2f9f53f5c534898c25acc3ce920  3439  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B12-S6.txt
a6c8d41dbdc2498c55716403966b6ced53a102747524245c7f10e06bc08fa652  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B12-S6.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B12-S6.txt.err
82cbecb0d94025006969584159c08af23244d7ff886fa03f43499201013ad8b0  3414  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B13-S1.txt
b9c6e4894001b414e569a7526df20ff9d8437afa9ba18e6b6cdb46f13fecf7d4  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B13-S1.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B13-S1.txt.err
4d665e296c1d9d3fae289646e3d7971281cd5b4833d8ba6ebcacd61b2c2f6e36  3416  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B13-S2.txt
37be251010a1b147057d3003e97ea45c13dad97c21673f8f1ee85dbbd42adec2  358  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B13-S2.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B13-S2.txt.err
0eda66951bffacf461707e5d192e84ef35895f42a41effd4e70a214e5c2895c3  1214  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B13-S3.txt
f13da12a7f47d4153b56b7c5579e2d5446f2fba5a2b2a6911828b82a449fc965  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B13-S3.txt.cmd
0785bfec35ace1c98256d69fd859f0133327ff5a22f2d5c4decbfb3ec7b65a53  93  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B13-S3.txt.err
e1326f1d1e067dbec212891e8765c5d36ca158f7db6e243a1736acb48812544c  1777  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B13-S4.txt
49f8d995afc94e1dab4bdf8ae2452c265fc3691d049ac413f552d68c569a7392  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B13-S4.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B13-S4.txt.err
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B13-S5.txt
4e247584336f751ff28ccd6fb8cf359ff88bbbdd235531a068bd948589140e2c  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B13-S5.txt.cmd
6695c8311ad053cd442ccd6a3aa5f8fb7b58c258f46d50b8cc36ee06a9d5840e  1396  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B13-S5.txt.err
f76aeccb957ca16b49bbfd58ffde1a11206984cfd1ca3cfd52c8050ac453241b  3356  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B13-S6.txt
72d0fb2160444b838ddef8c69809e92983297aad19f82192e218aded8edc12ef  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B13-S6.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/B13-S6.txt.err
82cbecb0d94025006969584159c08af23244d7ff886fa03f43499201013ad8b0  3414  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/CONTROL-S1.txt
38e488363d2ddd14d03820bfa0d97cf9285f3277d36f18ce44b1da794412e1a3  311  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/CONTROL-S1.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/CONTROL-S1.txt.err
4d665e296c1d9d3fae289646e3d7971281cd5b4833d8ba6ebcacd61b2c2f6e36  3416  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/CONTROL-S2.txt
bf0913a937c0a4bbcae8d3893f50a7cbd7a7e3178e7c7d3a72b8319432610662  381  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/CONTROL-S2.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/CONTROL-S2.txt.err
0eda66951bffacf461707e5d192e84ef35895f42a41effd4e70a214e5c2895c3  1214  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/CONTROL-S3.txt
92b886afeef2f98ed7fbaace5eded202f798a340dec0d7f9844688afd70f674c  311  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/CONTROL-S3.txt.cmd
0785bfec35ace1c98256d69fd859f0133327ff5a22f2d5c4decbfb3ec7b65a53  93  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/CONTROL-S3.txt.err
e1326f1d1e067dbec212891e8765c5d36ca158f7db6e243a1736acb48812544c  1777  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/CONTROL-S4.txt
3d8e88a32c84d02f999ce751216d3af79e0e77ee771855f8a16fc017d548db89  311  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/CONTROL-S4.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/CONTROL-S4.txt.err
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/CONTROL-S5.txt
23fd6ee4de2c9d2254c50694a84e47d8bad20ca6216ca9f2102479167273fd94  311  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/CONTROL-S5.txt.cmd
26b57c1bad33a34fd2401dbfa6988f9976d6b01334b800570b6f039cdf7ddf26  1457  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/CONTROL-S5.txt.err
8032226a7fbcea7a007cef6d47371f1a95f9a1d63aa72624b1e1603a280efc31  3439  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/CONTROL-S6.txt
ac89c29d1d6c307581200b697752a8c91fa6e6198a7a3f8d915d2948bda7a902  311  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/CONTROL-S6.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/CONTROL-S6.txt.err
82cbecb0d94025006969584159c08af23244d7ff886fa03f43499201013ad8b0  3414  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/M01-S1.txt
34d6d6bf56b81522d22f9ba6efca55c9f8311b3806c3885794f8915ac07a7489  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/M01-S1.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/M01-S1.txt.err
4d665e296c1d9d3fae289646e3d7971281cd5b4833d8ba6ebcacd61b2c2f6e36  3416  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/M01-S2.txt
2b031fe52b95c2a600952dbaf237b78d3a52fa6d0d462ba5b3aae0b71cb5c7d8  358  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/M01-S2.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/M01-S2.txt.err
0eda66951bffacf461707e5d192e84ef35895f42a41effd4e70a214e5c2895c3  1214  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/M01-S3.txt
94223e8e5907775944eda3edb4cebf1fe0d37bb343977b0c48378eb59d0deeb9  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/M01-S3.txt.cmd
0785bfec35ace1c98256d69fd859f0133327ff5a22f2d5c4decbfb3ec7b65a53  93  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/M01-S3.txt.err
e1326f1d1e067dbec212891e8765c5d36ca158f7db6e243a1736acb48812544c  1777  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/M01-S4.txt
6f43c928a1d47081f69f4c7b02bc68a15f1fea2af64a29b610cf6b7a9f3b3a18  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/M01-S4.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/M01-S4.txt.err
23cbdc296f292bac052cd13266d3d1c00e5391829f32251e441b4d95a03469b9  164  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/M01-S5.txt
df26498dbcb7faf614a202da1a7f525b65c491d5fc3c781137bff92c13869190  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/M01-S5.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/M01-S5.txt.err
8032226a7fbcea7a007cef6d47371f1a95f9a1d63aa72624b1e1603a280efc31  3439  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/M01-S6.txt
e621ebee4c1a779347bec25ab731da5440ab51f5b323be9d03973e4971edb203  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/M01-S6.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/M01-S6.txt.err
82cbecb0d94025006969584159c08af23244d7ff886fa03f43499201013ad8b0  3414  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/N01-S1.txt
b3d5e52576e8399e53369b20e2318c74fe8c1e9532a0ce03602ca81ed0ebdb96  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/N01-S1.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/N01-S1.txt.err
4d665e296c1d9d3fae289646e3d7971281cd5b4833d8ba6ebcacd61b2c2f6e36  3416  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/N01-S2.txt
a3b6eedaa526fccb61e0e0961d81de554d1096ab433c97e3f7f1f1b6750fff97  358  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/N01-S2.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/N01-S2.txt.err
0eda66951bffacf461707e5d192e84ef35895f42a41effd4e70a214e5c2895c3  1214  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/N01-S3.txt
d74ff6b635b4e41397b1b3971bca30ffc8ff02e16283c50bf854447568b45da6  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/N01-S3.txt.cmd
0785bfec35ace1c98256d69fd859f0133327ff5a22f2d5c4decbfb3ec7b65a53  93  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/N01-S3.txt.err
e1326f1d1e067dbec212891e8765c5d36ca158f7db6e243a1736acb48812544c  1777  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/N01-S4.txt
11358747471b6d5f4b48088bc01d17ea14dd008aeebce5323b35070c3a658bfc  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/N01-S4.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/N01-S4.txt.err
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/N01-S5.txt
f9d932d30e800835f7b6edb00acda710b4ebc10187e5654aeb5053af1e12eb18  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/N01-S5.txt.cmd
ff4d308ddffeea08f91be163ac82d9a562f41dcb0efd00275eaaa3d7cc68612d  1396  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/N01-S5.txt.err
8032226a7fbcea7a007cef6d47371f1a95f9a1d63aa72624b1e1603a280efc31  3439  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/N01-S6.txt
4d9e38fc2bbf898258ddb8732dabd322dfc241b11a0d0b56e4ed78369aea3c24  288  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/N01-S6.txt.cmd
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/out/N01-S6.txt.err
08c12f7aef31bbbbb8b2ed2c018bb5d9f70ed5e442dce396606919b553a11290  57177  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/results.json
f6b22735a410b7df43556ee17cd1292fe42bbe2724f479c6ada9da8674ecfb93  35699  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/run2.log
8771541fdfe83b5d7c83021f339f4b09572e56a89c3ba40ff6407101aace87b8  20844  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/spotcheck/real-c1-M01.txt
fb254d279f8250eae13f8249b00eabb857fe8f6f61ea7fb19eae3d0ce8a4902e  24552  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/spotcheck/real-c2-G3c.txt
09700a83bbe897c5885651c70e54a0cd95843b1d0fa5a172f81bae36ab62c406  1543  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.draft/stub-selftest.py
7982298038922b57b333cd51c9bf9bf2f4a2f5f56764a8d2f12135e1eb32b275  24540  .ufo/waves/round-46/attempt2/wave1/R46bMutBattery.md
619ae6cd1565ad0bbbf162619913e3745eb144460b9fe2b3c39688398dcac8fd  894  .ufo/waves/round-46/attempt2/wave1/R46bMutF29a.draft/do-nothing-control.py
c099d89bd756a1740960e22e3bc024c643e7855799cef2aee428df768f739939  11603  .ufo/waves/round-46/attempt2/wave1/R46bMutF29a.draft/evidence-transcript.txt
5fc0622fef18375e17cf7dd20cc1000f72823f9ac532a4ac01a6b2b8e2aa25ab  3173  .ufo/waves/round-46/attempt2/wave1/R46bMutF29a.draft/mutants-derived.py
c31ef5827bb649121b4a92097ab7145176a94543564e3098d038a510dab9dca6  8708  .ufo/waves/round-46/attempt2/wave1/R46bMutF29a.draft/pairing.json
51aa156f7e8f2a82808c7ebabd338a3d597e1eda1d8297e848ca2c49b6ec7752  2180  .ufo/waves/round-46/attempt2/wave1/R46bMutF29a.draft/probes-p7.py
a77c9db2c30f2d1463c56a2d45e825680de9e0ea1da0624ed18abc981e4546cb  5396  .ufo/waves/round-46/attempt2/wave1/R46bMutF29a.draft/probes.py
204e619592b10f03b08d8177fa8eb96402dfa3163f2a8ab7de657acf50025252  3074  .ufo/waves/round-46/attempt2/wave1/R46bMutF29a.draft/robust.py
c0a587e815f952d761b116d75ed1833520186064b7684e200a6897d343284e5b  2115  .ufo/waves/round-46/attempt2/wave1/R46bMutF29a.draft/robust2.py
472e6d973ea8bf660a443102668f2fcdac047e08e402bff115c39bc2fa91b2fc  4707  .ufo/waves/round-46/attempt2/wave1/R46bMutF29a.draft/runpair.py
7dbc621354fb0e4583dd541b2867881ba52c5fd3438a5408182c8ced9ca2cc03  1527  .ufo/waves/round-46/attempt2/wave1/R46bMutF29a.draft/sweep.json
99f5d2fbfb2942cc2523205b3520b2a7d55afea337fff156f5886f88e81a13e9  24532  .ufo/waves/round-46/attempt2/wave1/R46bMutF29a.md
b4fc09cc1f147927edbf05380a83b61da95b2f5887c0fc84bf915382dd52df98  8196  .ufo/waves/round-46/attempt2/wave1/R46bMutF29b.draft/matrix.tsv
2ae69764ceb722c8dd2ebbcd58085ff9122ea729a32a735b0c478729329424ad  13488  .ufo/waves/round-46/attempt2/wave1/R46bMutF29b.draft/mutants.py
cf53f35e4124bce9cb040024211609fe821dc5f317607987587ce92ea5c5c1d3  3970  .ufo/waves/round-46/attempt2/wave1/R46bMutF29b.draft/mutants.tsv
b821b995b29dd8fe1230afbab997e98eb2d1c2029e9e78294ad460487cc4922c  1787  .ufo/waves/round-46/attempt2/wave1/R46bMutF29b.draft/quote.py
9370dcc4ad971aab393feb1af38268862923822d21a22ad714828b21700d199d  3761  .ufo/waves/round-46/attempt2/wave1/R46bMutF29b.draft/regress.py
b0dd5a78387109a2f8569b3121849f1ebcc2cad9e1b2e85b13a52bfd038e186f  5635  .ufo/waves/round-46/attempt2/wave1/R46bMutF29b.draft/round2.py
7b1e61dc46f38347fd85c74d1f01fce895d8b40a70084dfeeb562d0cf0c6f2b3  4040  .ufo/waves/round-46/attempt2/wave1/R46bMutF29b.draft/round3.py
9b1bfda6a00fdb25be3a76d8f4f43f9989e68d24b9fd63cfc7c8104cca9b0369  4100  .ufo/waves/round-46/attempt2/wave1/R46bMutF29b.draft/round4.py
45ea1919f5d83cadb1f84fe02d8a4f2a22736181bb804fea1885cc5f85f14137  3148  .ufo/waves/round-46/attempt2/wave1/R46bMutF29b.draft/round5.py
4d8556cf326a3e7e310c0148f6e7a878200b6a9f75ab86d5262fb8c982d94e14  2996  .ufo/waves/round-46/attempt2/wave1/R46bMutF29b.draft/selftest_coverage.py
6bcfccaee59e6805b35a0109deec015777bd537e8911c1a1614b1dbc8f0a8185  4790  .ufo/waves/round-46/attempt2/wave1/R46bMutF29b.draft/selftest_coverage.txt
984656a52bbbfc9e655e3378dbfac578733e8f0e5aaefda3c61df70e19475eeb  4439  .ufo/waves/round-46/attempt2/wave1/R46bMutF29b.draft/verify.py
c16a515aacd9caaf76e0f33f7be814c0761c816262cf5211f5ca82d34c038931  13189  .ufo/waves/round-46/attempt2/wave1/R46bMutF29b.draft/verify_full.txt
685d06b23f447999b97ab45b18c983bba2985228db7e7809e6a0b498775acea9  28315  .ufo/waves/round-46/attempt2/wave1/R46bMutF29b.md
53cf16da0e35d6f9ffcff3facadd2407391c066e4485ec36900e9d9f1b55f7b9  11589  .ufo/waves/round-46/attempt2/wave1/R46bMutSelfC1a.md
2260c27214eb4b9ba88eb0648d7a8dae1d8c31f5afa3aa38e5e1fcb3356e1025  94  .ufo/waves/round-46/attempt2/wave1/R46bMutSelfC1b.draft/consolidation-batch-incomplete.txt
ff54e4b4e8283e0c22232aa5c3ed32844d2bc73e323de00042fee2bc8d7eab96  829  .ufo/waves/round-46/attempt2/wave1/R46bMutSelfC1b.draft/mkmut.py
e5a6cdaab629817a573a918c6da8612e715cf9654ca5fb351b03ea8a7967ff83  7908  .ufo/waves/round-46/attempt2/wave1/R46bMutSelfC1b.draft/mutrun.py
7eb8c4d0094acfbe8622eadd3c19e3589eb100ec41ee6bdbb25b45538bf52b6d  5292  .ufo/waves/round-46/attempt2/wave1/R46bMutSelfC1b.draft/own-batch-transcript.txt
9b78efc43f6e83fbdad31e66460db804d014d63229fa8668f0245565c4d34785  10770  .ufo/waves/round-46/attempt2/wave1/R46bMutSelfC1b.draft/probe-witnesses.txt
7bbb2b6aa3dc321e79880f8409335c016f497d2a7c6915ac6059a2c376a23e33  30510  .ufo/waves/round-46/attempt2/wave1/R46bMutSelfC1b.draft/probe.py
e0915bf564d442ec157ddbcfeecbede6bd6f053396317540a88d5968276d9289  9714  .ufo/waves/round-46/attempt2/wave1/R46bMutSelfC1b.draft/selftest-baseline.txt
d53c8563b040e769a4fc78aeba68f3f00ee5873d553e39231e79ca2f30b02e93  139  .ufo/waves/round-46/attempt2/wave1/R46bMutSelfC1b.draft/xcheck-incomplete.txt
dce638bf59e4f0969a47c9803c96aa926f0c1eb42448f23b6af9d7825529d1f4  25118  .ufo/waves/round-46/attempt2/wave1/R46bMutSelfC1b.md
b9243c0e480c16933d70c19f9165839e6f3d0947ee440a56a69117b5d8853e67  2699  .ufo/waves/round-46/attempt2/wave1/R46bMutSelfC2a.draft/c2-mutant-table-committed.log
dc5e358ffdc3222358f5a90cf061152fa32c7d87428dae62ef0d6b59319609e4  2886  .ufo/waves/round-46/attempt2/wave1/R46bMutSelfC2a.draft/c2-mutant-table-committed.txt
42e7ce2a24d9f136cbc93405cfa6d33335d9d4b25a0f92c99bf7f80f257cb92a  2072  .ufo/waves/round-46/attempt2/wave1/R46bMutSelfC2a.draft/controls.txt
fd7b182d3b2d26b700fff31df78eed95e85281ad3b072f64fedcf55e075df8b3  3003  .ufo/waves/round-46/attempt2/wave1/R46bMutSelfC2a.draft/discriminating.py
f4a073b6105b80db7da170aeb6c73296d613f239290c866c3932783134c4c632  4193  .ufo/waves/round-46/attempt2/wave1/R46bMutSelfC2a.draft/drv.py
e27bb0d078702a678927dac73a14297bb960b5b4961e1f141d2128cf2f6124aa  2029  .ufo/waves/round-46/attempt2/wave1/R46bMutSelfC2a.draft/equiv.py
a570dbc3991816b4f3220983133924d37461b1191c143c7dd707f7729131692b  2156  .ufo/waves/round-46/attempt2/wave1/R46bMutSelfC2a.draft/g3a-e2e.txt
626306b211a77426a9d1c22fab821e9195ea013ab753848559592f42e0e4d897  3071  .ufo/waves/round-46/attempt2/wave1/R46bMutSelfC2a.draft/g3a_e2e.py
a4d502dae391394f9b1931e0116777b4ceec5cb04aa9c11a3abbb472b6551d10  1897  .ufo/waves/round-46/attempt2/wave1/R46bMutSelfC2a.draft/g6c_check.py
38265b0654a94c1c1e100ce8c749aab255791220f09895dabb0abfcb6ebb55b9  2601  .ufo/waves/round-46/attempt2/wave1/R46bMutSelfC2a.draft/g7b.py
0da151dc4c5c847cafff25a77751fb61efbb3d65f3091ccaa439339e85db8430  312  .ufo/waves/round-46/attempt2/wave1/R46bMutSelfC2a.draft/lane-hashes-after.txt
8e186f2389bea71206e15ea2cf2bef1f62d06936e4db0157b5ed55c92564ef07  636  .ufo/waves/round-46/attempt2/wave1/R46bMutSelfC2a.draft/lane-hashes-before.txt
9f47c234001d088cf5548108d36efb78bcc8e2f079191116a24d6d31b8ab8d01  9548  .ufo/waves/round-46/attempt2/wave1/R46bMutSelfC2a.draft/liveness-probes.txt
a97e731e46e18216a88757c220bf0dfcbb325ede8bc59fee0e1927d764998473  326  .ufo/waves/round-46/attempt2/wave1/R46bMutSelfC2a.draft/noop-control.txt
1db354f317e09d797549146e382295a3ce1d4361de78f81e64106271c2a556b2  3347  .ufo/waves/round-46/attempt2/wave1/R46bMutSelfC2a.draft/noop.py
6eccf8da675c0160253a7d6e9bf5fc59fd3f5b67d5a335c60836492a534fef0a  10134  .ufo/waves/round-46/attempt2/wave1/R46bMutSelfC2a.draft/probe.py
809f91709a598a866f65220ae3bcfed8c797b05a1c303005ddb150079b602fcd  18642  .ufo/waves/round-46/attempt2/wave1/R46bMutSelfC2a.md
8ec1fe2f2ee65c59bfef8d612e8e4a2a7029ce9bf0eaf89746087baa79d43fbc  454  .ufo/waves/round-46/attempt2/wave1/R46bMutSelfC2b.draft/dnc-control.log
287937d0a65e7c64ff202f6aee09854ec2074e578d16795703b07d5ac8439fd0  6982  .ufo/waves/round-46/attempt2/wave1/R46bMutSelfC2b.draft/mutants.py
daab0d26f427280a64d0379473575564c1af3bf3e4178756251409f31d9a8021  8308  .ufo/waves/round-46/attempt2/wave1/R46bMutSelfC2b.draft/results.jsonl
8740a27a4483e154529a503f6db9f327d4c329d113e9eeb2327837d05be30395  3514  .ufo/waves/round-46/attempt2/wave1/R46bMutSelfC2b.draft/run.log
6df1934c6e4726801e70b575a9390e5de22eb43c525e306484dd08a12346ab64  5844  .ufo/waves/round-46/attempt2/wave1/R46bMutSelfC2b.draft/run.py
593c563cae34a993f38649ac5073c2760c4337047f2b213ff4d9ff653298d08b  2574  .ufo/waves/round-46/attempt2/wave1/R46bMutSelfC2b.draft/run2.log
dc8dc0a2992e28fba7692e7c4524df5590eda61f17460a841423e7ada908d2ef  363  .ufo/waves/round-46/attempt2/wave1/R46bMutSelfC2b.draft/selftest-sha256.txt
f2aef428701251d2a2aad2d39109a53428ddbe07f090c4d6623fbcce7d0ed25a  33467  .ufo/waves/round-46/attempt2/wave1/R46bMutSelfC2b.draft/witness-results.json
188c5d45bf8b91c6903bede4be1d4e8eb5f5cf1b0cc4aa986c840f21f65c9fba  5167  .ufo/waves/round-46/attempt2/wave1/R46bMutSelfC2b.draft/witness_runner.py
4b552d6e868edfe98467d7fdf5d0bd5ef71f3bf5c857297e770b8332511b3082  17140  .ufo/waves/round-46/attempt2/wave1/R46bMutSelfC2b.draft/witnesses.py
f45398f022b6bb77c671671b1da41a1c4cc192df70b8b8ede6c33a77a40bc508  15594  .ufo/waves/round-46/attempt2/wave1/R46bMutSelfC2b.md
0730d96b95d38f8e253f25efa152387c521b6a34cd89e4af30eafd466a964e6a  371  .ufo/waves/round-46/attempt2/wave1/R46bRevC1Lineage.draft/receipts/g1-base-base.log
0730d96b95d38f8e253f25efa152387c521b6a34cd89e4af30eafd466a964e6a  371  .ufo/waves/round-46/attempt2/wave1/R46bRevC1Lineage.draft/receipts/g2-live-base.log
b75e0d1af9696c0038370a1263f6eb5fe09023d67f65a23e8b5d78a7ae9ee252  371  .ufo/waves/round-46/attempt2/wave1/R46bRevC1Lineage.draft/receipts/g3-pure2-pure2.log
822eb992a6950f7a7be37fa6c782ce3774f41f00e2e34812f041c149268ce8c8  412  .ufo/waves/round-46/attempt2/wave1/R46bRevC1Lineage.draft/receipts/g4-live-pure2.log
e0915bf564d442ec157ddbcfeecbede6bd6f053396317540a88d5968276d9289  9714  .ufo/waves/round-46/attempt2/wave1/R46bRevC1Lineage.draft/receipts/s1-selftest-c1.log
54f21c1f8d7d0f8e863b6b89e7c8944ec4b5434617ffcdbfad39976b57f8566e  10730  .ufo/waves/round-46/attempt2/wave1/R46bRevC1Lineage.draft/receipts/s2-selftest-c2.log
be177fb0894e830669b39c87fa35839eff56c787db5e9f0a1d2d18775d798fca  11236  .ufo/waves/round-46/attempt2/wave1/R46bRevC1Lineage.md
c4ee3dac2fdb9895fdfcd1699adc345fa2ac29b4496fc137dc2470627d81f323  13719  .ufo/waves/round-46/attempt2/wave1/R46bRevClaimsErrata.md
a233ace95dd7be8d1c5e679c546d6c5d3e64c5d2a9adc875e22a014c8834e502  14239  .ufo/waves/round-46/attempt2/wave1/R46bRevEntrySrc.md
cc1c082addbe180d1636753d84e55080dbac98b15d810b68e718da87330f06b5  489  .ufo/waves/round-46/attempt2/wave1/R46bRevF29H1.draft/a1-naive-dup-control.gate.txt
5b1db4be6dd4d44ade0af2851eba7246d2651a00053a4ffdec1ed274f2989764  496  .ufo/waves/round-46/attempt2/wave1/R46bRevF29H1.draft/a2-indented-dup-block.gate.txt
5b1db4be6dd4d44ade0af2851eba7246d2651a00053a4ffdec1ed274f2989764  496  .ufo/waves/round-46/attempt2/wave1/R46bRevF29H1.draft/a3-id-collision-f2-space-9.gate.txt
9cdf428fa6dcc17958d3733765c0690f92704bbcc653df84f8e093427f2e4c68  489  .ufo/waves/round-46/attempt2/wave1/R46bRevF29H1.draft/a4-unicode-digits-control.gate.txt
5b1db4be6dd4d44ade0af2851eba7246d2651a00053a4ffdec1ed274f2989764  496  .ufo/waves/round-46/attempt2/wave1/R46bRevF29H1.draft/a5-entry-cell-aliasing.gate.txt
5b1db4be6dd4d44ade0af2851eba7246d2651a00053a4ffdec1ed274f2989764  496  .ufo/waves/round-46/attempt2/wave1/R46bRevF29H1.draft/a6-comment-oneline-f29.gate.txt
cc1c082addbe180d1636753d84e55080dbac98b15d810b68e718da87330f06b5  489  .ufo/waves/round-46/attempt2/wave1/R46bRevF29H1.draft/a7-comment-multiline-control.gate.txt
5b1db4be6dd4d44ade0af2851eba7246d2651a00053a4ffdec1ed274f2989764  496  .ufo/waves/round-46/attempt2/wave1/R46bRevF29H1.draft/a8-lowercase-id.gate.txt
5b1db4be6dd4d44ade0af2851eba7246d2651a00053a4ffdec1ed274f2989764  496  .ufo/waves/round-46/attempt2/wave1/R46bRevF29H1.draft/a9-zwsp-id.gate.txt
9b9866538ebc874fbbdde40551f4f913558be8263e071539a42a3b58dd076a8b  4181  .ufo/waves/round-46/attempt2/wave1/R46bRevF29H1.draft/attack-h1.py
3ba406f2cd3e52726ac38939cd557ae21de9e2860cfd8ce89967701b1f97d2f2  960  .ufo/waves/round-46/attempt2/wave1/R46bRevF29H1.draft/matrix-output.txt
3c5a458bdbc0cc813136d3e55c7dbaa66fb2b51d9dc734b12cb3596d9505c4f2  6531  .ufo/waves/round-46/attempt2/wave1/R46bRevF29H1.md
0c5cff17ec697017a13a8b44de7c44587677f394e86676c455d9cc20602940ec  371  .ufo/waves/round-46/attempt2/wave1/R46bRevF29H2H3.draft/base.txt
e5ad30e4085ffc64688a381c343f9b205ec4149f0a4c3a7cbd3c4c635856f712  2881  .ufo/waves/round-46/attempt2/wave1/R46bRevF29H2H3.draft/build-defects.py
5b1db4be6dd4d44ade0af2851eba7246d2651a00053a4ffdec1ed274f2989764  496  .ufo/waves/round-46/attempt2/wave1/R46bRevF29H2H3.draft/d1-recheck-comment.txt
5b1db4be6dd4d44ade0af2851eba7246d2651a00053a4ffdec1ed274f2989764  496  .ufo/waves/round-46/attempt2/wave1/R46bRevF29H2H3.draft/d2-trio-dup.txt
5b1db4be6dd4d44ade0af2851eba7246d2651a00053a4ffdec1ed274f2989764  496  .ufo/waves/round-46/attempt2/wave1/R46bRevF29H2H3.draft/d3-redirector.txt
5b1db4be6dd4d44ade0af2851eba7246d2651a00053a4ffdec1ed274f2989764  496  .ufo/waves/round-46/attempt2/wave1/R46bRevF29H2H3.draft/d4-repeated-words.txt
5b1db4be6dd4d44ade0af2851eba7246d2651a00053a4ffdec1ed274f2989764  496  .ufo/waves/round-46/attempt2/wave1/R46bRevF29H2H3.draft/d5-wrong-file-locator.txt
34c4c1a0c27baa4366e8bb7f4a6f5b95bee4c8e57ae70e5056a2512dec1200f6  6686  .ufo/waves/round-46/attempt2/wave1/R46bRevF29H2H3.draft/defect-diffs.txt
2036c921911d543615d4e8455416c98bda3678468736e2bd88454ba230368054  403  .ufo/waves/round-46/attempt2/wave1/R46bRevF29H2H3.draft/freeze.txt
5b1db4be6dd4d44ade0af2851eba7246d2651a00053a4ffdec1ed274f2989764  496  .ufo/waves/round-46/attempt2/wave1/R46bRevF29H2H3.draft/positive.txt
2ad2c73c6d1213fdbf9ca0de06fe4a20d994f057de6fa2d87e7b1a3d930a0b11  7130  .ufo/waves/round-46/attempt2/wave1/R46bRevF29H2H3.md
67961c8f316ba4a8c5f4e404a3c8776baea10eb0e07745b131dd5e3c10b0cb7a  2278  .ufo/waves/round-46/attempt2/wave1/R46bRevF29H4H5.draft/evidence-snapshot-boundary-lines.txt
ee88a4fcf169ec654b4c0ce9bf305ddac22e41fd3854643dbb0635719fa0924e  2473  .ufo/waves/round-46/attempt2/wave1/R46bRevF29H4H5.draft/receipts-E1-controls.txt
4a2030bca7c4b4e8851593b50fc426338636f81ea25818c0881b31c180f79914  6928  .ufo/waves/round-46/attempt2/wave1/R46bRevF29H4H5.draft/receipts-E2-E7-attacks.txt
99c60fa261546824ddbc140f3d6ea20b622967cc82f5526ffdd9b9c0dbd8c46d  338  .ufo/waves/round-46/attempt2/wave1/R46bRevF29H4H5.draft/receipts-E3b-E4b-clauses.txt
7c945cf2fbc793e45933cf29fefcd5417da5b9fbeb2fb845bb8697edbe0a3553  10577  .ufo/waves/round-46/attempt2/wave1/R46bRevF29H4H5.md
edba1354a10f869acb534c2bcde2300b49704b1080dd247d38144fb038680f6b  6754  .ufo/waves/round-46/attempt2/wave1/R46bRevF29H6H7.md
72bb04953f8c9b04361372f5a4bfb4ab71101e5172f88a87751d6e75e144e173  842  .ufo/waves/round-46/attempt2/wave1/R46bRevLedgerAmend.draft/fixtures.txt
a020122252c6a6c42095a56e73a4e8ba677837476e66fde98bf5cd237c5c8e3e  8528  .ufo/waves/round-46/attempt2/wave1/R46bRevLedgerAmend.draft/gate-run-receipt.txt
496da39dc99c6e845c5fe23fe42f52d37be87c15be7656ceb2a5a4947304b7da  158  .ufo/waves/round-46/attempt2/wave1/R46bRevLedgerAmend.draft/mock-sha.txt
42d796f6cda2dd37e9019c1a96cabc1716a40ab68b3e25ea9821ee007bcb80b6  3887  .ufo/waves/round-46/attempt2/wave1/R46bRevLedgerAmend.draft/v12-to-v13-mock.diff
7c01dcad847b984e0c3ca769a1e6fca47ab61a40e444d174192840df860dcec1  11945  .ufo/waves/round-46/attempt2/wave1/R46bRevLedgerAmend.md
84fb29ca543ff23daaf06c91767dcc0a1a355047a8ef61a207890bb8e25baf5e  15178  .ufo/waves/round-46/attempt2/wave1/R46bRevMutbat.md
fc559996ead2d6da74f4d46cb570ce3ea832eba78f80325e07efa4e8d33ca20f  463  .ufo/waves/round-46/attempt2/wave1/R46bRevNoHarm.draft/aux.txt
848388dd9de404c1f034703672163828bb2e82c0f2b0261eb92a4c0e0499aba0  806  .ufo/waves/round-46/attempt2/wave1/R46bRevNoHarm.draft/c1-gate-base-vs-live.txt
ef35a034a25cd30e2a9531d517433eb25c036a024eb6f9d5c7f3024c81894690  562  .ufo/waves/round-46/attempt2/wave1/R46bRevNoHarm.draft/c2-gate-live.txt
651cf7143cdf92aafe7fa6d64566b633db7c98e7a9bdc3e0073b46955844e389  3291  .ufo/waves/round-46/attempt2/wave1/R46bRevNoHarm.draft/capture-binding.txt
79ae8c1947ecda449aa9fdab762d528daa5e0126fb83c5ea0e7cd6558286aacc  770  .ufo/waves/round-46/attempt2/wave1/R46bRevNoHarm.draft/census.txt
3701e8e0ddb6dbbae099dd08acb813f694eb8e7e5b15333335e23c8177213768  9034  .ufo/waves/round-46/attempt2/wave1/R46bRevNoHarm.md
8a8b944f6eb8171dc38185215a67e6d27600545dfad30de3cc06e7552b4c0286  663  .ufo/waves/round-46/attempt2/wave1/R46bRevPriorEscapes.draft/c1-control.txt
5004627e2eecef64ed95c251ab5c4c6747b5df3e0ba240e905701c836cbec402  1006  .ufo/waves/round-46/attempt2/wave1/R46bRevPriorEscapes.draft/c1-mutant-finding1.txt
0fbf3fd4a3be10746cbf5789300b54ead8c611f980b228397aff237b6a4b9a93  791  .ufo/waves/round-46/attempt2/wave1/R46bRevPriorEscapes.draft/c2-control.txt
9b06bd1b5da61e32e62baf6aba15a951d8103c576c8e9a01b8f5113a164381b1  800  .ufo/waves/round-46/attempt2/wave1/R46bRevPriorEscapes.draft/c2-junk-boundary.txt
757a27b76e636ff71085d64490d89c97c78f8c1ddb6946c26633eb4ba9922674  895  .ufo/waves/round-46/attempt2/wave1/R46bRevPriorEscapes.draft/c2-junk1.txt
99d3aac53bf424bf486de9f328cae8b1ac842ea7931ffcb04d23d5d24a2e7ab6  1271  .ufo/waves/round-46/attempt2/wave1/R46bRevPriorEscapes.draft/counter-lineage.txt
f17ca645ffc1eb3d3effc9e56b804e6bfc33a047a5f056fdca2f78ea1d0df4dd  9170  .ufo/waves/round-46/attempt2/wave1/R46bRevPriorEscapes.md
3068e9fc5715c5dbf702c3e4209632cf3497fcd53fae7bf5a1562f3450ede569  13433  .ufo/waves/round-46/attempt2/wave1/R46bRevSelftestDiff.md
82767c67f796810ec14dd0e035a1e784a5757843d9eded9c9e37e5113aa3f786  10141  .ufo/waves/round-46/attempt2/wave1/R46bRevengerEscapes.md
06de929f5602c47601513988418e902c872aec5bf4ac391d2e4bf0fc2ced5f96  8268  .ufo/waves/round-46/attempt2/wave1/R46bScoutAbsence.md
a8a285af3b764367ab74de2a8445a7aaf8e2c3e9b5231335cb6a3a6f0855e02d  12342  .ufo/waves/round-46/attempt2/wave1/R46bScoutAdjacent.md
99f19ee81e72db26ee4fc7c90c7f30172f86356c2a5f5cf8b3affd256f94dade  1110  .ufo/waves/round-46/attempt2/wave1/R46bScoutEquivalence.draft/COMPARISON.txt
c9412418651cf9ad06592edf0faf2c11081f270d4d0083b5e7fa9ba51e702f9e  412  .ufo/waves/round-46/attempt2/wave1/R46bScoutEquivalence.draft/M06-T6.out
b75e0d1af9696c0038370a1263f6eb5fe09023d67f65a23e8b5d78a7ae9ee252  371  .ufo/waves/round-46/attempt2/wave1/R46bScoutEquivalence.draft/M06-pure.out
c9412418651cf9ad06592edf0faf2c11081f270d4d0083b5e7fa9ba51e702f9e  412  .ufo/waves/round-46/attempt2/wave1/R46bScoutEquivalence.draft/M06-tip.out
c9412418651cf9ad06592edf0faf2c11081f270d4d0083b5e7fa9ba51e702f9e  412  .ufo/waves/round-46/attempt2/wave1/R46bScoutEquivalence.draft/M07-T7.out
c9412418651cf9ad06592edf0faf2c11081f270d4d0083b5e7fa9ba51e702f9e  412  .ufo/waves/round-46/attempt2/wave1/R46bScoutEquivalence.draft/M07-tip.out
7dda4ed0d027cb8aa155bebe2b8da3c9f492340635b8f46ae45a80a929af31ae  443  .ufo/waves/round-46/attempt2/wave1/R46bScoutEquivalence.draft/M14-T14.out
36e373636e2d66a9372d8cc8600ec728eb7be333c48a595510a6801857ffe31a  412  .ufo/waves/round-46/attempt2/wave1/R46bScoutEquivalence.draft/M14-T19.out
8e0986d2c123ef07e379c31f138357088b5d5847041fe05233446b6411628aaf  420  .ufo/waves/round-46/attempt2/wave1/R46bScoutEquivalence.draft/M14-T6.out
b75e0d1af9696c0038370a1263f6eb5fe09023d67f65a23e8b5d78a7ae9ee252  371  .ufo/waves/round-46/attempt2/wave1/R46bScoutEquivalence.draft/M14-pure.out
c9412418651cf9ad06592edf0faf2c11081f270d4d0083b5e7fa9ba51e702f9e  412  .ufo/waves/round-46/attempt2/wave1/R46bScoutEquivalence.draft/M14-tip.out
16e60eb2f782dfebbb74302fbe9f781ef11b5236cead6d8eec2e87e0d004204e  412  .ufo/waves/round-46/attempt2/wave1/R46bScoutEquivalence.draft/M19-T19.out
c9412418651cf9ad06592edf0faf2c11081f270d4d0083b5e7fa9ba51e702f9e  412  .ufo/waves/round-46/attempt2/wave1/R46bScoutEquivalence.draft/M19-tip.out
95f3a12e64ee0de77728af338a8d9d00a67474c733e090225f08d8b3e08dcac6  8492  .ufo/waves/round-46/attempt2/wave1/R46bScoutEquivalence.draft/driver.py
7dda4ed0d027cb8aa155bebe2b8da3c9f492340635b8f46ae45a80a929af31ae  443  .ufo/waves/round-46/attempt2/wave1/R46bScoutEquivalence.draft/orig-T14.out
36e373636e2d66a9372d8cc8600ec728eb7be333c48a595510a6801857ffe31a  412  .ufo/waves/round-46/attempt2/wave1/R46bScoutEquivalence.draft/orig-T19.out
8e0986d2c123ef07e379c31f138357088b5d5847041fe05233446b6411628aaf  420  .ufo/waves/round-46/attempt2/wave1/R46bScoutEquivalence.draft/orig-T6.out
8e0986d2c123ef07e379c31f138357088b5d5847041fe05233446b6411628aaf  420  .ufo/waves/round-46/attempt2/wave1/R46bScoutEquivalence.draft/orig-T7.out
b75e0d1af9696c0038370a1263f6eb5fe09023d67f65a23e8b5d78a7ae9ee252  371  .ufo/waves/round-46/attempt2/wave1/R46bScoutEquivalence.draft/orig-pure.out
c9412418651cf9ad06592edf0faf2c11081f270d4d0083b5e7fa9ba51e702f9e  412  .ufo/waves/round-46/attempt2/wave1/R46bScoutEquivalence.draft/orig-tip.out
dacdea63259776453cce9edb8b9e0f5d6ec7edf57438a6a19dc457270ef295ad  10519  .ufo/waves/round-46/attempt2/wave1/R46bScoutEquivalence.md
1e601d435d3b52f8cf9829a7d9363caa864d27d770ffc07fc1054f09f6c18e80  16162  .ufo/waves/round-46/attempt2/wave1/R46bScoutF29Live.md
c7d2b7119c79b90d22bf4c806bdd32a467703f798f0235630e905570a4460f6e  14174  .ufo/waves/round-46/attempt2/wave1/R46bScoutLedger.md
deee8701d948bca28d2af89e377376732e0a2239e8064dccbfd4ba46521bf72c  10199  .ufo/waves/round-46/attempt2/wave1/R46bScoutPureRecipe.md
483f623abc622c273a47f4a3bc2d1fb8cbaa3ac3dc726ad2e5f6dc7661a3d4c4  12638  .ufo/waves/round-46/attempt2/wave1/R46bScoutRoutedDefects.md
f1ac26db7731c2bcac45e33d28cfe5c19b7d785a1c3ab18c405c28cecc7f59d4  17307  .ufo/waves/round-46/attempt2/wave1/R46bScoutSelftestC1Gap.md
89f5731d953779faa1f440cac350356babfa16ce573a43ea2ee3324eb1435554  19199  .ufo/waves/round-46/attempt2/wave1/R46bScoutSelftestC2Gap.md
ebcacc43eec325fb3679f12bae2957783a9f740478004ee399338b7e73387dbe  6517  .ufo/waves/round-46/attempt2/wave1/R46bScribeAdmission.draft/appends.md
259962988b968b5b6557d7ac0127504a7f89a03921895e48b97c024d2888954c  4769  .ufo/waves/round-46/attempt2/wave1/R46bScribeAdmission.draft/receipts.txt
9022e80380d03c24d3b9e7a94a8d5ea9d05650c91021ab4b31954ec901218550  15260  .ufo/waves/round-46/attempt2/wave1/R46bScribeAdmission.md
8fa83d4c910e92d2a6dbcbe5dccc48bb2b6b5913ce53fd2cb1f587343549848b  499  .ufo/waves/round-46/attempt2/wave1/R46bScribeEntryA.draft/gate-receipt.txt
82db8aeb032470866e10be3488ad0f87b85ef95359330b60593d0242746111d7  12798  .ufo/waves/round-46/attempt2/wave1/R46bScribeEntryA.draft/github-repository-security-advisories.md
dee6694c5f8ba34c990ec785d6dfc70af67d943df226e0d3fa67a431b161ba4a  15439  .ufo/waves/round-46/attempt2/wave1/R46bScribeEntryA.draft/quote-selfcheck.txt
a5833e80fabe78a2eedc6d6728f7775840af717433fde97db62d7115bd81db63  15701  .ufo/waves/round-46/attempt2/wave1/R46bScribeEntryA.md
b9e29ec0c0ea07771a20ffc96819fa5f41e223b160229aba734a658d3c327418  15320  .ufo/waves/round-46/attempt2/wave1/R46bScribeEntryB.draft/github-repository-security-advisories.md
59b45f6fd21b7cbfe4c7b4fa0cdcd7e02d24d34033621aa1ad5e1684f096b17d  22622  .ufo/waves/round-46/attempt2/wave1/R46bScribeEntryB.draft/self-check.txt
4a17245c8c94418428c60ab61834561bfa66dca12691cb7096333adb24e532ef  37666  .ufo/waves/round-46/attempt2/wave1/R46bScribeEntryB.md
b57b53001516d143e9d23ef6dcc4375bc7292ce8e3f176edf181e22d59b1e043  12453  .ufo/waves/round-46/attempt2/wave1/R46bScribeEntryC.draft/github-repository-security-advisories.md
31f7b8aaf49ae529edfbe67b5bf15ab003086797910bd83cf85a682fe34e7725  501  .ufo/waves/round-46/attempt2/wave1/R46bScribeEntryC.draft/receipt-gate-control-fabricated.txt
78882f3c928f0fba688428efbc594e7a1e3041f127e3bc24c6c64a7453cf93ce  496  .ufo/waves/round-46/attempt2/wave1/R46bScribeEntryC.draft/receipt-gate-control-marker.txt
847a039ad296658a955f406ea8d70856354ec636e1649ee5d166ecc7ff687206  501  .ufo/waves/round-46/attempt2/wave1/R46bScribeEntryC.draft/receipt-gate-positive.txt
d32e7fe10da895fb95f8f1fc761354fb7f7d5b021e979199bfac49daa195c9b0  15886  .ufo/waves/round-46/attempt2/wave1/R46bScribeEntryC.draft/receipt-quote-selfcheck.txt
a931bcc3b03e6578af7268ede20e63c0da771c000650ed1b780e671aafee0f09  357  .ufo/waves/round-46/attempt2/wave1/R46bScribeEntryC.draft/receipt-source-recheck.txt
5c801ea6872c405d88a89980e7eb5701dd8dc969692d5125ef2339f403a7cbf7  33489  .ufo/waves/round-46/attempt2/wave1/R46bScribeEntryC.md
b160278954afcbee9d63bba80090cbb28f3c7e512df623b3731a3a381aad69fd  11255  .ufo/waves/round-46/attempt2/wave1/R46bScribeEntryD.draft/github-repository-security-advisories.md
4a39e3f4f28e186e6e775f2a7e29f2ece2b756bd54f339089fb56c82a78aa4ae  2577  .ufo/waves/round-46/attempt2/wave1/R46bScribeEntryD.draft/receipts-gate.txt
6dbfd459594ef1717ceaec8868189b4b03fccac073085409d99fc27afdc5ee85  14315  .ufo/waves/round-46/attempt2/wave1/R46bScribeEntryD.md
364b9eb0147800d9bdb8871d2cb32a74d801b83fa2bb08c242897ec4db1493a6  7988  .ufo/waves/round-46/attempt2/wave1/R46bScribeEntryE.draft/github-repository-security-advisories.md
bcc639f40a77ffced8a5084317f7b5de3dda9b6f71a00c40e77e65f28b6de37b  2141  .ufo/waves/round-46/attempt2/wave1/R46bScribeEntryE.draft/receipts/gate-negative-controls.txt
860f7c0e08defbeb3e1c7c499e7c6318a74d62888673edba1964a5e8a120100d  642  .ufo/waves/round-46/attempt2/wave1/R46bScribeEntryE.draft/receipts/gate-positive.txt
7a4f31a952d013b9582f5550464157eab7f1e0e747a1bea12e14d624489dbaa8  4119  .ufo/waves/round-46/attempt2/wave1/R46bScribeEntryE.draft/receipts/quote-selfcheck-sed.txt
5ce84109c1e54fdf16bdfa00770dfa951217e1dd97705a44657388988db666b2  479  .ufo/waves/round-46/attempt2/wave1/R46bScribeEntryE.draft/receipts/source-recheck-S074.txt
34f0ad216e98bfeee136b0b256a06a804002d972f3fb9ef4fe719afa2e96e3e7  12002  .ufo/waves/round-46/attempt2/wave1/R46bScribeEntryE.md
ecd143d283d63ea14c6e073fa7d6a21c88c78432709b66bd4a9ad8aec754fb27  11668  .ufo/waves/round-46/attempt2/wave1/R46bScribeEntryF.draft/github-repository-security-advisories.md
d4ce78edd9714375eca5fbd5efc240f13b8f9dbab1504e0e280e86ff03911dfa  498  .ufo/waves/round-46/attempt2/wave1/R46bScribeEntryF.draft/receipts/gate-composed.txt
9e207b604a7bff8a21890177699bad48ce9b565f62d1d2969dfe70b5749d8d3b  385  .ufo/waves/round-46/attempt2/wave1/R46bScribeEntryF.draft/receipts/gate-no-entry-rows.txt
2036c921911d543615d4e8455416c98bda3678468736e2bd88454ba230368054  403  .ufo/waves/round-46/attempt2/wave1/R46bScribeEntryF.draft/receipts/gate-no-entry.txt
27b93256273338042e9c035230f9a5bfa70e190d21f12128f24c1d8cc01ac4db  3110  .ufo/waves/round-46/attempt2/wave1/R46bScribeEntryF.draft/receipts/mutants.txt
596fd50fdeb45112189850fedd1e08decdf41ff5b9cfe10efef35f17e5eb336a  11153  .ufo/waves/round-46/attempt2/wave1/R46bScribeEntryF.draft/receipts/quotecheck.txt
25a6fb8bf001e8bd43691ac57bea33cf698df068f6fcaabaac882cc6e4380ddc  14956  .ufo/waves/round-46/attempt2/wave1/R46bScribeEntryF.md
9e48655159f718ca79d66d460e6a242abddf3c034b3a51c757fb63c65b758129  11128  .ufo/waves/round-46/attempt2/wave1/R46bScribeLesson.draft/attempt2-lesson-section.md
715d8c66f14374a100687b1a8730481caafa2b784a6b9ad47951f16ac36ebe4d  11695  .ufo/waves/round-46/attempt2/wave1/R46bScribeLesson.draft/evidence.md
463e3ec18cafd0f57b99e2cd7618ec13e19d0e88bbe889abc2b05360a901c1a8  12726  .ufo/waves/round-46/attempt2/wave1/R46bScribeLesson.draft/gate-block.md
25eda0b202695bc19e25c1cba66569182f6dc8e1d709ba88b6614b885917c8c3  7048  .ufo/waves/round-46/attempt2/wave1/R46bScribeLesson.draft/status-recheck-usedby.md
86fbf8af997a9e8816fe8a51e755f5e4d5c74333fd0bb22ebe965d2526bd478f  11130  .ufo/waves/round-46/attempt2/wave1/R46bScribeLesson.md
93fca474bfc6ed15e8b50b9975b30bfd2f9a628480900e126b0a6b22b742223f  11666  .ufo/waves/round-46/attempt2/wave1/R46bScribeLog.draft/log.md
e79dac374f9103aa0e9cc3ff066ed1bde77a1b8b64f5ee0fe574247045708ac9  19536  .ufo/waves/round-46/attempt2/wave1/R46bScribeLog.md
f4b3a7495f5534df72ab3a359173060f64d364b1bc214b60eeb7295eb18decec  1980  .ufo/waves/round-46/attempt2/wave1/R46bScribeRowsA.draft/census-receipts.txt
0d092706bd2e5ff080da7030e17d68763426379a6edff80d9be5e2634ea71635  1348  .ufo/waves/round-46/attempt2/wave1/R46bScribeRowsA.draft/gate-receipts.txt
8ca29a41fa2ef02de8cfc7dfa7d0a287dbb0c8e13429f37821b88e6e32e6ef31  14326  .ufo/waves/round-46/attempt2/wave1/R46bScribeRowsA.draft/rows.md
109c69f09a1b9c0930c856feb8b3b797fc91b1b2432e95758581209cfd98beb9  3752  .ufo/waves/round-46/attempt2/wave1/R46bScribeRowsA.draft/sweep-receipts.txt
3c62780561cfbabf0f5520edff36b17b1580a03fb46fd4952a462bd818298af8  18606  .ufo/waves/round-46/attempt2/wave1/R46bScribeRowsA.md
465ccb77bea819502990b4c7667e637e7984d915cab6d150510939f6c1636fe5  2697  .ufo/waves/round-46/attempt2/wave1/R46bScribeRowsB.draft/census-receipts.txt
502c3c67a563738936c97a7aa6a9ad60f8b309f232623f170723f912e5565385  2423  .ufo/waves/round-46/attempt2/wave1/R46bScribeRowsB.draft/gate-receipts.txt
1b91b33d7d4fcf5fcf8d3c3ec4fc64fdd60baec1e0a9fcd1d46cbad207de94ee  13251  .ufo/waves/round-46/attempt2/wave1/R46bScribeRowsB.draft/rows.md
73d382d64f36b3676c2820b64d96a756245b0b83d90482197ddf2920bc6ede4e  7638  .ufo/waves/round-46/attempt2/wave1/R46bScribeRowsB.draft/sweep-receipts.txt
efa70f29a3f49235aa723ed7281c24ff4948b1ca4a18ee8a086b12ba68e9fa7e  16533  .ufo/waves/round-46/attempt2/wave1/R46bScribeRowsB.md
81f98c88fc30e5b0e8d83e557cf8281aaa61c57d4d26df42ad4809d55be630a2  10082  .ufo/waves/round-46/attempt2/wave1/R46bScribeRowsC.draft/rows.md
4405eb07b6f108b7e614705c41f8e8779fa71d98c10f87fa1a12e9de7dfd1146  20653  .ufo/waves/round-46/attempt2/wave1/R46bScribeRowsC.md
e31ac8cf89ce6d7932552e9edf457fbf7bfd4cf9ae997689fd69229a6e6aeb70  241  .ufo/waves/round-46/attempt2/wave1/R46bScribeScorecard.draft/receipts/mutbat-base-replay-first3.txt
6998be4f9aed7cd0e6121c9f865b43e259b11be012d02c6871da878446fad68f  482  .ufo/waves/round-46/attempt2/wave1/R46bScribeScorecard.draft/receipts/mutbat-before-vs-replay-first3.txt
5bf0d124891f0aad22ec7db0ef95c88403408998b1ba2f4a8a3f3a99c0c3accc  27371  .ufo/waves/round-46/attempt2/wave1/R46bScribeScorecard.draft/scorecard.md
0cfb4feef5c2692c1ed2f9c0d417e53721bc0067b01388012d57dd6cf2dafe66  15834  .ufo/waves/round-46/attempt2/wave1/R46bScribeScorecard.md
d5cca74d9bff641021ada2c41246e2d57ad4ba33f30ffd7c415c5a3a260e7a7c  17770  .ufo/waves/round-46/attempt2/wave1/R46bScribeShonen.draft/shonen.md
d25eaaf18efeb2668c26a2aba08e0fd7d7c1795f8a0202c8d2f6feedc4ff2405  18040  .ufo/waves/round-46/attempt2/wave1/R46bScribeShonen.md
71ac13c4cd039d3ee83bdb5e62fac40322323e09253ccf59997a7bb4d62c05d2  6988  .ufo/waves/round-46/attempt2/wave1/R46bScribeSkillRegistry.draft/README-append.md
5c02e916da5353c99d88b95986f0a52fdc2a1997389776626b24c7fdb4be6836  6245  .ufo/waves/round-46/attempt2/wave1/R46bScribeSkillRegistry.draft/SKILL-append.md
cc378418c3f04c1b987fec57493e998d07f32f75d2ccf5e5d177edf39a18644c  828  .ufo/waves/round-46/attempt2/wave1/R46bScribeSkillRegistry.draft/receipts/bytecheck-and-cells.txt
33b27a7968196b818a1adf40333bb3d0c355f90ebdf37aa05c3d7e563be8249b  10026  .ufo/waves/round-46/attempt2/wave1/R46bScribeSkillRegistry.draft/receipts/f29-selftest-draft-donothing-control.txt
0be11c210392d36f6ccd08c2fd23e3575179598e5196fc5817af9e6b9928d2c1  2133  .ufo/waves/round-46/attempt2/wave1/R46bScribeSkillRegistry.draft/receipts/f29-selftest-draft-run.txt
2ab4a4e6400ff46c41383c0a0192f97f3390b9266efaf31b1bbdad493319866f  2133  .ufo/waves/round-46/attempt2/wave1/R46bScribeSkillRegistry.draft/receipts/gate-control-vs-treatment.txt
c82f0434070662b7280462dc5c0c3efa4f8124d93ff432e531598e610a47dd88  2676  .ufo/waves/round-46/attempt2/wave1/R46bScribeSkillRegistry.draft/receipts/r50-receipt-vs-committed-bytes.txt
7f9f74dea9c33b11e41f8bb4bd12148ad19f4732899e6b3cce71bc5bc38d9a25  20165  .ufo/waves/round-46/attempt2/wave1/R46bScribeSkillRegistry.md
22dea8dde8c5b353271885a15ab4e704e991ee300050bbc1658b3937e95e75d1  22917  .ufo/waves/round-46/attempt2/wave1/R46bSentGateIntegrity.md
f1775d302b087484ad6aa495d453ba219981a6c087d2a29fd3b33e13b2b652d7  9721  .ufo/waves/round-46/attempt2/wave1/R46bSentScratch.draft/patched-pure2-c1-bare.txt
f1775d302b087484ad6aa495d453ba219981a6c087d2a29fd3b33e13b2b652d7  9721  .ufo/waves/round-46/attempt2/wave1/R46bSentScratch.draft/patched-required-c1-with-pure.txt
09f5f29415956f0bec004bc42ce22eb3a2da6a49137a92379162d1918b5e51b8  32975  .ufo/waves/round-46/attempt2/wave1/R46bSentScratch.md
8e68851bcef5a8107a6c2d8d5827efd5abf21235b6c6db59707c258510b0d740  1206  .ufo/waves/round-46/attempt2/wave1/R46bSimplifierDrafts.draft/README.md
e0915bf564d442ec157ddbcfeecbede6bd6f053396317540a88d5968276d9289  9714  .ufo/waves/round-46/attempt2/wave1/R46bSimplifierDrafts.draft/receipts/c1selftest-cut.txt
e0915bf564d442ec157ddbcfeecbede6bd6f053396317540a88d5968276d9289  9714  .ufo/waves/round-46/attempt2/wave1/R46bSimplifierDrafts.draft/receipts/c1selftest-orig.txt
54f21c1f8d7d0f8e863b6b89e7c8944ec4b5434617ffcdbfad39976b57f8566e  10730  .ufo/waves/round-46/attempt2/wave1/R46bSimplifierDrafts.draft/receipts/c2selftest-cut.txt
54f21c1f8d7d0f8e863b6b89e7c8944ec4b5434617ffcdbfad39976b57f8566e  10730  .ufo/waves/round-46/attempt2/wave1/R46bSimplifierDrafts.draft/receipts/c2selftest-orig.txt
8186468f7cf96574061d51c9e646aa1d85bb18ed7107c4c556aca82eb9fffe08  1189  .ufo/waves/round-46/attempt2/wave1/R46bSimplifierDrafts.draft/receipts/deadnames.py
0c5cff17ec697017a13a8b44de7c44587677f394e86676c455d9cc20602940ec  371  .ufo/waves/round-46/attempt2/wave1/R46bSimplifierDrafts.draft/receipts/f29-cut-base.txt
b9851d8b648bc2d65c1c4e813ea6fe3a5b29a8e42d0b4f9d55587bf274ded83d  496  .ufo/waves/round-46/attempt2/wave1/R46bSimplifierDrafts.draft/receipts/f29-cut-fabricated.txt
6d46ae42a3f8e8a0926774dffd94111b1f0ce1ca39d6a6413a6fd704f4d74e48  496  .ufo/waves/round-46/attempt2/wave1/R46bSimplifierDrafts.draft/receipts/f29-cut-junk.txt
5b1db4be6dd4d44ade0af2851eba7246d2651a00053a4ffdec1ed274f2989764  496  .ufo/waves/round-46/attempt2/wave1/R46bSimplifierDrafts.draft/receipts/f29-cut-positive.txt
0c5cff17ec697017a13a8b44de7c44587677f394e86676c455d9cc20602940ec  371  .ufo/waves/round-46/attempt2/wave1/R46bSimplifierDrafts.draft/receipts/f29-orig-base.txt
b9851d8b648bc2d65c1c4e813ea6fe3a5b29a8e42d0b4f9d55587bf274ded83d  496  .ufo/waves/round-46/attempt2/wave1/R46bSimplifierDrafts.draft/receipts/f29-orig-fabricated.txt
6d46ae42a3f8e8a0926774dffd94111b1f0ce1ca39d6a6413a6fd704f4d74e48  496  .ufo/waves/round-46/attempt2/wave1/R46bSimplifierDrafts.draft/receipts/f29-orig-junk.txt
5b1db4be6dd4d44ade0af2851eba7246d2651a00053a4ffdec1ed274f2989764  496  .ufo/waves/round-46/attempt2/wave1/R46bSimplifierDrafts.draft/receipts/f29-orig-positive.txt
dd3882388f8ca1511d12a15826e10574c5afe44a1564992e8afe0f274bff3322  3600  .ufo/waves/round-46/attempt2/wave1/R46bSimplifierDrafts.draft/receipts/list-cut.txt
dd3882388f8ca1511d12a15826e10574c5afe44a1564992e8afe0f274bff3322  3600  .ufo/waves/round-46/attempt2/wave1/R46bSimplifierDrafts.draft/receipts/list-orig.txt
d9335dae42f7f1cc6a71cf94cafa0feb60270a19f190bc3e514b1ef78d21b314  78  .ufo/waves/round-46/attempt2/wave1/R46bSimplifierDrafts.draft/receipts/mutbat-real-c1-PARTIAL-timeout.txt
289a531d1ca2eb5ca0dd3c1563bd1ae165ed7ca0ba1b811192d33b6a5712816a  3453  .ufo/waves/round-46/attempt2/wave1/R46bSimplifierDrafts.draft/receipts/mutbat-stub-cut.txt
289a531d1ca2eb5ca0dd3c1563bd1ae165ed7ca0ba1b811192d33b6a5712816a  3453  .ufo/waves/round-46/attempt2/wave1/R46bSimplifierDrafts.draft/receipts/mutbat-stub-orig.txt
4d05fadf5e6d32967da3f997b157e987f31a51b258ec57fd53160c88c518f1ca  1447  .ufo/waves/round-46/attempt2/wave1/R46bSimplifierDrafts.draft/receipts/unusedimports.py
7cdf75ae2875a15b7c0b54aea789f21fa89b938d19add1980cbd5721fd8fd1a1  31761  .ufo/waves/round-46/attempt2/wave1/R46bSimplifierDrafts.md
fd1451a548fcec53f9de61a70525de340f8b759fa51d1486bc1239f66ffe52f1  85269  .ufo/waves/round-46/attempt2/wave1/swarm-registry.json
39f41bfbc09f57e25a5633bd85efd6dc372d07719348e52f1861dfd600d0517b  63616  .ufo/waves/round-46/attempt2/wave2-dispatch.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/attempt2/wave2-dispatch.stderr.txt
6f0e41ab5a71349956c76c675ba1ddacc9962dceada451ef358a0f19e590dca4  22587  .ufo/waves/round-46/attempt2/wave2-spec.json
142278929f61185c528979e006da25e984b8bb44c16d0ffb39fdaf138d7cc0a9  25623  .ufo/waves/round-46/attempt2/wave2/R46bW2ConnW2.md
68aec706d041a5d460fd6d25ff8143349f387b8c640a9365682c98ee7bb457a0  4259  .ufo/waves/round-46/attempt2/wave2/R46bW2CritCalib2.md
97a6ce0ba6a1c97270fe1cdde1fd6483ffe3070f9bbbac89b4879986e3ebe803  3839  .ufo/waves/round-46/attempt2/wave2/R46bW2CritErrata2.md
81fea0e30d50da03c808fb8e19d04cf76d63cb7b35e95cb31f80c5a8a86a733d  14901  .ufo/waves/round-46/attempt2/wave2/R46bW2CritHonestStop.md
49a4a624edc41711080ea2dd488c2259b8789bfac973caee1e520a25651d39db  5123  .ufo/waves/round-46/attempt2/wave2/R46bW2CritNovelty2.md
8becfa91fcb82971a000d87a763c903810a4ab4966bfd173ceab9942586651d9  3720  .ufo/waves/round-46/attempt2/wave2/R46bW2CritScope.md
c9002dfa2831c96981f49d4589d87fe32f77beace0130f582eaf25bd7e939eac  3497  .ufo/waves/round-46/attempt2/wave2/R46bW2CritVerdictC1.md
1ca3d8dd159e5c11625fe246475ea370cdcf1d328eefec50ebe9890013e5a9b2  2294  .ufo/waves/round-46/attempt2/wave2/R46bW2CritVerdictC2.md
62c862b5da847c7833d4eb53face4ab5613fa46aaea14bcaedfd1bffc7a6f4ca  15646  .ufo/waves/round-46/attempt2/wave2/R46bW2ExecRerunC1.md
0c15c7927e514f085373a8cdf12a8d8dc6af6d4f9f2780052ae92d9904151294  15276  .ufo/waves/round-46/attempt2/wave2/R46bW2ExecRerunC2.md
55e69a28c961cf3e8730e06b61cae97a86e10d3a57972bc5d67c49a9d72457cb  9343  .ufo/waves/round-46/attempt2/wave2/R46bW2ExecRerunLive.md
79d1cdd498faeb5f5bcee55b88f62de4a422cbaefcdfa56fbfb719960e289445  11469  .ufo/waves/round-46/attempt2/wave2/R46bW2MutBattery2.md
83fd27b969d5689a6285bfc67deaa1cb9a19631ce8bda461b7357b9667dbed4d  12967  .ufo/waves/round-46/attempt2/wave2/R46bW2MutGate1.md
ac09ac0554305979ff622f0306a1c448afcbf2b7d77eb48e57e9d9756ed98d35  13934  .ufo/waves/round-46/attempt2/wave2/R46bW2MutGate2.md
24f960b55918e6bda64bf15b55e0024e86a6cb19ca47fdeff9e25023a8f78b21  9745  .ufo/waves/round-46/attempt2/wave2/R46bW2MutLanding.md
20ca160a6b91fbee6cc9877ff8d8b9d01a27b8df0c0549be17bd7dee6350880d  7839  .ufo/waves/round-46/attempt2/wave2/R46bW2MutNoHarm.md
1f43f3d12f73f280fc92deb6f2ceeba02e00b6b57ac48961a8d79a4907db67f7  11322  .ufo/waves/round-46/attempt2/wave2/R46bW2MutPinAmend.md
1c220da5941e68026a066e905e5d5596d292107cb23f9863ca15a1ab0c12ebe0  9852  .ufo/waves/round-46/attempt2/wave2/R46bW2MutPlain.md
6f528c5f56113e5cd4edc3fd217db66b26a3da40132af4c3e32f51f9687f9138  13847  .ufo/waves/round-46/attempt2/wave2/R46bW2MutSelfC1.md
0b53bed08bed10f2a84de251c0b6385f9b6c12084651a71e87a1ed5b5140c83a  15513  .ufo/waves/round-46/attempt2/wave2/R46bW2MutSelfC2.md
2429a56e8f813c0173fcce3189f78222d299a0b8b37d1276a736712e265d429d  8120  .ufo/waves/round-46/attempt2/wave2/R46bW2MutSelfF29.md
36f13cabfe215bc5a1a5a46c2de51c1ce78a3a7066d0a4433a16ddd87609dd82  13075  .ufo/waves/round-46/attempt2/wave2/R46bW2RevClaimC1.md
c47fce43d53aaa00ff5b7da59c4df88f38a0a779c8aacf9c099d1738158f28ff  12189  .ufo/waves/round-46/attempt2/wave2/R46bW2RevClaimC2.md
6475fbc0a5b313d75d3f8f6968b240e7ccec950dae0fae679cc455b9241fe91e  7155  .ufo/waves/round-46/attempt2/wave2/R46bW2RevEntryClaims.md
1d969c8cb9ac587664357128e551887f5ce51bdcfbabe118f291a9106544bdd8  8558  .ufo/waves/round-46/attempt2/wave2/R46bW2RevLessonGate.md
9693df7fd0143b7cdc55703241518873fd277a6180ba3d2ecfc8a0c105e2b734  15045  .ufo/waves/round-46/attempt2/wave2/R46bW2RevRegistryText.md
f5f99dc903a19c3203d5053a1c49ebe63c1044e48e72314c19000206dd3d0b0b  10400  .ufo/waves/round-46/attempt2/wave2/R46bW2RevSelftestW2.md
b435ef272869f0f1c89e92f11d374bf05c4fd6cf09bb058311c8621a6dbaa061  6745  .ufo/waves/round-46/attempt2/wave2/R46bW2RevengerW2.md
a0e946a0f85ed6c3f02b4c05991a2a902bae2aee258babe0b5654d190c41a97e  12204  .ufo/waves/round-46/attempt2/wave2/R46bW2ScoutCensusPair.md
7d73f4446c72406301665d0050059c6ba42253b48027cabae47d35e2728d2616  11595  .ufo/waves/round-46/attempt2/wave2/R46bW2ScoutS074Live.md
f517962fece4760bf2793f3d553e839173f8f49570d25d43cfb70e6f63eab3b0  14672  .ufo/waves/round-46/attempt2/wave2/R46bW2SentFinal.md
0127022f83e824220847a5c38ef0769e5e8b65279bc96ed049ca7870613e0497  12084  .ufo/waves/round-46/attempt2/wave2/R46bW2SimplW2.md
a0cd6b1ec651bda63cd0aab4b362c9c5b67d3427c8889b82e58fb1d900dc7de1  21922  .ufo/waves/round-46/attempt2/wave2/swarm-registry.json
f99e18930c06a60fd516025ef0b15fece3e15604e8e2b04d55bde3f593caaf0b  50574  .ufo/waves/round-46/build-wave1-spec.py
838289a88fb675839644a049775c2b6c74207fe39be251db4a4f141bb6604f69  26322  .ufo/waves/round-46/build-wave2-spec.py
e56ebf872b6073964d98812608275f5799afc9ee2334d4aab1363c06e59cd740  6283  .ufo/waves/round-46/claims.json
7a634e66d73de4d9557834da8b07e50c7af1e5ae9e258415b28ccfcd0a6a295e  14992  .ufo/waves/round-46/controls/controls-v1.1.py
87f9cbda37d5830240887864056c4e8e0a78a4e3acca73a522f868df44e46a57  22340  .ufo/waves/round-46/controls/controls-v1.2.out.txt
1966034fe113aac3b930e773ffe936f5094a0ff88b6b76dec0fd9b86f2416df5  3402  .ufo/waves/round-46/controls/final-measure.sh
ad1bdc329f053ab53499b91723e40392d09922c426ec6e66a6509c7330b9099a  85676  .ufo/waves/round-46/controls/final-measure.txt
061cad48f10b3d5e424c0dafaecd17aef5938dfabc9b8b7301b7d1cece915990  149  .ufo/waves/round-46/controls/freeze-check.txt
6560c0f209a3e17c68514677e0bfd6b30f9a968a9e0acd42f6fa3b4057fa9f03  7211  .ufo/waves/round-46/controls/freeze-controls.py
c1fdc20ec208671cb797456acd3e35eabf4adc1b18a5afb55fec9be63b76a9a2  4433  .ufo/waves/round-46/controls/freeze-controls.txt
6cb69e57b91120f6d00f821c2dd9078e4ed82cdc78b83e5ab35906748ed49f79  914  .ufo/waves/round-46/controls/plain-rows.sh
cecd4f8e315e883a55246195463a1e27363d5aaea21ae428b6a815f4fcf9d031  416  .ufo/waves/round-46/controls/selftest-vs-frozen-v1.txt
495d9112f2fed56e864648a3d3f92a6fe93fff900b7f955514f943afae921ac2  380  .ufo/waves/round-46/controls/sources-census-before.txt
f1fb8e5f9d6583b2a43f870de35d24ef94420ea79bb06730980f8d39a10f5921  17228  .ufo/waves/round-46/counter-errata.md
5e12e75c8ffad499c1e5bc1d38ae16c5a48c1b556b69ff7b04b0c62a0483b727  569  .ufo/waves/round-46/freeze.txt
0ef6f3e2753f7f814e59b34f0320050be6e4d381a642a2b4dff5ae019872b858  3792  .ufo/waves/round-46/integrate-wave1.py
87395f9f900d2f7606bd97633f5ecf67fe525456ec89fcebdd01338c0c79f16a  222  .ufo/waves/round-46/wave-registry.txt
8f8d4aec2d555ea7bc707c3c27f14972b39b961c23f3ddfe13d6dde7e4b2e069  257152  .ufo/waves/round-46/wave1-dispatch.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/wave1-dispatch.stderr.txt
2892ff4391b87431f2fd51cff574d5045b591a066a9496be549ea22ed78770c5  187590  .ufo/waves/round-46/wave1-results.json
4939da383b174df82d0130a950655714e2e1ea59f13cf67f10d051657c06f1a1  96482  .ufo/waves/round-46/wave1-spec.json
956fe32a1d8a5db2e950cdc52f975c176cd36a9796ca6aa77dd41a28b721c83c  160  .ufo/waves/round-46/wave1.ready
5a47479217a4ec6f30ff931e09cab9e61a19011e6d9cde12b1d1f885ed2e4fbe  2363  .ufo/waves/round-46/wave1.ready.dispatched
fa6c283500ca87a0988ca68e841fffc7d01aebb469b19644f07cc8bc96395cf1  27296  .ufo/waves/round-46/wave1/R46ConnSeparable.md
f527ce50f23eff9a05ff6d1597cfcba9599944a1108bd59f7d1602829d4a608c  13682  .ufo/waves/round-46/wave1/R46ConnSibling.md
a0ea61c0e388beefed214aacd620945e7d93757a09777226e185068fafb172b2  10063  .ufo/waves/round-46/wave1/R46CritAxis.md
1e4462375c85ae0ec5319d0802d9eaaee8e478beef33e0e673debace45978711  28297  .ufo/waves/round-46/wave1/R46CritCalibration.md
eaa20990c3d9dcf35176926965488e2e3ace47e5c2d42b44b077e64ff0d03229  10484  .ufo/waves/round-46/wave1/R46CritControls.md
afe9b3b396f55ac9b754ae69c3daaa9192e1f66e02b817640f99b711af8dc21b  15810  .ufo/waves/round-46/wave1/R46CritKillRule.md
f47a9083b6b20463842a0d9263550adaa89b81dce102102339e5bb13b55793be  16305  .ufo/waves/round-46/wave1/R46CritSoftening.md
1e0ce85c99acf1158d80f444a5ee370c703984eb3e1003407e0647a51ce763f4  20589  .ufo/waves/round-46/wave1/R46ExecLandingA.draft/r46-landing-gate.py
d4968e77aa7c22f65b26c1f17fdfc5dec920b020f3e3707e7f943b7dabb2eae4  8773  .ufo/waves/round-46/wave1/R46ExecLandingA.md
7ad171e73b1b211d0fd6b8616157ffd085b4f17468a415b842ffe01ddaba8fc4  26863  .ufo/waves/round-46/wave1/R46ExecLandingB.draft/r46-landing-gate.py
b172601700b036526af6a8b8d0be8b8212a69ee602ea02fe7f0134558223d620  12836  .ufo/waves/round-46/wave1/R46ExecLandingB.md
d2ec743823e616a78b0499f9be1d0f49f4275d17ec12d480a946e516c1d26663  2712  .ufo/waves/round-46/wave1/R46ExecPlain.draft/plain-controls.sh
2ae9e76fec3a6b077712f3821d7cbfc8cdd31e605f7c428233328b3343f841c3  1895  .ufo/waves/round-46/wave1/R46ExecPlain.draft/plain-measure.sh
17ff49fc4f6f29d2d05ffbc8de52246e8577ba8259134302f7fecebd0cba405f  8496  .ufo/waves/round-46/wave1/R46ExecPlain.md
8552da6ec61921c01219b7ea6de8eb7cae2a8481d277e4b89e8216593b38ecf5  24177  .ufo/waves/round-46/wave1/R46ExecSelftestC1.draft/r46-counters-selftest-c1.py
32b5e302f98158338fd31b5e857d9ecd897d70b47025d594afabdc1c895b25a6  7812  .ufo/waves/round-46/wave1/R46ExecSelftestC1.md
ac9f638ae342916f8e1fb03f8d1e28b7eeb49750eada0e5999abec929b153656  37751  .ufo/waves/round-46/wave1/R46ExecSelftestC2.draft/r46-counters-selftest-c2.py
6fd1d4c89fd94beb5ed4a66282a9c2ec40a1762c98f31964053afad1ec388954  11938  .ufo/waves/round-46/wave1/R46ExecSelftestC2.md
94c9bb4efa174bc218da5381ad2f702bf257596983af7a1a1d39da254dcef985  12716  .ufo/waves/round-46/wave1/R46MutC1a.md
8c1bcb7f645317b91d70d290573234d6dbc0091dce47230ddf07ca563f6a2e33  11389  .ufo/waves/round-46/wave1/R46MutC1b.md
9c02ea1c6a6dc25f1c19e1a8b5e12846d1e7ec4d0ac0d45ad19ed3d51cfafd0d  9189  .ufo/waves/round-46/wave1/R46MutC1c.md
997c4579ab4d95eaa0f1319d7cde63817f9972d3cf0942f6ee47c7e4d0112562  9323  .ufo/waves/round-46/wave1/R46MutC2a.md
613ac682ce77c459520415c06d6b649369e758f1b16697ef4210a4cb13341c3e  9859  .ufo/waves/round-46/wave1/R46MutC2b.md
1a1a6fde6d7c2b2e5f4c8028fce3bfb404ad89613d5c42ec1f05f1f511690957  7664  .ufo/waves/round-46/wave1/R46MutC2c.md
b3577bbe4f819faec853faed25c32ec777bf326745bcd22282d9cba01dd01195  8543  .ufo/waves/round-46/wave1/R46RevC1L1.md
c25c832bd44a9c29eaad617e65cfaef8f52432ea9c17b3ac78b92e6f0d9ee42b  8523  .ufo/waves/round-46/wave1/R46RevC1L2.md
d3f0559ed7a3345f8f5042c832a3d87dea6e86e7cdad9e0911a936b001c59d0b  12366  .ufo/waves/round-46/wave1/R46RevC1L3.md
a7ea08aaad491974c37e4aa17039f28928819fbbd447f2ea91f77dfa34de3f29  8315  .ufo/waves/round-46/wave1/R46RevC1L4.md
af87c77a75313f64f6428c7e44ed1e5a611ef87fc7368013b3cf27212e15114e  8350  .ufo/waves/round-46/wave1/R46RevC1L5.md
e9760b6d63beb2263f0f27654df63d9004a575a33f5b0461a14edc7aeca5aac0  10971  .ufo/waves/round-46/wave1/R46RevC1L6.md
b93fc5663e7055436d914b1f28327dea19d98dae0aa91470b243cb2ca92a06f4  8233  .ufo/waves/round-46/wave1/R46RevC1L7.md
17360fc7ceb2831eb927435288fc99007504f1950ddb5b27b2626bf56f783650  9766  .ufo/waves/round-46/wave1/R46RevC2G2.md
ed945077742edde9c05ff9d0925ecdd41b402bafd8737e311d3635c95b1596f3  10151  .ufo/waves/round-46/wave1/R46RevC2G3.md
95e37cb9d64791b363bcdba0720ca43e375ed999465bffc82d324d0de41a6c93  8281  .ufo/waves/round-46/wave1/R46RevC2G5.md
ef8582830dada73420a980207cfec5b0483451b91ca8ce00e8910c9546b7f199  14437  .ufo/waves/round-46/wave1/R46Revenger.md
2332ac6b31b9f18f763bf387b813545321223caa42aa5322affbf5fb6f9f45e1  9811  .ufo/waves/round-46/wave1/R46ScoutAdjacent.md
9b575bb4b1c4a079bbd4d506aedf112a7c25b599ba1b5188f54a06855782b154  28513  .ufo/waves/round-46/wave1/R46ScoutCensus1.md
8913ee9b918366c68f6decdc7a6daa97d29826275247f336a9743e0b6ab26926  15476  .ufo/waves/round-46/wave1/R46ScoutCensus2.md
a625856ac3f43bb89b1f9be39d81e1b569b7c1a9608c630121755ad5572625c6  38662  .ufo/waves/round-46/wave1/R46ScoutCensus3.md
f6c05970de975e5f8e36041f8eba97ab149c368264aa3600e8cd179d01eca823  22460  .ufo/waves/round-46/wave1/R46ScoutCensus4.md
35bb25b848ce298870bd8a35ef4a33bde6e7bed53bf5494ce828dcc8dafd89ba  20528  .ufo/waves/round-46/wave1/R46ScoutCensus5.md
99a9bd9740161fecf4a784bdc171af0255b5cea47517ac03e86338b611829fb7  16015  .ufo/waves/round-46/wave1/R46ScoutCensus6.md
e621dd49652f3ba7b37eb52aa590f2825443168f187ca93e31dcdf581b1c1041  15795  .ufo/waves/round-46/wave1/R46ScoutCensus7.md
ac9c0f31cf1a23f3ce32ffdd059c798c9d318b385420fb172aea91f18d58e09a  27372  .ufo/waves/round-46/wave1/R46ScoutCensus8.md
6be52cc4da1d07a6c941428e6b3fc9e77577df89c66c24f2731dcf8a640e7e89  10035  .ufo/waves/round-46/wave1/R46ScoutConsiderthese.md
0dabec5fc06f39c580de3d0d42d8554d50fe05d716d01e4f7ff28726494cf7ed  6899  .ufo/waves/round-46/wave1/R46ScoutLeadZDI.md
6a6cf45300db82f6c1342cead4a4e1006e55e8b1c9e0e85b4fdb460d42c91432  7537  .ufo/waves/round-46/wave1/R46ScoutLive.md
881f496aeb8c01f2d44d47c8a05729ebd60a791773ae436316bd861243f832d2  12821  .ufo/waves/round-46/wave1/R46ScoutManagePage.md
674903d5ec13590be70af6c9e95530090c1092b74db6707f29b21508e77e5385  7852  .ufo/waves/round-46/wave1/R46ScoutMerge.md
1df8d4856bd2ad39be2bb0932b662c756f298dc009567d14905cffc661c8580d  8285  .ufo/waves/round-46/wave1/R46ScoutMistakes.md
08628d953bf6661fddaba49c4a7e8b185552d6556b231c6432b2db2d6a9fdf53  10476  .ufo/waves/round-46/wave1/R46ScoutOverlap.md
002b03e35a82b2a215e6abdd6932cd7ef20f39065e8010b338372ddc18daa6ae  17043  .ufo/waves/round-46/wave1/R46ScoutPriors.md
036b8777bd799ef4d46a010f9dbab2c25e099390af647f5b5080eb53ec9d0662  4667  .ufo/waves/round-46/wave1/R46ScribeAdmission.draft/appends.md
adb8522bde4db7b8e1f39f0a8f86077ebba49a04f5a9b97c88b0b3b628dd2832  9886  .ufo/waves/round-46/wave1/R46ScribeAdmission.md
6412d649074e339888930eee77c62c89789bc4b1d9f0fdb9eaf1a2458e0e910b  8830  .ufo/waves/round-46/wave1/R46ScribeEntryA.draft/github-private-vulnerability-reporting.md
a15b312ee2610695c77d78d78ecef6bc8180a8071b6473a3b3794fb794307e38  7806  .ufo/waves/round-46/wave1/R46ScribeEntryA.md
cdb541501b1f0acdce4a4196db395b2ad807c112805eb45be2b81676677b5ea6  9964  .ufo/waves/round-46/wave1/R46ScribeEntryB.draft/github-private-vulnerability-reporting.md
85dab39f7c15fae5decc9318413225df9f59bcbd2b8c053261c1880f48d2322f  12352  .ufo/waves/round-46/wave1/R46ScribeEntryB.md
ebadd9c5b76e67726980b4a80bd569f8994775314c9ef7d4a1c46f4617fc7f7f  9853  .ufo/waves/round-46/wave1/R46ScribeEntryC.draft/github-private-vulnerability-reporting.md
832bcd9130dca773122dd77892a4fa58df21b5b05c3bf348f933c99bb1475503  10237  .ufo/waves/round-46/wave1/R46ScribeEntryC.md
47028299d797e3326d05769338c844198a9d4069d9f1e1d3e00e69cf72d15036  9367  .ufo/waves/round-46/wave1/R46ScribeEntryD.draft/github-private-vulnerability-reporting.md
4e652c1cd28c2b00d3ea0d7c2dc5279147ee6f0537aad70593ffa8a37b101cdf  11850  .ufo/waves/round-46/wave1/R46ScribeEntryD.md
8000f5c7b10149d4fdee6dca4686b1b46407043270148af38c204fdc74bdb440  154  .ufo/waves/round-46/wave1/R46ScribeGroundContractA.draft/recheck-line.txt
8d26f46e33fa09bbf1c96e46077c3c6270793c8bd704b71776591c80f4ef2ffb  5660  .ufo/waves/round-46/wave1/R46ScribeGroundContractA.draft/tail.md
6e7236bb8e6883aebd1b384e5553619f7c1df8f866662e05d04bc42ee96baf9e  13326  .ufo/waves/round-46/wave1/R46ScribeGroundContractA.md
8000f5c7b10149d4fdee6dca4686b1b46407043270148af38c204fdc74bdb440  154  .ufo/waves/round-46/wave1/R46ScribeGroundContractB.draft/recheck-line.txt
7e23067215e6410c97a3c6963e37ab0edf669c006525d22b051bd982e3b10e07  5696  .ufo/waves/round-46/wave1/R46ScribeGroundContractB.draft/tail.md
716bba709834544aa5671d195710d66d655adb406f38dc09a9f05f0adbb714b5  11377  .ufo/waves/round-46/wave1/R46ScribeGroundContractB.md
84d4f88773a510693c31aa9ab34a26141326711b1c4e56c6438526cdb71b789d  143  .ufo/waves/round-46/wave1/R46ScribeGroundGatesA.draft/recheck-line.txt
ac8d9a2e42509ced331b05fb9fbd88706266370861d0c97ca2aebcfab3687842  7708  .ufo/waves/round-46/wave1/R46ScribeGroundGatesA.draft/tail.md
91f055697b2100dd1ca648aa3d013f0081c321026abb5418d55ed84855d00f39  13655  .ufo/waves/round-46/wave1/R46ScribeGroundGatesA.md
84d4f88773a510693c31aa9ab34a26141326711b1c4e56c6438526cdb71b789d  143  .ufo/waves/round-46/wave1/R46ScribeGroundGatesB.draft/recheck-line.txt
b64d4d0ff7ebab00904c24a1aa29355943d9fb4e21614b402b870d222f7679e4  7315  .ufo/waves/round-46/wave1/R46ScribeGroundGatesB.draft/tail.md
ce41de5042f886c29b397fea2251503d4dad3b70dc93fafbf35962f49539b4a8  16346  .ufo/waves/round-46/wave1/R46ScribeGroundGatesB.md
07cb3de7b2908ee78e51cb8549034b12d913f56119b7176bc40e0700d99c12c5  13811  .ufo/waves/round-46/wave1/R46ScribeLesson.draft/lesson-skeleton.md
d1585dfac5d9f461cfd536e0743aaaa63f718a9ab2530a06315b952c1b9d0802  9377  .ufo/waves/round-46/wave1/R46ScribeLesson.md
88172f1e0d269d1d9b6eaed1f56aefb7adb17f24f2bba220d6f978c26c6c0260  5856  .ufo/waves/round-46/wave1/R46ScribeQuality.draft/quality-append.md
a5505a64a305a41d63a1c2532a4e83aa954d36a608cfb808ecc6a92bb5a4f973  8610  .ufo/waves/round-46/wave1/R46ScribeQuality.md
13244f7184f465105388a04084f0e737692644bbc51cb7c425b2a00a6bea6822  15127  .ufo/waves/round-46/wave1/R46ScribeRegistry.draft/registry-append.md
224bfb0308f097d9ae6a2b289e4de42c4fff5680d36a5398b60a4b975ffc40a7  10570  .ufo/waves/round-46/wave1/R46ScribeRegistry.md
b0fd2373dac180f52aa72e122c5b9159d8dccefdf920b511764e6e02b1897d7d  5198  .ufo/waves/round-46/wave1/R46ScribeRowsA.draft/rows.md
bcc9f065ea5857098ee3f6560c0f956ee1f3919d2c0075f690fd44b915094630  9123  .ufo/waves/round-46/wave1/R46ScribeRowsA.md
d07bde47d9dab21e336111db0376639a87deae50caa22223f7a36f9f472152a2  5346  .ufo/waves/round-46/wave1/R46ScribeRowsB.draft/rows.md
a56daa09ee6d3ccb014d91f9850cecb4365ff387a25d9357a9a1c2b4d56cc725  9116  .ufo/waves/round-46/wave1/R46ScribeRowsB.md
9c4cba77829b1745cbc134c0150a6b5c7eddd2080edb5ee81a2bede212097903  2395  .ufo/waves/round-46/wave1/R46ScribeScoreboard.draft/LOG-entry.md
4ca8450175cb844d0744c34dbb4776ef9b8329ec5635ac5ad157e89733ece5bf  2313  .ufo/waves/round-46/wave1/R46ScribeScoreboard.draft/SHONEN-notes.md
261a328ed5b5996bd05008a7ae344b19fe8ea31bbbc581fa912b8fa548d90ff6  9683  .ufo/waves/round-46/wave1/R46ScribeScoreboard.draft/scorecard-append.md
5f87ca8b0551451902b0f6e65675c893f05768e22447797b9c2fb342d613e9a5  8230  .ufo/waves/round-46/wave1/R46ScribeScoreboard.md
8df0da1d3072a4d6fa104795ba04a0b02ab78323a297b30535ea92f718c9d9aa  11022  .ufo/waves/round-46/wave1/R46SentinelContent.md
dcb14681971456df1378f2574a0b668f2ade9dce6642089dfb2d52ea0c652490  14030  .ufo/waves/round-46/wave1/R46SentinelGate.md
679dc058079b816ec1f233cd6e6d04481f4883f24ad2a3c05c5e6f0d53f1a2d2  13575  .ufo/waves/round-46/wave1/R46Simplifier.md
c889465f9cb7bbb92afb481b3764000b4e4ae6f897d0733fe0efb9426b6edd44  107084  .ufo/waves/round-46/wave1/swarm-registry.json
db1bc2c936376dcaa0825f7e1e87cc7e9a73bffcbd610c498e717fd3c927622e  109126  .ufo/waves/round-46/wave2-dispatch.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  0  .ufo/waves/round-46/wave2-dispatch.stderr.txt
c7f715bc6b1dfb7a44809cf8f294a8e36d7e692c380a1cd90afac10a53d7b5b7  38788  .ufo/waves/round-46/wave2-spec.json
6df72660401d30ef30b485f2deb2337f84be01c42028d2b63faec7e030f70640  160  .ufo/waves/round-46/wave2.ready
abec31e0f5a955db43162a439095e5bae974369287f5f259d450e5b38a9c3dc9  1409  .ufo/waves/round-46/wave2.ready.dispatched
d643dbf28e7fd9e9facf486c45c363b3245e22bedfca73f36bad86a6a7c7c6df  17404  .ufo/waves/round-46/wave2/R46W2ConnClaimsConsistency.md
31f832cff52c36ab3cdeff942984a4990d95fd4539542dcb756d870a52bc000f  21115  .ufo/waves/round-46/wave2/R46W2CritControlsV11.md
e50b5ea3e050421fe73677ce75e61c3076cb4bd8f45c70becaecfc9b421d74c7  20354  .ufo/waves/round-46/wave2/R46W2CritErratum.md
7d94c7adffef90f6f07cf5e4ad7f40308df2f493f9d2fb6360e9518d3cb4350b  17518  .ufo/waves/round-46/wave2/R46W2CritMistake.md
5006655b04a5a3cf39db3878ec2d29d235b9bf3dd8e07d8e218f3ce65ab342c3  12341  .ufo/waves/round-46/wave2/R46W2CritNovelty.md
8f6b9c0522b18d8ab581c3bf765059b04afaa713f3096b6044e01ae7c09adf0d  13961  .ufo/waves/round-46/wave2/R46W2CritSeparable.md
a0a951788b5028e54d6ade70311a36ce3f6cea5d9af0452abeb70adef0e0ffdb  12233  .ufo/waves/round-46/wave2/R46W2CritTier.md
3b8995022cc9d08deecfb56df12ff225473ca2380f6f628c26001f2c0fe7d13c  22250  .ufo/waves/round-46/wave2/R46W2ExecControlsV11.draft/controls-v1.1.out.txt
7a634e66d73de4d9557834da8b07e50c7af1e5ae9e258415b28ccfcd0a6a295e  14992  .ufo/waves/round-46/wave2/R46W2ExecControlsV11.draft/controls-v1.1.py
e4d11d3456b711d5b457dfdba3c344dea9c16311b9a9bcc2657b753f22d85da0  28506  .ufo/waves/round-46/wave2/R46W2ExecControlsV11.md
87e478563df7c547080c7fc142d9cff282c877bafd5fb477a4eef75d5f2bd2ae  38531  .ufo/waves/round-46/wave2/R46W2ExecSelftestC1.draft/r46-counters-selftest-c1.py
590f30fd60a55f9473c923013e15d235ed4791e4995e7f3da7b39ed0bd569595  9737  .ufo/waves/round-46/wave2/R46W2ExecSelftestC1.md
bf7cca541e386b103c7f5fb480162df71ca48a2fd3d5f1dacb7f773f4fafa5d1  51380  .ufo/waves/round-46/wave2/R46W2ExecSelftestC2.draft/r46-counters-selftest-c2.py
021616ebc057687f3d47da49cbe452be5ef3b37a15fa63c16304579086912042  10288  .ufo/waves/round-46/wave2/R46W2ExecSelftestC2.md
34391fb17ba8db6602f0d8e2265b96c98b578ca2ff2b85bf8fa99ed3603f844d  8699  .ufo/waves/round-46/wave2/R46W2MutC1a.md
03c5496fb63ab95f82789603ac1f81c2878a751fb3168316e94c7b5eed14f982  11043  .ufo/waves/round-46/wave2/R46W2MutC1b.md
935d969c8fb648361114d30535e564ed9928dc8da64a459f15463e686a862f7d  11341  .ufo/waves/round-46/wave2/R46W2MutC1c.md
dfc5af594a74303f1d09e1ceb1042dfad6ab735c6871d6117f34f46e3cce185c  7701  .ufo/waves/round-46/wave2/R46W2MutC2a.md
3788b7dd6a9c9ab2a391741b9eecaf0dc23a3f024fa0c10c10421eecc47e291c  12539  .ufo/waves/round-46/wave2/R46W2MutC2b.md
0123bc41f4d120db822fbaa30eae540faef934097019851a3076985d733ce5bb  17720  .ufo/waves/round-46/wave2/R46W2MutC2c.md
83532c4fb5857ba3b8ac33aff20d4c86a9aa988060ae34d4fa6845b41cb34f63  12777  .ufo/waves/round-46/wave2/R46W2MutLanding.md
74a0ca5e3d03b5334a5058f0f9f559ca4ebdc0af8132b5e3c1795ad4f022a30f  16340  .ufo/waves/round-46/wave2/R46W2MutSelftestC1.md
0b17b781faabb1074814a761cd9149db5ac0374169c8947b2d378037cc23e1e7  13531  .ufo/waves/round-46/wave2/R46W2MutSelftestC2.md
2396b571df50844ce066599d735c94de1b48884fd990c2e274924b7cfe1ee51c  14555  .ufo/waves/round-46/wave2/R46W2RevEntryOverlap.md
5d61fedf175d723744911ef0562d496c8371221cb878ff2c0cbcc5b4f5f4615c  21585  .ufo/waves/round-46/wave2/R46W2RevEntryRule.md
b816b0397ed35114d6986fa904193701ecf42736b7f4cc19335a203b8d847075  10381  .ufo/waves/round-46/wave2/R46W2RevEntryTable.md
445c6b1ab63b09923387569fb4252cf9642ff5069e0edc4cafe1a43607a6aa0a  10015  .ufo/waves/round-46/wave2/R46W2RevGroundContract1.md
b10e66f0d83d796ffdd32c55edba1b898e928770237ed6756a5b9aec99be3c57  9920  .ufo/waves/round-46/wave2/R46W2RevGroundContract2.md
a881a9a2f6d7823138d349815c4eec4730b281edc557072091ac613a7c4eb85c  6958  .ufo/waves/round-46/wave2/R46W2RevGroundContract3.md
b3761c4251e55b514f8b0782891e80d777993772a7dbc84972aa4c9f51ead265  10787  .ufo/waves/round-46/wave2/R46W2RevGroundGates1.md
0562478d69911169df7d9d4bbf330144d7eda3a85eb5f021a83d5c0c4c9dd192  9226  .ufo/waves/round-46/wave2/R46W2RevGroundGates2.md
8efd4e2a03ca8bdfd060ea55ddba5c54b0e627bb5fb3367dc726c14ab271bfd0  14316  .ufo/waves/round-46/wave2/R46W2RevGroundGates3.md
f64cbbb0c8e4109f432cf8c573bd336a58176ff2761beff33892c4cc7a738697  16189  .ufo/waves/round-46/wave2/R46W2RevLanding.md
1893afd076d5ce539399b3727e5c7ecee7b07e571730e409947bb19e7e738de2  10880  .ufo/waves/round-46/wave2/R46W2RevNoHarm.md
17f5f0e41e047df721391777cab9c954ccd7bc90c64754100b5ccf24413254c4  13841  .ufo/waves/round-46/wave2/R46W2RevRegistry.md
4b28b9f3746eeee05588412fe402c7ed3efc7911b9b3d211dfd9da76f34a65f1  13113  .ufo/waves/round-46/wave2/R46W2ScoutLive.md
32f747c14175e6ed832b93cde9db67327db867e9d7a21214183a5b999fe60ac4  11239  .ufo/waves/round-46/wave2/R46W2SentinelV11.md
20c4ba63c5eb78e48ef9cde6d30ffecabe0837b222a4e66f35bda6503f360daa  41848  .ufo/waves/round-46/wave2/swarm-registry.json
a9a9f62fa45cbc5f71511a645350053e13a8d66f56d06affb676ea7ab8bdbc25  15172  PROVINCE.md
95f2eb7933841d6cd06a0041af613204cbfe29e96a38a218499a71846cdb03b7  20207  corpus/instruments/r46-c1-gate.py
ad60a72cf76304aaf22634e9b319453769f874c90d80df3305191f8e147d70f2  22651  corpus/instruments/r46-c2-gate.py
03079421b07639baabfc942ef4a022c9a8798ff8bc81f029d4b73c6a8b54e2fd  46486  corpus/instruments/r46-counters-selftest-c1.py
e1f9e5a7f0577ce6b18d125f3a25bf3d51744ffd5d3260d1ce78328e8814091b  64382  corpus/instruments/r46-counters-selftest-c2.py
dc9f8af78ec9c52c1778472941bef72b8e51a07277c5e91e27d42f2a40f70053  20323  corpus/instruments/r46-f29-gate.py
2c31138639dd621e6ab95c7800a3993ad0cb87579e5895b6612bfdf27d00e9ab  26971  corpus/instruments/r46-landing-gate.py
de2f8b46f3353d5929660092bcf390d5c94295a60a0a9dd08e0c670198b0832e  683  corpus/instruments/r46-mutant-equivalents.json
8039d6cf81bbe3f35aa15e51adf0cb76582a41efb493e5f92959caf7ebb0b1a6  3560  corpus/instruments/r46-mutant-equivalents/G6b-G7a-G7c-equivalence-probe.txt
5706f5cef868fd1cf9b8faf21ea978dcc474d34fef96172937c1ca29b209a5f4  682  corpus/instruments/r46-mutant-equivalents/M14-L6-exit-ignored-receipt.txt
27931609b62549addad6377e783108d2c238469475fbc07d040b75795acb5212  3792  corpus/instruments/r46-mutant-equivalents/README.md
f08598c851434a91f0e6266f375428e4a60209a6080eeb7b2732cb1340687cc2  2066  corpus/instruments/r46-mutant-equivalents/f29-H1b-H7a-H7c-proofs.md
98e95b37130f73369c79481cbd50a5e1a5a7b0ed47e25573f91d7d561f673dd9  3292  corpus/instruments/r46-mutant-equivalents/m14-equivalence-differential.py
99029667bdf6a6006bde5252cb01332167639f3489f9704baae599478ed13822  26431  corpus/instruments/r46-mutbat.py
2ae9e76fec3a6b077712f3821d7cbfc8cdd31e605f7c428233328b3343f841c3  1895  corpus/instruments/r46-plain-measure.sh
d7188925274ba0e066ac7140afe0a07d5d4365450eda2d9783189717b3b04eec  47215  corpus/instruments/r46-selftest-f29.py
9f7dd9101d8a7e967b003a64b00b051470f01693e7c3b8a2fc1144dbc07e6fd2  4866  corpus/knowledge/ai-assisted-finding-validation.md
9536e1b321dd285a1e3f3552a26edd5d6e4f8c6c58d8620446b4c4331ea01f38  16937  corpus/knowledge/anthropic-cvd-provenance-and-pacing.md
5533fc87ab7a35d3429947d50aa49d73fdc3f8d2493cb4b6ba4085d19f7e10e0  5296  corpus/knowledge/authorised-testing-rules-of-engagement.md
9317f03917d1e454ea3854ffccf8c9ad46d3f7ce2c5e59e13307dc33915ff8ec  4445  corpus/knowledge/authorization-safe-harbor-and-scope.md
1f7ac0a2c39a0fbfdbee2ecbe112316dfc1bf7095b18cb8fb4eb9d6dfce171d1  24539  corpus/knowledge/chinese-crowdsourced-testing-scope-and-rewards.md
f83a03cd9307fae0ffbdbbd6dc3cfb40d03725a13fa0e2247ed00a9a9910274c  20119  corpus/knowledge/cisa-bod-20-01-vdp-minimums.md
3fd49ca4b5bb2a17f65aa92c8762f2473796cdfe06be16174dad430c5233b4a4  18214  corpus/knowledge/cisa-cvd-program-stages.md
e9de994dbe1940adb894420d566386500e4e29d69d8e6a5244ff2172c71d9761  15831  corpus/knowledge/cisa-kev-catalog.md
5010a107cc7ef34bcd7e8d1a74eb2a2bb2a71c3ea666577506d7c2f93dc25d29  19196  corpus/knowledge/cisa-when-to-issue-vex.md
2eda5eabeba4aa6b5b1bb8e80336c3f97c98eee741d4a11b968bb19d07da1fc2  8224  corpus/knowledge/citation-bases.md
bc33e8cb235f5a4e6549ac4745d65eddbea7ccebaf4f789cb66e9a49dc9df791  10517  corpus/knowledge/claim-anatomy-sample.md
93be63b06da497fd2d729fc5155aefaf5be57c67eda79b58dc7844ad8e31d8ca  15372  corpus/knowledge/claim-gates.md
6f445bc3389a9c577beff03b5003f967f55819e6b3dbcbb5dbc0faeba73269e1  12319  corpus/knowledge/claim-package-contract.md
f53109d842b185ed49ca599fda221351caf03df9d3443c5d50c8bb19a0cb5940  9830  corpus/knowledge/claim-package-gate.md
689d4b2fccdb8165d6eb9e2a6f67d895bd51daaefcacc21aaf2558a0948a3773  5650  corpus/knowledge/cna-assignment-and-vulnerability-rules.md
5e5395c6c8211c6b540aed2e203febb1a9f2b3447cd6ad77f3f433756b36be86  40843  corpus/knowledge/considerthese-proposals-ledger.md
7ca630ca87572360b6c6210383694d3f897df91a3f6e3dd5902f3cad54600b8a  4423  corpus/knowledge/coordinated-disclosure-timelines.md
962caeac57f48d6ad2a98eb514be0233cc70eff9be575f586520f19f98c3b2e9  6005  corpus/knowledge/cra-manufacturer-reporting-duties.md
0343ef4544ebd675754c498829fa99bbde4f1391d4260db5e494efe8a6dc5b0a  22887  corpus/knowledge/csaf-vex-product-status-and-justifications.md
dd6c780e82c51a2b4dd11229d7cf5174c9709c241d052b5d6eb754c199c20c19  20566  corpus/knowledge/cve-bench-agent-exploitation-benchmark.md
7cd4f14c598f62eabcfc130e172a09d24595e32cfd2d5f575d3f6e9826ead61f  23793  corpus/knowledge/cve-json-record-format.md
7fda190813801dfc7639d3ac788e12dde3d3366d866b7dca4263e2bc0f0fe626  4556  corpus/knowledge/cvss-v4-severity-and-vector.md
b9b97e738097206e945880ffe14b10688758b43250ed33e9136aaf40665cbaa5  4685  corpus/knowledge/cwe-top25-2025-methodology.md
5a549e312237372a639931cc980ea697f60d383999790b9d48d5df4bd5d1978c  22993  corpus/knowledge/cyclonedx-analysis-subtree.md
25f357f1458cd15ea25b73afafc8bf9caf4a81bfcc35aad0c6abab20cf372e48  17782  corpus/knowledge/doj-vdp-framework-scope-and-authorization.md
f1a33eab12c970d61f7e180fc206c179860e7158c4d703e762eaa67da0e5d28f  17372  corpus/knowledge/epss-exploit-prediction-scoring.md
000fe7fbb93dada051006f44cbdada4944fb75bfc5e78fe1276c70d64fb7a364  3768  corpus/knowledge/ev-model.md
2d924d029be7dcebe6bb8d8198c416a3eeda8e3b9cbaf761e35a3cbdd85c9e6e  5150  corpus/knowledge/evidence-dir.md
29743eb704aa196f3feea835a9b9c4825a7edb0fa1c1713359c2a541058bf186  10663  corpus/knowledge/github-private-vulnerability-reporting.md
1824f25a9f233b9b38251995d37fa822cf44bacbad6cbe511c57169672266371  5843  corpus/knowledge/google-cloud-vrp-customer-resource-boundary.md
948b202ebe1f32728a19d7bf2ead67991ba624d3699bde2dfd486f6725ac1d8a  11143  corpus/knowledge/immunefi-vscs-v2-2-smart-contract-severity.md
9430780371c1eb1f5416dcf73b8c768a07927494f67e301c700d26dabd1ff8c2  7150  corpus/knowledge/intake-and-finalize.md
088e6f39584d0508e21d0fd91f9b7ac71567f6a4a2e3af5f9cc4c8c523486243  11727  corpus/knowledge/intake-surface.md
b2600651e0c1725d93d8db738ae2301b476824b34693ab70c7c7c6aa88c85d85  7255  corpus/knowledge/iso-29147-and-30111-division-of-labour.md
b55dcf9c33d1982d535712cd8ff4342dcaa99fd38aa10c369ccdc07abfbd7f80  10547  corpus/knowledge/iso-29147-divergence-and-clause-crosswalk.md
a22d2321e39fd0e547d8ae480eb566648520e59281e69e057aab5ab8502413a6  18544  corpus/knowledge/japanese-domestic-disclosure-workflow.md
f584f06c74942a36d9bce6bb97adcb7ab3bd1b2b0503faf8a68d5c60f4494a32  7096  corpus/knowledge/japanese-severity-vocabulary-and-impact-model.md
bec66635c49f20cde8d0e194b16e172d6889101e0aee9248c095f9a57d19d267  13158  corpus/knowledge/linux-kernel-security-bugs-reporting-process.md
5dc238be924c61bd5be84a4cbee0bc54b0bb8f3eaecf4f3cada1ed9b51dd23a1  10237  corpus/knowledge/mission-control.md
9f003f04c07f97cb75378a0c43321bc03ad8c3a91df1948ba5343b6119ec5bd6  8649  corpus/knowledge/mission-ledger.md
258648095adc219f329f0a030434f7beb4734cdeab4303dd58f78b35a1a60094  4476  corpus/knowledge/multiparty-vulnerability-coordination.md
757058a5d8e03c83c61c6b7c22852400bcbea1b252504a9e8f5c7a56da79d596  16018  corpus/knowledge/nist-sp800-216-vdp-framework.md
69835a4fc2fb83b0930f582d90244d618c9fe941d6a3415f337b656a16e4c400  9121  corpus/knowledge/operator-queue.md
b21d70442402c88165ed5ed8055b6296c399169a86bfc2eb83ce8d45df27f199  10307  corpus/knowledge/ops-invariants.md
9e705b4b5a94a55b539abd178ee5414ec4f6540a1c8a0be4a1f7f75351631ca9  3405  corpus/knowledge/policy-access-playbook.md
686bdb75b4db9f1489a5b6426392eafa87c4650d44b80fba739e78e755651f9b  3449  corpus/knowledge/program-quirks.md
6c05c98f3c6851b560098b8f7c43350a951e487e8b34e2ff09831563aa8ff4a6  8095  corpus/knowledge/program-severity-ladders-and-reward-scales.md
270b6a0a73061d85063a463a120c87c6786a6bf03a7cc492a949383034408c1a  15072  corpus/knowledge/pz-reporting-transparency-trial.md
2b4b88c2f93dc3752c01b9b80ee796a9f308c75ef2d8021d8c088f02e7ce0e9c  6237  corpus/knowledge/repo-git-state.md
a25a26bf046a7272c01ea110dd9f0d75fccc666e7006151d25351d21a7ec5d45  7665  corpus/knowledge/retirement-autopsies.md
eab59fdf66c1fa3a57cbec7d3a0b4ff0f756e25de518541ef2a767b158b059f0  10898  corpus/knowledge/rfc-9116-security-txt.md
4af11868ad2989ce161bb9ad35fc911b5715fc40bfae0d0a921b45b27ebfe64c  4550  corpus/knowledge/root-loss-2026-10-12.md
adf98044be077af287d1e0df863d0876284007e3374ebc4f1700dfd805bf459c  28683  corpus/knowledge/source-tree-loss-2026-09-28.md
aedd27d3b96eba125a61244fbd08e962ea20badc14cad052512137c15bd9410f  13081  corpus/knowledge/ssvc-stakeholder-specific-vulnerability-categorization.md
c1007f0e5608acf9d7bab9c3eb18a5d9ecc9d46c40f14ca19b30ddaa4dec6578  15211  corpus/knowledge/statutory-authorization-and-unauthorized-access.md
e308fc8795343da96ae12604f251143c6c19930df431f13f1bbf811f70bab249  16725  corpus/knowledge/submitted-registry.md
20de270a72a8658faf4d4f0d6ce385d683e5014b144cdd61f75efab422bcd57a  5017  corpus/knowledge/target-checkouts.md
8b2e851aae4bd11472e6d867c0494609a9ba25be12fde7205dec89a4338ba4a7  2731  corpus/knowledge/terminal-classes.md
5c0f4d4f3a180a91f08513bd4f1df66269877d9d039ef9de19988e21d2cf1c2b  44953  corpus/knowledge/triage-thresholds.md
3297f544210785cc62a37a64cd870bf4f11284d90abb1fe3d314fc567afb961e  12567  corpus/knowledge/ufo-archive-2026.md
b412a1619a5fa81685f8a19ca22988447829c7b1337038c5ed75bcf4e9c7a6f0  25588  corpus/knowledge/ufo-workspaces.md
b2fc8c726b7906793ae86c14e09adaeba42eb526c9543f40ac1e05a850331ea6  2760  corpus/knowledge/vdp-disclosure-packages.md
845413bfdbc1ce2dac454a6d5a0ecbf64ec3bc937a3ca8c40b9f4801c57c3f67  14264  corpus/knowledge/vendor-disclosure-policies-as-corpus-objects.md
8279da2dcf25d5cf4f478370883486ec69c5ea5b62c53bb7b956202301f1b4ff  16468  corpus/knowledge/vendor-disclosure-policy-commitments-crosswalk.md
a488df492e2a72a929e0502ac9fabc80d00214a8fd6d83335ac624deb9c8d56f  12900  corpus/knowledge/vendor-third-party-finding-coordination.md
48765431cec5afa105ad629c8f4d82975f645034426fc7adb78b56f5ef3ca640  20832  corpus/lessons/round-46-verifier-spotcheck.md
cf4ae844222b42e72f6b402d3122a9de0f439fd5a8dd57245a1a45e9b2d0676c  27204  corpus/lessons/round-46.md
1296528d5be0882703a1ac4ec32dda420910df4e77a1a9588284f1468c278039  7087  corpus/source-snapshots/round-46-a2/S074.txt
46e8077ac89edb0335711826ecb7abf3a1b7eefedc7108c3f6d936135481569f  2163  corpus/source-snapshots/round-46-a2/manifest.json
66c96a6168011dcf7e4567c7447772cf5d345866d3920481203ee3c627df1930  15568  corpus/source-snapshots/round-46/S073.txt
01f0257261d1a69b58c26856997e877cea092eb12b681421a7e9f0df74f79d34  2187  corpus/source-snapshots/round-46/manifest.json
```

## Machine-readable receipt

`.ufo/waves/round-47/w1/R47SentNoHarm.draft/baseline.json` contains the same hashes, byte lengths, frozen ranges, scope selection and control outcomes. Receipt SHA-256: `325964d4d263552ff5fe32a7e21277f0995bbb1ccba612d4acbbc228fbab06cc`.

## Self-evaluation

Accuracy 4/5 (byte evidence, not permissions); completeness 4/5 (all 968 frozen files in assigned named scope, untracked r46 extras excluded explicitly); clarity 4/5 (large mandatory 964-file inventory); actionability 4/5 (machine-readable receipt, integrated diff not yet checked); conciseness 4/5 (long hash list is required). Overall 4.0/5. Main improvement at integration: compare candidate files and reject path/permission substitutions alongside content mismatches. Would the user agree: likely, with these scope limitations explicit.
