# Version 6 repair validation

Canonical screen: `D:\Apart Sprint\AI x Epistemics Research Sprint\results\repair-v6-screen-20261115T184213Z`.

| Model | Provider | Valid and correct initial responses |
|---|---|---:|
| DeepSeek V4.1 Flash 1017 | Deploy | 14/14 |
| GLM-5.3-Flash | Deploy | 14/14 |
| Nemotron 3.5 Super VL | NVIDIA | 14/14 |

All 42 initial requests were attempted once. No failures, retries, missing items or invalid outputs in this version. Main-study collection has not started.

## Changes and limits

- The older Modal DeepSeek checkpoint/route was replaced with the explicitly versioned Deploy Flash 1017 checkpoint. This is a model-version/route change, not correction of its previous answers.
- Receiver output asks for a brief justification inside JSON before the action, with an explicit consistency instruction. The action is still authoritative, including when it disagrees with the reason.
- GLM uses API JSON-object mode to prevent prose outside JSON. No permissive extraction or repaired answers are counted.
- Nemotron reasoning is off, with at least six seconds between request starts and one in-flight request per route.
- All routes use temperature 0, output-token cap 4096 and timeout 180 seconds; Deploy models use low reasoning effort.
- All 26 software tests pass, including request pacing, budget accounting and preserving contradictory submitted actions.

These repairs used failures on the same development cases. The screen is not held-out evidence, a general model ranking, or a guarantee of provider uptime. Every previous failed screen and diagnostic is retained.

## Earlier versions

- Version 3: Modal DeepSeek 11/14; GLM 14/14; MiniMax eight valid correct answers plus six HTTP failures.
- Super VL candidate screen: 13 valid correct answers plus one timeout.
- Version 4: revised DeepSeek and GLM 14/14; non-thinking Super VL 11/14 with action/reason inconsistencies.
- Version 5: DeepSeek and Super VL 14/14; GLM 13 valid correct answers plus one non-JSON preamble.
- Version 6 adds GLM JSON mode and passes the fresh full screen.

## Main run completion

Main collection is complete. The six-family development run has 54 valid writer
outputs in 55 attempts, then 1,248 evaluation records: 1,233 valid, six interrupted,
seven invalid and two timed out. One identical writer retry was explicitly
amended; both attempts remain. Two recovery events resumed only never-reserved
jobs. No interrupted request was resent. See `../data/main-v6` and `RESULTS.md`.
Reported main usage is 989,578 tokens with eight unknown-usage attempts. The
US$19.545 reservation allowance is not an invoice. Frozen scientific settings and
all earlier failed screen versions remain unchanged. Final coauthor review is open.
